"""
Convert canonical GeoParquet files into multiple geospatial data formats.

Steps:
1. For each file found in /data/geoparquet/*/*
    - Convert to GeoJSON, FlatGeobuf (FGB), and KML formats.
    - Skip GeoJSON export for "delimitations" files to preserve originals.
2. For each exported GeoJSON file in /data/geojson/*/*
    - Generate a corresponding TopoJSON file using geo2topo.

Dependencies:
- geo2topo installed globally: https://www.npmjs.com/package/topojson-server
"""

import warnings
import subprocess as sb
from glob import glob
import geopandas as gpd


def convert_files(file_type="delimitations"):
    """GeoParquet --> GeoJSON, FlatGeobuf, KML, TopoJSON"""
    files = sorted(glob(f"data/geoparquet/{file_type}/*"))
    for file in files:
        print(file)
        gf = gpd.read_parquet(file)
        name_field = "parlimen" if "parlimen" in gf.columns else "dun"

        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="Layer name '.*' adjusted to '.*' for XML validity.",  # suppres KML warning; known limitation of the format
                category=RuntimeWarning,
                module="pyogrio.raw",
            )

            # GeoJson: Skip for delimitations to preserve original source
            if "delimitations" not in file:  # don't override original GeoJSON source
                gf.to_file(
                    file.replace("geoparquet/", "geojson/").replace(".parquet", ".geojson"),
                    driver="GeoJSON",
                )

            # FlatGeobuf: Natively supported with geopandas
            gf.to_file(
                file.replace("geoparquet/", "fgb/").replace(".parquet", ".fgb"), driver="FlatGeobuf"
            )

            # KML: Need to set name to avoid attribute mixups
            gf["name"] = gf[name_field]
            gf.to_file(
                file.replace("geoparquet/", "kml/").replace(".parquet", ".kml"),
                driver="KML",
            )

        # TopoJSON: Call to command line to run geo2topo
        file_geojson = file.replace("geoparquet/", "geojson/").replace(".parquet", ".geojson")
        file_topojson = file.replace("geoparquet/", "topojson/").replace(".parquet", ".topojson")
        sb.run(f"geo2topo {file_geojson} > {file_topojson}", shell=True, check=True)


if __name__ == "__main__":
    print("\n--------- Compiling delimitations ----------\n")
    convert_files(file_type="delimitations")

    print("\n--------- Compiling elections ----------\n")
    convert_files(file_type="elections")

    print("\n--------- Compiling cartogram-electorate ----------\n")
    convert_files(file_type="cartogram-electorate")

    print("\n--------- Compiling cartogram-equal ----------\n")
    convert_files(file_type="cartogram-equal")

    print("\n--------- ✨✨✨ DONE ✨✨✨ ----------\n")
