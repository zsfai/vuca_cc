#!/usr/bin/env python3
"""Audit hreflang parity, titles, and outbound citation presence across locales."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_kit import ALL_PAGES, LOCALES, page_file  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    issues = []
    warnings = []
    for page in ALL_PAGES:
        present = {loc: page_file(loc, page).exists() for loc in LOCALES}
        if not any(present.values()):
            continue
        if not all(present.values()):
            missing = [loc or "en" for loc, ok in present.items() if not ok]
            issues.append(f"{page}: missing locales {missing}")
            continue
        for loc in LOCALES:
            path = page_file(loc, page)
            html = path.read_text(encoding="utf-8")
            if 'rel="alternate" hreflang=' not in html:
                issues.append(f"{path}: missing hreflang")
            if 'property="og:title"' not in html:
                issues.append(f"{path}: missing og:title")
            if "application/ld+json" not in html:
                issues.append(f"{path}: missing JSON-LD")
            if 'href="css/site.css"' not in html and 'href="../css/site.css"' not in html:
                warnings.append(f"{path}: not using compiled css/site.css")
            title = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
            if title and title.group(1).strip() in ("VUCA", ""):
                issues.append(f"{path}: weak title {title.group(1)!r}")
    # Citation pages should have outbound links
    for page in ("bibliography.html", "resources.html", "what-is-vuca.html", "faq.html"):
        p = page_file("", page)
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        if "noopener" not in html and "hbr.org" not in html and "wikipedia.org" not in html:
            warnings.append(f"{page}: few/no outbound citation links detected")
    print(f"ISSUES ({len(issues)})")
    for i in issues[:50]:
        print(" -", i)
    print(f"WARNINGS ({len(warnings)})")
    for w in warnings[:30]:
        print(" -", w)


if __name__ == "__main__":
    main()
