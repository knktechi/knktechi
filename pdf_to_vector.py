import argparse
import subprocess
import sys
import os

try:
    from osgeo import gdal
    gdal.UseExceptions()
    HAS_GDAL = True
except ImportError:
    HAS_GDAL = False


def convert_pdf_to_vector(input_pdf, output_file, format_name="GeoJSON"):
    """
    Converts a Geospatial PDF to a vector format using GDAL's ogr2ogr.
    """
    if not os.path.exists(input_pdf):
        print(f"Error: Input file '{input_pdf}' does not exist.")
        sys.exit(1)

    print(f"Converting '{input_pdf}' to '{output_file}' (Format: {format_name})...")

    # ⚡ Bolt Optimization: Use native GDAL bindings if available to avoid subprocess overhead
    # Impact: Reduces conversion time by eliminating process spawn and inter-process communication overhead.
    if HAS_GDAL:
        try:
            print("Attempting conversion using native GDAL python bindings...")
            # gdal.VectorTranslate is the Python API equivalent of ogr2ogr
            out_ds = gdal.VectorTranslate(output_file, input_pdf, format=format_name)
            # Explicitly flush and close the output dataset to ensure data is completely written to disk
            out_ds = None  # noqa: F841
            print("Conversion successful (Native GDAL)!")
            return
        except Exception as e:
            print(f"Native GDAL conversion failed: {e}. Falling back to subprocess ogr2ogr...")

    # Fallback: ogr2ogr -f "GeoJSON" output.geojson input.pdf
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
