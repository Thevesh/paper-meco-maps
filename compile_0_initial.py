"""
Validate all hand-produced GeoJSON delimitation to ensure:
- No topologial errors
- No invalid geometries

Then convert all GeoJSON into GeoParquet
"""

import json
from glob import glob as g
import geopandas as gpd
from shapely.geometry import shape
from shapely.errors import TopologicalError

MAP_STATUS_EMOJI = {0: "✅ Valid", 1: "❌ Invalid", -1: "❓ Error"}


def check_geometry_validity(file_path):
    """Check if all geometries in a GeoJSON file are valid."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
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


if __name__ == "__main__":
    files = sorted(g("data/geojson/delimitations/*.geojson"))
    for file in files:
        gf = gpd.read_file(file)
        gf.to_parquet(file.replace(".geojson", ".parquet").replace("geojson/", "geoparquet/"))
