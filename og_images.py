import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.io as pio
from glob import glob as g
from helper import generate_slug
from math import log2

from helper import upload_s3_bulk


def calculate_zoom(lon_span, lat_span):
    scale = max(lon_span / 360, lat_span / 180)
    zoom = -log2(scale) + 1
    return min(max(zoom, 0), 20)


def make_image(row, crs=4326):
    done = g(f"api/*.png")
    done = [x.replace("api/", "").replace(".png", "") for x in done]

    feature_gdf = gpd.GeoDataFrame([row], crs=crs)
    slug = (
        generate_slug(feature_gdf.parlimen.iloc[0]) + "-" + generate_slug(feature_gdf.state.iloc[0])
    )
    if slug in done:
        return None
    print(slug)

    minx, miny, maxx, maxy = feature_gdf.total_bounds
    x_margin = (maxx - minx) * 0.1
    y_margin = (maxy - miny) * 0.1
    minx -= x_margin
    maxx += x_margin
    miny -= y_margin
    maxy += y_margin

    center = {"lon": (minx + maxx) / 2, "lat": (miny + maxy) / 2}
    zoom = calculate_zoom(maxx - minx, maxy - miny)

    # fig = px.choropleth_map(
    #     feature_gdf,
    #     geojson=feature_gdf.geometry.__geo_interface__,
    #     locations=feature_gdf.index,
    #     color_discrete_sequence=['rgba(255,0,0,0.3)'],
    #     opacity=0.5,
    #     center=center,
    #     zoom=zoom,
    #     map_style="carto-positron"
    # )

    # fig.update_traces(marker_line_width=2, marker_line_color='red')

    # fig.update_layout(
    #     showlegend=False,
    #     margin={"r":0,"t":0,"l":0,"b":0},
    #     width=1200,
    #     height=630
    # )

    # pio.write_image(fig, f"api/{slug}.png", width=1200, height=630, scale=1)
    return slug, center, zoom


def upload_data(file_pattern="candidates/*", extension=".png"):
    """Upload data files to S3."""
    files = g(f"api/{file_pattern}{extension}")
    files_to_upload = sorted([(f, f.replace(f"api/", "")) for f in files])

    upload_s3_bulk(
        bucket_name="static.electiondata.my",
        files_to_upload=files_to_upload,
        max_workers=120,
    )


if __name__ == "__main__":

    # make images
    files = ["peninsular_2018_parlimen", "sabah_2019_parlimen", "sarawak_2015_parlimen"]
    res = pd.DataFrame(columns=["slug", "center_lat", "center_lon", "zoom"])

    for file in files:
        gf = gpd.read_file(f"src-geo/delimitations/{file}.geojson")
        gf = gf.to_crs(epsg=4326)
        df = pd.DataFrame(columns=["slug", "center_lat", "center_lon", "zoom"])
        for idx, row in gf.iterrows():
            slug, center, zoom = make_image(row, gf.crs)
            df.loc[len(df)] = [slug, center["lat"].round(6), center["lon"].round(6), zoom]

        # upload images
        # upload_data(file_pattern='og-image/*',extension='.png')
        res = pd.concat([res, df])
    res.to_csv("temp.csv", index=False)
