import argparse
import subprocess
import sys
import os


def convert_pdf_to_vector(input_pdf, output_file, format_name="GeoJSON"):
    """
    Converts a Geospatial PDF to a vector format using GDAL's ogr2ogr.
    """
    if not os.path.exists(input_pdf):
        print(f"Error: Input file '{input_pdf}' does not exist.")
        sys.exit(1)

    print(f"Converting '{input_pdf}' to '{output_file}' (Format: {format_name})...")

    try:
        # ⚡ Bolt Optimization: Attempt to use native GDAL Python bindings first
        # This avoids the overhead of spawning a subprocess and parsing stdout/stderr.
        # It's faster and uses memory more efficiently.
        from osgeo import gdal

        # Translate the dataset directly using the GDAL API
        options = gdal.VectorTranslateOptions(format=format_name)
        out_ds = gdal.VectorTranslate(output_file, input_pdf, options=options)

        if out_ds is not None:
            # Explicitly close the dataset to flush data to disk completely
            out_ds = None
            print("Conversion successful! (Using native GDAL bindings)")
            return
        else:
            print("Error: gdal.VectorTranslate failed to generate output.")
            sys.exit(1)

    except ImportError:
        print("Notice: 'osgeo.gdal' Python bindings not available, falling back to subprocess.")
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
            print("Conversion successful! (Using subprocess ogr2ogr)")
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
