#!/usr/bin/env python3
"""Safely repair core pages: head SEO only, fix main landmark, add Knowledge nav, never wipe body."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_kit import (  # noqa: E402
    ALL_PAGES,
    LANG_SCRIPT,
    LOCALES,
    css_href,
    config_href,
    analytics_href,
    head_tags,
    page_file,
    write_sitemap,
)

ROOT = Path(__file__).resolve().parent.parent

CORE_CONTENT = [
    "framework.html",
    "leadership.html",
    "action-guide.html",
    "examples.html",
    "resources.html",
    "assessment.html",
]

DE_DESCRIPTIONS = {
    "framework.html": (
        "VUCA Framework: Vollständiger Analyse- und Implementierungsleitfaden. "
        "Lernen Sie, Volatilität, Unsicherheit, Komplexität und Mehrdeutigkeit in Organisationen zu analysieren und zu nutzen."
    ),
    "leadership.html": (
        "VUCA-Führung: Fähigkeiten, Strategien und Trainingspfade für Führungskräfte in volatilen, unsicheren, "
        "komplexen und mehrdeutigen Umgebungen."
    ),
}

KNOWLEDGE_DESKTOP = {
    "": """                    <div class="relative group">
                        <button type="button" class="text-gray-700 hover:text-emerald-600 text-sm font-medium">Knowledge</button>
                        <div class="hidden group-hover:block absolute left-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50">
                            <a href="what-is-vuca.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">What is VUCA</a>
                            <a href="glossary.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Glossary</a>
                            <a href="frameworks-comparison.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Frameworks</a>
                            <a href="faq.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">FAQ</a>
                            <a href="about.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">About</a>
                        </div>
                    </div>
""",
    "ja": """                    <div class="relative group">
                        <button type="button" class="text-gray-700 hover:text-emerald-600 text-sm font-medium">ナレッジ</button>
                        <div class="hidden group-hover:block absolute left-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50">
                            <a href="what-is-vuca.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">VUCAとは</a>
                            <a href="glossary.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">用語集</a>
                            <a href="frameworks-comparison.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">比較</a>
                            <a href="faq.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">FAQ</a>
                            <a href="about.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">について</a>
                        </div>
                    </div>
""",
    "de": """                    <div class="relative group">
                        <button type="button" class="text-gray-700 hover:text-emerald-600 text-sm font-medium">Wissen</button>
                        <div class="hidden group-hover:block absolute left-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50">
                            <a href="what-is-vuca.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Was ist VUCA</a>
                            <a href="glossary.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Glossar</a>
                            <a href="frameworks-comparison.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Frameworks</a>
                            <a href="faq.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">FAQ</a>
                            <a href="about.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Über uns</a>
                        </div>
                    </div>
""",
    "zh": """                    <div class="relative group">
                        <button type="button" class="text-gray-700 hover:text-emerald-600 text-sm font-medium">知识库</button>
                        <div class="hidden group-hover:block absolute left-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50">
                            <a href="what-is-vuca.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">什么是 VUCA</a>
                            <a href="glossary.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">术语表</a>
                            <a href="frameworks-comparison.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">框架对比</a>
                            <a href="faq.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">常见问题</a>
                            <a href="about.html" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">关于</a>
                        </div>
                    </div>
""",
}

KNOWLEDGE_MOBILE = {
    "": """                <a href="what-is-vuca.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">What is VUCA</a>
                <a href="glossary.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">Glossary</a>
                <a href="faq.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">FAQ</a>
""",
    "ja": """                <a href="what-is-vuca.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">VUCAとは</a>
                <a href="glossary.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">用語集</a>
                <a href="faq.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">FAQ</a>
""",
    "de": """                <a href="what-is-vuca.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">Was ist VUCA</a>
                <a href="glossary.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">Glossar</a>
                <a href="faq.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">FAQ</a>
""",
    "zh": """                <a href="what-is-vuca.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">什么是 VUCA</a>
                <a href="glossary.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">术语表</a>
                <a href="faq.html" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600">常见问题</a>
""",
}


def replace_head(html: str, locale: str, page: str) -> str:
    t_match = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    d_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I | re.S)
    title = t_match.group(1).strip() if t_match else "VUCA"
    desc = d_match.group(1).strip() if d_match else ""
    if locale == "de" and page in DE_DESCRIPTIONS:
        desc = DE_DESCRIPTIONS[page]
    schema = "WebApplication" if page == "assessment.html" else "WebPage"
    new_head = head_tags(locale, page, title, desc, schema)
    return re.sub(r"<!DOCTYPE html>.*?</head>", new_head, html, count=1, flags=re.I | re.S)


def fix_main(html: str) -> str:
    # Remove broken escaped openers and orphan closers first
    html = html.replace('<main id=\\"main-content">', '<main id="main-content">')
    html = re.sub(r'<main[^>]*>', '<main id="main-content">', html, count=1, flags=re.I) if re.search(r"<main\b", html, re.I) else html

    has_open = bool(re.search(r"<main\b", html, re.I))
    has_close = bool(re.search(r"</main>", html, re.I))

    if not has_open:
        html = re.sub(r"(</nav>)", r'\1\n    <main id="main-content">', html, count=1, flags=re.I)
        has_open = True
    if has_open and not has_close:
        if re.search(r"<footer\b", html, re.I):
            html = re.sub(r"(<footer\b)", r"</main>\n\1", html, count=1, flags=re.I)
        else:
            # before last script group near body end
            html = re.sub(r"(</body>)", r"</main>\n\1", html, count=1, flags=re.I)
    # If multiple closes, leave as-is; if close without open already handled
    # Remove duplicate closes
    parts = html.split("</main>")
    if len(parts) > 2:
        html = "</main>".join(parts[:-1]) + "</main>" + parts[-1]
        # actually keep only first close after open
        html = re.sub(r"</main>", "</main>", html, count=1)
        # remove extra
        first = True
        out = []
        i = 0
        while i < len(html):
            if html.startswith("</main>", i):
                if first:
                    out.append("</main>")
                    first = False
                i += len("</main>")
            else:
                out.append(html[i])
                i += 1
        html = "".join(out)
    return html


def ensure_knowledge_nav(html: str, locale: str) -> str:
    if "group-hover:block" in html and "glossary.html" in html and any(
        x in html for x in ("Knowledge", "ナレッジ", "Wissen", "知识库")
    ):
        return html
    desk = KNOWLEDGE_DESKTOP[locale]
    if 'id="lang-button"' in html:
        html = html.replace(
            '<div class="relative ml-4">',
            desk + '                    <div class="relative ml-4">',
            1,
        )
    mob = KNOWLEDGE_MOBILE[locale]
    marker = 'uppercase tracking-wider">Language</div>'
    alt_markers = [
        'uppercase tracking-wider">Language</div>',
        'uppercase tracking-wider">言語</div>',
        'uppercase tracking-wider">Sprache</div>',
        'uppercase tracking-wider">语言</div>',
    ]
    if "glossary.html" not in html.split('id="mobile-menu"', 1)[-1][:1200]:
        for m in alt_markers:
            if m in html:
                html = html.replace(
                    '<div class="border-t border-gray-200 mt-2 pt-2">\n                    <div class="px-3 py-2 text-xs font-semibold text-gray-500 ' + m,
                    mob + '                <div class="border-t border-gray-200 mt-2 pt-2">\n                    <div class="px-3 py-2 text-xs font-semibold text-gray-500 ' + m,
                    1,
                )
                break
        else:
            # fallback insert before mobile lang links
            if 'id="lang-link-en-mobile"' in html:
                html = html.replace(
                    '<a id="lang-link-en-mobile"',
                    mob + '                <a id="lang-link-en-mobile"',
                    1,
                )
    html = html.replace("hidden md:flex space-x-8", "hidden lg:flex space-x-6")
    html = html.replace('class="md:hidden flex items-center"', 'class="lg:hidden flex items-center"')
    html = html.replace('class="hidden md:hidden', 'class="hidden lg:hidden')
    return html


def replace_lang_script_safe(html: str) -> str:
    """Replace only scripts that contain lang-link-en and do not cross script boundaries."""
    pattern = re.compile(
        r"<script(?![^>]*\btype=)[^>]*>((?:(?!</script>).)*\blang-link-en\b(?:(?!</script>).)*)</script>",
        re.I | re.S,
    )
    matches = list(pattern.finditer(html))
    if not matches:
        if "Object.keys(map)" not in html:
            html = re.sub(r"</body\s*>", LANG_SCRIPT + "\n</body>", html, count=1, flags=re.I)
        return html
    m = matches[-1]
    return html[: m.start()] + LANG_SCRIPT + html[m.end() :]


def patch_cdn(html: str, locale: str) -> str:
    html = re.sub(
        r'<script src="https://cdn\.tailwindcss\.com"></script>',
        f'<link rel="stylesheet" href="{css_href(locale)}">',
        html,
    )
    if "site-config.js" not in html:
        html = html.replace(
            "</head>",
            f'    <script src="{config_href(locale)}"></script>\n    <script src="{analytics_href(locale)}" defer></script>\n</head>',
            1,
        )
    return html


def patch_resources(html: str) -> str:
    pairs = {
        "What VUCA Really Means for You": "https://hbr.org/2014/01/what-vuca-really-means-for-you",
        "Leadership Skills for an Uncertain World": "https://www.ccl.org/articles/leading-effectively-articles/leadership-skills-for-an-uncertain-world/",
    }
    for title, url in pairs.items():
        if url in html:
            continue
        pattern = rf"(<h3[^>]*>)({re.escape(title)})(</h3>)"
        html = re.sub(
            pattern,
            rf'\1<a class="hover:text-emerald-700" href="{url}" target="_blank" rel="noopener noreferrer">\2</a>\3',
            html,
            count=1,
        )
    html = re.sub(
        r'<p class="text-4xl font-bold text-\w+-700">📚</p>',
        '<p class="text-sm font-bold text-gray-600 tracking-wide">BOOK</p>',
        html,
    )
    # knowledge strip
    if "bibliography.html" not in html:
        strip = """
    <section class="py-8 bg-white border-b border-gray-100">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-wrap gap-4 text-sm">
        <a class="text-emerald-700 underline" href="bibliography.html">Bibliography</a>
        <a class="text-emerald-700 underline" href="templates.html">Templates</a>
        <a class="text-emerald-700 underline" href="org-assessment.html">Organization diagnostic</a>
        <a class="text-emerald-700 underline" href="frameworks-comparison.html">Framework comparison</a>
      </div>
    </section>
"""
        html = html.replace("</section>", "</section>\n" + strip, 1)
    return html


def assert_healthy(path: Path, html: str) -> None:
    if not re.search(r"<h1\b", html, re.I):
        raise RuntimeError(f"{path}: missing H1 after repair")
    if not re.search(r"</footer>", html, re.I):
        raise RuntimeError(f"{path}: missing footer after repair")
    if html.count("<main") != html.count("</main>"):
        raise RuntimeError(f"{path}: main tag mismatch open={html.count('<main')} close={html.count('</main>')}")
    # body text roughly present
    m = re.search(r"<main\b[^>]*>([\s\S]*?)</main>", html, re.I)
    if not m or len(re.sub(r"<[^>]+>", "", m.group(1))) < 400:
        raise RuntimeError(f"{path}: main content too thin after repair")


def main() -> None:
    for loc in LOCALES:
        for page in CORE_CONTENT:
            path = page_file(loc, page)
            if not path.exists():
                continue
            original = path.read_text(encoding="utf-8")
            html = original
            html = replace_head(html, loc, page)
            html = patch_cdn(html, loc)
            html = fix_main(html)
            html = ensure_knowledge_nav(html, loc)
            html = replace_lang_script_safe(html)
            if page == "resources.html":
                html = patch_resources(html)
            html = html.replace("<p><p>", "<p>").replace("</p></p>", "</p>")
            try:
                assert_healthy(path, html)
            except RuntimeError as e:
                print("FAIL", e)
                # do not write broken result
                continue
            path.write_text(html, encoding="utf-8")
            print("ok", path.relative_to(ROOT).as_posix(), "lines", html.count("\n") + 1)

    # Re-expand action guides after restore
    try:
        from expand_action_guide import main as expand_main

        expand_main()
    except Exception as e:
        print("expand_action_guide skipped:", e)

    write_sitemap(ALL_PAGES)
    print("done")


if __name__ == "__main__":
    main()
