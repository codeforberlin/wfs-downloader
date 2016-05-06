#!/usr/bin/env python
import urllib

from settings import SERVICES

for key in SERVICES:
    service = SERVICES[key]

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
