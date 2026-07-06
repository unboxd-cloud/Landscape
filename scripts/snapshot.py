#!/usr/bin/env python3
"""Create a versioned landscape snapshot from the current registry."""

from __future__ import annotations

import datetime as dt
import json
import pathlib
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SNAPSHOTS = ROOT / "snapshots"


def read_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main() -> None:
    SNAPSHOTS.mkdir(exist_ok=True)
    today = dt.date.today().isoformat()

    landscape = read_yaml(ROOT / "landscape.yml")
    payload = {
        "snapshot_date": today,
        "landscape": landscape,
        "categories": read_yaml(DATA / "categories.yml").get("categories", []),
        "projects": read_yaml(DATA / "projects.yml").get("projects", []),
        "protocols": read_yaml(DATA / "protocols.yml").get("protocols", []),
        "platforms": read_yaml(DATA / "platforms.yml").get("platforms", []),
        "vendors": read_yaml(DATA / "vendors.yml").get("vendors", []),
        "relations": read_yaml(DATA / "relations.yml").get("relations", []),
        "scoring": read_yaml(DATA / "scoring.yml").get("scoring", {}),
        "scores": read_yaml(DATA / "scores.yml").get("scores", []),
    }

    output = SNAPSHOTS / f"landscape-{today}.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Snapshot written: {output}")


if __name__ == "__main__":
    main()
