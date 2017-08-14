WFS Downloader
==============

Downloads GML files from a set of WFS service in a pseudo-paginated way using bounding boxes and combine them again to one file.

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

where:

* `url` is the url of the WFS Service,
* `layer` is the name of the Layer,
* `bbox` is the bounding box for th objects you want to retrieve,
* `size` is the extend of a single request (or page),
* `outputfile` is the name of the resulting GML file,
* `projection` is the used projection, and
* `tmpfile` is the path to the directory to store temporary files for each request.

Then run the script with the `config.yml` as argument:

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
