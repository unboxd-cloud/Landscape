#!/usr/bin/env python3
"""Export the landscape relationship graph to Mermaid and Graphviz DOT."""

from __future__ import annotations

import pathlib
import re
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DIST = ROOT / "dist"


def read_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def safe_node_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", value)


def quote(value: str) -> str:
    return value.replace('"', '\\"')


def main() -> None:
    DIST.mkdir(exist_ok=True)

    categories = read_yaml(DATA / "categories.yml").get("categories", [])
    projects = read_yaml(DATA / "projects.yml").get("projects", [])
    protocols = read_yaml(DATA / "protocols.yml").get("protocols", [])
    platforms = read_yaml(DATA / "platforms.yml").get("platforms", [])
    vendors = read_yaml(DATA / "vendors.yml").get("vendors", [])
    relations = read_yaml(DATA / "relations.yml").get("relations", [])

    entries = [*categories, *projects, *protocols, *platforms, *vendors]
    names_by_id = {entry["id"]: entry["name"] for entry in entries}

    mermaid_lines = ["graph LR"]
    dot_lines = ["digraph Landscape {", "  rankdir=LR;", "  node [shape=box, style=rounded];"]

    for entry_id, name in sorted(names_by_id.items()):
        mermaid_lines.append(f"  {safe_node_id(entry_id)}[\"{quote(name)}\"]")
        dot_lines.append(f"  \"{quote(entry_id)}\" [label=\"{quote(name)}\"];")

    for relation in relations:
        source = relation["source"]
        target = relation["target"]
        relation_type = relation["type"]
        mermaid_lines.append(f"  {safe_node_id(source)} -- \"{quote(relation_type)}\" --> {safe_node_id(target)}")
        dot_lines.append(f"  \"{quote(source)}\" -> \"{quote(target)}\" [label=\"{quote(relation_type)}\"];")

    dot_lines.append("}")

    (DIST / "landscape-graph.mmd").write_text("\n".join(mermaid_lines) + "\n", encoding="utf-8")
    (DIST / "landscape-graph.dot").write_text("\n".join(dot_lines) + "\n", encoding="utf-8")

    print("Graph exports written to dist/")


if __name__ == "__main__":
    main()
