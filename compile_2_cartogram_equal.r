library(sf)
library(sfarrow)
library(dplyr)
library(cartogram)
library(readr)
library(purrr)

params <- read_csv("data/cartogram_equal_k.csv")

run_one <- function(state, election_name, seat_type, k) {
    g <- st_read_parquet(
        sprintf(
            "data/geoparquet/elections/%s_%s.parquet",
            state, election_name
        )
    )

    if (is.na(st_crs(g))) st_crs(g) <- 4326
    g$equal_weight <- 1

    g_dorling <- g %>%
        st_transform(3857) %>%
        cartogram_dorling(weight = "equal_weight", k = k, itermax = 1000) %>%
        st_transform(4326)
    g_dorling$equal_weight <- NULL

    st_write_parquet(
        g_dorling,
        sprintf(
            "data/geoparquet/cartogram-equal/%s_%s.parquet",
            state, election_name
        )
    )
}

pwalk(params, run_one)
