#!/usr/bin/env python2
import argparse
import os
import urllib

from lxml import etree

parser = argparse.ArgumentParser(usage='Downloads GML files from a set of WFS service in a pseudo-paginated way using bounding boxes and combine them again to one file. The WFS services are specified in settings.py.')
parser.add_argument('--no-download', help='skip the download', action='store_true')
parser.add_argument('--no-combine', help='skip the combine', action='store_true')
parser.add_argument('--service', help='download/combine only this service')

args = parser.parse_args()

from settings import SERVICES

if args.service:
    try:
        services = {args.service: SERVICES[args.service]}
    except KeyError:
        parser.error('service not found')
else:
    services = SERVICES

for key in services:
    service = services[key]

    if not args.no_download:
        url_args = service

        extend_xmin, extend_ymin, extend_xmax, extend_ymax = service['extend']

        delta_x = (extend_xmax - extend_xmin) / service['paging']['nx']
        delta_y = (extend_ymax - extend_ymin) / service['paging']['ny']

        for i in xrange(service['paging']['nx']):
            for j in xrange(service['paging']['ny']):
                xmin = extend_xmin + delta_x * i
                ymin = extend_ymin + delta_y * j
                xmax = extend_xmin + delta_x * (i + 1)
                ymax = extend_ymin + delta_y * (j + 1)

                url_args['bbox'] = '%s, %s, %s, %s' % (xmin, ymin, xmax, ymax)

                url = '%(url)s?service=WFS&request=GetFeature&version=2.0.0&typeNames=%(layer)s&srsName=%(srid)s&BBOX=%(bbox)s' % url_args

                filename = '%s%s_%i_%i.xml' % (service['tmp_dir'], service['layer'], i, j)

                print 'fetching %s, BBOX(%s)' % (filename, url_args['bbox'])
                urllib.urlretrieve(url, filename)

    if not args.no_combine:
        # read the first xml file
        first_filename = '%s%s_0_0.xml' % (service['tmp_dir'], service['layer'])

        first_xml = etree.parse(first_filename)
        first_root = first_xml.getroot()
        nsmap = first_root.nsmap

        number_matched = int(first_root.get('numberMatched'))
        number_returned = int(first_root.get('numberReturned'))

        for filename in os.listdir(service['tmp_dir']):
            if filename.startswith(service['layer']):
                abs_filename = service['tmp_dir'] + filename
                if abs_filename != first_filename:
                    print 'merging', abs_filename

                    xml = etree.parse(abs_filename)
                    root = xml.getroot()

                    number_matched += int(root.get('numberMatched'))
                    number_returned += int(root.get('numberReturned'))

                    for node in xml.xpath('.//wfs:member', namespaces=nsmap):
                        first_root.append(node)

        # manipulate numberMatched numberReturned
        first_root.set('numberMatched', str(number_matched))
        first_root.set('numberReturned', str(number_returned))

        # manipulate the extend / bounding box
        first_root.xpath('.//wfs:boundedBy/gml:Envelope/gml:lowerCorner', namespaces=nsmap)[0].text = '%s %s' % (service['extend'][0], service['extend'][1])
        first_root.xpath('.//wfs:boundedBy/gml:Envelope/gml:upperCorner', namespaces=nsmap)[0].text = '%s %s' % (service['extend'][2], service['extend'][3])

        f = open(service['filename'], 'w')
        f.write(etree.tostring(first_xml))
        f.close()
