# DE Pipeline Lab

A personal data engineering project exploring end-to-end pipeline development — from open API ingestion through local transformation to cloud storage.

Built and run entirely in GitHub Codespaces. No local setup required.

## Stack

| Layer | Tool |
|---|---|
| Environment | GitHub Codespaces |
| Language | Python 3.12 |
| Data ingestion | requests |
| Transformation | pandas + DuckDB |
| Storage format | Apache Parquet |
| Cloud storage | AWS S3 (roadmap) |

## Pipeline Architecture
Open API → Python → pandas DataFrame → DuckDB SQL → Parquet files

## Scripts

### `DE Ingestion/pipeline.py`
Foundational pipeline — builds a sample macroeconomic dataset, runs DuckDB SQL queries including filters, GROUP BY, and aggregations, and saves output as Parquet. Demonstrates the core pipeline pattern with no external dependencies.

### `DE Ingestion/fred_pipeline.py`
Live data pipeline — pulls real 7-day weather forecast data for London, New York, and Mumbai from the Open-Meteo API (free, no API key required). Runs DuckDB queries to rank cities by temperature and calculate weekly averages. Saves results as Parquet.

## How To Run

```bash
pip install duckdb pandas pyarrow requests
cd "DE Ingestion"
python pipeline.py
python fred_pipeline.py
```

## Roadmap

- [ ] Extend to 90-day historical dataset
- [ ] Add large-scale open dataset (Companies House or Spotify)
- [ ] Push Parquet files to AWS S3
- [ ] Load into cloud data warehouse
- [ ] SQL analytics and classification layer

## About

Built by [Sid Shah](https://github.com/MrSidShah) — senior data leader and DataIQ Top 100 2026. This repo documents hands-on data engineering practice — building and running real pipelines, not just talking about them.
