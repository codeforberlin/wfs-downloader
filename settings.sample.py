
SERVICES = {
    'anlagenbaeume': {
        'filename': 'anlagenbaeume.xml',
        'tmp_dir': '/tmp/',
        'url': 'http://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_wfs_baumbestand',
        'extend': [367190.96, 5798934.34, 417447.14, 5838875.02],
        'srid': 'EPSG:25833',
        'layer': 'fis:s_wfs_baumbestand',
        'paging': {
            'nx': 4,
            'ny': 4
        }
    },
    'strassenbaeume': {
        'filename': 'strassenbaeume.xml',
        'tmp_dir': '/tmp/',
        'url': 'http://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_wfs_baumbestand_an',
        'extend': [367190.96, 5798934.34, 417447.14, 5838875.02],
        'srid': 'EPSG:25833',
        'layer': 'fis:s_wfs_baumbestand_an',
        'paging': {
            'nx': 4,
            'ny': 4
        }
    }
}
