import argparse
import os
import yaml
import sys
import xml.etree.ElementTree as ET

from urllib.request import urlretrieve
import urllib.request


class Parser(argparse.ArgumentParser):

    def error(self, message):
        self.print_help()
        sys.exit(2)


def main():
    parser = Parser(usage='Downloads GML files from a set of WFS service in a pseudo-paginated '
                          'way using bounding boxes and combine them again to one file. The WFS '
                          'services are specified in settings.py.')
    parser.add_argument('config', help='config file', default=None)
    parser.add_argument('--no-download', help='skip the download', action='store_true')
    parser.add_argument('--no-combine', help='skip the combine', action='store_true')

    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f.read())

    if not args.no_download:
        download_files(config)

    if not args.no_combine:
        combine_files(config)


def download_files(config):

    if (sys.version_info > (3, 0)):
        # Python 3 code in this block
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'wfs-downloader/0.1')]
        urllib.request.install_opener(opener)
    else:
        # Python 2 code in this block
        urllib.URLopener.version = "wfs-downloader/0.1"

    west_range = list(arange(config['bbox']['west'], config['bbox']['east'], config['size']))
    south_range = list(arange(config['bbox']['south'], config['bbox']['north'], config['size']))

    for west in west_range:
        for south in south_range:

            url = '%(url)s?service=WFS&request=GetFeature&version=2.0.0&typeNames=%(layer)s&srsName=%(srid)s&BBOX=%(west)f,%(south)f,%(east)f,%(north)f' % {
                'url': config['url'],
                'layer': config['layer'],
                'srid': config['projection'],
                'west': west,
                'east': west + config['size'],
                'south': south,
                'north': south + config['size']
            }

            name, extension = os.path.splitext(config['outputfile'])
            filename = os.path.join(config['tmpdir'], '%(name)s_%(west)s_%(south)s%(extension)s' % {
                'name': name,
                'west': west,
                'south': south,
                'extension': extension
            })
            print('fetching %s' % filename)
            urlretrieve(url, filename)


def combine_files(config):
    # read the first xml file
    name, extension = os.path.splitext(config['outputfile'])
    first_filename = os.path.join(config['tmpdir'], '%(name)s_%(west)s_%(south)s%(extension)s' % {
        'name': name,
        'west': config['bbox']['west'],
        'south': config['bbox']['south'],
        'extension': extension
    })

    first_xml = ET.parse(first_filename)
    first_root = first_xml.getroot()
    nsmap = dict([node for _, node in ET.iterparse(first_filename, events=['start-ns'])])

    try:
        number_matched = int(first_root.get('numberMatched'))
    except ValueError:
        number_matched = False

    try:
        number_returned = int(first_root.get('numberReturned'))
    except ValueError:
        number_returned = False

    for filename in os.listdir(config['tmpdir']):
        if filename.startswith(name):
            abs_filename = os.path.join(config['tmpdir'], filename)
            if abs_filename != first_filename:
                print('merging', abs_filename)

                xml = ET.parse(abs_filename)
                root = xml.getroot()

                if number_matched is not False:
                    number_matched += int(root.get('numberMatched'))

                if number_returned is not False:
                    number_returned += int(root.get('numberReturned'))

                for node in xml.findall('.//wfs:member', namespaces=nsmap):
                    first_root.append(node)

    # manipulate numberMatched numberReturned
    if number_matched is not False:
        first_root.set('numberMatched', str(number_matched))

    if number_returned is not False:
        first_root.set('numberReturned', str(number_returned))

    # manipulate the extend / bounding box
    first_root.findall('.//wfs:boundedBy/gml:Envelope/gml:lowerCorner', namespaces=nsmap)[0].text = \
        '%s %s' % (config['bbox']['west'], config['bbox']['east'])
    first_root.findall('.//wfs:boundedBy/gml:Envelope/gml:upperCorner', namespaces=nsmap)[0].text = \
        '%s %s' % (config['bbox']['south'], config['bbox']['north'])

    # write the result as outputfile
    first_xml.write(config['outputfile'])


def arange(start, stop, step):
    current = start
    while current < stop:
        yield current
        current += step


if __name__ == "__main__":
    main()
