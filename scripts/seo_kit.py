#!/usr/bin/env python3
"""Shared SEO/GEO helpers for vuca.cc static site."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LASTMOD = "2026-11-22"
SITE = "https://vuca.cc"

LOCALES = {
    "": {"hreflang": "en", "html_lang": "en", "og_locale": "en_US", "dir": ""},
    "ja": {"hreflang": "ja", "html_lang": "ja", "og_locale": "ja_JP", "dir": "ja"},
    "de": {"hreflang": "de", "html_lang": "de", "og_locale": "de_DE", "dir": "de"},
    "zh": {"hreflang": "zh-Hans", "html_lang": "zh-CN", "og_locale": "zh_CN", "dir": "zh"},
}

# Core + knowledge pages (filename keys)
CORE_PAGES = [
    "index.html",
    "framework.html",
    "leadership.html",
    "action-guide.html",
    "examples.html",
    "resources.html",
    "assessment.html",
    "about.html",
]

KNOWLEDGE_PAGES = [
    "what-is-vuca.html",
    "history.html",
    "vuca-prime.html",
    "vuca-vs-bani.html",
    "tuna.html",
    "rupt.html",
    "cynefin-and-vuca.html",
    "frameworks-comparison.html",
    "glossary.html",
    "volatility.html",
    "uncertainty.html",
    "complexity.html",
    "ambiguity.html",
    "faq.html",
    "bibliography.html",
    "industry-healthcare.html",
    "industry-finance.html",
    "industry-supply-chain.html",
    "industry-tech.html",
    "industry-education.html",
    "templates.html",
    "org-assessment.html",
    "case-netflix.html",
    "case-toyota.html",
    "editorial.html",
]

ALL_PAGES = CORE_PAGES + KNOWLEDGE_PAGES
SCORECARD_PATH = "templates/vuca-scorecard.html"

PAGE_PRIORITIES = {
    "index.html": 1.0,
    "what-is-vuca.html": 0.95,
    "framework.html": 0.9,
    "frameworks-comparison.html": 0.9,
    "leadership.html": 0.9,
    "assessment.html": 0.9,
    "vuca-prime.html": 0.85,
    "history.html": 0.85,
    "faq.html": 0.85,
    "glossary.html": 0.8,
    "vuca-vs-bani.html": 0.8,
    "action-guide.html": 0.8,
    "examples.html": 0.8,
    "resources.html": 0.7,
    "bibliography.html": 0.7,
    "templates.html": 0.7,
    "about.html": 0.6,
    "editorial.html": 0.5,
}


def page_file(locale: str, page: str) -> Path:
    if locale:
        return ROOT / locale / page
    return ROOT / page


def canonical_url(locale: str, page: str) -> str:
    prefix = f"/{locale}" if locale else ""
    if page == "index.html":
        return f"{SITE}{prefix}/"
    return f"{SITE}{prefix}/{page}"


def hreflang_block(page: str) -> str:
    lines = []
    for loc, meta in LOCALES.items():
        lines.append(
            f'    <link rel="alternate" hreflang="{meta["hreflang"]}" href="{canonical_url(loc, page)}">'
        )
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="{canonical_url("", page)}">')
    return "\n".join(lines)


def icon_href(locale: str) -> str:
    return "../V.svg" if locale else "V.svg"


def css_href(locale: str) -> str:
    return "../css/site.css" if locale else "css/site.css"


def config_href(locale: str) -> str:
    return "../js/site-config.js" if locale else "js/site-config.js"


def analytics_href(locale: str) -> str:
    return "../js/analytics.js" if locale else "js/analytics.js"


NAV_LABELS = {
    "": {
        "home": "Home",
        "framework": "Framework",
        "leadership": "Leadership",
        "action": "Action Guide",
        "examples": "Examples",
        "resources": "Resources",
        "assessment": "Assessment",
        "knowledge": "Knowledge",
        "what_is": "What is VUCA",
        "glossary": "Glossary",
        "faq": "FAQ",
        "compare": "Frameworks",
        "about": "About",
        "lang": "EN",
    },
    "ja": {
        "home": "ホーム",
        "framework": "フレームワーク",
        "leadership": "リーダーシップ",
        "action": "アクションガイド",
        "examples": "事例",
        "resources": "リソース",
        "assessment": "評価",
        "knowledge": "ナレッジ",
        "what_is": "VUCAとは",
        "glossary": "用語集",
        "faq": "FAQ",
        "compare": "比較",
        "about": "について",
        "lang": "JA",
    },
    "de": {
        "home": "Start",
        "framework": "Framework",
        "leadership": "Führung",
        "action": "Leitfaden",
        "examples": "Beispiele",
        "resources": "Ressourcen",
        "assessment": "Assessment",
        "knowledge": "Wissen",
        "what_is": "Was ist VUCA",
        "glossary": "Glossar",
        "faq": "FAQ",
        "compare": "Frameworks",
        "about": "Über uns",
        "lang": "DE",
    },
    "zh": {
        "home": "首页",
        "framework": "框架",
        "leadership": "领导力",
        "action": "行动指南",
        "examples": "案例",
        "resources": "资源",
        "assessment": "评估",
        "knowledge": "知识库",
        "what_is": "什么是 VUCA",
        "glossary": "术语表",
        "faq": "常见问题",
        "compare": "框架对比",
        "about": "关于",
        "lang": "中文",
    },
}

FOOTER_COPY = {
    "": "Professional resource for VUCA education and leadership development.",
    "ja": "VUCA教育とリーダーシップ開発のための専門リソース。",
    "de": "Fachressource für VUCA-Bildung und Führungsentwicklung.",
    "zh": "VUCA 教育与领导力发展专业资源。",
}

LAST_UPDATED_LABEL = {
    "": "Last updated",
    "ja": "最終更新",
    "de": "Zuletzt aktualisiert",
    "zh": "最近更新",
}


def base_prefix(locale: str) -> str:
    return f"/{locale}/" if locale else "/"


def href(locale: str, page: str) -> str:
    if page == "index.html":
        return base_prefix(locale)
    return page if locale else page  # relative within locale dir


def build_nav(locale: str, active: str) -> str:
    L = NAV_LABELS[locale]
    prefix = base_prefix(locale)
    home = prefix

    def cls(page: str) -> str:
        if page == active:
            return "text-gray-900 hover:text-emerald-600 font-medium"
        return "text-gray-700 hover:text-emerald-600"

    def mcls(page: str) -> str:
        if page == active:
            return "block px-3 py-2 rounded-md text-gray-900 font-medium bg-emerald-50"
        return "block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50 hover:text-emerald-600"

    return f'''    <nav class="border-b border-gray-200 bg-white sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <a href="{home}" class="text-2xl font-bold text-emerald-600">VUCA</a>
                </div>
                <div class="hidden lg:flex space-x-6 items-center">
                    <a href="{home}" class="{cls("index.html")}">{L["home"]}</a>
                    <a href="framework.html" class="{cls("framework.html")}">{L["framework"]}</a>
                    <a href="leadership.html" class="{cls("leadership.html")}">{L["leadership"]}</a>
                    <a href="action-guide.html" class="{cls("action-guide.html")}">{L["action"]}</a>
                    <a href="examples.html" class="{cls("examples.html")}">{L["examples"]}</a>
                    <a href="resources.html" class="{cls("resources.html")}">{L["resources"]}</a>
                    <a href="assessment.html" class="{cls("assessment.html")}">{L["assessment"]}</a>
                    <div class="relative">
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
                    </div>
                    <div class="relative ml-2">
                        <button id="lang-button" class="flex items-center text-gray-700 hover:text-emerald-600 focus:outline-none">
                            <span class="text-sm font-medium">{L["lang"]}</span>
                            <svg class="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                        </button>
                        <div id="lang-menu" class="hidden absolute right-0 mt-2 w-36 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50">
                            <a id="lang-link-en" href="/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">English</a>
                            <a id="lang-link-ja" href="/ja/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">日本語</a>
                            <a id="lang-link-de" href="/de/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Deutsch</a>
                            <a id="lang-link-zh" href="/zh/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">中文</a>
                        </div>
                    </div>
                </div>
                <div class="lg:hidden flex items-center">
                    <button id="mobile-menu-button" class="text-gray-700 hover:text-emerald-600 focus:outline-none" aria-label="Menu">
                        <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path id="menu-icon" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                            <path id="close-icon" class="hidden" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <div id="mobile-menu" class="hidden lg:hidden border-t border-gray-200">
            <div class="px-2 pt-2 pb-3 space-y-1">
                <a href="{home}" class="{mcls("index.html")}">{L["home"]}</a>
                <a href="framework.html" class="{mcls("framework.html")}">{L["framework"]}</a>
                <a href="leadership.html" class="{mcls("leadership.html")}">{L["leadership"]}</a>
                <a href="action-guide.html" class="{mcls("action-guide.html")}">{L["action"]}</a>
                <a href="examples.html" class="{mcls("examples.html")}">{L["examples"]}</a>
                <a href="resources.html" class="{mcls("resources.html")}">{L["resources"]}</a>
                <a href="assessment.html" class="{mcls("assessment.html")}">{L["assessment"]}</a>
                <a href="glossary.html" class="{mcls("glossary.html")}">{L["glossary"]}</a>
                <a href="frameworks-comparison.html" class="{mcls("frameworks-comparison.html")}">{L["compare"]}</a>
                <a href="faq.html" class="{mcls("faq.html")}">{L["faq"]}</a>
                <a href="about.html" class="{mcls("about.html")}">{L["about"]}</a>
                <div class="border-t border-gray-200 mt-2 pt-2">
                    <div class="px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">Language</div>
                    <a id="lang-link-en-mobile" href="/" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50">English</a>
                    <a id="lang-link-ja-mobile" href="/ja/" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50">日本語</a>
                    <a id="lang-link-de-mobile" href="/de/" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50">Deutsch</a>
                    <a id="lang-link-zh-mobile" href="/zh/" class="block px-3 py-2 rounded-md text-gray-700 hover:bg-gray-50">中文</a>
                </div>
            </div>
        </div>
    </nav>'''


def build_footer(locale: str) -> str:
    home = base_prefix(locale)
    return f'''    <footer class="bg-gray-900 text-gray-300 py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-5 gap-8">
                <div class="md:col-span-1">
                    <a href="{home}" class="text-2xl font-bold text-white">VUCA</a>
                    <p class="mt-4 text-sm text-gray-400">{FOOTER_COPY[locale]}</p>
                    <p class="mt-3 text-xs text-gray-500">{LAST_UPDATED_LABEL[locale]}: {LASTMOD}</p>
                </div>
                <div>
                    <h3 class="text-white font-medium mb-4">Learn</h3>
                    <ul class="space-y-2 text-sm">
                        <li><a href="what-is-vuca.html" class="hover:text-white">What is VUCA</a></li>
                        <li><a href="history.html" class="hover:text-white">History</a></li>
                        <li><a href="framework.html" class="hover:text-white">Framework</a></li>
                        <li><a href="glossary.html" class="hover:text-white">Glossary</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-white font-medium mb-4">Compare</h3>
                    <ul class="space-y-2 text-sm">
                        <li><a href="frameworks-comparison.html" class="hover:text-white">All frameworks</a></li>
                        <li><a href="vuca-vs-bani.html" class="hover:text-white">VUCA vs BANI</a></li>
                        <li><a href="tuna.html" class="hover:text-white">TUNA</a></li>
                        <li><a href="cynefin-and-vuca.html" class="hover:text-white">Cynefin</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-white font-medium mb-4">Practice</h3>
                    <ul class="space-y-2 text-sm">
                        <li><a href="action-guide.html" class="hover:text-white">Action Guide</a></li>
                        <li><a href="assessment.html" class="hover:text-white">Assessment</a></li>
                        <li><a href="templates.html" class="hover:text-white">Templates</a></li>
                        <li><a href="org-assessment.html" class="hover:text-white">Org Diagnostic</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-white font-medium mb-4">Trust</h3>
                    <ul class="space-y-2 text-sm">
                        <li><a href="bibliography.html" class="hover:text-white">Bibliography</a></li>
                        <li><a href="faq.html" class="hover:text-white">FAQ</a></li>
                        <li><a href="about.html" class="hover:text-white">About</a></li>
                        <li><a href="editorial.html" class="hover:text-white">Editorial</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 mt-12 pt-8 text-sm text-center text-gray-400">
                <p>2026 VUCA.cc. {FOOTER_COPY[locale]}</p>
            </div>
        </div>
    </footer>'''


LANG_SCRIPT = '''    <script>
        (function () {
            const mobileMenuButton = document.getElementById('mobile-menu-button');
            const mobileMenu = document.getElementById('mobile-menu');
            const menuIcon = document.getElementById('menu-icon');
            const closeIcon = document.getElementById('close-icon');
            const langButton = document.getElementById('lang-button');
            const langMenu = document.getElementById('lang-menu');
            const knowledgeButton = document.getElementById('knowledge-button');
            const knowledgeMenu = document.getElementById('knowledge-menu');
            if (mobileMenuButton && mobileMenu) {
                mobileMenuButton.addEventListener('click', () => {
                    mobileMenu.classList.toggle('hidden');
                    if (menuIcon) menuIcon.classList.toggle('hidden');
                    if (closeIcon) closeIcon.classList.toggle('hidden');
                });
            }
            function closeLang() {
                if (langMenu) langMenu.classList.add('hidden');
            }
            function closeKnowledge() {
                if (knowledgeMenu) knowledgeMenu.classList.add('hidden');
                if (knowledgeButton) knowledgeButton.setAttribute('aria-expanded', 'false');
            }
            if (langButton && langMenu) {
                langButton.addEventListener('click', (e) => {
                    e.stopPropagation();
                    closeKnowledge();
                    langMenu.classList.toggle('hidden');
                });
            }
            if (knowledgeButton && knowledgeMenu) {
                knowledgeButton.addEventListener('click', (e) => {
                    e.stopPropagation();
                    closeLang();
                    const open = knowledgeMenu.classList.toggle('hidden') === false;
                    knowledgeButton.setAttribute('aria-expanded', open ? 'true' : 'false');
                });
            }
            document.addEventListener('click', (e) => {
                if (langButton && langMenu && !langButton.contains(e.target) && !langMenu.contains(e.target)) {
                    closeLang();
                }
                if (knowledgeButton && knowledgeMenu && !knowledgeButton.contains(e.target) && !knowledgeMenu.contains(e.target)) {
                    closeKnowledge();
                }
            });
            const parts = window.location.pathname.replace(/\\/+$/, '').split('/').filter(Boolean);
            let page = 'index.html';
            if (parts.length === 0) page = 'index.html';
            else if (parts[parts.length - 1].endsWith('.html')) page = parts[parts.length - 1];
            else if (['ja', 'de', 'zh'].includes(parts[parts.length - 1])) page = 'index.html';
            const en = page === 'index.html' ? '/' : '/' + page;
            const ja = page === 'index.html' ? '/ja/' : '/ja/' + page;
            const de = page === 'index.html' ? '/de/' : '/de/' + page;
            const zh = page === 'index.html' ? '/zh/' : '/zh/' + page;
            const map = { 'lang-link-en': en, 'lang-link-ja': ja, 'lang-link-de': de, 'lang-link-zh': zh,
                'lang-link-en-mobile': en, 'lang-link-ja-mobile': ja, 'lang-link-de-mobile': de, 'lang-link-zh-mobile': zh };
            Object.keys(map).forEach((id) => { const el = document.getElementById(id); if (el) el.href = map[id]; });
        })();
    </script>'''


def head_tags(
    locale: str,
    page: str,
    title: str,
    description: str,
    schema_type: str = "WebPage",
    extra_schema: dict | None = None,
) -> str:
    meta = LOCALES[locale]
    canon = canonical_url(locale, page)
    og_type = "website" if page == "index.html" else "article"
    schema = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": title,
        "description": description,
        "url": canon,
        "inLanguage": meta["html_lang"],
        "dateModified": LASTMOD,
        "isPartOf": {"@type": "WebSite", "name": "VUCA.cc", "url": SITE},
        "publisher": {
            "@type": "Organization",
            "name": "VUCA.cc",
            "url": SITE,
            "logo": {"@type": "ImageObject", "url": f"{SITE}/V.svg"},
        },
    }
    if page == "index.html":
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Organization",
                    "name": "VUCA.cc",
                    "url": SITE,
                    "logo": f"{SITE}/V.svg",
                    "description": "Professional knowledge base for VUCA frameworks, leadership, and practice.",
                },
                {
                    "@type": "WebSite",
                    "name": "VUCA.cc",
                    "url": SITE,
                    "inLanguage": ["en", "ja", "de", "zh-CN"],
                    "publisher": {"@type": "Organization", "name": "VUCA.cc", "url": SITE},
                },
            ],
        }
    if extra_schema:
        if "@graph" in schema:
            schema["@graph"].append(extra_schema)
        else:
            schema = {"@context": "https://schema.org", "@graph": [schema, extra_schema]}

    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)
    return f'''<!DOCTYPE html>
<html lang="{meta["html_lang"]}" class="overflow-x-hidden">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canon}">
{hreflang_block(page)}
    <meta property="og:type" content="{og_type}">
    <meta property="og:site_name" content="VUCA.cc">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canon}">
    <meta property="og:locale" content="{meta["og_locale"]}">
    <meta property="og:image" content="{SITE}/V.svg">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{SITE}/V.svg">
    <meta name="last-modified" content="{LASTMOD}">
    <link rel="icon" type="image/svg+xml" href="{icon_href(locale)}">
    <link rel="stylesheet" href="{css_href(locale)}">
    <script type="application/ld+json">
{schema_json}
    </script>
    <script src="{config_href(locale)}"></script>
    <script src="{analytics_href(locale)}" defer></script>
</head>'''


def wrap_page(
    locale: str,
    page: str,
    title: str,
    description: str,
    main_html: str,
    schema_type: str = "WebPage",
    extra_schema: dict | None = None,
) -> str:
    return "\n".join(
        [
            head_tags(locale, page, title, description, schema_type, extra_schema),
            '<body class="bg-white text-gray-900 overflow-x-hidden">',
            build_nav(locale, page),
            f'    <main id="main-content">',
            main_html,
            "    </main>",
            build_footer(locale),
            LANG_SCRIPT,
            "</body>",
            "</html>",
        ]
    )


def inject_seo_into_existing(html: str, locale: str, page: str, title: str | None = None, description: str | None = None) -> str:
    """Patch an existing page head with hreflang/OG/schema while preserving body.

    Never matches across JSON-LD or other typed <script> tags when rewriting nav JS.
    """
    t_match = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    d_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I | re.S)
    old_title = title or (t_match.group(1).strip() if t_match else "VUCA")
    old_desc = description or (d_match.group(1).strip() if d_match else "")

    if page == "index.html" and locale == "" and old_title.strip() == "VUCA":
        old_title = "VUCA World: Volatility, Uncertainty, Complexity & Ambiguity Guide"
    if page == "index.html" and locale == "zh" and old_title.strip() == "VUCA":
        old_title = "VUCA 世界：易变性、不确定性、复杂性与模糊性完整指南"

    schema_type = "WebApplication" if page == "assessment.html" else "WebPage"
    new_head = head_tags(locale, page, old_title, old_desc, schema_type)

    html2 = re.sub(r"<!DOCTYPE html>.*?</head>", new_head, html, count=1, flags=re.I | re.S)

    # Fix previously broken escaped main ids
    html2 = html2.replace('<main id=\\"main-content">', '<main id="main-content">')
    html2 = html2.replace("<main id=\\\"main-content\">", '<main id="main-content">')

    # Ensure <main> wrapper if missing (use non-raw replacement to avoid \" leakage)
    if re.search(r"<main\b", html2, re.I) is None:
        html2 = re.sub(r"(</nav>\s*)", r'\1\n    <main id="main-content">\n', html2, count=1, flags=re.I)
        if re.search(r"<footer\b", html2, re.I) and not re.search(r"</main>", html2, re.I):
            html2 = re.sub(r"(<footer\b)", r"    </main>\n\1", html2, count=1, flags=re.I)

    # Close unclosed main before footer if needed
    if re.search(r"<main\b", html2, re.I) and not re.search(r"</main>", html2, re.I):
        if re.search(r"<footer\b", html2, re.I):
            html2 = re.sub(r"(<footer\b)", r"    </main>\n\1", html2, count=1, flags=re.I)
        else:
            html2 = re.sub(r"(<script\b(?![^>]*type=))", r"</main>\n\1", html2, count=1, flags=re.I)

    # Replace only untyped scripts that contain lang-link-en WITHOUT crossing </script>
    nav_script_re = re.compile(
        r"<script(?![^>]*\btype=)[^>]*>((?:(?!</script>).)*\blang-link-en\b(?:(?!</script>).)*)</script>",
        re.I | re.S,
    )
    matches = list(nav_script_re.finditer(html2))
    if matches:
        m = matches[-1]
        html2 = html2[: m.start()] + LANG_SCRIPT + html2[m.end() :]
    elif "lang-link-en" in html2 and "Object.keys(map)" not in html2:
        html2 = re.sub(r"</body>", LANG_SCRIPT + "\n</body>", html2, count=1, flags=re.I)

    # Ensure analytics/config scripts in head
    cfg = config_href(locale)
    ana = analytics_href(locale)
    if "site-config.js" not in html2:
        html2 = html2.replace("</head>", f'    <script src="{cfg}"></script>\n    <script src="{ana}" defer></script>\n</head>', 1)

    label = LAST_UPDATED_LABEL[locale]
    if f"{label}:" not in html2:
        html2 = html2.replace(
            '<div class="border-t border-gray-800 mt-12 pt-8 text-sm text-center text-gray-400">',
            f'<div class="border-t border-gray-800 mt-12 pt-8 text-sm text-center text-gray-400">\n                <p class="mb-2 text-xs">{label}: {LASTMOD}</p>',
            1,
        )

    html2 = re.sub(
        r'<script src="https://cdn\.tailwindcss\.com"></script>',
        f'<link rel="stylesheet" href="{css_href(locale)}">',
        html2,
    )

    return html2


def write_sitemap(pages: list[str] | None = None) -> None:
    pages = pages or [p for p in ALL_PAGES if any(page_file(loc, p).exists() for loc in LOCALES)]
    # Only include pages that exist in at least EN
    pages = [p for p in pages if page_file("", p).exists()]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for page in pages:
        for loc in LOCALES:
            if not page_file(loc, page).exists():
                continue
            loc_url = canonical_url(loc, page)
            pri = PAGE_PRIORITIES.get(page, 0.6)
            if loc:
                pri = max(0.5, pri - 0.1)
            lines.append("  <url>")
            lines.append(f"    <loc>{loc_url}</loc>")
            lines.append(f"    <lastmod>{LASTMOD}</lastmod>")
            lines.append(f"    <changefreq>{'weekly' if page == 'index.html' else 'monthly'}</changefreq>")
            lines.append(f"    <priority>{pri:.1f}</priority>")
            for alt in LOCALES:
                if page_file(alt, page).exists():
                    lines.append(
                        f'    <xhtml:link rel="alternate" hreflang="{LOCALES[alt]["hreflang"]}" href="{canonical_url(alt, page)}"/>'
                    )
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{canonical_url("", page)}"/>'
            )
            lines.append("  </url>")
    # EN-only printable scorecard
    score = ROOT / SCORECARD_PATH
    if score.exists():
        lines.append("  <url>")
        lines.append(f"    <loc>{SITE}/{SCORECARD_PATH}</loc>")
        lines.append(f"    <lastmod>{LASTMOD}</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append("    <priority>0.4</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
