WFS Downloader
==============

Downloads GML files from a set of WFS service in a pseudo-paginated way using bounding boxes and combine them again to one file. The WFS services are specified in settings.py.

Prerequisites
-------------
The download-script requires the `lxml` package.
You can install it via `pip install -r requirements.txt`.

Install
-------

```
pip install wfs-downloader
```

Usage
-----

Create a `config.yml` specifying your setup like this:

```yml
url: http://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_wfs_baumbestand_an
layer: fis:s_wfs_baumbestand_an

bbox:
  west:   370000.0
  south: 5800000.0
  east:   415000.0
  north: 5837000.0

size: 10000
outputfile: strassenbaeume.xml
projection: EPSG:25833
tmpdir: /tmp
```

Then run the script in the same directory as `config.yml` or use the `-c` argument:

```
wfs-downloader config.yml
```

Help
----

```
$ wfs-downloader --help
usage: Downloads GML files from a set of WFS service in a pseudo-paginated way using bounding boxes and combine them again to one file. The WFS services are specified in settings.py.

positional arguments:
  config         config file

optional arguments:
  -h, --help     show this help message and exit
  --no-download  skip the download
  --no-combine   skip the combine
```
