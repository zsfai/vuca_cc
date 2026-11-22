#!/usr/bin/env python3
"""Rewrite locale homepages as knowledge hubs linking to pillar pages."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_kit import LASTMOD, wrap_page, page_file, write_sitemap, ALL_PAGES  # noqa: E402


def t(loc, en, ja, de, zh):
    return {"": en, "ja": ja, "de": de, "zh": zh}[loc]


def card(href, title, blurb):
    return f'''<a href="{href}" class="block rounded-3xl border border-gray-200 p-6 hover:border-emerald-300 hover:bg-emerald-50/40 transition">
  <h3 class="text-lg font-bold text-gray-900 mb-2">{title}</h3>
  <p class="text-sm text-gray-700 leading-relaxed">{blurb}</p>
</a>'''


def build(loc: str) -> tuple[str, str, str]:
    title = t(
        loc,
        "VUCA World: Volatility, Uncertainty, Complexity & Ambiguity Guide",
        "VUCAワールド：変動性・不確実性・複雑性・曖昧性の完全ガイド",
        "VUCA: Die VUCA-Welt verstehen und navigieren",
        "VUCA 世界：易变性、不确定性、复杂性与模糊性完整指南",
    )
    desc = t(
        loc,
        "Professional VUCA knowledge base: definitions, framework comparisons, leadership, industry guides, assessments, and templates in four languages.",
        "VUCAの専門ナレッジベース。定義、フレームワーク比較、リーダーシップ、業界ガイド、評価、テンプレート。",
        "Professionelle VUCA-Wissensbasis: Definitionen, Framework-Vergleiche, Führung, Branchenleitfäden, Assessments und Vorlagen.",
        "专业 VUCA 知识库：定义、框架对比、领导力、行业指南、评估与模板，支持四语。",
    )
    h1 = t(loc, "Understanding the VUCA World", "VUCAワールドを理解する", "Die VUCA-Welt verstehen", "理解 VUCA 世界")
    lead = t(
        loc,
        "Volatility, Uncertainty, Complexity, and Ambiguity shape modern strategy and leadership. This site is a structured reference for definitions, related frameworks, practice tools, and industry applications.",
        "変動性・不確実性・複雑性・曖昧性は、現代の戦略とリーダーシップを形作ります。本サイトは定義、関連フレームワーク、実践ツール、業界応用の体系的なリファレンスです。",
        "Volatilität, Unsicherheit, Komplexität und Mehrdeutigkeit prägen moderne Strategie und Führung. Diese Site ist eine strukturierte Referenz für Definitionen, verwandte Frameworks, Praxiswerkzeuge und Branchenanwendungen.",
        "易变性、不确定性、复杂性和模糊性塑造现代战略与领导力。本站是定义、相关框架、实践工具与行业应用的结构化参考。",
    )

    dim_title = t(loc, "The four dimensions", "四つの次元", "Die vier Dimensionen", "四个维度")
    dims = [
        ("volatility.html", "Volatility", "変動性", "Volatilität", "易变性",
         "Speed and magnitude of change.", "変化の速度と規模。", "Geschwindigkeit und Ausmaß des Wandels.", "变化的速度与幅度。"),
        ("uncertainty.html", "Uncertainty", "不確実性", "Unsicherheit", "不确定性",
         "Limited predictability and information gaps.", "予測可能性の欠如と情報ギャップ。", "Begrenzte Vorhersagbarkeit und Informationslücken.", "可预测性不足与信息缺口。"),
        ("complexity.html", "Complexity", "複雑性", "Komplexität", "复杂性",
         "Interconnected systems without linear cause-effect.", "線形因果のない相互接続システム。", "Vernetzte Systeme ohne lineare Ursache-Wirkung.", "非线性因果的互联系统。"),
        ("ambiguity.html", "Ambiguity", "曖昧性", "Mehrdeutigkeit", "模糊性",
         "Unclear meaning and multiple interpretations.", "意味が不明で解釈が複数。", "Unklare Bedeutung und multiple Interpretationen.", "意义不清与多种解释。"),
    ]
    dim_cards = []
    for href, en, ja, de, zh, e2, j2, d2, z2 in dims:
        dim_cards.append(card(href, t(loc, en, ja, de, zh), t(loc, e2, j2, d2, z2)))

    pillars_title = t(loc, "Core knowledge", "コアナレッジ", "Kernwissen", "核心知识")
    pillars = [
        ("what-is-vuca.html", t(loc, "What is VUCA", "VUCAとは", "Was ist VUCA", "什么是 VUCA"),
         t(loc, "Clear definition, usage, and how to apply the acronym as a diagnostic lens.", "定義、使い方、診断レンズとしての適用。", "Klare Definition und Anwendung als diagnostische Linse.", "清晰定义，以及作为诊断透镜的用法。")),
        ("history.html", t(loc, "Origins and history", "起源と歴史", "Ursprung und Geschichte", "起源与历史"),
         t(loc, "From Army War College and Bennis/Nanus to business adoption.", "陸軍大学とBennis/Nanusからビジネス採用まで。", "Vom Army War College und Bennis/Nanus zur Business-Adoption.", "从陆军战争学院与 Bennis/Nanus 到商业采纳。")),
        ("vuca-prime.html", t(loc, "VUCA Prime", "VUCA Prime", "VUCA Prime", "VUCA Prime"),
         t(loc, "Vision, Understanding, Clarity, Agility as leadership responses.", "ビジョン・理解・明確性・アジリティという応答。", "Vision, Verständnis, Klarheit, Agilität als Führungsantworten.", "愿景、理解、清晰、敏捷作为领导力回应。")),
        ("frameworks-comparison.html", t(loc, "Framework comparison", "フレームワーク比較", "Framework-Vergleich", "框架对比"),
         t(loc, "VUCA vs BANI vs TUNA vs RUPT vs Cynefin in one matrix.", "VUCA・BANI・TUNA・RUPT・Cynefinを一枚の表で。", "VUCA, BANI, TUNA, RUPT und Cynefin in einer Matrix.", "一张表对比 VUCA、BANI、TUNA、RUPT、Cynefin。")),
        ("leadership.html", t(loc, "VUCA leadership", "VUCAリーダーシップ", "VUCA-Führung", "VUCA 领导力"),
         t(loc, "Skills, models, training paths, and common mistakes.", "スキル、モデル、研修、よくある誤り。", "Skills, Modelle, Training und typische Fehler.", "技能、模型、培训路径与常见错误。")),
        ("faq.html", t(loc, "FAQ", "FAQ", "FAQ", "常见问题"),
         t(loc, "Short answers for the questions people and models ask first.", "人とモデルが最初に問う質問への短い回答。", "Kurze Antworten auf die häufigsten Fragen.", "人们与模型最先会问到的简短回答。")),
    ]
    pillar_cards = [card(h, ti, bl) for h, ti, bl in pillars]

    practice_title = t(loc, "Practice and tools", "実践とツール", "Praxis und Tools", "实践与工具")
    practice = [
        ("assessment.html", t(loc, "Leadership assessment", "リーダーシップ評価", "Leadership Assessment", "领导力评估"),
         t(loc, "12-question self-assessment across VUCA dimensions.", "VUCA次元にわたる12問の自己評価。", "12-Fragen-Selbstcheck über VUCA-Dimensionen.", "覆盖 VUCA 维度的 12 题自评。")),
        ("org-assessment.html", t(loc, "Organization diagnostic", "組織診断", "Organisationsdiagnose", "组织诊断"),
         t(loc, "Team and org-level checklist with scoring guidance.", "チーム/組織チェックリストと採点ガイド。", "Checkliste mit Scoring-Leitfaden für Teams und Organisationen.", "团队与组织级清单及评分指南。")),
        ("templates.html", t(loc, "Templates", "テンプレート", "Vorlagen", "模板"),
         t(loc, "Scorecards, scenario planning, and agility checklists.", "スコアカード、シナリオ計画、アジリティリスト。", "Scorecards, Szenarioplanung und Agilitäts-Checklisten.", "记分卡、情景规划与敏捷清单。")),
        ("action-guide.html", t(loc, "Action guide", "アクションガイド", "Handlungsleitfaden", "行动指南"),
         t(loc, "Playbooks for career, teams, supply chain, strategy, and more.", "キャリア、チーム、サプライチェーン、戦略などのプレイブック。", "Playbooks für Karriere, Teams, Supply Chain, Strategie u. a.", "职业、团队、供应链、战略等行动手册。")),
        ("examples.html", t(loc, "Examples", "事例", "Beispiele", "案例"),
         t(loc, "Contemporary events mapped to VUCA dimensions.", "現代の出来事をVUCA次元にマッピング。", "Aktuelle Ereignisse, den VUCA-Dimensionen zugeordnet.", "将当代事件映射到 VUCA 维度。")),
        ("bibliography.html", t(loc, "Bibliography", "文献", "Bibliografie", "文献"),
         t(loc, "Cited books and articles with outbound links.", "出典付きの書籍・論文リンク。", "Bücher und Artikel mit ausgehenden Links.", "带外链的书籍与文章引用。")),
    ]
    practice_cards = [card(h, ti, bl) for h, ti, bl in practice]

    industry_title = t(loc, "Industry applications", "業界応用", "Branchenanwendungen", "行业应用")
    industries = [
        ("industry-healthcare.html", t(loc, "Healthcare", "ヘルスケア", "Gesundheitswesen", "医疗健康")),
        ("industry-finance.html", t(loc, "Finance", "金融", "Finanzen", "金融")),
        ("industry-supply-chain.html", t(loc, "Supply chain", "サプライチェーン", "Lieferkette", "供应链")),
        ("industry-tech.html", t(loc, "Technology", "テクノロジー", "Technologie", "科技")),
        ("industry-education.html", t(loc, "Education", "教育", "Bildung", "教育")),
    ]
    ind_links = "".join(
        f'<a href="{h}" class="px-4 py-2 rounded-full border border-gray-200 text-sm text-gray-800 hover:border-emerald-400 hover:text-emerald-700">{lab}</a>'
        for h, lab in industries
    )

    cta_assess = t(loc, "Start assessment", "評価を開始", "Assessment starten", "开始评估")
    cta_what = t(loc, "What is VUCA", "VUCAとは", "Was ist VUCA", "什么是 VUCA")
    compare_note = t(
        loc,
        f'Also explore <a class="text-emerald-700 underline" href="vuca-vs-bani.html">VUCA vs BANI</a>, <a class="text-emerald-700 underline" href="tuna.html">TUNA</a>, <a class="text-emerald-700 underline" href="rupt.html">RUPT</a>, and <a class="text-emerald-700 underline" href="cynefin-and-vuca.html">Cynefin</a>.',
        f'<a class="text-emerald-700 underline" href="vuca-vs-bani.html">VUCA対BANI</a>、<a class="text-emerald-700 underline" href="tuna.html">TUNA</a>、<a class="text-emerald-700 underline" href="rupt.html">RUPT</a>、<a class="text-emerald-700 underline" href="cynefin-and-vuca.html">Cynefin</a>も参照。',
        f'Auch <a class="text-emerald-700 underline" href="vuca-vs-bani.html">VUCA vs BANI</a>, <a class="text-emerald-700 underline" href="tuna.html">TUNA</a>, <a class="text-emerald-700 underline" href="rupt.html">RUPT</a> und <a class="text-emerald-700 underline" href="cynefin-and-vuca.html">Cynefin</a>.',
        f'也可阅读 <a class="text-emerald-700 underline" href="vuca-vs-bani.html">VUCA 与 BANI</a>、<a class="text-emerald-700 underline" href="tuna.html">TUNA</a>、<a class="text-emerald-700 underline" href="rupt.html">RUPT</a> 与 <a class="text-emerald-700 underline" href="cynefin-and-vuca.html">Cynefin</a>。',
    )
    about_note = t(
        loc,
        f'Methodology and sourcing: <a class="text-emerald-700 underline" href="about.html">About</a> · <a class="text-emerald-700 underline" href="editorial.html">Editorial standards</a> · Last updated {LASTMOD}',
        f'方法論: <a class="text-emerald-700 underline" href="about.html">について</a> · <a class="text-emerald-700 underline" href="editorial.html">編集方針</a> · 更新 {LASTMOD}',
        f'Methodik: <a class="text-emerald-700 underline" href="about.html">Über uns</a> · <a class="text-emerald-700 underline" href="editorial.html">Editorial</a> · Stand {LASTMOD}',
        f'方法与来源：<a class="text-emerald-700 underline" href="about.html">关于</a> · <a class="text-emerald-700 underline" href="editorial.html">编辑标准</a> · 更新于 {LASTMOD}',
    )

    main = f'''
    <section class="py-20 bg-gradient-to-br from-emerald-50 to-white">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-5xl md:text-6xl font-bold text-gray-900 mb-6">{h1}</h1>
        <p class="text-xl text-gray-700 mb-8 max-w-3xl mx-auto leading-relaxed">{lead}</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <a href="assessment.html" class="px-8 py-3 bg-emerald-600 text-white rounded-lg font-medium hover:bg-emerald-700">{cta_assess}</a>
          <a href="what-is-vuca.html" class="px-8 py-3 border border-gray-300 text-gray-900 rounded-lg font-medium hover:border-emerald-500">{cta_what}</a>
        </div>
        <p class="mt-6 text-sm text-gray-600">{compare_note}</p>
      </div>
    </section>

    <section class="py-16 bg-white">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-8">{dim_title}</h2>
        <div class="grid md:grid-cols-2 gap-6">{''.join(dim_cards)}</div>
        <p class="mt-6 text-sm text-gray-600"><a class="text-emerald-700 underline" href="glossary.html">{t(loc, "Full glossary", "用語集", "Glossar", "完整术语表")}</a></p>
      </div>
    </section>

    <section class="py-16 bg-gray-50">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-8">{pillars_title}</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">{''.join(pillar_cards)}</div>
      </div>
    </section>

    <section class="py-16 bg-white">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-8">{practice_title}</h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">{''.join(practice_cards)}</div>
      </div>
    </section>

    <section class="py-16 bg-gray-50">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-gray-900 mb-6">{industry_title}</h2>
        <div class="flex flex-wrap gap-3">{ind_links}</div>
        <p class="mt-8 text-sm text-gray-600">{about_note}</p>
      </div>
    </section>
'''
    return title, desc, main


def main():
    for loc in ("", "ja", "de", "zh"):
        title, desc, main_html = build(loc)
        html = wrap_page(loc, "index.html", title, desc, main_html)
        path = page_file(loc, "index.html")
        path.write_text(html, encoding="utf-8")
        print("wrote", path)
    write_sitemap(ALL_PAGES)
    print("sitemap refreshed")


if __name__ == "__main__":
    main()
