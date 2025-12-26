"""
Steps:
1. Sort and normalize geometries
2. Convert to GeoParquet
"""

import json
from glob import glob
import geopandas as gpd
from shapely.geometry import shape, MultiPolygon
from shapely.errors import TopologicalError

MAP_STATUS_EMOJI = {0: "✅ Valid", 1: "❌ Invalid", -1: "❓ Error"}


def check_geometry_validity(file_path):
    """Check if all geometries in a GeoJSON file are valid."""
    try:
        with open(file_path, "r", encoding="utf-8") as out_file:
            data = json.load(out_file)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {file_path}: {e}")
        return -1

    invalid_features = []
    for i, feature in enumerate(data.get("features", [])):
        try:
            geom = shape(feature["geometry"])
            if not geom.is_valid:
                invalid_features.append((i, "Geometry not valid"))
        except (ValueError, TopologicalError) as e:
            invalid_features.append((i, f"Error: {str(e)}"))

    if invalid_features:
        print(f"Invalid features in {file_path}:")
        for idx, msg in invalid_features:
            print(f"  Feature {idx}: {msg}")
        return 1

    return 0


def normalize_geom(geom):
    """Normalize a geometry to a single Polygon or MultiPolygon."""
    if isinstance(geom, MultiPolygon) and len(geom.geoms) == 1:
        return geom.geoms[0]
    return geom


if __name__ == "__main__":
    # first, ensure proper sorting and normalization of geometries
    print("\n--------- Sorting and normalizing geometries ----------\n")
    files = glob("data/geojson/delimitations/*.geojson")
    for f in files:
        sort_by = ["parlimen"] if "parlimen" in f else ["parlimen", "dun"]
        g = gpd.read_file(f)
        g = g.sort_values(by=sort_by).reset_index(drop=True)
        g["geometry"] = g["geometry"].apply(normalize_geom)
        g.to_file(f, driver="GeoJSON", layer_options={"COORDINATE_PRECISION": 6})

    # then, convert to GeoParquet which will be the canonical format for all else
    print("\n--------- Converting to GeoParquet ----------\n")
    for f in files:
        g = gpd.read_file(f)
        g.to_parquet(
            f.replace(".geojson", ".parquet").replace("geojson/", "geoparquet/"), compression="zstd"
        )

    print("\n--------- ✨✨✨ DONE ✨✨✨ ----------\n")
