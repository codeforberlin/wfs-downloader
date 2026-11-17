WFS Downloader
==============

Downloads GML files from a [WFS 2.0](https://www.ogc.org/standard/wfs/) service in a pseudo-paginated way using bounding boxes and combines them again into one file.

Many WFS services limit how many features a single request may return. `wfs-downloader` splits a large bounding box into square tiles, downloads each tile with a separate `GetFeature` request, and then merges all tiles into one GML file. Progress bars show how many tiles are downloaded and merged.

Setup
-----

```
pip install wfs-downloader                                       # from PyPI
pip install git+https://github.com/codeforberlin/wfs-downloader  # directly from GitHub
```

Usage
-----

Create a `config.yml` specifying your setup, e.g. for all street trees in Berlin:

```yml
url: https://gdi.berlin.de/services/wfs/baumbestand
layer: baumbestand:strassenbaeume

bbox:
  west:   360000.0
  south: 5790000.0
  east:   420000.0
  north: 5840000.0

size: 10000
outputfile: strassenbaeume.xml
projection: EPSG:25833
tmpdir: tmp
```

where:

* `url` is the URL of the WFS service, without query parameters,
* `layer` is the name of the layer (the `typeNames` of the request),
* `bbox` is the bounding box for the objects you want to retrieve, in the units of `projection`,
* `size` is the edge length of a single tile (or page), in the units of `projection`,
* `outputfile` is the path of the resulting GML file,
* `projection` is the projection used for the requests and the result, and
* `tmpdir` is the directory to store the downloaded tiles. It is created if it does not exist.

The example covers Berlin with 6 × 5 tiles of 10 × 10 km, i.e. 30 requests.

Then run the script with the `config.yml` as argument:

```
wfs-downloader config.yml
```

To only download the tiles, or to only merge tiles that were already downloaded, use:

```
wfs-downloader config.yml --no-combine
wfs-downloader config.yml --no-download
```
