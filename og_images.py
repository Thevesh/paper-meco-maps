"""
Script to generate and upload OG (Open Graph) images for each parliamentary constituency and state.

Steps:

    1. Read geometry and attribute data (e.g., constituency boundaries and metadata).
    2. For each row (constituency or state), generate a corresponding GeoPandas GeoDataFrame.
    3. For each item not already processed, calculate proper map bounding box with appropriate margins.
    4. Calculate map center and zoom level for visualization.
    5. Render map visualization using Plotly, highlighting the constituency/state area.
    6. Save the resulting image to the `api` directory, avoiding recomputation when possible.
    7. Upload generated images in bulk to S3 storage using helper scripts.

Notes:
    - Uses Plotly for map rendering.
    - Utilizes helper functions for slug generation and S3 uploads.
    - Skip regeneration if image for a given area already exists in the output folder.
"""

from glob import glob
from math import log2
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.io as pio

from helper import generate_slug, upload_s3_bulk


def calculate_zoom(lon_span, lat_span):
    """Calculate a suitable zoom level (for map display)
    based on the spans of longitude and latitude.
    Returns a value generally between 0-20 for web mapping.
    """
    scale = max(lon_span / 360, lat_span / 180)
    zoom_value = -log2(scale) + 1
    return min(max(zoom_value, 0), 20)


def make_image(feature_row, crs=4326):
    """Generate center, zoom, and slug for an area,
    checking if the image already exists. Returns tuple
    (slug, center, zoom) or None if already done.
    Generates both light and dark versions of the image.
    """
    done = glob("api/og-image/*.png")
    done = [x.replace("api/og-image/", "").replace(".png", "") for x in done]

    feature_gdf = gpd.GeoDataFrame([feature_row], crs=crs)
    feature_slug = (
        generate_slug(feature_gdf.dun.iloc[0]) + "-" + generate_slug(feature_gdf.state.iloc[0])
    )

    # Check if both light and dark versions already exist
    if feature_slug in done and f"{feature_slug}-dark" in done:
        return None
    print(feature_slug)

    minx, miny, maxx, maxy = feature_gdf.total_bounds
    x_margin = (maxx - minx) * 0.1
    y_margin = (maxy - miny) * 0.1
    minx -= x_margin
    maxx += x_margin
    miny -= y_margin
    maxy += y_margin

    center_dict = {"lon": (minx + maxx) / 2, "lat": (miny + maxy) / 2}
    zoom_level = calculate_zoom(maxx - minx, maxy - miny)

    # Generate light version
    if feature_slug not in done:
        fig_light = px.choropleth_map(
            feature_gdf,
            geojson=feature_gdf.geometry.__geo_interface__,
            locations=feature_gdf.index,
            color_discrete_sequence=["rgba(255,0,0,0.3)"],
            opacity=0.5,
            center=center_dict,
            zoom=zoom_level,
            map_style="carto-positron",
        )

        fig_light.update_traces(marker_line_width=2, marker_line_color="red")

        fig_light.update_layout(
            showlegend=False, margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=1200, height=630
        )

        pio.write_image(
            fig_light, f"api/og-image/{feature_slug}.png", width=1200, height=630, scale=1
        )

    # Generate dark version
    if f"{feature_slug}-dark" not in done:
        fig_dark = px.choropleth_map(
            feature_gdf,
            geojson=feature_gdf.geometry.__geo_interface__,
            locations=feature_gdf.index,
            color_discrete_sequence=["rgba(239,68,68,0.6)"],  # Brighter red fill
            opacity=0.7,  # Increased opacity
            center=center_dict,
            zoom=zoom_level,
            map_style="carto-darkmatter",
        )

        fig_dark.update_traces(marker_line_width=2, marker_line_color="rgb(248,113,113)")

        fig_dark.update_layout(
            showlegend=False, margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=1200, height=630
        )

        pio.write_image(
            fig_dark, f"api/og-image/{feature_slug}-dark.png", width=1200, height=630, scale=1
        )

    return feature_slug, center_dict, zoom_level


def upload_data(file_pattern="candidates/*", extension=".png"):
    """Upload PNG images (or other data files) from `api/` to S3 in bulk.

    Args:
        file_pattern (str): Glob pattern inside the api directory.
        extension (str): File extension to match.
    """
    files = glob(f"api/{file_pattern}{extension}")
    files_to_upload = sorted([(f, f.replace("api/", "")) for f in files])

    upload_s3_bulk(
        bucket_name="static.electiondata.my",
        files_to_upload=files_to_upload,
        max_workers=120,
    )


if __name__ == "__main__":

    # FILES = ["peninsular_2018_parlimen", "sabah_2019_parlimen", "sarawak_2015_parlimen"]
    FILES = []
    res = pd.DataFrame(columns=["slug", "center_lat", "center_lon", "zoom"])

    for filename in FILES:
        gf = gpd.read_file(f"data/geojson/delimitations/{filename}.geojson")
        gf = gf.to_crs(epsg=4326)
        df = pd.DataFrame(columns=["slug", "center_lat", "center_lon", "zoom"])
        for idx, row in gf.iterrows():
            result = make_image(row, gf.crs)
            if result is not None:
                slug, center, zoom = result
                df.loc[len(df)] = [
                    slug,
                    round(center["lat"], 6),
                    round(center["lon"], 6),
                    zoom,
                ]

        if len(res) == 0:
            res = df.copy()
        else:
            res = pd.concat([res, df])
    upload_data(file_pattern="og-image/*", extension=".png")
    res.to_csv("temp.csv", index=False)
