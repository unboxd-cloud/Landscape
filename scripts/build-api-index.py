#!/usr/bin/env python3
"""Build a small API index for generated landscape artifacts."""

from __future__ import annotations

import datetime as dt
import json
import pathlib
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


def read_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main() -> None:
    SITE.mkdir(exist_ok=True)
    landscape = read_yaml(ROOT / "landscape.yml")
    payload: dict[str, Any] = {
        "name": landscape.get("name"),
        "description": landscape.get("description"),
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "artifacts": {
            "json": "landscape.json",
            "entries_csv": "exports/entries.csv",
            "relations_csv": "exports/relations.csv",
            "scores_csv": "exports/scores.csv",
            "mermaid_graph": "graph/landscape-graph.mmd",
            "graphviz_dot": "graph/landscape-graph.dot",
            "manifest": "landscape.yml",
            "data": {
                "categories": "data/categories.yml",
                "projects": "data/projects.yml",
                "protocols": "data/protocols.yml",
                "platforms": "data/platforms.yml",
                "vendors": "data/vendors.yml",
                "relations": "data/relations.yml",
                "scoring": "data/scoring.yml",
                "scores": "data/scores.yml"
            }
        }
    }
    (SITE / "api.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print("API index written to _site/api.json")


if __name__ == "__main__":
    main()
