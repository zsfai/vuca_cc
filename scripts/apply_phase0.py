#!/usr/bin/env python3
"""Apply Phase 0 SEO patches to existing core pages."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_kit import (  # noqa: E402
    CORE_PAGES,
    LOCALES,
    inject_seo_into_existing,
    page_file,
    write_sitemap,
)

TITLE_OVERRIDES = {
    ("", "index.html"): (
        "VUCA World: Volatility, Uncertainty, Complexity & Ambiguity Guide",
        "Professional guide to VUCA: definitions, frameworks, leadership strategies, and practical approaches for volatile, uncertain, complex, and ambiguous environments.",
    ),
    ("zh", "index.html"): (
        "VUCA 世界：易变性、不确定性、复杂性与模糊性完整指南",
        "掌握 VUCA：学习框架、领导力策略与应对易变性、不确定性、复杂性和模糊性环境的实用方法。",
    ),
}


def patch_resources_outbound(html: str) -> str:
    """Add outbound citation links and remove emoji book placeholders."""
    replacements = [
        (
            "<h3 class=\"text-2xl font-bold text-gray-900 mb-2\">Leaders Make the Future</h3>",
            '<h3 class="text-2xl font-bold text-gray-900 mb-2"><a class="hover:text-emerald-700" href="https://www.iftf.org/" target="_blank" rel="noopener noreferrer">Leaders Make the Future</a></h3>',
        ),
        (
            'content="What VUCA Really Means for You"',
            'content="What VUCA Really Means for You"',
        ),
    ]
    for a, b in replacements:
        html = html.replace(a, b)

    # Common article cards: inject links if titles present
    link_map = {
        "What VUCA Really Means for You": "https://hbr.org/2014/01/what-vuca-really-means-for-you",
        "Leadership Skills for an Uncertain World": "https://www.ccl.org/articles/leading-effectively-articles/leadership-skills-for-an-uncertain-world/",
        "Facing the Future": "https://en.wikipedia.org/wiki/VUCA",
    }
    for title, url in link_map.items():
        pattern = rf"(<h3[^>]*>)({re.escape(title)})(</h3>)"
        html = re.sub(
            pattern,
            rf'\1<a class="hover:text-emerald-700" href="{url}" target="_blank" rel="noopener noreferrer">\2</a>\3',
            html,
            count=1,
        )

    # Remove emoji book glyphs
    html = re.sub(
        r'<p class="text-4xl font-bold text-\w+-700">📚</p>',
        '<p class="text-sm font-bold text-gray-600 tracking-wide">BOOK</p>',
        html,
    )
    return html


def ensure_about_footer_link(html: str) -> str:
    if "about.html" in html:
        return html
    # Add about link in resources column if present
    return html.replace(
        '<li><a href="resources.html#case-studies" class="hover:text-white">Case Studies</a></li>',
        '<li><a href="resources.html#case-studies" class="hover:text-white">Case Studies</a></li>\n                        <li><a href="about.html" class="hover:text-white">About</a></li>\n                        <li><a href="faq.html" class="hover:text-white">FAQ</a></li>',
        1,
    )


def main() -> None:
    for loc in LOCALES:
        for page in CORE_PAGES:
            path = page_file(loc, page)
            if not path.exists():
                continue
            html = path.read_text(encoding="utf-8")
            title = desc = None
            if (loc, page) in TITLE_OVERRIDES:
                title, desc = TITLE_OVERRIDES[(loc, page)]
            html = inject_seo_into_existing(html, loc, page, title, desc)
            if page == "resources.html":
                html = patch_resources_outbound(html)
            html = ensure_about_footer_link(html)
            # Ensure analytics/config scripts if inject missed body assets
            cfg = "../js/site-config.js" if loc else "js/site-config.js"
            ana = "../js/analytics.js" if loc else "js/analytics.js"
            if "site-config.js" not in html:
                html = html.replace("</head>", f'    <script src="{cfg}"></script>\n    <script src="{ana}" defer></script>\n</head>', 1)
            path.write_text(html, encoding="utf-8")
            print(f"patched {path.relative_to(path.parent.parent if loc else path.parent)}")
    write_sitemap(CORE_PAGES)
    print("sitemap updated (core)")


if __name__ == "__main__":
    main()
