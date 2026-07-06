#!/usr/bin/env python3
"""Build SaaS management product pages."""

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


def render_modules(modules: list[dict[str, Any]]) -> str:
    return "".join(
        f"""
        <article class="card">
          <h3>{esc(module.get('name'))}</h3>
          <p>{esc(module.get('description'))}</p>
          <ul>{list_items(module.get('capabilities', []))}</ul>
        </article>
        """
        for module in modules
    )


def render_personas(personas: list[dict[str, Any]]) -> str:
    return "".join(
        f"""
        <article class="card compact">
          <h3>{esc(persona.get('name'))}</h3>
          <ul>{list_items(persona.get('needs', []))}</ul>
        </article>
        """
        for persona in personas
    )


def render_tiers(tiers: list[dict[str, Any]]) -> str:
    return "".join(
        f"""
        <article class="card tier">
          <h3>{esc(tier.get('name'))}</h3>
          <p>{esc(tier.get('audience'))}</p>
          <ul>{list_items(tier.get('features', []))}</ul>
        </article>
        """
        for tier in tiers
    )


def main() -> None:
    SITE.mkdir(exist_ok=True)
    payload = read_yaml(DATA / "saas-management.yml").get("saas_management", {})
    product = payload.get("product", {})

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(product.get('name'))}</title>
  <meta name="description" content="{esc(product.get('description'))}" />
  <style>
    :root {{ --ink: #0f172a; --muted: #475569; --line: #e2e8f0; --bg: #f8fafc; --card: #ffffff; --soft: #f1f5f9; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: var(--ink); background: var(--bg); }}
    header {{ padding: 72px 24px; background: var(--card); border-bottom: 1px solid var(--line); }}
    main, .hero {{ max-width: 1180px; margin: 0 auto; }}
    main {{ padding: 36px 24px 80px; }}
    h1 {{ font-size: clamp(42px, 7vw, 78px); line-height: .95; margin: 0 0 20px; letter-spacing: -0.05em; }}
    h2 {{ font-size: 32px; margin: 42px 0 18px; letter-spacing: -0.03em; }}
    h3 {{ margin: 0 0 10px; }}
    p, li {{ color: var(--muted); line-height: 1.6; }}
    .lead {{ max-width: 850px; font-size: 21px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }}
    .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 22px; padding: 22px; }}
    .compact {{ min-height: 220px; }}
    .tier {{ border-top: 6px solid var(--ink); }}
    a {{ color: var(--ink); font-weight: 700; }}
    footer {{ border-top: 1px solid var(--line); padding: 24px; color: var(--muted); text-align: center; }}
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <p><strong>SaaS Management Website</strong></p>
      <h1>{esc(product.get('name'))}</h1>
      <p class="lead">{esc(product.get('description'))}</p>
    </div>
  </header>
  <main>
    <section>
      <h2>Management modules</h2>
      <div class="grid">{render_modules(payload.get('modules', []))}</div>
    </section>
    <section>
      <h2>Personas</h2>
      <div class="grid">{render_personas(payload.get('personas', []))}</div>
    </section>
    <section>
      <h2>Pricing and deployment tiers</h2>
      <div class="grid">{render_tiers(payload.get('pricing_tiers', []))}</div>
    </section>
  </main>
  <footer><a href="index.html">Landscape</a> · <a href="markets.html">Market building blocks</a> · <a href="api.json">API</a></footer>
</body>
</html>
"""
    (SITE / "saas.html").write_text(html_doc, encoding="utf-8")
    print("SaaS management page written to _site/saas.html")


if __name__ == "__main__":
    main()
