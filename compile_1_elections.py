import pandas as pd
import geopandas as gpd
import duckdb

from helper import get_states

path_delims = "data/geoparquet/delimitations/"
path_elections = "data/geoparquet/elections/"
map_state_iso3 = dict(zip(get_states(my=1), get_states(my=1, codes=1)))


def compile():
    df = pd.read_csv("data/delims_to_elections.csv")
    for s in df.state.unique():
        tf = df[df.state == s].copy()
        area_type = "parlimen" if s == "Malaysia" else "dun"
        state_iso3 = map_state_iso3[s]
        for i in range(len(tf)):
            election = tf.election.iloc[i]
            files = [
                f"peninsular_{tf.peninsular.iloc[i]}_{area_type}.parquet",
                f"sabah_{tf.sabah.iloc[i]}_{area_type}.parquet",
                f"sarawak_{tf.sarawak.iloc[i]}_{area_type}.parquet",
            ]
            files = [f for f in files if "_0_" not in f]
            gdf = gpd.read_parquet(path_delims + files[0])
            for f in files[1:]:
                gtf = gpd.read_parquet(path_delims + f)
                gdf = pd.concat([gdf, gtf], axis=0, ignore_index=True)
            if "GE" in election:
                gdf["code_parlimen"] = [f"P.{x:03d}" for x in range(1, len(gdf) + 1)]
                gdf["parlimen"] = gdf.code_parlimen + gdf.parlimen.str[5:]
            else:
                gdf = gdf[gdf.state == s]
                if state_iso3 == "SWK" and election == "SE-02":
                    map_new_code = dict(
                        zip(
                            [f"P.{x:03d}" for x in range(121, 145)],
                            [f"P.{x:03d}" for x in range(131, 155)],
                        )
                    )
                    gdf["code_parlimen"] = gdf.code_parlimen.map(map_new_code)
                    gdf["parlimen"] = gdf.code_parlimen + gdf.parlimen.str[5:]
                if state_iso3 == "SWK" and election == "SE-05":
                    map_new_code = dict(
                        zip(
                            [f"P.{x:03d}" for x in range(131, 155)],
                            [f"P.{x:03d}" for x in range(154, 178)],
                        )
                    )
                    gdf["code_parlimen"] = gdf.code_parlimen.map(map_new_code)
                    gdf["parlimen"] = gdf.code_parlimen + gdf.parlimen.str[5:]
            gdf.to_parquet(
                path_elections + f"{state_iso3}_{election}.parquet", index=False, compression="gzip"
            )

        print(f"Wrote {len(tf)} files for {s}")


def validate():
    QUERY = """
        SELECT 
            state, 
            parlimen AS seat,
            substr(split_part(filename, '/', -1), -13, 5) AS election
        FROM read_parquet('data/geoparquet/elections/MYS*.parquet', union_by_name=true)
        WHERE parlimen IS NOT NULL
    """

    df1 = duckdb.sql(QUERY).df()
    df2 = duckdb.sql(QUERY.replace("parlimen", "dun").replace("MYS", "")).df()

    df = pd.concat([df1, df2], axis=0, ignore_index=True)
    df["geo"] = 1
    rf = pd.read_parquet("https://public.electiondata.my/results/consol_stats.parquet")
    rf = rf[~rf.election.str.contains("BY-")][["election", "state", "seat", "date", "voters_total"]]

    cf = pd.merge(df, rf, on=["election", "state", "seat"], how="left")
    assert len(cf[cf.voters_total.isnull()]) == 0, "Geospatial data not found in results!"
    cf = pd.merge(rf, df, on=["election", "state", "seat"], how="left")
    assert len(cf[cf.geo.isnull()]) == 0, "Results data not found in maps!"
    print("Validation successful - perfect match between maps and results!")


if __name__ == "__main__":
    print("\n--------- Compiling election-specific files ----------\n")
    compile()
    print("\n--------- Validating against election results ----------\n")
    validate()
    print("\n--------- ✨✨✨ DONE ✨✨✨ ----------\n")
