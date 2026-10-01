## 2024-05-01 - [Bolt Initialization]
**Learning:** Initializing Bolt journal.
**Action:** Ready to record critical learnings.

## 2024-05-01 - [CLI Wrapper Caching]
**Learning:** Checking file modification times (`mtime`) is a highly effective, low-effort caching strategy for command-line wrappers like `pdf_to_vector.py` around heavy tools (e.g., GDAL).
**Action:** Always consider checking if the output artifact is newer than the input artifact before running expensive synchronous subprocesses.
