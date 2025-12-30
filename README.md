[![Preprint](https://img.shields.io/badge/Preprint-arXiv-orange)](#)
[![Code DOI](https://img.shields.io/badge/Code%20Archive-Zenodo-blue)](#)
[![Data Archive](https://img.shields.io/badge/Data%20Archive-Harvard%20Dataverse-green)](https://doi.org/10.7910/DVN/DVFK54)
[![Cite This](https://img.shields.io/badge/Cite%20This-BibTeX-lightgrey)](#Citation)
[![License](https://img.shields.io/badge/License-CC0_1.0-lightgrey)](LICENSE)

# Malaysian Election Corpus (MECo): Electoral Maps and Cartograms since 1954

Electoral boundaries in Malaysia are not publicly available in machine-readable form. This prevents rigorous analysis of geography-centric issues such as malapportionment and gerrymandering, and constrains spatial perspectives on electoral outcomes. We present the second component of the Malaysian Election Corpus (MECo), an open-access collection of digital electoral boundaries covering all 19 approved delimitation exercises in Malaysia's history, from the first set of Malayan boundaries in 1954 until the 2019 Sabah delimitation. We also auto-generate election-time maps for all federal and state elections up to 2025, and include equal-area and electorate-weighted cartograms to support deeper geospatial analysis. This is the first complete, publicly-available, and machine-readable record of Malaysia's electoral boundaries, and fills a critical gap in the country's electoral data infrastructure.

## Repository Structure

| Directory/File                  | Description                                                              |
|---------------------------------|--------------------------------------------------------------------------|
| `data/`                     | Geospatial data (GeoJSON, TopoJSON, GeoParquet, FlatGeobuf, KML)                                  |
| `tex/`                          | LaTeX files for manuscript generation                                    |
| `compile_*.py`                   | Scripts to compile and validate all datases from raw delimitations exported as GeoJSON |
| `compile_*.r` | Scripts to generate Dorling cartograms |
| `dataviz.py`                    | Generate summary visualisations                                          |
| `helper.py`                     | Helper functions used across scripts                                     |


## Features

- Compilation and validation of Malaysian election maps (1955–present)
- LaTeX manuscript source files

## Installation and Usage

1. Clone the repository:
```bash
git clone git@github.com:thevesh/paper-meco-results.git
cd paper-meco-results
```

2. This project uses `uv` to manage Python dependencies.
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
```

3. Compile data and dashboards:
```bash
python3 compile_0_initial.py
python3 compile_1_elections.py
# --- Run cartogram-generation in R ---
python3 compile_3_formats.py
python3 dataviz.py
```

## Citation

If you use this work, please cite it as:

> Thevesh Thevananthan and Danesh Prakash Chacko, "The Malaysian Election Corpus (MECo): Election Boundaries from 1955 to 2018", 2025.


## Questions / Suggestions

If you want to improve the quality of the underlying data, please fork this repo, then make a pull request for review. However, do consider opening an issue to discuss your desired changes first!
