#!/usr/bin/env python3
"""Build SEO artifacts for the generated landscape site."""

from __future__ import annotations

import datetime as dt
import pathlib
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
DEFAULT_BASE_URL = "https://unboxd-cloud.github.io/Landscape"


def read_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main() -> None:
    SITE.mkdir(exist_ok=True)
    landscape = read_yaml(ROOT / "landscape.yml")
    base_url = str(landscape.get("site_url") or DEFAULT_BASE_URL).rstrip("/")
    today = dt.date.today().isoformat()

    robots = f"""User-agent: *
Allow: /

Sitemap: {base_url}/sitemap.xml
"""
    (SITE / "robots.txt").write_text(robots, encoding="utf-8")

    urls = [
        ("/", "daily", "1.0"),
        ("/landscape.json", "daily", "0.8"),
        ("/api.json", "daily", "0.8"),
        ("/exports/entries.csv", "daily", "0.6"),
        ("/exports/relations.csv", "daily", "0.6"),
        ("/exports/scores.csv", "daily", "0.6"),
        ("/graph/landscape-graph.mmd", "daily", "0.5"),
        ("/graph/landscape-graph.dot", "daily", "0.5"),
    ]

    items = []
    for path, changefreq, priority in urls:
        loc = base_url + path
        items.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )

    sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</urlset>
""" % "\n".join(items)
    (SITE / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    print("SEO artifacts written to _site/")


if __name__ == "__main__":
    main()
