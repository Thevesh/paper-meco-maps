"""Validate GeoJSON geometry files for topological errors and invalid geometries."""

import json
from glob import glob as g
from shapely.geometry import shape
from shapely.errors import TopologicalError

MAP_STATUS_EMOJI = {
    0: "✅ Valid",
    1: "❌ Invalid",
    -1: "❓ Error"
}


def check_geometry_validity(file_path):
    """Check if all geometries in a GeoJSON file are valid."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    invalid_features = []

    for i, feature in enumerate(data.get('features', [])):
        try:
            geom = shape(feature['geometry'])
            if not geom.is_valid:
                invalid_features.append((i, "Geometry not valid"))
        except (ValueError, TopologicalError) as e:
            invalid_features.append((i, f"Error: {str(e)}"))

    if invalid_features:
        print("Invalid features found:")
        for idx, msg in invalid_features:
            print(f"  Feature {idx}: {msg}")
        return 1
    else:
        return 0

# Usage
if __name__ == "__main__":
    geojsons = sorted(g("src-geo/delimitations/*.geojson"))
    print("\nChecking geometry validity:\n")
    for geojson in geojsons:
        print(f"{MAP_STATUS_EMOJI[check_geometry_validity(geojson)]}:\ {geojson.replace("src-geo/delimitations/", "")}")

    print('')
