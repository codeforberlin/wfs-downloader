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

```

Then run the script in the same directory as `config.yml` or use the `-c` argument:

```
wfs-downloader
wfs-downloader -c /path/to/my_custom_config.yml
```

Help
----

```
$ wfs-downloader --help
```
