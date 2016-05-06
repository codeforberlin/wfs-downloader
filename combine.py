#!/usr/bin/env python
import os

from lxml import etree

from settings import SERVICES

for key in SERVICES:
    service = SERVICES[key]

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
