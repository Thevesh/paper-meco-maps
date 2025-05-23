[![Preprint](https://img.shields.io/badge/project-paper-lightgrey)](https://doi.org/10.48550/arxiv.2505.06564)
[![Cite This Work](https://img.shields.io/badge/citation-notready-red)](#Citation)
[![Python](https://img.shields.io/badge/python-3.11+-pink.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-CC0_1.0-blue.svg)](LICENSE)

# Malaysian Election Corpus (MECo): Election Boundaries since 1955

## Repository Structure

| Directory/File                  | Description                                                              |
|---------------------------------|--------------------------------------------------------------------------|
| `src-geo/`                     | Geospatial data (GeoJSON + shapefile + XML)                                  |
| `tex/`                          | LaTeX files for manuscript generation                                    |
| `helper.py`                     | Helper functions used across scripts                                     |
| `requirements.txt`              | Python dependencies                                                     |
| `README.md`                     | This file                                                                |
| `LICENSE`                       | License file (CC0)                                                       |

## Features

- Compilation and validation of Malaysian election maps (1955–present)
- LaTeX manuscript source files

## Installation and Usage

1. Clone the repository:
```bash
git clone git@github.com:thevesh/paper-meco-maps.git
cd paper-meco-maps
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Citation

If you use this work, please cite it as:

> Thevesh Thevananthan and Danesh Prakash Chacko, "The Malaysian Election Corpus (MECo): Election Boundaries from 1955 to 2018", 2025.


## Questions / Suggestions

Contributions are not welcome, in order to maintain appropriate provenance for academic credit. However, you are free to open an issue!
