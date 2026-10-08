import argparse
import subprocess
import sys
import os

try:
    from osgeo import gdal
    # Enable exceptions to ensure errors are caught and trigger the fallback
    gdal.UseExceptions()
    HAS_GDAL_BINDINGS = True
except ImportError:
    HAS_GDAL_BINDINGS = False


def convert_pdf_to_vector(input_pdf, output_file, format_name="GeoJSON"):
    """
    Converts a Geospatial PDF to a vector format using GDAL.
    """
    if not os.path.exists(input_pdf):
        print(f"Error: Input file '{input_pdf}' does not exist.")
        sys.exit(1)

    print(f"Converting '{input_pdf}' to '{output_file}' (Format: {format_name})...")

    # Optimization: Use native osgeo.gdal bindings if available to avoid subprocess overhead
    # This avoids spawning a new shell process and is generally faster for repeated or large operations.
    if HAS_GDAL_BINDINGS:
        print("Using native GDAL bindings for faster conversion...")
        try:
            # gdal.VectorTranslate is the equivalent of ogr2ogr
            out_ds = gdal.VectorTranslate(output_file, input_pdf, format=format_name)
            if out_ds is None:
                # If UseExceptions isn't quite doing it, fall back here.
                raise RuntimeError("gdal.VectorTranslate returned None.")
            # Explicitly flush and close the output dataset to ensure data is written to disk
            out_ds = None
            print("Conversion successful!")
            return
        except Exception as e:
            print(f"GDAL bindings failed: {e}. Falling back to subprocess...")
    else:
        print("Native GDAL bindings not found. Falling back to subprocess...")

    # ogr2ogr -f "GeoJSON" output.geojson input.pdf
    cmd = [
        "ogr2ogr",
        "-f", format_name,
        output_file,
        input_pdf
    ]

    try:
        # Run the ogr2ogr command
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Conversion successful!")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during conversion.")
        print(f"Command returned non-zero exit status {e.returncode}.")
        if e.stderr:
            print("Error Details:\n", e.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Error: 'ogr2ogr' command not found. Please ensure GDAL is installed and in your system PATH.")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CAD/Geospatial PDF to a GIS Vector format using GDAL.")
    parser.add_argument("input_pdf", help="Path to the input PDF file")
    parser.add_argument("output_file", help="Path to the output vector file")
    parser.add_argument("--format", dest="format_name", default="GeoJSON",
                        help="Output format (default: GeoJSON). Examples: 'ESRI Shapefile', 'GeoJSON', 'KML'")

    args = parser.parse_args()

    convert_pdf_to_vector(args.input_pdf, args.output_file, args.format_name)
