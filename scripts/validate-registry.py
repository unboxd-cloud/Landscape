#!/usr/bin/env python3
"""Validate landscape registry semantics."""

from __future__ import annotations

import pathlib
import sys
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def read_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_unique_ids(collection_name: str, items: list[dict[str, Any]]) -> None:
    seen: set[str] = set()
    for item in items:
        item_id = item.get("id")
        if not item_id:
            fail(f"{collection_name} contains an entry without id")
        if item_id in seen:
            fail(f"{collection_name} contains duplicate id: {item_id}")
        seen.add(item_id)


def check_categories(collection_name: str, items: list[dict[str, Any]], valid_categories: set[str]) -> None:
    for item in items:
        category = item.get("category")
        if category and category not in valid_categories:
            fail(f"{collection_name}/{item.get('id')} uses unknown category: {category}")


def main() -> None:
    categories = read_yaml(DATA / "categories.yml").get("categories", [])
    projects = read_yaml(DATA / "projects.yml").get("projects", [])
    protocols = read_yaml(DATA / "protocols.yml").get("protocols", [])
    platforms = read_yaml(DATA / "platforms.yml").get("platforms", [])
    vendors = read_yaml(DATA / "vendors.yml").get("vendors", [])

    check_unique_ids("categories", categories)
    check_unique_ids("projects", projects)
    check_unique_ids("protocols", protocols)
    check_unique_ids("platforms", platforms)
    check_unique_ids("vendors", vendors)

    valid_categories = {item["id"] for item in categories}
    check_categories("projects", projects, valid_categories)
    check_categories("protocols", protocols, valid_categories)
    check_categories("platforms", platforms, valid_categories)

    print("Registry validation passed")


if __name__ == "__main__":
    main()
