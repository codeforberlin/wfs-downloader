WFS Downloader
==============

Downloads GML files from a set of WFS service in a pseudo-paginated way using bounding boxes and combine them again to one file. The WFS services are specified in settings.py.

Prerequisites
-------------
The download-script requires Python 2 and the `lxml` package.

Setup
-----

```
cp settings.sample.py settings.py
```

Edit `settings.py` for services.


Usage
-----

```
./download.py
```

Help
----

```
./download.py --help
usage: Downloads GML files from a set of WFS service in a pseudo-paginated way using bounding boxes and combine them again to one file. The WFS services are specified in settings.py.

optional arguments:
  -h, --help         show this help message and exit
  --no-download      skip the download
  --no-combine       skip the combine
  --service SERVICE  download/combine only this service
```
