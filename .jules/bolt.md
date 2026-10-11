## 2026-10-11 - Avoid Subprocess Overhead with Native C-bindings
**Learning:** Calling command-line tools like `ogr2ogr` via `subprocess` introduces unnecessary overhead and latency when manipulating geospatial data in Python.
**Action:** When working with GDAL/OGR operations, always prefer the native Python C-bindings (`osgeo.gdal`) like `gdal.VectorTranslate` over spawning subprocesses to optimize performance.
