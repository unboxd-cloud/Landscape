#!/usr/bin/env python3
"""Build a static HTML site and JSON export from the landscape YAML registry."""

from __future__ import annotations

import html
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


def esc(value: Any) -> str:
    return html.escape(str(value or ""))


def normalize(kind: str, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in items:
        entry = dict(item)
        entry["kind"] = kind
        entry["summary"] = item.get("description") or item.get("role") or ""
        normalized.append(entry)
    return normalized


def render_cards(items: list[dict[str, Any]]) -> str:
    cards = []
    for item in items:
        homepage = item.get("homepage")
        link = f'<a href="{esc(homepage)}" target="_blank" rel="noreferrer">Homepage</a>' if homepage else ""
        meta_parts = [item.get("kind"), item.get("category"), item.get("type"), item.get("maturity"), item.get("status")]
        meta = " · ".join(esc(part) for part in meta_parts if part)
        search_text = " ".join(
            str(part or "")
            for part in [
                item.get("name"),
                item.get("id"),
                item.get("kind"),
                item.get("category"),
                item.get("type"),
                item.get("maturity"),
                item.get("status"),
                item.get("summary"),
            ]
        ).lower()
        cards.append(
            f"""
            <article class="card" data-kind="{esc(item.get('kind'))}" data-category="{esc(item.get('category'))}" data-search="{esc(search_text)}">
              <div class="card-topline">{esc(item.get('kind')).replace('-', ' ')}</div>
              <h3>{esc(item.get('name'))}</h3>
              <p class="meta">{meta}</p>
              <p>{esc(item.get('summary'))}</p>
              {link}
            </article>
            """
        )
    return "".join(cards)


def render_relations(relations: list[dict[str, Any]], names_by_id: dict[str, str]) -> str:
    rows = []
    for relation in relations:
        source = names_by_id.get(relation.get("source"), relation.get("source"))
        target = names_by_id.get(relation.get("target"), relation.get("target"))
        rows.append(
            f"""
            <article class="relation">
              <strong>{esc(source)}</strong>
              <span>{esc(relation.get('type'))}</span>
              <strong>{esc(target)}</strong>
              <p>{esc(relation.get('description'))}</p>
            </article>
            """
        )
    return "".join(rows)


def main() -> None:
    SITE.mkdir(exist_ok=True)

    landscape = read_yaml(ROOT / "landscape.yml")
    categories = read_yaml(DATA / "categories.yml").get("categories", [])
    projects = read_yaml(DATA / "projects.yml").get("projects", [])
    protocols = read_yaml(DATA / "protocols.yml").get("protocols", [])
    platforms = read_yaml(DATA / "platforms.yml").get("platforms", [])
    vendors = read_yaml(DATA / "vendors.yml").get("vendors", [])
    relations = read_yaml(DATA / "relations.yml").get("relations", [])

    entries = [
        *normalize("category", categories),
        *normalize("project", projects),
        *normalize("protocol", protocols),
        *normalize("platform", platforms),
        *normalize("foundation", vendors),
    ]
    names_by_id = {entry["id"]: entry["name"] for entry in entries}

    export = {
        "landscape": landscape,
        "entries": entries,
        "relations": relations,
    }
    (SITE / "landscape.json").write_text(json.dumps(export, indent=2, sort_keys=True), encoding="utf-8")

    kind_options = sorted({entry.get("kind", "") for entry in entries if entry.get("kind")})
    category_options = sorted({entry.get("category", "") for entry in entries if entry.get("category")})

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(landscape.get('name'))}</title>
  <meta name="description" content="{esc(landscape.get('description'))}" />
  <meta property="og:title" content="{esc(landscape.get('name'))}" />
  <meta property="og:description" content="{esc(landscape.get('description'))}" />
  <meta property="og:type" content="website" />
  <style>
    :root {{ --ink: #0f172a; --muted: #475569; --line: #e2e8f0; --bg: #f8fafc; --card: #ffffff; --soft: #f1f5f9; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: var(--ink); background: var(--bg); }}
    header {{ padding: 72px 24px 48px; background: var(--card); border-bottom: 1px solid var(--line); }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 36px 24px 80px; }}
    .hero {{ max-width: 1180px; margin: 0 auto; }}
    h1 {{ font-size: clamp(40px, 7vw, 76px); line-height: .95; margin: 0 0 20px; letter-spacing: -0.05em; }}
    h2 {{ font-size: 28px; margin: 36px 0 16px; letter-spacing: -0.03em; }}
    h3 {{ margin: 0 0 8px; font-size: 20px; }}
    p {{ color: var(--muted); line-height: 1.6; }}
    .lead {{ font-size: 21px; max-width: 820px; }}
    .principles {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 28px; }}
    .pill {{ border: 1px solid var(--line); background: var(--bg); border-radius: 999px; padding: 8px 12px; color: var(--muted); font-size: 14px; }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 28px 0; }}
    .stat {{ background: var(--card); border: 1px solid var(--line); border-radius: 18px; padding: 18px; }}
    .stat strong {{ display: block; font-size: 30px; letter-spacing: -0.04em; }}
    .toolbar {{ position: sticky; top: 0; z-index: 10; display: grid; grid-template-columns: 1fr 190px 220px; gap: 12px; padding: 14px; margin: 0 0 22px; background: rgba(248, 250, 252, .92); backdrop-filter: blur(10px); border: 1px solid var(--line); border-radius: 22px; }}
    input, select {{ width: 100%; border: 1px solid var(--line); background: var(--card); border-radius: 14px; padding: 12px 14px; font: inherit; color: var(--ink); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(255px, 1fr)); gap: 16px; }}
    .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 20px; padding: 20px; min-height: 210px; }}
    .card[hidden] {{ display: none; }}
    .card-topline {{ display: inline-flex; margin-bottom: 12px; padding: 5px 9px; border-radius: 999px; background: var(--soft); color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }}
    .meta {{ font-size: 12px; text-transform: uppercase; letter-spacing: .08em; color: #64748b; }}
    a {{ color: var(--ink); font-weight: 700; }}
    .empty {{ display: none; padding: 28px; border: 1px dashed var(--line); border-radius: 20px; text-align: center; color: var(--muted); }}
    .relations {{ display: grid; gap: 12px; }}
    .relation {{ background: var(--card); border: 1px solid var(--line); border-radius: 18px; padding: 16px; }}
    .relation span {{ display: inline-flex; margin: 0 8px; padding: 4px 8px; border-radius: 999px; background: var(--soft); color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }}
    .relation p {{ margin-bottom: 0; }}
    footer {{ border-top: 1px solid var(--line); padding: 24px; color: var(--muted); text-align: center; }}
    @media (max-width: 780px) {{ .toolbar {{ grid-template-columns: 1fr; }} }}
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
    <section class="stats" aria-label="Landscape statistics">
      <div class="stat"><strong>{len(entries)}</strong><span>Total entries</span></div>
      <div class="stat"><strong>{len(projects)}</strong><span>Projects</span></div>
      <div class="stat"><strong>{len(protocols)}</strong><span>Protocols</span></div>
      <div class="stat"><strong>{len(relations)}</strong><span>Relations</span></div>
    </section>

    <section class="toolbar" aria-label="Landscape filters">
      <input id="search" type="search" placeholder="Search projects, protocols, platforms..." aria-label="Search landscape" />
      <select id="kind" aria-label="Filter by kind">
        <option value="">All kinds</option>
        {''.join(f'<option value="{esc(k)}">{esc(k.title())}</option>' for k in kind_options)}
      </select>
      <select id="category" aria-label="Filter by category">
        <option value="">All categories</option>
        {''.join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in category_options)}
      </select>
    </section>

    <section>
      <h2>Landscape entries</h2>
      <div id="count" class="meta">Showing {len(entries)} entries</div>
      <div id="cards" class="grid">{render_cards(entries)}</div>
      <div id="empty" class="empty">No entries match the current filters.</div>
    </section>

    <section>
      <h2>Relationship graph</h2>
      <p>These relations explain how technologies connect across runtime, identity, policy, data, observability, and infrastructure layers.</p>
      <div class="relations">{render_relations(relations, names_by_id)}</div>
    </section>
  </main>
  <footer><a href="landscape.json">JSON export</a> · Apache-2.0 code · CC BY 4.0 documentation · Generated from YAML registry data.</footer>
  <script>
    const search = document.querySelector('#search');
    const kind = document.querySelector('#kind');
    const category = document.querySelector('#category');
    const cards = Array.from(document.querySelectorAll('.card'));
    const count = document.querySelector('#count');
    const empty = document.querySelector('#empty');

    function applyFilters() {{
      const q = search.value.trim().toLowerCase();
      const k = kind.value;
      const c = category.value;
      let visible = 0;
      for (const card of cards) {{
        const matchesSearch = !q || card.dataset.search.includes(q);
        const matchesKind = !k || card.dataset.kind === k;
        const matchesCategory = !c || card.dataset.category === c;
        const show = matchesSearch && matchesKind && matchesCategory;
        card.hidden = !show;
        if (show) visible += 1;
      }}
      count.textContent = `Showing ${{visible}} entries`;
      empty.style.display = visible === 0 ? 'block' : 'none';
    }}

    search.addEventListener('input', applyFilters);
    kind.addEventListener('change', applyFilters);
    category.addEventListener('change', applyFilters);
  </script>
</body>
</html>
"""

    (SITE / "index.html").write_text(html_doc, encoding="utf-8")


if __name__ == "__main__":
    main()
