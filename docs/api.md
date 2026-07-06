# Landscape API and Exports

The landscape publishes machine-readable exports through GitHub Pages.

## API index

`api.json` is the discovery document for generated artifacts.

It points to:

- complete JSON registry
- CSV exports
- graph exports
- source YAML files

## JSON export

`landscape.json` contains:

- landscape manifest
- entries
- relations
- scoring rubric
- per-entry scores

## CSV exports

CSV files are published under `exports/`:

- `entries.csv`
- `relations.csv`
- `scores.csv`

These are useful for spreadsheets, dashboards, notebooks, and lightweight analysis.

## Graph exports

Graph files are published under `graph/`:

- `landscape-graph.mmd`
- `landscape-graph.dot`

## Local generation

```bash
python scripts/build-site.py
python scripts/export-graph.py
python scripts/export-csv.py
python scripts/build-api-index.py
```
