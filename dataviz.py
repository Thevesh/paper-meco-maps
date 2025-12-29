"""
Generates all data visualisations used in the paper.
Dataviz generated:
    1. Heatmap of number of Parliament seats at each delimitation round.
    2. Heatmap of number of DUN seats at each delimitation round.
    3. Implied coastline of Penang.
    4. Plot of Semporna.
    5. Choropleth map vs Dorling cartogram
    6. Topology-preserving cartogram
    7. Error validation
"""

import duckdb
import geopandas as gpd
import cartogram
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
import seaborn as sb

BALLOTS = "https://public.electiondata.my/results/consol_ballots.parquet"
STATS = "https://public.electiondata.my/results/consol_stats.parquet"


def heatmap_n_parlimen():
    """
    Heatmap of number of Parliament seats at each delimitation round.
    """
    q = r"""
    WITH g AS (
    SELECT
        regexp_extract(filename, '_(\d{4})_', 1)::INT AS year,
        state
    FROM parquet_scan('data/geoparquet/delimitations/*parlimen*.parquet', filename=true)
    ),
    counts AS (
    SELECT year, state, COUNT(*) AS n
    FROM g
    WHERE year IS NOT NULL
    GROUP BY year, state
    ),
    ranked AS (
    SELECT
        state,
        year,
        n,
        6 - (ROW_NUMBER() OVER (PARTITION BY state ORDER BY year DESC) - 1) AS round
    FROM counts
    )
    SELECT round, year, state, n
    FROM ranked
    ORDER BY state, year;
    """

    df = duckdb.sql(q).df().drop("year", axis=1)
    df = df.pivot(index="state", columns="round", values="n")
    df = pd.concat(
        [
            df[df.index.isin(["Sabah", "Sarawak"])].sort_values(6, ascending=False),
            df[~df.index.isin(["Sabah", "Sarawak"])].sort_values(6, ascending=False),
        ]
    )

    ss = "\n\n\n\n"
    df.columns = [
        f"0{ss}PEN: 1955{ss}SBH: - {ss}SWK: - \n",
        f"1{ss}PEN: 1959{ss}SBH: 1967{ss}SWK: 1967\n",
        f"2{ss}PEN: 1974{ss}SBH: 1974{ss}SWK: 1977\n",
        f"3{ss}PEN: 1984{ss}SBH: 1984{ss}SWK: 1987\n",
        f"4{ss}PEN: 1994{ss}SBH: 1994{ss}SWK: 1996\n",
        f"5{ss}PEN: 2003{ss}SBH: 2003{ss}SWK: 2005\n",
        f"6{ss}PEN: 2018{ss}SBH: 2019{ss}SWK: 2015\n",
    ]

    # heatmap
    _, ax = plt.subplots(figsize=[9, 6])  # width, height
    sb.heatmap(
        df,
        annot=True,
        fmt=",.0f",
        annot_kws={"fontsize": 11},
        vmin=-1,
        cmap="Blues",
        cbar=False,
        cbar_kws={"shrink": 0.9},
        ax=ax,
    )
    ax.set_ylabel("")
    ax.set_xlabel("")
    ax.set_facecolor("white")
    # ax.set_title('Seats per Federal Election by State\n', fontsize=10.5, linespacing=1)

    # ticks
    plt.yticks(rotation=0)
    ax.tick_params(
        axis="both",
        which="both",
        length=0,
        labelsize=11,
        labelbottom=False,
        labeltop=True,
        bottom=False,
        top=False,
    )
    plt.xticks(rotation=0, linespacing=0.3)

    plt.savefig("tex/dataviz/heatmap_delim_parlimen.png", dpi=400, bbox_inches="tight")
    plt.savefig("tex/dataviz/heatmap_delim_parlimen.eps", bbox_inches="tight")
    plt.close()


def heatmap_n_dun():
    """
    Heatmap of number of DUN seats at each delimitation round.
    """
    q = r"""
    WITH g AS (
    SELECT
        regexp_extract(filename, '_(\d{4})_', 1)::INT AS year,
        state
    FROM parquet_scan('data/geoparquet/delimitations/*dun*.parquet', filename=true)
    ),
    counts AS (
    SELECT year, state, COUNT(*) AS n
    FROM g
    WHERE year IS NOT NULL
    GROUP BY year, state
    ),
    ranked AS (
    SELECT
        state,
        year,
        n,
        6 - (ROW_NUMBER() OVER (PARTITION BY state ORDER BY year DESC) - 1) AS round
    FROM counts
    )
    SELECT round, year, state, n
    FROM ranked
    ORDER BY state, year;
    """

    df = duckdb.sql(q).df().drop("year", axis=1)
    df = df.pivot(index="state", columns="round", values="n")
    df = pd.concat(
        [
            df[df.index.isin(["Sabah", "Sarawak"])].sort_values(6, ascending=False),
            df[~df.index.isin(["Sabah", "Sarawak"])].sort_values(6, ascending=False),
        ]
    )

    ss = "\n\n\n\n"
    df.columns = [
        f"1{ss}PEN: 1959{ss}SBH: 1967{ss}SWK: 1967\n",
        f"2{ss}PEN: 1974{ss}SBH: 1974{ss}SWK: 1977\n",
        f"3{ss}PEN: 1984{ss}SBH: 1984{ss}SWK: 1987\n",
        f"4{ss}PEN: 1994{ss}SBH: 1994{ss}SWK: 1996\n",
        f"5{ss}PEN: 2003{ss}SBH: 2003{ss}SWK: 2005\n",
        f"6{ss}PEN: 2018{ss}SBH: 2019{ss}SWK: 2015\n",
    ]

    # heatmap
    _, ax = plt.subplots(figsize=[9, 5])  # width, height
    sb.heatmap(
        df,
        annot=True,
        fmt=",.0f",
        annot_kws={"fontsize": 11},
        vmin=-1,
        cmap="Blues",
        cbar=False,
        cbar_kws={"shrink": 0.9},
        ax=ax,
    )
    ax.set_ylabel("")
    ax.set_xlabel("")
    ax.set_facecolor("white")
    # ax.set_title('Seats per Federal Election by State\n', fontsize=10.5, linespacing=1)

    # ticks
    plt.yticks(rotation=0)
    ax.tick_params(
        axis="both",
        which="both",
        length=0,
        labelsize=11,
        labelbottom=False,
        labeltop=True,
        bottom=False,
        top=False,
    )
    plt.xticks(rotation=0, linespacing=0.3)

    plt.savefig("tex/dataviz/heatmap_delim_dun.png", dpi=400, bbox_inches="tight")
    plt.savefig("tex/dataviz/heatmap_delim_dun.eps", bbox_inches="tight")
    plt.close()


def penang_coastline():
    """
    Implied coastline of Penang.
    """
    gf = {}
    for y in [1974, 1994, 2018]:
        tf = gpd.read_parquet(f"data/geoparquet/delimitations/peninsular_{y}_parlimen.parquet")
        gf[y] = tf[tf.state == "Pulau Pinang"][["state", "geometry"]].dissolve(by="state")

    plt.rcParams.update(
        {
            "font.size": 12,
            "font.family": "sans-serif",
            "grid.linestyle": "dotted",
            "figure.figsize": [6, 6],
            "figure.autolayout": True,
        }
    )
    _, ax = plt.subplots()
    ax.set_axisbelow(True)
    ax.tick_params(
        axis="both",
        which="both",
        top=True,
        right=True,
        direction="inout",
        labeltop=True,
        labelright=True,
    )
    ax.grid(True, color="lightgrey")
    ax.set_xlim(100.16, 100.36)
    ax.set_ylim(5.25, 5.5)

    gf[2018].plot(edgecolor="red", linewidth=1, facecolor="white", ax=ax)
    gf[1994].plot(edgecolor="black", linewidth=1, facecolor="white", ax=ax)

    legend_elements = [
        Line2D([0], [0], color="black", lw=2, label="1994"),
        Line2D([0], [0], color="red", lw=2, label="2018"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", frameon=True, framealpha=1)
    plt.savefig("tex/dataviz/penang_coastline.png", dpi=400, bbox_inches="tight")
    plt.savefig("tex/dataviz/penang_coastline.eps", bbox_inches="tight")
    plt.close()


def semporna_latest():
    """
    Plot of Semporna as of latest delimitation.
    """
    gf = gpd.read_parquet("data/geoparquet/delimitations/sabah_2019_parlimen.parquet")
    gf = gf[gf["parlimen"] == "P.189 Semporna"]

    plt.rcParams.update(
        {
            "font.size": 12,
            "font.family": "sans-serif",
            "grid.linestyle": "dotted",
            "figure.figsize": [6, 6],
            "figure.autolayout": True,
        }
    )
    _, ax = plt.subplots()
    ax.set_axisbelow(True)
    ax.tick_params(
        axis="both",
        which="both",
        top=True,
        right=True,
        direction="inout",
        labeltop=True,
        labelright=True,
    )
    ax.grid(True, color="lightgrey")

    gf.plot(edgecolor="red", linewidth=1, facecolor="white", ax=ax)

    plt.savefig("tex/dataviz/semporna_latest.png", dpi=400, bbox_inches="tight")
    plt.savefig("tex/dataviz/semporna_latest.eps", bbox_inches="tight")
    plt.close()


def choropleth_v_dorling():
    """
    Plot GE-15 results for Peninsular Malaysia using choropleth vs Dorling cartogram
    """
    party_color = {
        "PH": "#e41a1c",  # Red
        "PN": "#4daf4a",  # Green
        "BN": "#031a93",  # Blue
    }

    df = pd.read_parquet(BALLOTS)
    df = df[(df.election == "GE-15") & (df.result == "won")][["state", "seat", "coalition"]].rename(
        columns={"seat": "parlimen", "coalition": "party"}
    )

    gf = {
        "map": gpd.read_parquet("data/geoparquet/elections/MYS_GE-15.parquet"),
        "ce": gpd.read_parquet("data/geoparquet/cartogram-electorate/MYS_GE-15.parquet"),
    }
    for t in ["map", "ce"]:
        gf[t] = gf[t].to_crs(4326)
        gf[t] = gf[t][~gf[t].state.isin(["Sabah", "Sarawak", "W.P. Labuan"])]
        gf[t] = gf[t].merge(df, on=["state", "parlimen"], how="left")
        gf[t]["colour"] = gf[t].party.map(party_color)

    plt.rcParams.update(
        {
            "font.size": 12,
            "font.family": "sans-serif",
            "grid.linestyle": "dotted",
            "figure.figsize": [11, 6],
            "figure.autolayout": True,
        }
    )
    fig, ax = plt.subplots(1, 2)
    ax[0].axis("off")
    ax[1].axis("off")

    gf["map"].boundary.plot(edgecolor="#eeeeee", linewidth=0.03, ax=ax[1], zorder=0)
    for p in list(party_color.keys())[:3]:
        gf["map"][(gf["map"].party == p)].plot(
            color=party_color[p], edgecolor="#555555", linewidth=0.1, ax=ax[0], zorder=1
        )
        gf["ce"][(gf["ce"].party == p)].plot(color=party_color[p], ax=ax[1], zorder=1)

    legend_handles = [
        mpatches.Patch(color=color, label=party) for party, color in party_color.items()
    ]
    fig.legend(
        handles=legend_handles,
        loc="upper center",
        ncols=3,
        frameon=True,
        framealpha=1,
        bbox_to_anchor=(0.5, 1.05),
    )
    plt.savefig("tex/dataviz/choropleth_v_dorling.png", dpi=400, bbox_inches="tight")
    plt.savefig("tex/dataviz/choropleth_v_dorling.eps", bbox_inches="tight")
    plt.close()


def topology_preserving_cartogram():
    """
    Plot topology-preserving cartogram.
    """
    party_color = {
        "PH": "#e41a1c",  # Red
        "PN": "#4daf4a",  # Green
        "BN": "#031a93",  # Blue
    }

    df = duckdb.query(
        f"SELECT state, seat AS parlimen, coalition AS party FROM '{BALLOTS}' WHERE election = 'GE-15' AND result = 'won'"
    ).to_df()
    vf = duckdb.query(
        f"SELECT state, seat AS parlimen, voters_total FROM '{STATS}' WHERE election = 'GE-15'"
    ).to_df()

    gf = gpd.read_parquet("data/geoparquet/elections/MYS_GE-15.parquet")
    gf = gf.to_crs(epsg=3375)
    gf = gf[~gf.state.isin(["Sabah", "Sarawak", "W.P. Labuan"])]
    gf = gf.merge(df, on=["state", "parlimen"], how="left")
    gf = gf.merge(vf, on=["state", "parlimen"], how="left")
    gf["colour"] = gf.party.map(party_color)
    gf["area"] = gf.geometry.area
    gf["density"] = gf.voters_total / gf.area
    gf["scale"] = gf.density / gf.density.max()

    c = gf.copy()
    c = cartogram.Cartogram(c, "voters_total", max_iterations=25)

    plt.rcParams.update(
        {
            "font.size": 12,
            "font.family": "sans-serif",
            "grid.linestyle": "dotted",
            "figure.figsize": [6, 6],
            "figure.autolayout": True,
        }
    )
    fig, ax = plt.subplots()
    ax.axis("off")

    gf.boundary.plot(edgecolor="#cccccc", linewidth=0.15, ax=ax, zorder=1)
    for p, colour in party_color.items():
        c[c.party == p].plot(color=colour, ax=ax, zorder=2)

    legend_handles = [
        mpatches.Patch(color=color, label=party) for party, color in party_color.items()
    ]
    fig.legend(
        handles=legend_handles,
        loc="upper center",
        ncols=3,
        frameon=True,
        framealpha=1,
        bbox_to_anchor=(0.5, 1.03),
    )

    plt.savefig("tex/dataviz/topology_preserving_cartogram.png", dpi=400, bbox_inches="tight")
    plt.savefig("tex/dataviz/topology_preserving_cartogram.eps", bbox_inches="tight")
    plt.close()


def derived_v_reported():
    """
    Plot derived area vs reported area of DUNs.
    """
    files = {
        0: [2018, 2019, 2015],
        1: [2003, 2003, 2005],
        2: [1994, 1994, 1996],
    }

    plt.rcParams.update(
        {
            "font.size": 10,
            "font.family": "sans-serif",
            "grid.linestyle": "dotted",
            "figure.figsize": [8, 8],
            "figure.autolayout": False,  # IMPORTANT: don't fight tight_layout()
        }
    )

    fig, axarr = plt.subplots(2, 2)

    # Bottom row axes (normal)
    ax_bl = axarr[1, 0]
    ax_br = axarr[1, 1]

    # Top axis (we'll recenter later)
    ax_top = axarr[0, 0]
    fig.delaxes(axarr[0, 1])  # remove unused top-right cell

    axes = [ax_top, ax_bl, ax_br]

    for ax, (i, (sm, sbh, swk)) in zip(axes, files.items()):
        title = f"Peninsular {sm}, Sabah {sbh}, Sarawak {swk}\n"

        df = pd.concat(
            [
                pd.read_csv(f"logs/peninsular_{sm}_dun.csv"),
                pd.read_csv(f"logs/sabah_{sbh}_dun.csv"),
                pd.read_csv(f"logs/sarawak_{swk}_dun.csv"),
            ],
            ignore_index=True,
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        min_val = min(df["area_gazette"].min(), df["area_compute"].min())
        max_val = max(df["area_gazette"].max(), df["area_compute"].max())

        ax.plot(
            [min_val, max_val],
            [min_val, max_val],
            color="grey",
            linestyle="--",
            label="y=x",
        )

        ax.scatter(df["area_gazette"], df["area_compute"], c="black")

        vspace = "\n\n" if i == 0 else ""
        ax.set_xlabel(f"\nArea per Delimitation Report (km²){vspace}", linespacing=0.67)
        ax.set_ylabel("Computed Area (km²)\n", linespacing=0.67)
        ax.set_title(title, fontsize=10, linespacing=1.5)

        ax.xaxis.set_major_formatter(lambda x, _: f"{x:,.0f}")
        ax.yaxis.set_major_formatter(lambda y, _: f"{y:,.0f}")

        ax.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9), frameon=True, framealpha=1)

    # Let matplotlib finalize layout first
    plt.tight_layout()
    fig.canvas.draw()

    # Recenter the top axis only AFTER tight_layout
    pos_bl = ax_bl.get_position()
    pos_br = ax_br.get_position()

    w = pos_bl.width
    h = pos_bl.height
    x_center = (pos_bl.x0 + pos_br.x1) / 2
    x0 = x_center - w / 2

    pos_top = ax_top.get_position()
    y0 = pos_top.y0  # keep same vertical placement

    ax_top.set_position([x0, y0, w, h])

    plt.savefig("tex/dataviz/area_derived_v_reported.png", dpi=400, bbox_inches="tight")
    plt.savefig("tex/dataviz/area_derived_v_reported.eps", bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    print("\nPlotting implied coastline of Penang...")
    penang_coastline()
    print("\nPlotting Semporna as of latest delimitation (2019)...")
    semporna_latest()
    print("\nPlotting GE15 results on choropleth vs Dorling cartogram...")
    choropleth_v_dorling()
    print("\nPlotting topology-preserving cartogram...")
    topology_preserving_cartogram()
    print("\nPlotting derived area vs reported area of DUNs...")
    derived_v_reported()
    print("\nPlotting heatmap of N Parliaments by State at each delimitation round...")
    heatmap_n_parlimen()
    print("\nPlotting heatmap of N DUNs by State at each delimitation round...")
    heatmap_n_dun()
    print("\n✨✨✨ DONE ✨✨✨\n")
