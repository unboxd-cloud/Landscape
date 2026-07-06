#!/usr/bin/env python3
"""Check that generated site links point to existing local artifacts."""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
HREF_RE = re.compile(r'href="([^"]+)"')


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def is_external(link: str) -> bool:
    return link.startswith(("http://", "https://", "mailto:", "#"))


def main() -> None:
    index = SITE / "index.html"
    if not index.exists():
        fail("_site/index.html does not exist")

    content = index.read_text(encoding="utf-8")
    missing: list[str] = []
    for link in HREF_RE.findall(content):
        if is_external(link):
            continue
        path = SITE / link.split("#", 1)[0].split("?", 1)[0]
        if not path.exists():
            missing.append(link)

    if missing:
        fail("Missing generated links: " + ", ".join(sorted(set(missing))))

    print("Generated links validated")


if __name__ == "__main__":
    main()
