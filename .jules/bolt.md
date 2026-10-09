## 2024-05-13 - Initial Setup
**Learning:** Found an uninitialized environment. Installed GDAL and flake8 as instructed in Memory.
**Action:** Always verify dependencies before analyzing code in a fresh environment.

## 2024-10-09 - Subprocess vs Native GDAL
**Learning:** In highly intensive I/O data pipelines using GDAL, invoking tools like `ogr2ogr` via `subprocess` introduces significant per-operation overhead (process spawning, IPC, string parsing) which can become a bottleneck at scale.
**Action:** When performing Python-based data manipulation with GDAL, prioritize the native `osgeo.gdal` bindings (`gdal.VectorTranslate`, `gdal.Warp`) over subprocess wrappers to maximize throughput. Always remember to call `gdal.UseExceptions()` and properly flush I/O (e.g., `ds = None`).
