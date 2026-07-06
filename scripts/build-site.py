#!/usr/bin/env python3
"""Build a small static HTML site from the landscape YAML registry."""

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


def render_cards(title: str, items: list[dict[str, Any]]) -> str:
    cards = []
    for item in items:
        homepage = item.get("homepage")
        link = f'<a href="{esc(homepage)}" target="_blank" rel="noreferrer">Homepage</a>' if homepage else ""
        meta_parts = [item.get("category"), item.get("type"), item.get("maturity"), item.get("status")]
        meta = " · ".join(esc(part) for part in meta_parts if part)
        cards.append(
            f"""
            <article class="card">
              <h3>{esc(item.get('name'))}</h3>
              <p class="meta">{meta}</p>
              <p>{esc(item.get('description') or item.get('role'))}</p>
              {link}
            </article>
            """
        )
    return f"<section><h2>{esc(title)}</h2><div class=\"grid\">{''.join(cards)}</div></section>"


def main() -> None:
    SITE.mkdir(exist_ok=True)

    landscape = read_yaml(ROOT / "landscape.yml")
    categories = read_yaml(DATA / "categories.yml").get("categories", [])
    projects = read_yaml(DATA / "projects.yml").get("projects", [])
    protocols = read_yaml(DATA / "protocols.yml").get("protocols", [])
    platforms = read_yaml(DATA / "platforms.yml").get("platforms", [])
    vendors = read_yaml(DATA / "vendors.yml").get("vendors", [])

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(landscape.get('name'))}</title>
  <meta name="description" content="{esc(landscape.get('description'))}" />
  <style>
    :root {{ --ink: #0f172a; --muted: #475569; --line: #e2e8f0; --bg: #f8fafc; --card: #ffffff; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: var(--ink); background: var(--bg); }}
    header {{ padding: 72px 24px 48px; background: var(--card); border-bottom: 1px solid var(--line); }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 40px 24px 80px; }}
    .hero {{ max-width: 1120px; margin: 0 auto; }}
    h1 {{ font-size: clamp(40px, 7vw, 76px); line-height: .95; margin: 0 0 20px; letter-spacing: -0.05em; }}
    h2 {{ font-size: 32px; margin: 48px 0 20px; letter-spacing: -0.03em; }}
    h3 {{ margin: 0 0 8px; font-size: 20px; }}
    p {{ color: var(--muted); line-height: 1.6; }}
    .lead {{ font-size: 21px; max-width: 780px; }}
    .principles {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 28px; }}
    .pill {{ border: 1px solid var(--line); background: var(--bg); border-radius: 999px; padding: 8px 12px; color: var(--muted); font-size: 14px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(245px, 1fr)); gap: 16px; }}
    .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 20px; padding: 20px; min-height: 180px; }}
    .meta {{ font-size: 13px; text-transform: uppercase; letter-spacing: .08em; color: #64748b; }}
    a {{ color: var(--ink); font-weight: 700; }}
    footer {{ border-top: 1px solid var(--line); padding: 24px; color: var(--muted); text-align: center; }}
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <h1>{esc(landscape.get('name'))}</h1>
      <p class="lead">{esc(landscape.get('description'))}</p>
      <div class="principles">
        {''.join(f'<span class="pill">{esc(p)}</span>' for p in landscape.get('principles', []))}
      </div>
    </div>
  </header>
  <main>
    {render_cards('Categories', categories)}
    {render_cards('Projects', projects)}
    {render_cards('Protocols', protocols)}
    {render_cards('Platforms', platforms)}
    {render_cards('Foundations and Vendors', vendors)}
  </main>
  <footer>Apache-2.0 code · CC BY 4.0 documentation · Generated from YAML registry data.</footer>
</body>
</html>
"""

    (SITE / "index.html").write_text(html_doc, encoding="utf-8")


if __name__ == "__main__":
    main()
