import argparse
import subprocess
import sys
import os
import time

try:
    from osgeo import gdal
    GDAL_AVAILABLE = True
except ImportError:
    GDAL_AVAILABLE = False

def convert_pdf_to_vector(input_pdf, output_file, format_name="GeoJSON"):
    """
    Converts a Geospatial PDF to a vector format using GDAL's ogr2ogr.
    """
    if not os.path.exists(input_pdf):
        print(f"Error: Input file '{input_pdf}' does not exist.")
        sys.exit(1)

    print(f"Converting '{input_pdf}' to '{output_file}' (Format: {format_name})...")

    if GDAL_AVAILABLE:
        print("Using native GDAL Python bindings for conversion...")
        try:
            gdal.UseExceptions()
            options = gdal.VectorTranslateOptions(format=format_name)

            # Start timer for performance measurement
            start_time = time.time()

            # Perform conversion using VectorTranslate
            out_ds = gdal.VectorTranslate(output_file, input_pdf, options=options)

            # Important: Flush and close the output dataset to ensure data is written
            out_ds = None

            end_time = time.time()

            print(f"Conversion successful! Took {end_time - start_time:.2f} seconds.")
            return
        except Exception as e:
            print(f"Native GDAL conversion failed: {e}")
            print("Falling back to subprocess ogr2ogr...")
            # Fall through to subprocess

    print("Using subprocess ogr2ogr for conversion...")
    # ogr2ogr -f "GeoJSON" output.geojson input.pdf
    cmd = [
        "ogr2ogr",
        "-f", format_name,
        output_file,
        input_pdf
    ]

    try:
        start_time = time.time()
        # Run the ogr2ogr command
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        end_time = time.time()
        print(f"Conversion successful! Took {end_time - start_time:.2f} seconds.")
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
