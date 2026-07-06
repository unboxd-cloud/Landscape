#!/usr/bin/env python3
"""Inject JSON-LD structured data into the generated HTML site."""

from __future__ import annotations

import json
import pathlib
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
DATA = ROOT / "data"


def read_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main() -> None:
    index = SITE / "index.html"
    if not index.exists():
        raise SystemExit("_site/index.html does not exist. Run scripts/build-site.py first.")

    landscape = read_yaml(ROOT / "landscape.yml")
    projects = read_yaml(DATA / "projects.yml").get("projects", [])
    protocols = read_yaml(DATA / "protocols.yml").get("protocols", [])
    platforms = read_yaml(DATA / "platforms.yml").get("platforms", [])

    site_url = str(landscape.get("site_url") or "https://unboxd-cloud.github.io/Landscape").rstrip("/")
    graph: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": landscape.get("name"),
        "description": landscape.get("description"),
        "url": site_url + "/",
        "license": "https://www.apache.org/licenses/LICENSE-2.0",
        "creator": {
            "@type": "Organization",
            "name": "Unboxd Cloud",
            "url": "https://github.com/unboxd-cloud"
        },
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": site_url + "/landscape.json"},
            {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": site_url + "/exports/entries.csv"},
            {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": site_url + "/exports/relations.csv"},
            {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": site_url + "/exports/scores.csv"}
        ],
        "about": [
            {"@type": "Thing", "name": item.get("name"), "url": item.get("homepage")}
            for item in [*projects, *protocols, *platforms]
        ]
    }

    script = "<script type=\"application/ld+json\">" + json.dumps(graph, sort_keys=True) + "</script>\n"
    html = index.read_text(encoding="utf-8")
    if "application/ld+json" in html:
        print("JSON-LD already present")
        return
    html = html.replace("</head>", script + "</head>")
    index.write_text(html, encoding="utf-8")
    print("JSON-LD injected into _site/index.html")


if __name__ == "__main__":
    main()
