#!/usr/bin/env python3
"""Validate landscape registry semantics."""

from __future__ import annotations

import pathlib
import re
import sys
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ID_PATTERN = re.compile(r"^[a-z0-9]+[a-z0-9-]*[a-z0-9]$")
MATURITY_VALUES = {"design", "emerging", "active", "incubating", "graduated", "archived"}
STATUS_VALUES = {"design", "active", "archived"}
RELATION_TYPES = {"runs", "uses", "supports", "integrates-with", "observes", "complements", "depends-on", "replaces"}
SCORE_FIELDS = ["openness", "maturity", "self-hostability", "governance-readiness", "cloud-native-fit"]


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
        if not ID_PATTERN.match(item_id):
            fail(f"{collection_name}/{item_id} has invalid id format")
        if item_id in seen:
            fail(f"{collection_name} contains duplicate id: {item_id}")
        seen.add(item_id)


def check_required_text(collection_name: str, items: list[dict[str, Any]], fields: list[str]) -> None:
    for item in items:
        for field in fields:
            if not str(item.get(field, "")).strip():
                fail(f"{collection_name}/{item.get('id')} is missing required field: {field}")


def check_categories(collection_name: str, items: list[dict[str, Any]], valid_categories: set[str]) -> None:
    for item in items:
        category = item.get("category")
        if category and category not in valid_categories:
            fail(f"{collection_name}/{item.get('id')} uses unknown category: {category}")


def check_allowed_values(collection_name: str, items: list[dict[str, Any]]) -> None:
    for item in items:
        maturity = item.get("maturity")
        status = item.get("status")
        if maturity and maturity not in MATURITY_VALUES:
            fail(f"{collection_name}/{item.get('id')} has invalid maturity: {maturity}")
        if status and status not in STATUS_VALUES:
            fail(f"{collection_name}/{item.get('id')} has invalid status: {status}")


def check_relations(relations: list[dict[str, Any]], valid_ids: set[str]) -> None:
    check_unique_ids("relations", relations)
    check_required_text("relations", relations, ["source", "target", "type", "description"])
    for relation in relations:
        relation_id = relation.get("id")
        source = relation.get("source")
        target = relation.get("target")
        relation_type = relation.get("type")
        if source not in valid_ids:
            fail(f"relations/{relation_id} uses unknown source: {source}")
        if target not in valid_ids:
            fail(f"relations/{relation_id} uses unknown target: {target}")
        if relation_type not in RELATION_TYPES:
            fail(f"relations/{relation_id} uses invalid type: {relation_type}")


def check_scores(scores: list[dict[str, Any]], valid_ids: set[str]) -> None:
    seen: set[str] = set()
    for score in scores:
        entry = score.get("entry")
        if not entry:
            fail("scores contains an entry without entry id")
        if entry in seen:
            fail(f"scores contains duplicate entry: {entry}")
        if entry not in valid_ids:
            fail(f"scores/{entry} references unknown entry")
        seen.add(entry)
        for field in SCORE_FIELDS:
            value = score.get(field)
            if not isinstance(value, int) or value < 0 or value > 5:
                fail(f"scores/{entry} has invalid {field}: {value}")


def main() -> None:
    categories = read_yaml(DATA / "categories.yml").get("categories", [])
    projects = read_yaml(DATA / "projects.yml").get("projects", [])
    protocols = read_yaml(DATA / "protocols.yml").get("protocols", [])
    platforms = read_yaml(DATA / "platforms.yml").get("platforms", [])
    vendors = read_yaml(DATA / "vendors.yml").get("vendors", [])
    relations = read_yaml(DATA / "relations.yml").get("relations", [])
    scores = read_yaml(DATA / "scores.yml").get("scores", [])

    collections = {
        "categories": categories,
        "projects": projects,
        "protocols": protocols,
        "platforms": platforms,
        "vendors": vendors,
    }

    for name, items in collections.items():
        check_unique_ids(name, items)
        check_required_text(name, items, ["id", "name"])
        check_allowed_values(name, items)

    check_required_text("categories", categories, ["description"])
    check_required_text("projects", projects, ["category", "role"])
    check_required_text("protocols", protocols, ["category", "role"])
    check_required_text("platforms", platforms, ["category", "role", "status"])
    check_required_text("vendors", vendors, ["type", "role"])

    valid_categories = {item["id"] for item in categories}
    check_categories("projects", projects, valid_categories)
    check_categories("protocols", protocols, valid_categories)
    check_categories("platforms", platforms, valid_categories)

    valid_ids = set(valid_categories)
    for items in [projects, protocols, platforms, vendors]:
        valid_ids.update(item["id"] for item in items)
    check_relations(relations, valid_ids)
    check_scores(scores, valid_ids)

    print("Registry validation passed")


if __name__ == "__main__":
    main()
