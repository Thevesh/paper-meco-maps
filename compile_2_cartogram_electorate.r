library(sf)
library(sfarrow)
library(dplyr)
library(cartogram)
library(readr)
library(purrr)

params <- read_csv("data/cartogram_electorate_k.csv")
results <- read.csv("https://public.electiondata.my/results/consol_stats.csv")

run_one <- function(state, election_name, seat_type, k) {
    g <- st_read_parquet(
        sprintf(
            "data/geoparquet/elections/%s_%s.parquet",
            state, election_name
        )
    )

    if (is.na(st_crs(g))) st_crs(g) <- 4326

    df <- results %>%
        filter(election == election_name) %>%
        select(state, seat, voters_total) %>%
        rename(!!seat_type := seat)

    g <- left_join(g, df, by = c("state", seat_type))
    g$voters_total <- as.integer(g$voters_total)
    stopifnot(all(!is.na(g$voters_total)))

    g_dorling <- g %>%
        st_transform(3857) %>%
        cartogram_dorling(weight = "voters_total", k = k, itermax = 1000) %>%
        st_transform(4326)

    st_write_parquet(
        g_dorling,
        sprintf(
            "data/geoparquet/cartogram-electorate/%s_%s.parquet",
            state, election_name
        )
    )
}

pwalk(params, run_one)
