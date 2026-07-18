# General Scientific Formats

Cross-discipline formats: arrays, tables, hierarchical containers, archives, time series, and geospatial. Columns: **ext · format · read with · EDA focus**.

## Arrays & Tables

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.npy` | NumPy array | `numpy.load` (`mmap_mode='r'` for large) | shape, dtype, min/max/mean/std, NaN/inf, sparsity, histogram |
| `.npz` | compressed NumPy archive | `numpy.load` → dict-like | array list, per-array shapes, compression ratio |
| `.csv` | comma-separated values | `pandas.read_csv`, `polars`, `numpy.genfromtxt` | rows/cols, dtype inference, missing patterns, stats, correlation, duplicates, encoding |
| `.tsv`/`.tab` | tab-separated | `pandas.read_csv(sep='\t')` | as CSV; verify tab vs space, quoting |
| `.xlsx`/`.xls` | Excel | `pandas.read_excel`, `openpyxl`, `xlrd` (legacy) | sheet enumeration, per-sheet stats, formulas, merged/hidden cells, named ranges |
| `.json` | JSON | `json`, `pandas.read_json`, `ujson` | schema inference, nesting depth, key/value distribution, type consistency |
| `.xml` | XML | `lxml`, `xml.etree.ElementTree`, `xmltodict` | schema/DTD validation, element hierarchy, namespaces, attribute vs text |
| `.yaml`/`.yml` | YAML | `yaml.safe_load`, `ruamel.yaml` | config structure, depth, anchors/aliases, multi-doc, schema validation |
| `.toml` | TOML | `tomllib` (3.11+), `tomli`, `toml` | sections, key/value types, nested tables, required vs optional |
| `.ini` | INI | `configparser` | sections, key/value, type conversion, comments |

## Binary & Compressed Containers

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.hdf5`/`.h5` | HDF5 | `h5py`, `pytables`, `pandas` HDFStore | group/dataset hierarchy, shapes/dtypes, attributes, chunking/compression, sampling |
| `.zarr` | chunked array store | `zarr`, `xarray` | dimensions, chunk size, codec/ratio, multi-scale hierarchy, attributes |
| `.gz`/`.bz2` | gzip / bzip2 | `gzip`, `bz2` (pandas auto-handles) | compression ratio, inner file type, decompression validation |
| `.zip` | ZIP archive | `zipfile` | member listing, per-file method, total vs compressed size, structure |
| `.tar`/`.tar.gz` | TAR archive | `tarfile` | member listing, compression, directory structure, extraction test |

## Time Series & Waveforms

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.wav` | audio waveform | `scipy.io.wavfile`, `soundfile`, `wave` | sample rate, duration, bit depth, channels, amplitude dist, FFT, clipping, SNR |
| `.mat` | MATLAB data | `scipy.io.loadmat`; `h5py`/`mat73` for v7.3 | variable names/types, dimensions, struct fields, sparse detection |
| `.edf` | European Data Format | `pyedflib`, `mne` | signal count/names, sampling freqs, ranges/units, duration, annotations, saturation |
| `.csv` (time series) | timestamped CSV | `pandas.read_csv(parse_dates=)` | temporal range/resolution, sampling regularity, gaps, trend/seasonality, stationarity, autocorrelation |

## Geospatial & Environmental

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.shp` | Shapefile | `geopandas`, `fiona`, `pyshp` | geometry type/count, CRS, bounding box, attribute table, validity, sidecar files |
| `.geojson` | GeoJSON | `geopandas`, `json` | feature count/types, CRS, bbox, property schema, geometry complexity |
| `.tif`/`.tiff` (geo) | GeoTIFF | `rasterio`, `gdal`, `rioxarray` | dims/resolution, band count, CRS, geotransform, NoData, pixel histogram, overviews |
| `.nc`/`.netcdf` | NetCDF | `netCDF4`, `xarray` | variables, dimensions, CF metadata, spatial/temporal coverage, chunking |
| `.grib`/`.grib2` | Gridded Binary | `pygrib`, `cfgrib` | message inventory, parameters/levels, grid spec, temporal coverage, ensemble members |
| `.hdf4` | HDF4 (NASA EOS) | `pyhdf`, `gdal` | scientific dataset listing, Vdata/attributes, dimension scales, quality flags |

## Specialized

| ext | format | read with | EDA focus |
|-----|--------|-----------|-----------|
| `.fits` | FITS (astronomy) | `astropy.io.fits`, `fitsio` | HDU structure, image dims + WCS, header keywords, table columns, scaling, checksum |
| `.asdf` | ASDF | `asdf` | tree structure, schema validation, internal/external arrays, compression, versioning |
| `.root` | CERN ROOT | `uproot`, `ROOT` | TTree structure, branch types/entries, histograms, compression, split level |
| `.txt`/`.dat` | generic text/binary | `pandas`, `numpy.loadtxt`/`fromfile`, `struct` | delimiter/header detection, dtype inference, missing codes, endianness (binary) |
| `.log` | log file | text read, `pandas`, regex | log-level distribution, timestamps, error/warning frequency, event sequencing, anomalies |

**Notes:** For arrays/HDF5/Zarr, prefer memory-mapped or chunked reads on large files. Sample the first N rows for big CSVs (the analyzer script defaults to 10,000). Never treat lossy or derived formats as raw quantitative data.
