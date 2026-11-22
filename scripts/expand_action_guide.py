#!/usr/bin/env python3
"""Append strategy/HR/risk/PM playbooks to action-guide pages (all locales)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MARKER = "<!-- EXPANDED_PLAYBOOKS -->"

EN_BLOCK = '''
            ''' + MARKER + '''
            <div class="mt-12 grid md:grid-cols-2 gap-8">
                <div class="bg-gradient-to-br from-emerald-50 to-white border border-emerald-200 rounded-3xl p-8">
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">Strategy under Uncertainty</h3>
                    <p class="text-gray-700 mb-6">Replace single-point forecasts with decision-ready options.</p>
                    <div class="space-y-3 text-sm text-gray-700">
                        <p><span class="font-bold text-gray-900">1.</span> Write three scenarios (base, adverse, opportunity) with explicit triggers.</p>
                        <p><span class="font-bold text-gray-900">2.</span> Pre-commit options, not detailed 3-year plans.</p>
                        <p><span class="font-bold text-gray-900">3.</span> Review assumptions monthly; kill stale initiatives.</p>
                        <p><span class="font-bold text-gray-900">4.</span> Link strategy reviews to <a class="text-emerald-700 underline" href="framework.html">VUCA dimension scores</a>.</p>
                    </div>
                </div>
                <div class="bg-gradient-to-br from-blue-50 to-white border border-blue-200 rounded-3xl p-8">
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">Product Discovery Loop</h3>
                    <p class="text-gray-700 mb-6">Reduce ambiguity with fast evidence, not bigger decks.</p>
                    <div class="space-y-3 text-sm text-gray-700">
                        <p><span class="font-bold text-gray-900">1.</span> Frame one risky assumption per sprint.</p>
                        <p><span class="font-bold text-gray-900">2.</span> Run the cheapest test that can falsify it.</p>
                        <p><span class="font-bold text-gray-900">3.</span> Record learnings in a shared log.</p>
                        <p><span class="font-bold text-gray-900">4.</span> Escalate only when evidence conflicts with strategy.</p>
                    </div>
                </div>
                <div class="bg-gradient-to-br from-amber-50 to-white border border-amber-200 rounded-3xl p-8">
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">HR and Talent Agility</h3>
                    <p class="text-gray-700 mb-6">Build capacity for redistribution when environments shift.</p>
                    <div class="space-y-3 text-sm text-gray-700">
                        <p><span class="font-bold text-gray-900">1.</span> Map critical roles and backup coverage.</p>
                        <p><span class="font-bold text-gray-900">2.</span> Cross-train for surge skills quarterly.</p>
                        <p><span class="font-bold text-gray-900">3.</span> Hire for learning velocity, not only current stack.</p>
                        <p><span class="font-bold text-gray-900">4.</span> Pair with the <a class="text-emerald-700 underline" href="org-assessment.html">organization diagnostic</a>.</p>
                    </div>
                </div>
                <div class="bg-gradient-to-br from-purple-50 to-white border border-purple-200 rounded-3xl p-8">
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">Risk and Project Portfolio</h3>
                    <p class="text-gray-700 mb-6">Separate volatility shocks from true ambiguity experiments.</p>
                    <div class="space-y-3 text-sm text-gray-700">
                        <p><span class="font-bold text-gray-900">1.</span> Tag each initiative as V, U, C, or A dominant.</p>
                        <p><span class="font-bold text-gray-900">2.</span> Volatility: buffers and speed. Ambiguity: probes.</p>
                        <p><span class="font-bold text-gray-900">3.</span> Cap WIP; protect learning capacity.</p>
                        <p><span class="font-bold text-gray-900">4.</span> Use <a class="text-emerald-700 underline" href="templates.html">templates</a> for scorecards and scenario sheets.</p>
                    </div>
                </div>
            </div>
'''

# Localized short blocks
LOCS = {
    "": EN_BLOCK,
    "ja": EN_BLOCK.replace("Strategy under Uncertainty", "不確実性下の戦略")
    .replace("Replace single-point forecasts with decision-ready options.", "単一予測を、意思決定可能なオプションに置き換えます。")
    .replace("Product Discovery Loop", "プロダクト発見ループ")
    .replace("Reduce ambiguity with fast evidence, not bigger decks.", "大きな資料ではなく、速い証拠で曖昧性を減らします。")
    .replace("HR and Talent Agility", "人事と人材アジリティ")
    .replace("Build capacity for redistribution when environments shift.", "環境が変わったときに再配分できる能力を築きます。")
    .replace("Risk and Project Portfolio", "リスクとプロジェクトポートフォリオ")
    .replace("Separate volatility shocks from true ambiguity experiments.", "変動ショックと真の曖昧性実験を区別します。"),
    "de": EN_BLOCK.replace("Strategy under Uncertainty", "Strategie unter Unsicherheit")
    .replace("Replace single-point forecasts with decision-ready options.", "Ersetzen Sie Einzelprognosen durch entscheidungsreife Optionen.")
    .replace("Product Discovery Loop", "Product-Discovery-Schleife")
    .replace("Reduce ambiguity with fast evidence, not bigger decks.", "Reduzieren Sie Mehrdeutigkeit mit schnellen Belegen, nicht größeren Decks.")
    .replace("HR and Talent Agility", "HR- und Talent-Agilität")
    .replace("Build capacity for redistribution when environments shift.", "Bauen Sie Kapazität für Umverteilung bei Umweltwechseln auf.")
    .replace("Risk and Project Portfolio", "Risiko- und Projektportfolio")
    .replace("Separate volatility shocks from true ambiguity experiments.", "Trennen Sie Volatilitätsschocks von echten Mehrdeutigkeitsexperimenten."),
    "zh": EN_BLOCK.replace("Strategy under Uncertainty", "不确定环境下的战略")
    .replace("Replace single-point forecasts with decision-ready options.", "用可决策的选项替代单一预测点。")
    .replace("Product Discovery Loop", "产品探索闭环")
    .replace("Reduce ambiguity with fast evidence, not bigger decks.", "用快速证据降低模糊性，而不是更大的汇报材料。")
    .replace("HR and Talent Agility", "人力资源与人才敏捷")
    .replace("Build capacity for redistribution when environments shift.", "在环境变化时具备重新配置能力。")
    .replace("Risk and Project Portfolio", "风险与项目组合")
    .replace("Separate volatility shocks from true ambiguity experiments.", "区分易变性冲击与真正的模糊性实验。"),
}


def patch(path: Path, block: str) -> None:
    html = path.read_text(encoding="utf-8")
    if MARKER in html:
        # replace existing expanded block through next CTA-ish section
        html = re.sub(
            re.escape(MARKER) + r"[\s\S]*?(?=<div class=\"mt-16|<section class=\"py-20 bg-emerald|<section class=\"py-16 bg-emerald)",
            "",
            html,
            count=1,
        )
    # Insert before wrap-up / CTA patterns
    patterns = [
        r'(<div class="mt-8 bg-gradient-to-r from-emerald-50)',
        r'(<div class="mt-16[^"]*text-center">)',
        r'(<section class="py-20 bg-emerald-600)',
        r'(<section class="py-16 bg-emerald-600)',
        r'(<!-- CTA -->)',
        r'(<div class="bg-emerald-600 rounded-3xl)',
    ]
    inserted = False
    for pat in patterns:
        if re.search(pat, html):
            html = re.sub(pat, block + r"\n\1", html, count=1)
            inserted = True
            break
    if not inserted:
        html = html.replace("</main>", block + "\n</main>", 1) if "</main>" in html else html.replace("<footer", block + "\n<footer", 1)
    path.write_text(html, encoding="utf-8")
    print("expanded", path)


def main():
    for loc, block in LOCS.items():
        path = ROOT / loc / "action-guide.html" if loc else ROOT / "action-guide.html"
        if path.exists():
            patch(path, block)


if __name__ == "__main__":
    main()
