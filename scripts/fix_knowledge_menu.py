#!/usr/bin/env python3
"""Convert hover Knowledge dropdowns to clickable menus site-wide."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_kit import LANG_SCRIPT, LOCALES, NAV_LABELS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

DROPDOWN_RE = re.compile(
    r'<div class="relative group">\s*'
    r'<button type="button"[^>]*>.*?</button>\s*'
    r'<div class="hidden group-hover:block absolute left-0 mt-2 w-48[^"]*"[^>]*>'
    r'[\s\S]*?'
    r'</div>\s*</div>',
    re.I,
)


def knowledge_block(locale: str) -> str:
    L = NAV_LABELS[locale]
    return f'''                    <div class="relative">
                        <button type="button" id="knowledge-button" class="text-gray-700 hover:text-emerald-600 text-sm font-medium focus:outline-none" aria-expanded="false" aria-haspopup="true">{L["knowledge"]}</button>
                        <div id="knowledge-menu" class="hidden absolute left-0 top-full pt-1 w-48 z-50">
                            <div class="bg-white rounded-lg shadow-lg border border-gray-200 py-1">
                                <a href="what-is-vuca.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">{L["what_is"]}</a>
                                <a href="glossary.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">{L["glossary"]}</a>
                                <a href="frameworks-comparison.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">{L["compare"]}</a>
                                <a href="faq.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">{L["faq"]}</a>
                                <a href="about.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">{L["about"]}</a>
                            </div>
                        </div>
                    </div>'''


def locale_of(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    if parts and parts[0] in ("ja", "de", "zh"):
        return parts[0]
    return ""


def replace_nav_script(html: str) -> str:
    pattern = re.compile(
        r"<script(?![^>]*\btype=)[^>]*>((?:(?!</script>).)*\blang-link-en\b(?:(?!</script>).)*)</script>",
        re.I | re.S,
    )
    matches = list(pattern.finditer(html))
    if matches:
        m = matches[-1]
        return html[: m.start()] + LANG_SCRIPT + html[m.end() :]
    if "knowledge-button" in html and "getElementById('knowledge-button')" not in html:
        return re.sub(r"</body\s*>", LANG_SCRIPT + "\n</body>", html, count=1, flags=re.I)
    return html


def main() -> None:
    n_html = 0
    n_drop = 0
    n_script = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in path.parts or path.parts[0] == "templates":
            continue
        html = path.read_text(encoding="utf-8")
        loc = locale_of(path)
        original = html
        if "group-hover:block" in html and "glossary.html" in html:
            html2, count = DROPDOWN_RE.subn(knowledge_block(loc), html, count=1)
            if count:
                html = html2
                n_drop += 1
            else:
                # looser fallback
                html2, count = re.subn(
                    r'<div class="relative group">[\s\S]*?group-hover:block[\s\S]*?</div>\s*</div>',
                    knowledge_block(loc),
                    html,
                    count=1,
                )
                if count:
                    html = html2
                    n_drop += 1
        html = replace_nav_script(html)
        if html != original:
            path.write_text(html, encoding="utf-8")
            n_html += 1
            if "getElementById('knowledge-button')" in html or 'getElementById("knowledge-button")' in html:
                n_script += 1
            print("fixed", path.relative_to(ROOT).as_posix())
    print(f"updated_files={n_html} dropdowns={n_drop}")


if __name__ == "__main__":
    main()
