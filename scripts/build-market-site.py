#!/usr/bin/env python3
"""Build market building-block pages for the SaaS management website."""

from __future__ import annotations

import html
import pathlib
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
DATA = ROOT / "data"


def read_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def esc(value: Any) -> str:
    return html.escape(str(value or ""))


def list_items(items: list[str]) -> str:
    return "".join(f"<li>{esc(item)}</li>" for item in items)


def render_family(family: dict[str, Any]) -> str:
    return f"""
    <article class="family" id="{esc(family.get('id'))}">
      <h2>{esc(family.get('name'))}</h2>
      <p>{esc(family.get('description'))}</p>
      <div class="cols">
        <section>
          <h3>Example markets</h3>
          <ul>{list_items(family.get('example_markets', []))}</ul>
        </section>
        <section>
          <h3>Building blocks</h3>
          <ul>{list_items(family.get('building_blocks', []))}</ul>
        </section>
        <section>
          <h3>Landscape categories</h3>
          <ul>{list_items(family.get('landscape_categories', []))}</ul>
        </section>
      </div>
    </article>
    """


def main() -> None:
    SITE.mkdir(exist_ok=True)
    market = read_yaml(DATA / "market-building-blocks.yml").get("market_building_blocks", {})
    families = market.get("families", [])
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Enterprise Market Building Blocks</title>
  <meta name="description" content="Enterprise SaaS market building-block taxonomy for architecture and platform teams." />
  <style>
    :root {{ --ink: #0f172a; --muted: #475569; --line: #e2e8f0; --bg: #f8fafc; --card: #ffffff; --soft: #f1f5f9; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: var(--ink); background: var(--bg); }}
    header {{ padding: 64px 24px; background: var(--card); border-bottom: 1px solid var(--line); }}
    main, .hero {{ max-width: 1180px; margin: 0 auto; }}
    main {{ padding: 32px 24px 80px; }}
    h1 {{ font-size: clamp(38px, 6vw, 68px); line-height: .98; margin: 0 0 16px; letter-spacing: -0.05em; }}
    h2 {{ font-size: 28px; margin: 0 0 12px; }}
    h3 {{ margin-bottom: 8px; }}
    p, li {{ color: var(--muted); line-height: 1.6; }}
    .lead {{ max-width: 820px; font-size: 20px; }}
    .family {{ background: var(--card); border: 1px solid var(--line); border-radius: 24px; padding: 24px; margin: 18px 0; }}
    .cols {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; }}
    section section {{ background: var(--soft); border-radius: 18px; padding: 16px; }}
    a {{ color: var(--ink); font-weight: 700; }}
    footer {{ border-top: 1px solid var(--line); padding: 24px; color: var(--muted); text-align: center; }}
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <h1>Enterprise Market Building Blocks</h1>
      <p class="lead">A SaaS management taxonomy that turns enterprise software market categories into reusable architecture building blocks.</p>
      <p>Reference: <a href="{esc(market.get('reference', {}).get('url'))}">{esc(market.get('reference', {}).get('name'))}</a></p>
    </div>
  </header>
  <main>
    {''.join(render_family(family) for family in families)}
  </main>
  <footer><a href="index.html">Landscape</a> · <a href="data/market-building-blocks.yml">Source YAML</a></footer>
</body>
</html>
"""
    (SITE / "markets.html").write_text(html_doc, encoding="utf-8")
    print("Market building-block page written to _site/markets.html")


if __name__ == "__main__":
    main()
