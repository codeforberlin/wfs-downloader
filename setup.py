from setuptools import setup, find_packages

from wfs_downloader import (
    __title__ as title,
    __version__ as version,
    __author__ as author,
    __license__ as license
)

description = 'Downloads GML files from a WFS service in a pseudo-paginated way using bounding boxes and combine them again to one file.'
email = 'mail@jochenklar.de'
url = 'https://github.com/codeforberlin/wfs-downloader'

requirements = [
    'PyYAML'
]

console_scripts = [
    'wfs-downloader=wfs_downloader.download:main'
]

setup(
    name=title,
    version=version,
    description=description,
    url=url,
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    license=license,
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[],
    entry_points={
        'console_scripts': console_scripts
    }
)
