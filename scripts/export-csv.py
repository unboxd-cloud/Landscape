#!/usr/bin/env python3
"""Export landscape registry data to CSV files."""

from __future__ import annotations

import csv
import pathlib
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DIST = ROOT / "dist"
SCORE_FIELDS = ["openness", "maturity", "self-hostability", "governance-readiness", "cloud-native-fit"]


def read_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def write_csv(path: pathlib.Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def average_score(row: dict[str, Any]) -> str:
    values = [row.get(field) for field in SCORE_FIELDS]
    if not all(isinstance(value, int) for value in values):
        return ""
    return str(round(sum(values) / len(values), 1))


def main() -> None:
    DIST.mkdir(exist_ok=True)

    categories = read_yaml(DATA / "categories.yml").get("categories", [])
    projects = read_yaml(DATA / "projects.yml").get("projects", [])
    protocols = read_yaml(DATA / "protocols.yml").get("protocols", [])
    platforms = read_yaml(DATA / "platforms.yml").get("platforms", [])
    vendors = read_yaml(DATA / "vendors.yml").get("vendors", [])
    relations = read_yaml(DATA / "relations.yml").get("relations", [])
    scores = read_yaml(DATA / "scores.yml").get("scores", [])

    entries = []
    for kind, rows in [
        ("category", categories),
        ("project", projects),
        ("protocol", protocols),
        ("platform", platforms),
        ("foundation", vendors),
    ]:
        for row in rows:
            entry = dict(row)
            entry["kind"] = kind
            entry["summary"] = row.get("description") or row.get("role") or ""
            entries.append(entry)

    score_rows = []
    for row in scores:
        score = dict(row)
        score["average"] = average_score(row)
        score_rows.append(score)

    write_csv(
        DIST / "entries.csv",
        entries,
        ["id", "name", "kind", "category", "type", "maturity", "status", "summary", "homepage"],
    )
    write_csv(
        DIST / "relations.csv",
        relations,
        ["id", "source", "target", "type", "description"],
    )
    write_csv(
        DIST / "scores.csv",
        score_rows,
        ["entry", "average", *SCORE_FIELDS, "notes"],
    )

    print("CSV exports written to dist/")


if __name__ == "__main__":
    main()
