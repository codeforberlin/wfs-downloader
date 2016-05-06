
SERVICES = {
    'anlagenbaeume': {
        'filename': 'anlagenbaeume.xml',
        'tmp_dir': '/tmp/',
        'url': 'http://fbinter.stadt-berlin.de/fb/wfs/geometry/senstadt/re_anlagenbaeume',
        'extend': [367190.96, 5798934.34, 417447.14, 5838875.02],
        'srid': 'EPSG:25833',
        'layer': 'fis:re_anlagenbaeume',
        'paging': {
            'nx': 4,
            'ny': 4
        }
    },
    'strassenbaeume': {
        'filename': 'strassenbaeume.xml',
        'tmp_dir': '/tmp/',
        'url': 'http://fbinter.stadt-berlin.de/fb/wfs/geometry/senstadt/re_strassenbaeume',
        'extend': [367190.96, 5798934.34, 417447.14, 5838875.02],
        'srid': 'EPSG:25833',
        'layer': 'fis:re_strassenbaeume',
        'paging': {
            'nx': 4,
            'ny': 4
        }
    }
}
