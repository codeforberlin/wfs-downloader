import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import yaml
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)


def create_progress():
    return Progress(
        TextColumn('{task.description}', markup=False),
        BarColumn(bar_width=None),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    )


def main():
    parser = argparse.ArgumentParser(
        description='Downloads GML files from a WFS service in a pseudo-paginated way '
        'using bounding boxes and combines them again into one file.'
    )
    parser.add_argument('config', help='config file')
    parser.add_argument('--no-download', help='skip the download', action='store_true')
    parser.add_argument('--no-combine', help='skip the combine', action='store_true')

    args = parser.parse_args()

    config = yaml.safe_load(Path(args.config).read_text())

    if not args.no_download:
        download_files(config)

    if not args.no_combine:
        combine_files(config)


def download_files(config):
    tmp_path = Path(config['tmpdir'])
    tmp_path.mkdir(parents=True, exist_ok=True)
    output_path = Path(config['outputfile'])

    west_range = list(arange(config['bbox']['west'], config['bbox']['east'], config['size']))
    south_range = list(arange(config['bbox']['south'], config['bbox']['north'], config['size']))

    with create_progress() as progress:
        task = progress.add_task(f'Downloading to {tmp_path}', total=len(west_range) * len(south_range))
        for west in west_range:
            for south in south_range:
                file_path = tmp_path / f'{output_path.stem}_{west}_{south}{output_path.suffix}'

                if not file_path.exists():
                    east, north = west + config['size'], south + config['size']
                    response = requests.get(
                        config['url'],
                        params={
                            'service': 'WFS',
                            'request': 'GetFeature',
                            'version': '2.0.0',
                            'typeNames': config['layer'],
                            'srsName': config['projection'],
                            'BBOX': f'{west:f},{south:f},{east:f},{north:f}',
                        },
                        headers={'User-Agent': 'wfs-downloader/0.1'},
                    )
                    response.raise_for_status()
                    file_path.write_bytes(response.content)

                progress.advance(task)


def combine_files(config):
    # read the first xml file
    tmp_path = Path(config['tmpdir'])
    output_path = Path(config['outputfile'])
    first_path = tmp_path / '{name}_{west}_{south}{extension}'.format(
        name=output_path.stem, west=config['bbox']['west'], south=config['bbox']['south'], extension=output_path.suffix
    )

    first_xml = ET.parse(first_path)
    first_root = first_xml.getroot()
    nsmap = dict([node for _, node in ET.iterparse(first_path, events=['start-ns'])])

    try:
        number_matched = int(first_root.get('numberMatched'))
    except ValueError:
        number_matched = False

    try:
        number_returned = int(first_root.get('numberReturned'))
    except ValueError:
        number_returned = False

    file_paths = [
        file_path
        for file_path in sorted(tmp_path.iterdir())
        if file_path.name.startswith(output_path.stem) and file_path != first_path
    ]

    with create_progress() as progress:
        task = progress.add_task(f'Merging into {output_path}', total=len(file_paths))
        for file_path in file_paths:
            xml = ET.parse(file_path)
            root = xml.getroot()

            if number_matched is not False:
                number_matched += int(root.get('numberMatched'))

            if number_returned is not False:
                number_returned += int(root.get('numberReturned'))

            for node in xml.findall('.//wfs:member', namespaces=nsmap):
                first_root.append(node)

            progress.advance(task)

    # manipulate numberMatched numberReturned
    if number_matched is not False:
        first_root.set('numberMatched', str(number_matched))

    if number_returned is not False:
        first_root.set('numberReturned', str(number_returned))

    # manipulate the extend / bounding box, an empty first tile has no envelope, so create one
    envelope = first_root.find('./wfs:boundedBy/gml:Envelope', namespaces=nsmap)
    if envelope is None:
        bounded_by = ET.Element(f'{{{nsmap["wfs"]}}}boundedBy')
        envelope = ET.SubElement(bounded_by, f'{{{nsmap["gml"]}}}Envelope', srsName=config['projection'])
        ET.SubElement(envelope, f'{{{nsmap["gml"]}}}lowerCorner')
        ET.SubElement(envelope, f'{{{nsmap["gml"]}}}upperCorner')
        first_root.insert(0, bounded_by)

    envelope.find('./gml:lowerCorner', namespaces=nsmap).text = f'{config["bbox"]["west"]} {config["bbox"]["south"]}'
    envelope.find('./gml:upperCorner', namespaces=nsmap).text = f'{config["bbox"]["east"]} {config["bbox"]["north"]}'

    # keep the namespace prefixes of the original files, e.g. wfs: and gml: instead of ns0: and ns1:
    for prefix, uri in nsmap.items():
        ET.register_namespace(prefix, uri)

    # write the result as outputfile
    first_xml.write(output_path, encoding='utf-8', xml_declaration=True)


def arange(start, stop, step):
    current = start
    while current < stop:
        yield current
        current += step
