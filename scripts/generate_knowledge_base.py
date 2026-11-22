#!/usr/bin/env python3
"""Generate VUCA knowledge base pages (Phase 1+2) for vuca.cc."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo_kit import ALL_PAGES, LASTMOD, LOCALES, ROOT, page_file, wrap_page, write_sitemap

HBR = "https://hbr.org/2014/01/what-vuca-really-means-for-you"
WIKI = "https://en.wikipedia.org/wiki/VUCA"
CCL = "https://www.ccl.org/articles/leading-effectively-articles/what-is-vuca/"
CYNEFIN = "https://cynefin.io/"
BANI_WIKI = "https://en.wikipedia.org/wiki/BANI_(acronym)"
BANI_HBR = "https://hbr.org/2020/05/a-framework-for-shaping-a-post-pandemic-world"
TUNA_SRC = "https://www.oxford-review.com/blog/what-is-tuna-and-how-does-it-relate-to-vuca-and-bani/"
RUPT_SRC = "https://thedecisionlab.com/reference-guide/management/rupt-framework"

PAGES = [
    "what-is-vuca.html", "history.html", "vuca-prime.html", "vuca-vs-bani.html",
    "tuna.html", "rupt.html", "cynefin-and-vuca.html", "frameworks-comparison.html",
    "glossary.html", "volatility.html", "uncertainty.html", "complexity.html",
    "ambiguity.html", "faq.html", "bibliography.html", "about.html", "editorial.html",
    "templates.html", "org-assessment.html", "industry-healthcare.html",
    "industry-finance.html", "industry-supply-chain.html", "industry-tech.html",
    "industry-education.html", "case-netflix.html", "case-toyota.html",
]

LOCS = ("", "ja", "de", "zh")


def t(locale: str, en: str, ja: str, de: str, zh: str) -> str:
    return {"": en, "ja": ja, "de": de, "zh": zh}[locale]


def ext(url: str, label: str) -> str:
    return (
        f'<a href="{url}" rel="noopener noreferrer" target="_blank" '
        f'class="text-emerald-700 hover:underline">{label}</a>'
    )


def hero(locale: str, crumb_href: str, crumb: str, h1: str, lead: str) -> str:
    lu = t(locale, "Last updated", "最終更新", "Zuletzt aktualisiert", "最近更新")
    return f'''<section class="py-16 bg-gradient-to-br from-emerald-50 to-white">
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
    <p class="text-sm text-emerald-700 mb-3"><a href="{crumb_href}" class="hover:underline">{crumb}</a></p>
    <h1 class="text-4xl md:text-5xl font-bold text-gray-900 tracking-tight">{h1}</h1>
    <p class="text-lg text-gray-700 mt-4 leading-relaxed">{lead}</p>
    <p class="text-xs text-gray-500 mt-4">{lu}: {LASTMOD}</p>
  </div>
</section>'''


def wrap_body(*sections: str) -> str:
    inner = "\n".join(sections)
    return f'''<section class="py-12 bg-white">
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6 text-sm leading-relaxed text-gray-800">
{inner}
  </div>
</section>'''


def h2(text: str) -> str:
    return f'<h2 class="text-2xl font-bold text-gray-900 mt-8">{text}</h2>'


def p(text: str) -> str:
    return f'<p>{text}</p>'


def card(inner: str) -> str:
    return f'<div class="rounded-3xl border border-gray-200 p-6 bg-white">{inner}</div>'


def ul_items(items: list[str]) -> str:
    lis = "".join(f'<li class="ml-4 list-disc">{x}</li>' for x in items)
    return f'<ul class="space-y-2 my-4">{lis}</ul>'


def paras_html(paragraphs: list[str]) -> str:
    out = []
    for x in paragraphs:
        s = x.strip()
        if s.startswith("<p") or s.startswith("<div") or s.startswith("<h"):
            out.append(s)
        else:
            out.append(p(s))
    return "".join(out)


def industry_paras(slug: str, locale: str) -> list[str]:
    data = INDUSTRY_CONTENT[slug][locale]
    return [x.strip() for x in data.split("\n\n") if x.strip()]


def crumb_kb(locale: str) -> str:
    return t(locale, "Knowledge base", "ナレッジ", "Wissensbasis", "知识库")


def page_hero(locale: str, h1: str, lead: str, crumb_href: str = "glossary.html") -> str:
    return hero(locale, crumb_href, crumb_kb(locale), h1, lead)


def dim_page(locale: str, letter: str, slug: str, title: str, desc: str, body_paras: list[str]) -> tuple[str, str, str]:
    links = card(
        p(t(locale,
           f'Return to the <a href="glossary.html" class="text-emerald-700 hover:underline">glossary</a> or explore '
           f'<a href="framework.html" class="text-emerald-700 hover:underline">the VUCA framework</a>.',
           '「<a href="glossary.html" class="text-emerald-700 hover:underline">用語集</a>」に戻るか、'
           '「<a href="framework.html" class="text-emerald-700 hover:underline">VUCAフレームワーク</a>」を参照してください。',
           'Zurück zum <a href="glossary.html" class="text-emerald-700 hover:underline">Glossar</a> oder zum '
           '<a href="framework.html" class="text-emerald-700 hover:underline">VUCA-Framework</a>.',
           '返回<a href="glossary.html" class="text-emerald-700 hover:underline">术语表</a>，或阅读'
           '<a href="framework.html" class="text-emerald-700 hover:underline">VUCA 框架</a>。'))
    )
    main = page_hero(locale, title, desc, "glossary.html") + wrap_body(paras_html(body_paras), links)
    return title, desc, main

INDUSTRY_CONTENT = {
    "healthcare": {
        "": (
            "Healthcare organizations encounter VUCA daily across clinical operations, payer contracts, workforce planning, "
            "and public health policy. Volatility shows up in drug shortages, seasonal demand spikes, and reimbursement rule "
            "changes that land with little notice. Emergency departments feel this most acutely when census swings break "
            "staffing models built for average days rather than peak load.\n\n"
            "Uncertainty dominates strategic choices: will value-based care contracts expand, how will AI diagnostic tools "
            "be regulated, and which alliances will insurers prioritize? Leaders often plan capital projects on multi-year "
            "horizons while policy signals shift quarterly. That mismatch creates stranded investments and delayed "
            "modernization of electronic health records.\n\n"
            "Complexity arises from interdependent systems—clinical pathways, supply chain, billing, and compliance each "
            "optimize locally while patients experience care as one journey. A single sepsis protocol touches nursing "
            "documentation, pharmacy formularies, lab turnaround, and coding rules. Improving one node without mapping "
            "feedback loops frequently produces unintended harm elsewhere.\n\n"
            "Ambiguity is visible in guideline updates, cultural differences in informed consent, and emerging roles such "
            "as community health workers whose scope varies by state. Teams interpret the same compliance memo differently, "
            "leading to uneven patient experience and audit risk.\n\n"
            "Resilient health systems build shared situational awareness: daily huddles that track capacity, supply, and "
            "safety signals; interdisciplinary boards that review near-miss events; and investment guardrails that stage "
            "technology pilots before enterprise rollout.\n\n"
            "Scenario planning helps finance and clinical leaders align. A useful set includes sustained labor shortage, "
            "cyber incident disrupting EHR access, pandemic resurgence, and abrupt payer rate cuts. Each scenario should "
            "name decision owners, trigger indicators, and pre-authorized spending envelopes.\n\n"
            "Workforce agility matters as much as technology. Cross-training nurses across med-surg and observation units, "
            "credentialing telehealth providers across state lines, and maintaining float pools reduce volatility impact. "
            "Transparency about burnout metrics allows executives to trade productivity goals against retention.\n\n"
            "Data ethics and equity cannot be optional add-ons. When algorithms triage patients or predict no-shows, leaders "
            "must audit bias, document limitations, and keep clinicians in the loop for contested cases. Ambiguity in model "
            "outputs should map to human review paths rather than silent automation.\n\n"
            "Partnerships with public health agencies, academia, and community organizations extend sensing capacity. "
            "Integrated delivery networks that share anonymized utilization trends can spot emerging disease patterns "
            "earlier than any single hospital dashboard.\n\n"
            "Practical next steps: run a VUCA scan on your top three strategic initiatives, link each dimension to metrics "
            "you already report, and assign an executive sponsor to close gaps in uncertainty monitoring. Use the "
            "organizational diagnostic on this site to score readiness across departments."
        ),
        "ja": (
            "医療機関は診療運用、支払契約、人材計画、公衆衛生政策のあらゆる場面でVUCAに直面します。ボラティリティは、"
            "医薬品不足、季節需要の急増、突然の償還ルール変更として現れます。救急は平均日ベースの人員配置では吸収できない"
            "患者数変動に特に脆弱です。\n\n"
            "不確実性は戦略選択を支配します。バリューベース医療の拡大、AI診断規制、保険者の提携方針は読みにくく、"
            "数年単位の設備投資と四半期ごとの政策変更が噛み合わないと、投資の沈滞やEHR更新遅延を招きます。\n\n"
            "複雑性は相互依存システムから生じます。臨床パス、サプライチェーン、請求、コンプライアンスが局所最適すると、"
            "患者体験は分断されます。敗血症プロトコル一つが看護記録、薬局、検査、コーディングにまたがり、一点改善が"
            "他部門に副作用を及ぼすことがあります。\n\n"
            "曖昧さはガイドライン改訂、同意取得の文化的差異、地域保健師など役割定義のばらつきに表れます。同じコンプライ"
            "アンス文書でも解釈が分かれ、患者体験と監査リスクが不均一になります。\n\n"
            "強靭な医療システムは共通状況認況認識を築きます。キャパシティと安全指標の日次ハドル、ヒヤリハットの学際レビュー、"
            "本番前の段階的技術パイロットなどが有効です。\n\n"
            "シナリオ計画は財務と臨床の合意形成に役立ちます。慢性的人手不足、EHR停止サイバー事案、パンデミック再燃、"
            "急な支払率引下げなど、意思決定者・トリガー指標・事前承認予算を各シナリオに明記します。\n\n"
            "人材の機敏性は技術と同等に重要です。病棟間クロストレーニング、テレヘルスの多州資格、フロートプールは"
            "ボラティリティの衝撃を和らげます。燃え尽き指標の可視化は生産性と定着のトレードオフを経営判断に載せます。\n\n"
            "データ倫理と公正は後付けできません。トリアージやノーショー予測アルゴリズムにはバイアス監査、限界の明示、"
            "争点案件の人間レビューが必要です。\n\n"
            "公衆衛生、大学、地域団体との連携はセンシング能力を高めます。匿名化利用トレンドの共有は単独病院より"
            "早く異常パターンを検知できます。\n\n"
            "次の一手：主要戦略3件にVUCAスキャンを実施し、既存KPIに各次元を結びつけ、不確実性モニタリングの"
            "ギャップにエグゼクティブスポンサーを置いてください。本サイトの組織診断で部門横断の準備度を点検できます。"
        ),
        "de": (
            "Gesundheitsorganisationen erleben VUCA täglich in Klinikbetrieb, Vergütungsverträgen, Personalplanung und "
            "Gesundheitspolitik. Volatilität zeigt sich in Arzneimittelengpässen, saisonalen Nachfragespitzen und kurzfristigen "
            "Erstattungsänderungen. Notaufnahmen spüren dies, wenn Belegungsschwankungen Personalmodelle für Durchschnittstage "
            "sprengen.\n\n"
            "Unsicherheit prägt Strategieentscheidungen: Ausbau von Value-based Care, KI-Regulierung, Prioritäten der "
            "Kostenträger. Mehrjährige Investitionen kollidieren mit vierteljährlich wechselnden politischen Signalen – "
            "das führt zu gestrandeten Projekten und verzögerten EHR-Modernisierungen.\n\n"
            "Komplexität entsteht durch vernetzte Teilsysteme – klinische Pfade, Supply Chain, Abrechnung und Compliance "
            "optimieren lokal, während Patienten eine durchgängige Journey erleben. Ein Sepsis-Protokoll berührt Pflege, "
            "Apotheke, Labor und Kodierung; punktuelle Verbesserungen erzeugen oft Nebenwirkungen.\n\n"
            "Mehrdeutigkeit zeigt sich in Leitlinienupdates, kulturellen Unterschieden bei Aufklärung und variierenden "
            "Rollen wie Community Health Workers. Gleiche Compliance-Memos werden unterschiedlich gelesen – mit "
            "ungleichmäßiger Patientenerfahrung und Audit-Risiko.\n\n"
            "Resiliente Systeme bauen gemeinsame Lagebilder: tägliche Huddles zu Kapazität und Sicherheit, "
            "interdisziplinäre Near-Miss-Reviews und gestufte Technologiepiloten vor Rollouts.\n\n"
            "Szenarioplanung aligniert Klinik und Finanzen: anhaltender Fachkräftemangel, Cyberangriff auf EHR, "
            "Pandemiewelle, abrupte Tarifkürzungen. Jedes Szenario braucht Entscheider, Trigger und vorab freigegebene Budgets.\n\n"
            "Workforce-Agilität zählt wie Technologie: Cross-Training, Telehealth-Lizenzen über Bundesländer, Float-Pools "
            "dämpfen Volatilität. Sichtbare Burnout-Kennzahlen ermöglichen ehrliche Produktivitäts-Retention-Trade-offs.\n\n"
            "Datenethik und Gerechtigkeit sind Pflicht. Algorithmen für Triage oder No-Show-Prognosen brauchen Bias-Audits, "
            "Dokumentation von Grenzen und Human-in-the-loop bei strittigen Fällen.\n\n"
            "Partnerschaften mit Öffentlichem Gesundheitsdienst, Hochschulen und Communities erweitern Frühwarnung. "
            "Geteilte anonymisierte Auslastungstrends erkennen Muster früher als einzelne Klinik-Dashboards.\n\n"
            "Praxis: VUCA-Scan für die drei wichtigsten Strategien, Dimensionen an vorhandene KPIs koppeln, Sponsor für "
            "Uncertainty-Monitoring benennen. Nutzen Sie die Organisationsdiagnose auf dieser Website."
        ),
        "zh": (
            "医疗机构在临床运营、支付合同、人力规划和公共卫生政策中每天都在面对 VUCA。易变性体现在药品短缺、季节性需求"
            "高峰以及报销规则突然调整。急诊往往首当其冲，收治波动会击穿按“平均日”编制的人力模型。\n\n"
            "不确定性主导战略选择：价值医疗会否扩大、AI 诊断如何监管、保险公司优先哪些联盟？领导者常以多年资本规划对"
            "抗按季度变化的政策信号，容易造成投资沉淀与电子病历现代化停滞。\n\n"
            "复杂性来自相互依赖的子系统——临床路径、供应链、计费与合规各自局部最优，而患者体验是一条旅程。单一脓毒症"
            "流程会牵动护理文书、药房目录、检验周转与编码规则；未映射反馈回路的一域改进，常在另一域产生伤害。\n\n"
            "模糊性见于指南更新、知情同意文化差异，以及社区健康工作者等角色边界因地区而异。同一合规通知可被不同解读，"
            "导致体验不均与审计风险。\n\n"
            "有韧性的体系会建立共享态势感知：追踪容量与安全的日例会、跨学科复盘险情事件，以及在全面上线前分阶段试点"
            "新技术。\n\n"
            "情景规划帮助财务与临床对齐。可建设性短缺、电子病历遭网络安全攻击、疫情复燃、支付费率骤降等情景，并标明"
            "决策人、触发指标与预授权支出包。\n\n"
            "人力敏捷与技术同等重要：科室交叉培训、跨州远程医疗资质、机动班组可缓释易变性；公开倦怠指标有助于在生产力"
            "与留任之间做坦诚权衡。\n\n"
            "数据伦理与公平不能事后补丁。分诊或爽约预测算法需要偏见审计、局限披露，以及对争议病例保留人工复核路径。\n\n"
            "与公共卫生部门、高校及社区组织合作可强化感知能力。共享匿名利用趋势比单一医院仪表盘更早发现异常模式。\n\n"
            "行动建议：对三项核心战略做 VUCA 扫描，将四维映射到现有指标，并指定高管牵头弥合不确定性监测缺口。可使用本站"
            "组织诊断工具评估跨部门准备度。"
        ),
    },
"finance": {
        "": (
            "Financial institutions live inside VUCA: rates and spreads move with volatility, regulatory agendas create "
            "uncertainty, balance-sheet linkages amplify complexity, and reputational narratives stay ambiguous long after "
            "numbers are published. Retail banks feel volatility when deposit betas reprice overnight; asset managers see it "
            "when liquidity windows narrow in stressed markets.\n\n"
            "Uncertainty dominates strategic planning cycles. Supervisors hint at capital buffer changes, climate stress "
            "tests evolve, and digital-asset rules remain draft forms in multiple jurisdictions. Treasurers model interest "
            "paths while political shocks reorder priorities mid-quarter.\n\n"
            "Complexity is structural: a mortgage product touches sales conduct, funding desks, risk-weight models, "
            "servicing partners, and investor reporting. Optimizing approval speed without coordinating fraud controls can "
            "inflate losses that appear quarters later.\n\n"
            "Ambiguity shows up in customer trust. Identical APR disclosures are read differently across demographics; ESG "
            "labels carry multiple definitions. Compliance and marketing may use the same words with divergent intent.\n\n"
            "Resilient banks invest in unified risk telemetry—linking trading, liquidity, and operational incidents on one "
            "timeline. Scenario drills include cyber outages, sudden deposit flight, and correlated market gaps.\n\n"
            "Capital and liquidity buffers are volatility absorbers, but they must be governance-owned, not spreadsheet "
            "fetishes. Boards should see trigger thresholds tied to named decision rights.\n\n"
            "Uncertainty tools include staged product launches, sandbox partnerships with fintechs, and real-options pricing "
            "for technology bets. Document kill criteria before funding.\n\n"
            "Complexity practice means architecture reviews for every new API channel, with explicit data lineage into "
            "anti-money-laundering and conduct surveillance.\n\n"
            "Ambiguity practice means plain-language testing of customer letters and chair-level alignment on crisis "
            "narratives before markets open.\n\n"
            "Cross-industry contagion is a supply-chain problem for finance: when logistics firms fail, trade finance "
            "exposure spikes. Maintain counterparty maps beyond tier-one names.\n\n"
            "Practical next steps: run a four-dimension scan on your top three revenue initiatives, attach existing KPIs, "
            "and publish a quarterly lessons log for failed forecasts—this builds institutional understanding under "
            "uncertainty better than another static plan.\n\n"
            "Treasury and risk committees should rehearse communication when volatility breaches intraday limits—who may halt "
            "trading, who briefs regulators, and how retail branches receive approved scripts. Pair these drills with "
            "post-trade analytics that tag which assumptions failed, so complexity in correlated books becomes visible rather "
            "than hidden in siloed dashboards.\n\n"
            "Wealth and insurance arms share brand ambiguity with retail—synchronized crisis language across channels matters "
            "when social media spreads partial screenshots of internal memos."
        ),
        "ja": (
            "金融機関は金利・スプレッドの変動、規制不確実性、貸借対照表連鎖の複雑性、評判ナラティブの曖昧さの中で稼働します。"
            "変動性は預金ベータの急変や市場ストレス時の流動性窓の狭まりとして現れます。\n\n"
            "不確実性は資本バッファー、気候ストレステスト、デジタル資産規制の草案など、戦略計画を支配します。\n\n"
            "複雑性は住宅ローンが営業・資金・RWA・サービサー・投資家報告にまたがることで構造的に増幅されます。\n\n"
            "曖昧性はAPR開示やESGラベルの解釈差として顧客信頼に影響します。\n\n"
            "強靭な銀行は取引・流動性・オペリスクを一本タイムラインで可視化し、サイバー・預金フライト・相関ギャップの演習を行います。\n\n"
            "バッファーはガバナンス所有であり、閾値と決裁権をセットで設計します。\n\n"
            "不確実性には段階的ローンチ、フィンテック連携、技術投資の撤退基準が有効です。\n\n"
            "複雑性にはAPIチャネルごとのアーキテクチャ審査とAML・コンダクトへのデータ系譜が必要です。\n\n"
            "曖昧性には平易文言テストと危機ナラティブの事前統一が有効です。\n\n"
            "物流破綻は貿易金融リスクを増幅するため、取引先マップを階層2以降まで拡張します。\n\n"
            "次の一手：主要収益施策3件にVUCAスキャンを行い、既存KPIを紐づけ、失敗予測の四半期学習ログを公開してください。"
        ),
        "de": (
            "Finanzinstitute operieren in VUCA: Zinsvolatilität, regulatorische Unsicherheit, bilanzieller Komplexitätsdruck "
            "und mehrdeutige Reputationsnarrative. Volatilität zeigt sich in Deposit-Betas und enger Liquidität unter Stress.\n\n"
            "Unsicherheit prägt Kapitalpuffer, Klimaszenarien und Krypto-Regulierung in Entwurfsform.\n\n"
            "Komplexität verbindet Vertrieb, Treasury, Risikogewichte, Servicer und Reporting eines Produkts.\n\n"
            "Mehrdeutigkeit betrifft APR-Transparenz und ESG-Definitionen.\n\n"
            "Resiliente Banken verknüpfen Handel, Liquidität und OpRisk telemetrisch und üben Cyber-, Deposit-Run- und Korrelationsszenarien.\n\n"
            "Puffer brauchen klare Trigger und Entscheidungsrechte.\n\n"
            "Bei Unsicherheit: gestufte Launches, Fintech-Sandboxes, dokumentierte Kill-Kriterien.\n\n"
            "Bei Komplexität: Architektur-Reviews je API mit Datenherkunft in AML/Conduct.\n\n"
            "Bei Mehrdeutigkeit: Klartexttests und vorab abgestimmte Krisenkommunikation.\n\n"
            "Lieferkettenausfälle treffen Trade Finance – Gegenpartei-Karten über Tier 1 hinaus.\n\n"
            "Praxis: VUCA-Scan der Top-3-Umsatzinitiativen, KPI-Anbindung, Quartals-Lernlog für Fehlprognosen."
        ),
        "zh": (
            "金融机构置身 VUCA：利率波动、监管不确定、资产负债联动复杂、声誉叙事长期模糊。易变性体现为存款定价重定锚、压力市况下流动性窗口变窄。\n\n"
            "不确定性主导战略规划：资本缓冲、气候压力测试、数字资产规则仍在草案阶段。\n\n"
            "结构性复杂性使房贷同时牵动销售、资金、风险权重、服务商与投资者披露。\n\n"
            "模糊性影响客户信任：相同 APR 披露在不同人群中的理解不同，ESG 标签定义各异。\n\n"
            "有韧性的机构统一风险遥测，将交易、流动性与操作风险置于同一时间线，并演练网络、存款外流与相关性缺口。\n\n"
            "资本与流动性缓冲需治理主体明确触发阈值与决策权。\n\n"
            "面对不确定性可采用分阶段上线、金融科技沙盒及技术投资的终止标准。\n\n"
            "面对复杂性应为每个 API 渠道做架构审查，并标明流入反洗钱与行为监管的数据血缘。\n\n"
            "面对模糊性应做通俗语言测试，并在开市前统一危机对外口径。\n\n"
            "物流失败会抬升贸易融资敞口，应将交易对手图谱扩展至一级以外。\n\n"
            "行动建议：对三大营收举措做四维扫描、映射现有 KPI，并发布季度预测失误学习日志。"
        ),
    },
    "supply-chain": {
        "": (
            "Global supply chains concentrate VUCA: freight rates spike, port labor actions stall flows, tier-two suppliers "
            "fail quietly, and sustainability rules reinterpret sourcing overnight. Volatility is visible in spot container "
            "pricing and air-freight surcharges that erase quarterly margin guidance.\n\n"
            "Uncertainty sits in demand forecasts when retail partners share less data, in sanctions lists that update "
            "weekly, and in nearshoring decisions with multi-year paybacks.\n\n"
            "Complexity is the mesh of bills of material, dual sourcing rules, quality holds, and finance programs that "
            "incentivize opposite behaviors. A cost-down project in metals can raise defect rates in assembly three nodes away.\n\n"
            "Ambiguity emerges when ESG scores, force-majeure clauses, and customer comms about delays use inconsistent "
            "definitions. Operations and legal may believe they aligned while customers hear mixed messages.\n\n"
            "Leaders build control towers that fuse inventory, inbound logistics, and supplier health—not only ERP snapshots. "
            "Leading indicators include supplier payment stress and social sentiment in factory regions.\n\n"
            "Dual sourcing is a volatility hedge when designed with interchangeable specs; otherwise it doubles complexity "
            "without resilience.\n\n"
            "Scenario planning should cover canal closures, semiconductor allocation shocks, and sudden customs policy shifts.\n\n"
            "Network design reviews every six months beat annual strategies when volatility is high.\n\n"
            "Cross-functional war rooms need finance present so expedite decisions understand margin impact in real time.\n\n"
            "Digitization helps, but data ambiguity remains: duplicate part numbers and partial BOMs distort analytics until "
            "master data stewards enforce standards.\n\n"
            "Start with a VUCA heatmap by region and commodity, tie to service-level metrics, and assign owners for "
            "uncertainty monitoring on sanctions and weather models.\n\n"
            "Supplier development funds are ambiguity reducers when specifications are co-authored with engineering and "
            "quality—shared test fixtures beat email debates about tolerance. After disruptions, run blameless retrospectives "
            "that separate volatility (price spikes) from complexity (routing changes) so the next playbook targets the right "
            "root cause.\n\n"
            "Logistics leaders increasingly model climate volatility as a first-class scenario, not a footnote: heat-related "
            "rail slowdowns, storm reroutes, and water-level constraints on inland waterways appear in quarterly operating "
            "reviews alongside traditional demand variance.\n\n"
            "Inventory positioning is a complexity lever: pushing stock closer to customers absorbs volatility but raises "
            "obsolescence risk; centralized hubs simplify planning but lengthen lead times. Finance and operations should "
            "model total landed cost under at least two volatility regimes quarterly.\n\n"
            "Procurement ethics and forced-labor diligence introduce ambiguity when documentation standards differ by country; "
            "central audit playbooks with locale-specific annexes keep compliance and operations aligned."
        ),
        "ja": (
            "グローバル・サプライチェーンは運賃急変、港湾スト、二次サプライヤー陰性破綻、サステナ規制の急転でVUCAが集中します。\n\n"
            "不確実性は需要予測の低下、週次更新の制裁リスト、ニアショア投資の回収年数にあります。\n\n"
            "複雑性はBOM、デュアルソーシング、品質保留、金融条件の逆行が絡み合う網です。\n\n"
            "曖昧性はESGスコア、不可抗力、遅延説明の定義ズレとして表れます。\n\n"
            "コントロールタワーは在庫・入庫・サプライヤー健全性を融合します。\n\n"
            "デュアルソーシングは互換仕様でなければ複雑性だけが増えます。\n\n"
            "運河閉鎖、半導体配分、関税急変のシナリオを用意します。\n\n"
            "高変動下は年次より半年ごとのネットワーク見直しが有効です。\n\n"
            "財務参加のウォールルームで特急コストと粗利を同時に見ます。\n\n"
            "マスターデータを整備しないと分析は曖昧なままです。\n\n"
            "地域・品目のVUCAヒートマップをSLAに結び、制裁・気象のモニタリング担当を置いてください。"
        ),
        "de": (
            "Globale Lieferketten bündeln VUCA: Frachtspitzen, Hafenstreiks, Ausfälle bei Tier-2-Lieferanten, ESG-Regeln.\n\n"
            "Unsicherheit in Nachfrageprognosen, Sanktionslisten, Nearshoring mit langen Paybacks.\n\n"
            "Komplexität aus Stücklisten, Dual Sourcing, Quality Holds und widersprüchlichen Finanzanreizen.\n\n"
            "Mehrdeutigkeit bei ESG, Force Majeure und Kundenkommunikation.\n\n"
            "Control Towers verbinden Bestand, Inbound und Lieferantengesundheit.\n\n"
            "Dual Sourcing nur mit austauschbaren Specs als Volatilitätspuffer.\n\n"
            "Szenarien: Kanalsperrungen, Halbleiterzuteilung, Zollschocks.\n\n"
            "Netzwerk-Reviews halbjährlich statt nur jährlich.\n\n"
            "War Rooms mit Finance für Eilentscheidungen.\n\n"
            "Master Data Stewards gegen analytische Mehrdeutigkeit.\n\n"
            "VUCA-Heatmap je Region/Commodity, SLA-Kopplung, Owner für Sanktions-/Wettermonitoring."
        ),
        "zh": (
            "全球供应链集中体现 VUCA：运价飙升、港口劳资、二级供应商隐性失败、可持续规则突变。\n\n"
            "不确定性在削弱的需求预测、每周更新的制裁清单、回流投资的回收期。\n\n"
            "复杂性来自物料清单、双源规则、质量冻结与财务激励的拉扯。\n\n"
            "模糊性体现于 ESG 评分、不可抗力与客户延期沟通的语义不一。\n\n"
            "控制塔应融合库存、入库物流与供应商健康度。\n\n"
            "双源只有在可互换规格下才是易变性对冲，否则只增复杂性。\n\n"
            "情景应覆盖运河中断、芯片配给、关税突变。\n\n"
            "高波动环境下每半年做一次网络设计审视。\n\n"
            "跨职能作战室应有财务在场以实时理解加急对毛利的影响。\n\n"
            "主数据不治理，分析就仍模糊。\n\n"
            "按区域与品类绘制 VUCA 热图，绑定服务水平指标，并指定制裁与气象监测负责人。"
        ),
    },
    "tech": {
        "": (
            "Technology companies amplify VUCA because product half-lives shrink, platform rules shift, and security threats "
            "redraw roadmaps quarterly. Volatility appears in cloud spend swings, talent market spikes, and model release cycles "
            "that reset competitive positioning overnight.\n\n"
            "Uncertainty sits in AI regulation, open-source license debates, and enterprise buyers delaying commitments until "
            "budget clarity returns.\n\n"
            "Complexity spans microservices, data pipelines, entitlement systems, and support tiers—each with separate on-call "
            "rotations. A pricing change can ripple through billing, sales compensation, and customer success playbooks.\n\n"
            "Ambiguity is common in positioning: every vendor claims AI leadership; customers interpret safety and privacy "
            "promises differently across regions.\n\n"
            "Strong engineering orgs pair volatility buffers (feature flags, gradual rollouts) with error budgets that make "
            "trade-offs explicit.\n\n"
            "Discovery tracks under uncertainty should have capped durations and pre-registered success metrics.\n\n"
            "Architecture decision records reduce complexity debt by documenting why boundaries exist.\n\n"
            "Inclusive design reviews lower ambiguity in UX copy and consent flows.\n\n"
            "Platform reliability is a board topic when volatility in usage threatens SLAs tied to revenue.\n\n"
            "Third-party risk programs must include AI subprocessors and data residency chains, not only classic SaaS vendors.\n\n"
            "Run a quarterly VUCA review on your platform strategy, linking each dimension to SRE, product discovery, and "
            "communications metrics you already collect.\n\n"
            "Boards should see security and reliability as volatility problems, not separate checklists: incident frequency, "
            "patch latency, and customer-visible downtime belong on the same slide as revenue guidance. Talent volatility "
            "requires succession plans for principal engineers and explicit knowledge transfer before reorganizations, "
            "otherwise complexity debt reappears under new team names.\n\n"
            "Commercial leaders should align pricing experiments with volatility triggers—when cloud costs or model-training "
            "spend moves more than a band in a month, automatic review gates pause broad discounting until finance and product "
            "jointly sign off, preventing ambiguity about margin guardrails.\n\n"
            "Open-source program offices reduce legal ambiguity by maintaining a single approved license matrix and automated "
            "scanning on every merge request, so security and legal speak from the same artifact during incidents.\n\n"
            "Customer trust metrics—support backlog, escalation rate, and public issue threads—should appear beside "
            "deployment frequency so ambiguity in outward messaging is caught before it becomes a volatility event in churn.\n\n"
            "Multi-cloud commitments are uncertainty bets—document exit costs, portability tests, and data gravity assumptions "
            "before signing multi-year spends so complexity in billing does not surprise finance during the next renewal window."
        ),
        "ja": (
            "テック企業はプロダクト寿命の短縮、プラットフォームルール変化、セキュリティ脅威でVUCAを増幅します。クラウド費用、"
            "人材市場、モデル公開が競争を一夜で塗り替えます。\n\n"
            "不確実性はAI規制、OSSライセンス、エンタープライズ予算先送りにあります。\n\n"
            "マイクロサービス、データパイプライン、Entitlement、サポート階層が複雑性を生みます。\n\n"
            "ポジショニングの曖昧さは「AIリーダー」乱立と地域ごとの安全・プライバシー解釈差です。\n\n"
            "Feature flagと段階ロールアウト、エラーバジェットが変動性バッファになります。\n\n"
            "探索は期限と成功指標を事前登録します。\n\n"
            "ADRが境界理由を残し複雑性負債を抑えます。\n\n"
            "包含的レビューがUX文言と同意フローの曖昧さを減らします。\n\n"
            "利用変動が収益SLAを脅かすとき信頼性は取締役会議題です。\n\n"
            "第三者リスクにAIサブプロセッサとデータ所在地を含めます。\n\n"
            "四半期VUCAレビューでSRE・発見・広報指標に各次元を結び付けてください。"
        ),
        "de": (
            "Tech-Unternehmen verstärken VUCA durch kurze Produktlebenszyklen, Plattformregeln und Security-Schocks.\n\n"
            "Unsicherheit durch KI-Regulierung, OSS-Lizenzen und verschobene Enterprise-Budgets.\n\n"
            "Komplexität aus Microservices, Datenpipelines, Entitlements und Support-Tiers.\n\n"
            "Mehrdeutigkeit in AI-Positionierung und regional unterschiedlicher Privacy-Deutung.\n\n"
            "Feature Flags, Rollouts und Error Budgets puffern Volatilität.\n\n"
            "Discovery-Tracks mit Cap und vorregistrierten Metriken.\n\n"
            "ADRs dokumentieren Grenzen gegen Komplexitätsschulden.\n\n"
            "Inklusive Reviews für UX und Consent.\n\n"
            "Reliabilität wird Board-Thema bei SLA-Risiko.\n\n"
            "Third-Party-Risk inkl. KI-Subprozessoren und Datenresidenz.\n\n"
            "Quartals-VUCA-Review mit SRE-, Discovery- und Comms-KPIs."
        ),
        "zh": (
            "科技公司因产品半衰期缩短、平台规则变化与安全威胁而放大 VUCA。\n\n"
            "不确定性来自 AI 监管、开源许可争议与企业采购推迟。\n\n"
            "微服务、数据管道、授权与支持层级构成复杂性。\n\n"
            "定位模糊表现为人人都称 AI 领先，各地对安全与隐私承诺理解不同。\n\n"
            "特性开关、灰度发布与错误预算缓冲易变性。\n\n"
            "探索轨道应设上限与预设成功指标。\n\n"
            "架构决策记录降低复杂性债务。\n\n"
            "包容性设计评审减少 UX 与同意的模糊性。\n\n"
            "用量波动威胁收入 SLA 时，可靠性上升为董事会议题。\n\n"
            "第三方风险应纳入 AI 子处理者与数据驻留链。\n\n"
            "每季度对平台战略做 VUCA 审视并绑定 SRE、发现与传播指标。"
        ),
    },
    "education": {
        "": (
            "Education systems face VUCA from demographic shifts, funding rules, technology adoption, and public debate about "
            "curriculum values. Volatility appears in enrollment swings, substitute-teacher availability, and sudden policy "
            "changes on assessments or accreditation.\n\n"
            "Uncertainty affects long capital plans: will hybrid delivery persist, how will employers credential skills, and "
            "which grants survive budget cycles?\n\n"
            "Complexity arises when academic departments, student services, IT, and facilities each optimize locally while "
            "students experience one journey. A learning-management rollout touches pedagogy, accessibility, privacy, and "
            "help-desk load simultaneously.\n\n"
            "Ambiguity surrounds terms like rigor, equity, and competency—stakeholders agree on goals but not definitions.\n\n"
            "Resilient institutions publish transparent enrollment scenarios and tie austerity triggers to protect "
            "instructional quality before amenities.\n\n"
            "Cross-disciplinary curriculum committees map dependencies so gen-ed changes do not break major pathways.\n\n"
            "Digital equity programs need complexity-aware implementation: device logistics, bandwidth, and support hours "
            "must move together.\n\n"
            "Communications playbooks reduce ambiguity during strikes, weather closures, or public controversies.\n\n"
            "Partnerships with employers should include uncertainty clauses on enrollment commitments and shared data use.\n\n"
            "Use the organizational diagnostic and scenario templates on this site to score readiness across academic and "
            "administrative units quarterly.\n\n"
            "Accreditation cycles are uncertainty milestones—begin evidence collection early and tag artifacts to VUCA "
            "dimensions so reviewers see systematic preparation. Faculty shared governance reduces ambiguity when union "
            "contracts, state mandates, and donor expectations overlap; publish decision principles before crises so "
            "interim leaders do not invent policy under pressure.\n\n"
            "Student success analytics can amplify ambiguity when labels like at-risk mean different things to advisors, "
            "registrars, and financial aid. Publish operational definitions and audit models each term. Community colleges and "
            "research universities face different volatility profiles—customize VUCA playbooks rather than importing templates "
            "from unlike institutions.\n\n"
            "Workforce volatility in adjunct hiring cycles deserves explicit volatility metrics—fill rates, class cancellation "
            "counts, and student credit-hour throughput—so leaders see instructional impact before end-of-term surveys arrive.\n\n"
            "Alumni and foundation relations add complexity to crisis communications; pre-negotiated holding statements for "
            "controversial speakers or research findings reduce ad-hoc ambiguity when news cycles compress decision windows.\n\n"
            "International student flows remain a volatility driver; visa policy uncertainty should feed enrollment scenarios "
            "and housing plans so auxiliary services do not overbuild during ambiguous policy windows.\n\n"
            "Capital planning committees benefit from linking deferred-maintenance backlogs to complexity maps of building "
            "systems—HVAC, IT cabling, and accessibility refits often share vendors and should be sequenced under a single "
            "volatility-informed portfolio."
        ),
        "ja": (
            "教育は人口動態、財政ルール、技術採用、カリキュラム価値の議論でVUCAに直面します。変動性は入学数、代替教員、"
            "評価・認証政策の急変です。\n\n"
            "不確実性はハイブリッド継続、技能認定、助成金存続に影響します。\n\n"
            "学務・学生支援・IT・施設が局所最適すると学生体験が分断され複雑性が増します。\n\n"
            "厳密さ・公正・コンピテンシーなど言葉の曖昧さが残ります。\n\n"
            "透明な入学シナリオと質の保護トリガーが強靭性を支えます。\n\n"
            "カリキュラム委員会が依存をマップし専攻パスを守ります。\n\n"
            "デジタルエクイティは端末・帯域・サポートを一体で設計します。\n\n"
            "争議・休校・論争時の広報手順が曖昧さを減らします。\n\n"
            "企業連携は入学コミットとデータ利用の不確実性条項を含めます。\n\n"
            "本サイトの診断とテンプレで学務・事務の準備度を四半期評価してください。"
        ),
        "de": (
            "Bildung erlebt VUCA durch Demografie, Finanzierung, Technologie und Curriculum-Debatten.\n\n"
            "Unsicherheit bei Hybridmodellen, Zertifizierungen und Zuschüssen.\n\n"
            "Komplexität zwischen Fakultäten, Services, IT und Facilities.\n\n"
            "Mehrdeutigkeit bei Begriffen wie Rigor, Equity, Kompetenz.\n\n"
            "Szenarien für Einschreibung und Qualitätsschutz.\n\n"
            "Curriculum-Gremien mappen Abhängigkeiten.\n\n"
            "Digital Equity nur als Gesamtpaket.\n\n"
            "Kommunikations-Playbooks in Krisen.\n\n"
            "Arbeitgeberpartnerschaften mit Unsicherheitsklauseln.\n\n"
            "Quartals-Diagnose mit Vorlagen dieser Website."
        ),
        "zh": (
            "教育系统因人口结构、经费规则、技术采纳与课程价值争论而面对 VUCA。易变性体现为招生波动、代课供给与评估认证政策突变。\n\n"
            "不确定性影响长期资本规划：混合式会否延续、雇主如何认证技能、拨款能否跨预算周期。\n\n"
            "教务、学生服务、IT 与后勤各自局部最优，学生却经历一条旅程，形成复杂性。\n\n"
            "严谨、公平、能力等词汇的模糊性使利益相关者在定义上难一致。\n\n"
            "有韧性的院校公开招生情景，并以触发机制优先保护教学质量。\n\n"
            "跨学科课程委员会应绘制依赖，避免通识改动破坏专业路径。\n\n"
            "数字公平需设备、带宽与支持时段同步设计。\n\n"
            "罢工、停课与舆论危机的传播手册可降低模糊性。\n\n"
            "校企合作应包含招生承诺与数据使用的不确定性条款。\n\n"
            "请用本站诊断与模板每季度评估教学与行政单元的准备度。"
        ),
    },
}

# Data for generate_knowledge_base.py (merged at build)

DIM_META = {
    "volatility": {
        "title": lambda locale: t(locale, "Volatility", "変動性", "Volatilität", "易变性"),
        "desc": lambda locale: t(
            locale,
            "Rapid, large swings in conditions and metrics.",
            "条件・指標の急速かつ大きな変動。",
            "Schnelle, starke Schwankungen von Rahmenbedingungen.",
            "条件与指标的快速大幅波动。",
        ),
    },
    "uncertainty": {
        "title": lambda locale: t(locale, "Uncertainty", "不確実性", "Unsicherheit", "不确定性"),
        "desc": lambda locale: t(
            locale,
            "When credible probabilities are unavailable.",
            "信頼できる確率が得られない状態。",
            "Wenn verlässliche Wahrscheinlichkeiten fehlen.",
            "缺乏可信概率估计的状态。",
        ),
    },
    "complexity": {
        "title": lambda locale: t(locale, "Complexity", "複雑性", "Komplexität", "复杂性"),
        "desc": lambda locale: t(
            locale,
            "Many interacting parts with nonlinear effects.",
            "非線形効果を生む多数の相互作用。",
            "Viele Wechselwirkungen mit nichtlinearen Effekten.",
            "大量相互作用并产生非线性效应。",
        ),
    },
    "ambiguity": {
        "title": lambda locale: t(locale, "Ambiguity", "曖昧性", "Mehrdeutigkeit", "模糊性"),
        "desc": lambda locale: t(
            locale,
            "Signals allow multiple valid readings.",
            "複数の妥当な読み取りが可能なシグナル。",
            "Signale mit mehreren gültigen Deutungen.",
            "信号存在多种有效解读。",
        ),
    },
}

DIM_PARAS = {
    "volatility": {
        "": [
            "Volatility describes how quickly and how far key variables move. Markets, input costs, talent availability, "
            "and cyber risk can all spike within a quarter. Volatility is not inherently negative—it can create opportunity "
            "for prepared organizations—but it punishes rigid plans.",
            "Leaders respond with slack resources, diversified suppliers, and monitoring cadences matched to decision "
            "cycles. Financial buffers, modular product architectures, and cross-trained teams reduce recovery time "
            "after shocks.",
            "Distinguish volatility from mere seasonality: volatile regimes show unpredictable amplitude. Dashboards "
            "should track rate-of-change, not only level.",
        ],
        "ja": [
            "変動性は重要変数がどれだけ速く・大きく動くかを示します。市場、コスト、人材、サイバーリスクは四半期単位で急変し得ます。",
            "余力、供給多元化、監視頻度の調整が対応策です。財務バッファとクロストレーニングが回復時間を短縮します。",
            "季節性との違いは振幅の予測困難さです。水準だけでなく変化率を追跡してください。",
        ],
        "de": [
            "Volatilität beschreibt Geschwindigkeit und Ausmaß von Veränderungen zentraler Variablen.",
            "Antworten: Puffer, Lieferantendiversifikation, passende Überwachungsfrequenz.",
            "Unterscheide Volatilität von Saisonalität; tracke Änderungsraten.",
        ],
        "zh": [
            "易变性描述关键变量变化的速度与幅度，市场、成本、人才与网络风险都可能在短期内飙升。",
            "领导者以冗余资源、供应多元化和匹配决策周期的监测节奏应对。",
            "易变不同于单纯季节性，应追踪变化率而非仅看水平。",
        ],
    },
    "uncertainty": {
        "": [
            "Uncertainty appears when the range of outcomes is wide and probabilities are disputed. Regulatory drafts, "
            "geopolitical shifts, and emerging technologies often land here.",
            "Discovery-driven planning, real options, and staged investments reduce commitment risk. Maintain a decision "
            "log that records assumptions so teams can revisit them when facts change.",
            "Pair quantitative models with qualitative scenarios. When models disagree, document the disagreement instead "
            "of forcing consensus.",
        ],
        "ja": [
            "不確実性は結果の幅が広く確率が争点になる状態です。",
            "探索型計画、実物オプション、段階投資が有効です。",
            "モデル不一致は合意を急がず記録します。",
        ],
        "de": [
            "Unsicherheit: breite Ergebnisspanne, umstrittene Wahrscheinlichkeiten.",
            "Discovery-driven Planning und gestufte Investments helfen.",
            "Modellkonflikte dokumentieren statt erzwingen.",
        ],
        "zh": [
            "不确定性出现在结果区间宽、概率存在争议时。",
            "探索式规划、实物期权与分阶段投资可降低承诺风险。",
            "模型不一致时应记录而非强行共识。",
        ],
    },
    "complexity": {
        "": [
            "Complexity multiplies interdependencies: changing one policy rewires incentives across departments. "
            "Healthcare pathways, platform ecosystems, and global supply webs are canonical examples.",
            "Systems mapping, bounded experiments, and network stewards help. Avoid optimizing local KPIs that "
            "export failure to neighbors in the graph.",
            "Use small safe-to-fail probes before scaling. Complexity rewards learners, not single heroic plans.",
        ],
        "ja": [
            "複雑性は相互依存の連鎖を増幅します。",
            "システムマップと安全に失敗できる実験が鍵です。",
            "ヒーロー計画より学習を優先します。",
        ],
        "de": [
            "Komplexität vervielfacht Abhängigkeiten.",
            "Systemkarten und safe-to-fail-Proben helfen.",
            "Lernen schlägt Hero-Pläne.",
        ],
        "zh": [
            "复杂性使部门间激励联动放大。",
            "系统图与可安全失败的实验是关键。",
            "奖励学习而非英雄式计划。",
        ],
    },
    "ambiguity": {
        "": [
            "Ambiguity means language, culture, or incomplete data leave multiple plausible stories. Mergers, AI ethics, "
            "and public messaging frequently sit in ambiguity.",
            "Facilitated dialogue, narrative testing, and explicit definition of terms reduce friction. Write glossaries "
            "for overloaded words like agility or transformation.",
            "Leaders should name what is unknown versus what is unknowable—different audiences need different reassurance.",
        ],
        "ja": [
            "曖昧性は複数の妥当な物語が共存する状態です。",
            "対話と用語定義が摩擦を減らします。",
            "未知と不可知を区別して示します。",
        ],
        "de": [
            "Mehrdeutigkeit: mehrere plausible Deutungen.",
            "Dialog und Begriffsdefinitionen helfen.",
            "Unbekannt vs. unwissbar unterscheiden.",
        ],
        "zh": [
            "模糊性指多种合理解释并存。",
            "对话与术语定义可降低摩擦。",
            "区分未知与不可知并分别沟通。",
        ],
    },
}

FAQ_ITEMS = {
    "": [
        ("What does VUCA stand for?", "Volatility, Uncertainty, Complexity, and Ambiguity."),
        ("Who created VUCA?", "U.S. Army War College educators popularized the acronym in the early 1990s; business later adopted it. Bennis/Nanus inform the broader turbulent-leadership discussion—see History."),
        ("Is VUCA still relevant?", "Yes as a diagnostic; pair with BANI or Cynefin for intervention choice."),
        ("How is VUCA different from risk management?", "VUCA describes context; risk management quantifies specific threats."),
    ],
    "ja": [
        ("VUCAとは何の略？", "Volatility（変動性）、Uncertainty（不確実性）、Complexity（複雑性）、Ambiguity（曖昧性）。"),
        ("誰が作った？", "1990年代初に米陸軍大学院が頭字語を普及。ビジネスが後に採用。Bennis/Nanusは関連議論（歴史ページ参照）。"),
        ("今も有効？", "診断として有効。介入にはBANIやCynefinと併用。"),
        ("リスク管理との違い？", "VUCAは文脈記述、リスク管理は特定脅威の定量化。"),
    ],
    "de": [
        ("Wofür steht VUCA?", "Volatility, Uncertainty, Complexity, Ambiguity."),
        ("Wer erfand VUCA?", "US Army War College popularisierte das Akronym Anfang der 1990er; Business übernahm später. Bennis/Nanus: siehe Geschichte."),
        ("Noch relevant?", "Ja zur Diagnose; mit BANI/Cynefin kombinieren."),
        ("Unterschied zu Risikomanagement?", "VUCA beschreibt Kontext, RM quantifiziert Bedrohungen."),
    ],
    "zh": [
        ("VUCA 代表什么？", "易变性、不确定性、复杂性、模糊性。"),
        ("谁提出的？", "1990 年代初美国陆军战争学院普及该缩写，后被商业采用。Bennis/Nanus 属相关领导力讨论，详见历史页。"),
        ("今天还有用吗？", "作为诊断仍有用，可配合 BANI 或 Cynefin 选择干预。"),
        ("与风险管理有何不同？", "VUCA 描述情境，风险管理量化具体威胁。"),
    ],
}

BIB_ITEMS = {
    "": [
        (HBR, "HBR: What VUCA Really Means for You"),
        (WIKI, "Wikipedia: VUCA"),
        (CCL, "CCL: What Is VUCA?"),
        (CYNEFIN, "Cynefin.io"),
        (BANI_WIKI, "Wikipedia: BANI"),
        (BANI_HBR, "HBR: Post-pandemic framing"),
        (TUNA_SRC, "Oxford Review: TUNA"),
        (RUPT_SRC, "The Decision Lab: RUPT"),
    ],
    "ja": [
        (HBR, "HBR: VUCAの実務的意味"),
        (WIKI, "Wikipedia: VUCA"),
        (CCL, "CCL: VUCAとは"),
        (CYNEFIN, "Cynefin.io"),
        (BANI_WIKI, "Wikipedia: BANI"),
        (BANI_HBR, "HBR: ポストパンデミック"),
        (TUNA_SRC, "Oxford Review: TUNA"),
        (RUPT_SRC, "The Decision Lab: RUPT"),
    ],
    "de": [
        (HBR, "HBR: VUCA für Führungskräfte"),
        (WIKI, "Wikipedia: VUCA"),
        (CCL, "CCL: Was ist VUCA?"),
        (CYNEFIN, "Cynefin.io"),
        (BANI_WIKI, "Wikipedia: BANI"),
        (BANI_HBR, "HBR: Post-Pandemie"),
        (TUNA_SRC, "Oxford Review: TUNA"),
        (RUPT_SRC, "The Decision Lab: RUPT"),
    ],
    "zh": [
        (HBR, "HBR：VUCA 的实践含义"),
        (WIKI, "Wikipedia：VUCA"),
        (CCL, "CCL：什么是 VUCA"),
        (CYNEFIN, "Cynefin.io"),
        (BANI_WIKI, "Wikipedia：BANI"),
        (BANI_HBR, "HBR：后疫情框架"),
        (TUNA_SRC, "Oxford Review：TUNA"),
        (RUPT_SRC, "The Decision Lab：RUPT"),
    ],
}

ORG_CHECKLIST = {
    "": [
        "V1: We track leading indicators for external shocks.",
        "V2: We keep capacity or inventory buffers for critical paths.",
        "V3: Decision rights for rapid response are named and practiced.",
        "V4: Post-shock reviews update playbooks within 30 days.",
        "U1: Major bets document assumptions and kill criteria.",
        "U2: We run at least three scenarios for material strategies.",
        "U3: Experiments have owners, budgets, and learning logs.",
        "U4: Forecasts show confidence ranges, not single points.",
        "C1: Cross-team dependencies are mapped at least quarterly.",
        "C2: Local KPIs cannot override system-level safety or trust metrics.",
        "C3: Architecture/process changes require impact review across domains.",
        "C4: Network stewards (not only project managers) own interfaces.",
        "A1: We maintain a shared glossary for overloaded terms.",
        "A2: Customer/employee messages are tested for multiple readings.",
        "A3: Leaders separate unknown vs unknowable in communications.",
        "A4: Conflict forums exist when interpretations of the same data diverge.",
    ],
    "ja": [
        "V1: 外部ショックの先行指標を追跡している。",
        "V2: 重要経路にバッファ容量・在庫がある。",
        "V3: 迅速対応の決裁権が明示され訓練されている。",
        "V4: ショック後30日以内にプレイブックを更新する。",
        "U1: 大型投資の前提と撤退基準を文書化している。",
        "U2: 重要戦略で少なくとも3シナリオを作成する。",
        "U3: 実験に担当・予算・学習ログがある。",
        "U4: 予測は単一点ではなく信頼区間を示す。",
        "C1: 四半期ごとに部門間依存をマップしている。",
        "C2: 局所KPIが安全・信頼の全体指標を上書きできない。",
        "C3: アーキ/プロセス変更は横断インパクト審査がある。",
        "C4: インターフェースにネットワーク・スチュワードがいる。",
        "A1: 多義語の共有用語集がある。",
        "A2: 顧客/社員向け文言の多重解釈テストを行う。",
        "A3: 未知と不可知を分けて伝える。",
        "A4: 同一データの解釈対立を扱う場がある。",
    ],
    "de": [
        "V1: Frühindikatoren für externe Schocks.",
        "V2: Puffer für kritische Pfade vorhanden.",
        "V3: Entscheidungsrechte für Rapid Response benannt und geübt.",
        "V4: Playbooks binnen 30 Tagen nach Schocks aktualisiert.",
        "U1: Annahmen und Kill-Kriterien dokumentiert.",
        "U2: Mindestens drei Szenarien für Materialstrategien.",
        "U3: Experimente mit Owner, Budget, Lernlog.",
        "U4: Prognosen mit Bandbreiten statt Einzelpunkten.",
        "C1: Abhängigkeiten quartalsweise kartiert.",
        "C2: Lokale KPIs überschreiben keine System-Sicherheitsmetriken.",
        "C3: Architektur-/Prozessänderungen brauchen Impact-Reviews.",
        "C4: Network Stewards für Schnittstellen benannt.",
        "A1: Gemeinsames Glossar für Mehrdeutigkeit.",
        "A2: Botschaften auf Mehrfachlesen getestet.",
        "A3: Unbekannt vs. Unwissbar getrennt kommuniziert.",
        "A4: Foren bei divergierenden Dateninterpretationen.",
    ],
    "zh": [
        "V1: 跟踪外部冲击的领先指标。",
        "V2: 关键路径保留产能或库存缓冲。",
        "V3: 快速响应决策权已命名并演练。",
        "V4: 冲击后 30 日内更新行动手册。",
        "U1: 重大押注记录假设与终止标准。",
        "U2: 重要战略至少做三种情景。",
        "U3: 实验有负责人、预算与学习日志。",
        "U4: 预测给出区间而非单点。",
        "C1: 至少每季度绘制跨团队依赖。",
        "C2: 局部 KPI 不能覆盖系统安全/信任指标。",
        "C3: 架构或流程变更需跨域影响审查。",
        "C4: 接口有网络 steward 负责。",
        "A1: 维护多义词共享术语表。",
        "A2: 对外对内文案做多重解读测试。",
        "A3: 沟通中区分未知与不可知。",
        "A4: 对同一数据的解释冲突有讨论机制。",
    ],
}

CASE_META = {
    "netflix": {
        "title": lambda locale: t(locale, "Case: Netflix", "事例：Netflix", "Fallstudie: Netflix", "案例：Netflix"),
        "desc": lambda locale: t(
            locale,
            "Pivoting from DVD mailers to streaming under volatile technology shifts.",
            "DVDからストリーミングへ、技術変動下での転換。",
            "Vom DVD-Versand zum Streaming unter Technologiewandel.",
            "从 DVD 邮递到流媒体的易变技术转型。",
        ),
    },
    "toyota": {
        "title": lambda locale: t(locale, "Case: Toyota", "事例：トヨタ", "Fallstudie: Toyota", "案例：丰田"),
        "desc": lambda locale: t(
            locale,
            "Lean, resilience, and supply shock response.",
            "リーン、レジリエンス、供給ショック対応。",
            "Lean, Resilienz und Supply-Shock-Reaktion.",
            "精益、韧性与供应冲击应对。",
        ),
    },
}

CASE_BODY = {
    "netflix": {
        "": [
            "Netflix illustrates volatility in technology and licensing markets. Leadership bet on broadband adoption early, "
            "accepting short-term margin pressure while building streaming expertise.",
            "Uncertainty around studio contracts pushed Netflix to invest in originals—an option that increased cost but "
            "reduced dependence on ambiguous renewal terms.",
            "Complex platform operations (CDN, encoding, personalization) required modular teams with clear service ownership.",
        ],
        "ja": [
            "Netflixは技術・ライセンス市場の変動性の事例です。早期にブロードバンド普及へ賭けました。",
            "契約不確実性からオリジナル投資へシフトしました。",
            "プラットフォーム運用の複雑性にモジュール型チームが対応しました。",
        ],
        "de": [
            "Netflix zeigt Volatilität in Technologie- und Lizenzmärkten.",
            "Unsicherheit bei Studios führte zu Originalinvestitionen.",
            "Komplexe Plattform mit klaren Service-Ownerships.",
        ],
        "zh": [
            "Netflix 体现了技术与授权市场的易变性，早期押注宽带普及。",
            "合同不确定性推动自制内容投资。",
            "复杂平台运营依靠模块化团队与服务所有权。",
        ],
    },
    "toyota": {
        "": [
            "Toyota's lean system buffers complexity on the plant floor while exposing problems quickly. After global supply "
            "disruptions, the firm rebalanced just-in-time with strategic inventory for critical semiconductors.",
            "Ambiguity in geopolitics forced diversified sourcing narratives communicated consistently to regulators and unions.",
        ],
        "ja": [
            "トヨタのリーンは現場の複雑性を抑えつつ問題を可視化します。供給混乱後、半導体の戦略在庫を強化しました。",
            "地政学の曖昧さに対し、調達多角化を一貫して説明しました。",
        ],
        "de": [
            "Toyotas Lean puffert Komplexität und macht Probleme sichtbar; strategische Halbleiterbestände nach Schocks.",
            "Geopolitische Mehrdeutigkeit erforderte konsistente Kommunikation zur Beschaffung.",
        ],
        "zh": [
            "丰田精益在抑制车间复杂性的同时快速暴露问题；供应冲击后增加关键芯片战略库存。",
            "地缘模糊性下对采购多元化保持对监管与工会的一致表述。",
        ],
    },
}
def article(locale: str, title: str, desc: str, paras: list[str], crumb: str = "glossary.html") -> tuple[str, str, str]:
    main = page_hero(locale, title, desc, crumb) + wrap_body(paras_html(paras))
    return title, desc, main


def industry_slug(page: str) -> str:
    return page.replace("industry-", "").replace(".html", "")


def build_industry(locale: str, page: str) -> tuple[str, str, str]:
    slug = industry_slug(page)
    titles = {
        "healthcare": t(locale, "VUCA in Healthcare", "医療におけるVUCA", "VUCA im Gesundheitswesen", "医疗健康领域的 VUCA"),
        "finance": t(locale, "VUCA in Financial Services", "金融サービスにおけるVUCA", "VUCA im Finanzsektor", "金融服务中的 VUCA"),
        "supply-chain": t(locale, "VUCA in Supply Chain", "サプライチェーンにおけるVUCA", "VUCA in der Lieferkette", "供应链中的 VUCA"),
        "tech": t(locale, "VUCA in Technology", "テクノロジーにおけるVUCA", "VUCA in der Technologiebranche", "科技行业中的 VUCA"),
        "education": t(locale, "VUCA in Education", "教育におけるVUCA", "VUCA im Bildungswesen", "教育领域的 VUCA"),
    }
    descs = {
        "healthcare": t(
            locale,
            "How hospitals and health systems interpret volatility, uncertainty, complexity, and ambiguity.",
            "病院・保健システムが四要素をどう捉えるかの実務ガイド。",
            "Wie Kliniken und Gesundheitssysteme die VUCA-Dimensionen interpretieren.",
            "医院与卫生体系如何理解并应对四维挑战。",
        ),
        "finance": t(
            locale,
            "Practical VUCA analysis for banks, insurers, and capital markets.",
            "銀行・保険・資本市場向けのVUCA実務分析。",
            "Praktische VUCA-Analyse für Banken, Versicherer und Kapitalmärkte.",
            "面向银行、保险与资本市场的 VUCA 实务分析。",
        ),
        "supply-chain": t(
            locale,
            "Resilience patterns for global logistics and manufacturing networks.",
            "グローバル物流・製造ネットワークのレジリエンス。",
            "Resilienzmuster für globale Logistik und Fertigungsnetzwerke.",
            "全球物流与制造网络的韧性模式。",
        ),
        "tech": t(
            locale,
            "Product, platform, and engineering leadership under rapid change.",
            "急速な変化下のプロダクト・プラットフォーム・エンジニアリング統制。",
            "Produkt-, Plattform- und Engineering-Führung bei raschem Wandel.",
            "快速变化下的产品、平台与工程领导。",
        ),
        "education": t(
            locale,
            "Universities and K-12 systems adapting curricula and operations.",
            "大学・K-12がカリキュラムと運営を適応させる方法。",
            "Hochschulen und Schulsysteme passen Curricula und Betrieb an.",
            "高校与大学体系如何调整课程与运营。",
        ),
    }
    title, desc = titles[slug], descs[slug]
    body = industry_paras(slug, locale)
    cross = card(
        p(
            t(
                locale,
                'See also <a href="org-assessment.html" class="text-emerald-700 hover:underline">organizational diagnostic</a> '
                'and <a href="templates.html" class="text-emerald-700 hover:underline">printable templates</a>.',
                '「<a href="org-assessment.html" class="text-emerald-700 hover:underline">組織診断</a>」と'
                '「<a href="templates.html" class="text-emerald-700 hover:underline">テンプレート</a>」も参照。',
                'Siehe auch <a href="org-assessment.html" class="text-emerald-700 hover:underline">Organisationsdiagnose</a> '
                'und <a href="templates.html" class="text-emerald-700 hover:underline">Vorlagen</a>.',
                '另见<a href="org-assessment.html" class="text-emerald-700 hover:underline">组织诊断</a>与'
                '<a href="templates.html" class="text-emerald-700 hover:underline">可打印模板</a>。',
            )
        )
    )
    main = page_hero(locale, title, desc, "glossary.html") + wrap_body(paras_html(body), cross)
    return title, desc, main


def build_what_is_vuca(locale: str) -> tuple[str, str, str, None]:
    title = t(
        locale,
        "What Is VUCA? Definition and Diagnostic Use",
        "VUCAとは：定義と診断としての使い方",
        "Was ist VUCA? Definition und diagnostische Nutzung",
        "什么是 VUCA？定义与诊断用法",
    )
    desc = t(
        locale,
        "VUCA means Volatility, Uncertainty, Complexity, and Ambiguity—a diagnostic lens from military planning to business strategy, with sources and practical responses.",
        "VUCAは変動性・不確実性・複雑性・曖昧性。軍事計画から経営戦略へ広がった診断レンズと実務対応、出典付き。",
        "VUCA bedeutet Volatilität, Unsicherheit, Komplexität und Mehrdeutigkeit—diagnostische Linse mit Quellen und Praxisantworten.",
        "VUCA 即易变性、不确定性、复杂性与模糊性：从军事规划到商业战略的诊断透镜，含出处与实务应对。",
    )
    refs = p(
        t(
            locale,
            f"Primers: {ext(HBR, 'HBR — What VUCA Really Means for You')}, {ext(WIKI, 'Wikipedia: VUCA')}, "
            f"{ext(CCL, 'CCL on leadership in uncertain environments')}. Deep dive: "
            f'<a class="text-emerald-700 hover:underline" href="framework.html">Framework guide</a>, '
            f'<a class="text-emerald-700 hover:underline" href="history.html">History</a>, '
            f'<a class="text-emerald-700 hover:underline" href="vuca-prime.html">VUCA Prime</a>.',
            f"入門: {ext(HBR, 'HBR')}, {ext(WIKI, 'Wikipedia')}, {ext(CCL, 'CCL')}。"
            f"詳細は<a class=\"text-emerald-700 hover:underline\" href=\"framework.html\">フレームワーク</a>、"
            f"<a class=\"text-emerald-700 hover:underline\" href=\"history.html\">歴史</a>、"
            f"<a class=\"text-emerald-700 hover:underline\" href=\"vuca-prime.html\">VUCA Prime</a>。",
            f"Einführung: {ext(HBR, 'HBR')}, {ext(WIKI, 'Wikipedia')}, {ext(CCL, 'CCL')}. "
            f"Tiefe: <a class=\"text-emerald-700 hover:underline\" href=\"framework.html\">Framework</a>, "
            f"<a class=\"text-emerald-700 hover:underline\" href=\"history.html\">Geschichte</a>, "
            f"<a class=\"text-emerald-700 hover:underline\" href=\"vuca-prime.html\">VUCA Prime</a>.",
            f"入门：{ext(HBR, 'HBR')}、{ext(WIKI, 'Wikipedia')}、{ext(CCL, 'CCL')}。"
            f"深读：<a class=\"text-emerald-700 hover:underline\" href=\"framework.html\">框架指南</a>、"
            f"<a class=\"text-emerald-700 hover:underline\" href=\"history.html\">历史</a>、"
            f"<a class=\"text-emerald-700 hover:underline\" href=\"vuca-prime.html\">VUCA Prime</a>。",
        )
    )
    paras = [
        t(
            locale,
            "VUCA names four conditions that make forecasting and control harder: rapid change (volatility), "
            "unpredictable futures (uncertainty), dense interdependencies (complexity), and unclear meaning (ambiguity). "
            "U.S. Army War College educators used the acronym for the post–Cold War environment; business writers later "
            "popularized it for globalization and digital disruption. Leadership theories by Warren Bennis and Burt Nanus "
            "are often cited in the broader conversation about turbulent leadership contexts, while the four-letter acronym "
            "itself is tied to military professional education in the early 1990s—see our history page for a sourced timeline.",
            "VUCAは予測と統制を難しくする四条件です。米陸軍大学院が冷戦後環境に用い、その後ビジネスへ広がりました。"
            "Bennis/Nanusのリーダーシップ議論と、1990年代初頭の軍事教育での頭字語採用は区別して理解してください（歴史ページ参照）。",
            "VUCA beschreibt vier Bedingungen, die Prognose und Steuerung erschweren. Das US Army War College nutzte das "
            "Akronym für das Umfeld nach dem Kalten Krieg; die Wirtschaft übernahm es später. Bennis/Nanus gehören zur "
            "breiteren Führungsdiskussion—die vier Buchstaben selbst zur militärischen Ausbildung der frühen 1990er "
            "(siehe Geschichtsseite).",
            "VUCA 概括使预测与控制变难的四种条件。美国陆军战争学院在冷战后环境中使用该缩写，后进入商业语境。"
            "Bennis/Nanus 常被一并讨论，但四字母缩写本身更直接关联 1990 年代初的军事职业教育——详见历史页。",
        ),
        t(
            locale,
            "Leaders should diagnose which dimension dominates before choosing tools. High volatility favors buffers, "
            "speed, and real-time monitoring. High uncertainty favors intelligence gathering, experiments, and scenarios. "
            "Complexity calls for systems mapping and interface ownership. Ambiguity requires sensemaking, shared language, "
            "and stakeholder alignment. Treating all four as a single slogan wastes the framework.",
            "どの次元が支配的かを診断してから手段を選びます。変動→バッファと速度、不確実→実験とシナリオ、"
            "複雑→システムマップ、曖昧→センスメイキングと共有言語。四文字をスローガン化するのは枠組みの浪費です。",
            "Diagnostizieren Sie die dominante Dimension, dann wählen Sie Werkzeuge: Volatilität→Puffer/Tempo; "
            "Unsicherheit→Experimente/Szenarien; Komplexität→Systemkarten; Mehrdeutigkeit→Sensemaking und Sprache. "
            "Als reiner Slogan verfehlt VUCA seinen Nutzen.",
            "先判断哪一维占主导再选工具：易变性→缓冲与速度；不确定性→情报、实验与情景；复杂性→系统图与接口负责；"
            "模糊性→意义建构与共同语言。把四字当口号会浪费这个框架。",
        ),
        t(
            locale,
            "Bob Johansen’s VUCA Prime (Vision, Understanding, Clarity, Agility) pairs each pressure with a leadership "
            "capability. Adjacent lenses—BANI, TUNA, RUPT, and Cynefin—answer related but different questions; compare "
            "them before replacing VUCA wholesale.",
            "ボブ・ジョハンセンのVUCA Prime（ビジョン・理解・明確性・アジリティ）が各圧に能力を対応づけます。"
            "BANI・TUNA・RUPT・Cynefinは隣接レンズであり、安易な置換前に比較してください。",
            "Bob Johansens VUCA Prime (Vision, Understanding, Clarity, Agility) ordnet jeder Dimension eine Fähigkeit zu. "
            "BANI, TUNA, RUPT und Cynefin sind benachbarte Linsen—vor einem Ersatz vergleichen.",
            "Bob Johansen 的 VUCA Prime（愿景、理解、清晰、敏捷）为每一压力配对领导能力。"
            "BANI、TUNA、RUPT、Cynefin 是相邻透镜，替换 VUCA 前先对比。",
        ),
        t(
            locale,
            "On this site: dedicated articles for each letter, a full framework implementation guide, industry applications, "
            "assessments, and templates. Start with the dimension pages if you need definitions; use the framework and "
            "action guide when you need operating routines.",
            "本サイトでは各文字の記事、実装ガイド、産業応用、評価とテンプレートを提供します。"
            "定義は次元ページ、運用はフレームワークとアクションガイドから。",
            "Hier: Artikel je Buchstabe, Implementierungsleitfaden, Branchen, Assessments und Vorlagen. "
            "Definitionen auf den Dimensionsseiten; Betrieb über Framework und Action Guide.",
            "本站提供四维专文、完整框架实施指南、行业应用、评估与模板。要定义看维度页；要运营看框架与行动指南。",
        ),
    ]
    main = page_hero(locale, title, desc, "glossary.html") + wrap_body(
        paras_html(paras),
        h2(t(locale, "Sources and next reading", "出典と次の読書", "Quellen und Weiterlesen", "来源与延伸阅读")),
        refs,
        card(
            ul_items(
                [
                    f'<a href="volatility.html" class="text-emerald-700 hover:underline">{t(locale, "Volatility", "変動性", "Volatilität", "易变性")}</a>',
                    f'<a href="uncertainty.html" class="text-emerald-700 hover:underline">{t(locale, "Uncertainty", "不確実性", "Unsicherheit", "不确定性")}</a>',
                    f'<a href="complexity.html" class="text-emerald-700 hover:underline">{t(locale, "Complexity", "複雑性", "Komplexität", "复杂性")}</a>',
                    f'<a href="ambiguity.html" class="text-emerald-700 hover:underline">{t(locale, "Ambiguity", "曖昧性", "Mehrdeutigkeit", "模糊性")}</a>',
                    f'<a href="glossary.html" class="text-emerald-700 hover:underline">{t(locale, "Full glossary", "用語集", "Glossar", "完整术语表")}</a>',
                    f'<a href="frameworks-comparison.html" class="text-emerald-700 hover:underline">{t(locale, "Compare frameworks", "フレーム比較", "Frameworks vergleichen", "框架对比")}</a>',
                ]
            )
        ),
    )
    return title, desc, main, None


def build_history(locale: str) -> tuple:
    title = t(
        locale,
        "History of VUCA: Origins and Business Adoption",
        "VUCAの歴史：起源とビジネスへの普及",
        "Geschichte von VUCA: Ursprung und Business-Adoption",
        "VUCA 历史：起源与商业采纳",
    )
    desc = t(
        locale,
        "Sourced timeline: U.S. Army War College, leadership theory context (Bennis/Nanus), business adoption, HBR 2014, Johansen’s VUCA Prime, and BANI.",
        "出典付き年表：米陸軍大学院、Bennis/Nanus文脈、ビジネス普及、HBR 2014、JohansenのVUCA Prime、BANI。",
        "Quellenbasierte Timeline: Army War College, Bennis/Nanus-Kontext, Business-Adoption, HBR 2014, Johansen VUCA Prime, BANI.",
        "带出处时间线：陆军战争学院、Bennis/Nanus 语境、商业采纳、HBR 2014、Johansen 的 VUCA Prime 与 BANI。",
    )
    paras = [
        t(
            locale,
            "Educators at the U.S. Army War College applied VUCA in the early 1990s to describe the post–Cold War "
            "operating environment. Volatility and uncertainty were familiar in doctrine; pairing them with complexity "
            "and ambiguity as equal strategic factors made the acronym useful for professional military education.",
            "1990年代初、米陸軍大学院が冷戦後の作戦環境を記述するためにVUCAを用い、複雑性と曖昧性を同列の戦略要因として結びました。",
            "Anfang der 1990er nutzte das US Army War College VUCA für das post-Cold-War-Umfeld und stellte Komplexität "
            "sowie Mehrdeutigkeit gleichrangig neben Volatilität und Unsicherheit.",
            "1990 年代初，美国陆军战争学院用 VUCA 描述冷战后作战环境，并将复杂性与模糊性提升为与易变性、不确定性并列的战略因素。",
        ),
        t(
            locale,
            "Warren Bennis and Burt Nanus’s leadership work is frequently referenced when writers discuss turbulent "
            "leadership contexts. That intellectual lineage sits beside—not identical to—the military acronym’s "
            "institutional use. Keep the distinction when citing origins.",
            "BennisとNanusのリーダーシップ研究は激動環境の議論でよく引用されますが、軍事頭字語の制度的使用と同一視しないでください。",
            "Bennis/Nanus werden oft in Turbulenzdiskursen zitiert—das ist verwandt, aber nicht identisch mit der "
            "institutionellen Nutzung des Militär-Akronyms.",
            "讨论动荡领导力时，常引用 Bennis 与 Nanus；该思想谱系与军事缩写的制度用法相关但并不等同，引用起源时请区分。",
        ),
        t(
            locale,
            "Business writers and schools adopted VUCA as globalization and digital disruption accelerated. "
            f"{ext(HBR, 'Bennett and Lemoine (HBR, 2014)')} argued leaders must separate the four challenges because "
            "each demands a different response—not a single ‘VUCA world’ shrug. Futurist Bob Johansen (Institute for the Future) "
            "advanced VUCA Prime: Vision, Understanding, Clarity, Agility. In 2020, Jamais Cascio popularized BANI as a "
            "complementary lens for brittle, anxious, non-linear, incomprehensible conditions.",
            f"グローバル化とデジタル化の中で経営教育がVUCAを採用。"
            f"{ext(HBR, 'Bennett & Lemoine (HBR, 2014)')}は四課題を分けて対応せよと論じ、"
            f"Bob Johansen（Institute for the Future）がVUCA Primeを提示。2020年Jamais CascioのBANIが補完レンズとして広まりました。",
            f"Wirtschaft und Business Schools übernahmen VUCA. {ext(HBR, 'Bennett/Lemoine (HBR 2014)')} forderten "
            f"getrennte Antworten je Dimension. Bob Johansen (IFTF) prägte VUCA Prime; 2020 popularisierte Jamais Cascio BANI.",
            f"全球化与数字化推动商学院采纳 VUCA。"
            f"{ext(HBR, 'Bennett 与 Lemoine（HBR, 2014）')}强调四维须分别应对；"
            f"未来学家 Bob Johansen（IFTF）提出 VUCA Prime；2020 年 Jamais Cascio 推广 BANI 作为互补透镜。",
        ),
        p(
            t(
                locale,
                f"Chronology references: {ext(WIKI, 'Wikipedia: VUCA')}, {ext(HBR, 'HBR on VUCA')}, "
                f'<a class="text-emerald-700 hover:underline" href="vuca-prime.html">VUCA Prime</a>, '
                f'<a class="text-emerald-700 hover:underline" href="vuca-vs-bani.html">VUCA vs BANI</a>.',
                f"年表: {ext(WIKI, 'Wikipedia')}, {ext(HBR, 'HBR')}, "
                f'<a class="text-emerald-700 hover:underline" href="vuca-prime.html">VUCA Prime</a>, '
                f'<a class="text-emerald-700 hover:underline" href="vuca-vs-bani.html">VUCA対BANI</a>。',
                f"Chronologie: {ext(WIKI, 'Wikipedia')}, {ext(HBR, 'HBR')}, "
                f'<a class="text-emerald-700 hover:underline" href="vuca-prime.html">VUCA Prime</a>, '
                f'<a class="text-emerald-700 hover:underline" href="vuca-vs-bani.html">VUCA vs BANI</a>.',
                f"年表参考：{ext(WIKI, 'Wikipedia')}、{ext(HBR, 'HBR')}、"
                f'<a class="text-emerald-700 hover:underline" href="vuca-prime.html">VUCA Prime</a>、'
                f'<a class="text-emerald-700 hover:underline" href="vuca-vs-bani.html">VUCA 与 BANI</a>。',
            )
        ),
    ]
    return *article(locale, title, desc, paras), None


def build_vuca_prime(locale: str) -> tuple:
    title = t(locale, "VUCA-Prime", "VUCA-Prime", "VUCA-Prime", "VUCA-Prime 对应领导力")
    desc = t(
        locale,
        "Bob Johansen's counter-capabilities: Vision, Understanding, Clarity, Agility.",
        "ボブ・ジョハンセンの対応能力：ビジョン・理解・明確性・敏捷性。",
        "Bob Johansens Gegenfähigkeiten: Vision, Understanding, Clarity, Agility.",
        "Bob Johansen 的对应能力：愿景、理解、清晰、敏捷。",
    )
    rows = card(
        "<table class='min-w-full text-sm border border-gray-200'><thead><tr class='border-b bg-gray-50'>"
        f"<th class='p-2 text-left'>{t(locale, 'VUCA', 'VUCA', 'VUCA', 'VUCA')}</th>"
        f"<th class='p-2 text-left'>{t(locale, 'Prime response', 'Prime対応', 'Prime-Antwort', 'Prime 回应')}</th>"
        "</tr></thead><tbody>"
        "<tr class='border-b'><td class='p-2'>Volatility</td><td class='p-2'>Vision</td></tr>"
        "<tr class='border-b'><td class='p-2'>Uncertainty</td><td class='p-2'>Understanding</td></tr>"
        "<tr class='border-b'><td class='p-2'>Complexity</td><td class='p-2'>Clarity</td></tr>"
        "<tr><td class='p-2'>Ambiguity</td><td class='p-2'>Agility</td></tr>"
        "</tbody></table>"
    )
    paras = [
        t(
            locale,
            "VUCA-Prime reframes each disruptive factor as a leadership behavior to cultivate. Vision stabilizes "
            "direction when markets swing; understanding deepens learning when forecasts fail; clarity simplifies "
            "messages when systems tangle; agility speeds adjustment when signals conflict.",
            "VUCA-Primeは各要因に対応するリーダー行動を育てます。",
            "VUCA-Prime ordnet jeder Störgröße eine zu entwickelnde Führungskompetenz zu.",
            "VUCA-Prime 为每种扰动因素对应一种应培养的领导力行为。",
        ),
    ]
    main = page_hero(locale, title, desc) + wrap_body(paras_html(paras), h2(t(locale, "Mapping", "対応表", "Zuordnung", "对应表")), rows)
    return title, desc, main, None


def build_vuca_vs_bani(locale: str) -> tuple:
    title = t(locale, "VUCA vs BANI", "VUCAとBANI", "VUCA vs BANI", "VUCA 与 BANI")
    desc = t(
        locale,
        "Compare classic VUCA with Jamais Cascio's brittle, anxious, nonlinear, incomprehensible world.",
        "VUCAとジャマイス・カスキオのBANI世界観を比較。",
        "Vergleich von VUCA mit Jamais Cascios BANI-Rahmen.",
        "经典 VUCA 与 Jamais Cascio 的 BANI 对比。",
    )
    paras = [
        t(
            locale,
            "VUCA emphasizes diagnostic nuance: leaders decide which dimension dominates. BANI stresses emotional "
            "and systemic fragility after shocks like pandemics—brittle systems, anxious publics, nonlinear cascades, "
            "and incomprehensible narratives.",
            "VUCAは診断の微分、BANIはショック後の脆さと不安に焦点を当てます。",
            "VUCA diagnostiziert Nuancen; BANI betont Zerbrechlichkeit und Angst nach Schocks.",
            "VUCA 强调诊断细分；BANI 强调冲击后的脆弱与焦虑。",
        ),
        p(
            t(
                locale,
                f"See {ext(BANI_WIKI, 'BANI (Wikipedia)')}, {ext(BANI_HBR, 'HBR on post-pandemic framing')}, and our "
                f'<a href="frameworks-comparison.html" class="text-emerald-700 hover:underline">frameworks comparison</a>.',
                f"{ext(BANI_WIKI, 'BANI (Wikipedia)')}と{ext(BANI_HBR, 'HBR')}、比較ページを参照。",
                f"{ext(BANI_WIKI, 'BANI')}, {ext(BANI_HBR, 'HBR')} und Framework-Vergleich.",
                f"见 {ext(BANI_WIKI, 'BANI')}、{ext(BANI_HBR, 'HBR')} 及框架对比页。",
            )
        ),
    ]
    return *article(locale, title, desc, paras), None


def build_tuna(locale: str) -> tuple:
    title = t(locale, "TUNA Framework", "TUNAフレームワーク", "TUNA-Rahmen", "TUNA 框架")
    desc = t(locale, "Turbulent, Uncertain, Novel, Ambiguous—an alternative lens.", "TUNAの四要素。", "TUNA: turbulent, unsicher, neuartig, mehrdeutig.", "TUNA：动荡、不确定、新颖、模糊。")
    paras = [
        t(
            locale,
            "TUNA highlights novelty: many post-2020 challenges combine familiar uncertainty with unprecedented "
            "technologies or regulations. Practitioners pair TUNA with discovery-driven planning when historical data is thin.",
            "TUNAは新規性を強調し、履歴データが薄いとき探索型計画と組み合わせます。",
            "TUNA betont Neuheit; mit discovery-driven Planning bei dünnen Daten kombinieren.",
            "TUNA 强调新颖性，常与探索式规划结合。",
        ),
        p(t(locale, f"Overview: {ext(TUNA_SRC, 'Oxford Review on TUNA')}.", f"概要: {ext(TUNA_SRC, 'Oxford Review')}.", f"Überblick: {ext(TUNA_SRC, 'Oxford Review')}.", f"概述：{ext(TUNA_SRC, 'Oxford Review')}。")),
    ]
    return *article(locale, title, desc, paras), None


def build_rupt(locale: str) -> tuple:
    title = t(locale, "RUPT Framework", "RUPTフレームワーク", "RUPT-Rahmen", "RUPT 框架")
    desc = t(locale, "Rapid, Unpredictable, Uncertain, Tangled.", "急速・予測不能・不確実・絡み合い。", "Rapid, Unpredictable, Uncertain, Tangled.", "急速、不可预测、不确定、缠结。")
    paras = [
        t(
            locale,
            "RUPT is used in organizational design literature to describe teams operating under constant rewiring of "
            "priorities. It pairs well with portfolio governance that caps work-in-progress.",
            "RUPTは優先度の絶え間ない組み替え下のチーム設計に使われます。",
            "RUPT beschreibt Teams unter ständig wechselnden Prioritäten.",
            "RUPT 描述优先级不断重组下的团队运作。",
        ),
        p(t(locale, f"Reference: {ext(RUPT_SRC, 'The Decision Lab')}.", f"参照: {ext(RUPT_SRC, 'The Decision Lab')}.", f"Referenz: {ext(RUPT_SRC, 'The Decision Lab')}.", f"参考：{ext(RUPT_SRC, 'The Decision Lab')}。")),
    ]
    return *article(locale, title, desc, paras), None


def build_cynefin(locale: str) -> tuple:
    title = t(locale, "Cynefin and VUCA", "CynefinとVUCA", "Cynefin und VUCA", "Cynefin 与 VUCA")
    desc = t(locale, "When to move from VUCA diagnosis to Cynefin sensemaking.", "VUCA診断からCynefinへ。", "Vom VUCA-Diagnose zu Cynefin.", "何时从 VUCA 转向 Cynefin。")
    paras = [
        t(
            locale,
            "VUCA names environmental traits; Cynefin classifies decision contexts (clear, complicated, complex, chaotic, confused). "
            "Use VUCA to explain why plans wobble, then Cynefin to pick intervention patterns—probe-sense-respond in complexity, "
            "act-sense-respond in chaos.",
            "VUCAは環境特性、Cynefinは意思決定文脈を分類します。",
            "VUCA beschreibt Umwelt; Cynefin ordnet Entscheidungskontexte.",
            "VUCA 描述环境；Cynefin 分类决策情境。",
        ),
        p(t(locale, f"Official resource: {ext(CYNEFIN, 'Cynefin.io')}.", f"公式: {ext(CYNEFIN, 'Cynefin.io')}.", f"Offiziell: {ext(CYNEFIN, 'Cynefin.io')}.", f"官方资源：{ext(CYNEFIN, 'Cynefin.io')}。")),
    ]
    return *article(locale, title, desc, paras), None


def build_frameworks_comparison(locale: str) -> tuple:
    title = t(locale, "Frameworks Comparison", "フレームワーク比較", "Framework-Vergleich", "框架对比")
    desc = t(locale, "VUCA, BANI, TUNA, RUPT, and Cynefin at a glance.", "主要フレームの一覧。", "VUCA, BANI, TUNA, RUPT, Cynefin im Überblick.", "五大框架一览。")
    hdr = t(locale, "Framework", "フレーム", "Rahmen", "框架")
    focus = t(locale, "Primary focus", "主眼", "Schwerpunkt", "侧重点")
    when = t(locale, "When to use", "使いどころ", "Einsatz", "适用情境")
    table = f'''<div class="overflow-x-auto rounded-3xl border border-gray-200">
<table class="min-w-full text-sm">
<thead><tr class="border-b bg-gray-50 text-left">
<th class="p-3">{hdr}</th><th class="p-3">{focus}</th><th class="p-3">{when}</th>
</tr></thead><tbody>
<tr class="border-b"><td class="p-3 font-medium">VUCA</td><td class="p-3">{t(locale, "Four environmental dimensions", "四つの環境次元", "Vier Umweltdimensionen", "四种环境维度")}</td>
<td class="p-3">{t(locale, "Strategic diagnosis", "戦略診断", "Strategische Diagnose", "战略诊断")}</td></tr>
<tr class="border-b"><td class="p-3 font-medium">BANI</td><td class="p-3">{t(locale, "Post-shock fragility", "ショック後の脆弱性", "Fragilität nach Schocks", "冲击后脆弱")}</td>
<td class="p-3">{t(locale, "Cultural resilience", "文化的レジリエンス", "Kulturelle Resilienz", "文化韧性")}</td></tr>
<tr class="border-b"><td class="p-3 font-medium">TUNA</td><td class="p-3">{t(locale, "Novel disruption", "新規性", "Neuartigkeit", "新颖扰动")}</td>
<td class="p-3">{t(locale, "Innovation portfolios", "イノベポートフォリオ", "Innovationsportfolios", "创新组合")}</td></tr>
<tr class="border-b"><td class="p-3 font-medium">RUPT</td><td class="p-3">{t(locale, "Operating tempo", "運用テンポ", "Betriebstempo", "运营节奏")}</td>
<td class="p-3">{t(locale, "Team design", "チーム設計", "Teamdesign", "团队设计")}</td></tr>
<tr><td class="p-3 font-medium">Cynefin</td><td class="p-3">{t(locale, "Decision domains", "意思決定領域", "Entscheidungsdomänen", "决策域")}</td>
<td class="p-3">{t(locale, "Intervention selection", "介入選択", "Interventionswahl", "干预选择")}</td></tr>
</tbody></table></div>'''
    main = page_hero(locale, title, desc) + wrap_body(p(table), card(ul_items([
        f'<a href="what-is-vuca.html" class="text-emerald-700 hover:underline">VUCA</a>',
        f'<a href="vuca-vs-bani.html" class="text-emerald-700 hover:underline">BANI</a>',
        f'<a href="tuna.html" class="text-emerald-700 hover:underline">TUNA</a>',
        f'<a href="rupt.html" class="text-emerald-700 hover:underline">RUPT</a>',
        f'<a href="cynefin-and-vuca.html" class="text-emerald-700 hover:underline">Cynefin</a>',
    ])))
    return title, desc, main, None


def build_glossary(locale: str) -> tuple:
    title = t(locale, "VUCA Glossary", "VUCA用語集", "VUCA-Glossar", "VUCA 术语表")
    desc = t(locale, "Core terms and links to dimension guides.", "用語と次元ガイドへのリンク。", "Kernbegriffe mit Dimensionsleitfäden.", "核心术语及四维指南链接。")
    entries = card(
        "<dl class='space-y-4'>"
        f"<dt class='font-semibold'><a href='volatility.html' class='text-emerald-700 hover:underline'>{t(locale, 'Volatility', '変動性', 'Volatilität', '易变性')}</a></dt>"
        f"<dd class='text-gray-700'>{t(locale, 'Speed and magnitude of change.', '変化の速度と振幅。', 'Geschwindigkeit und Ausmaß von Veränderung.', '变化的速度与幅度。')}</dd>"
        f"<dt class='font-semibold mt-4'><a href='uncertainty.html' class='text-emerald-700 hover:underline'>{t(locale, 'Uncertainty', '不確実性', 'Unsicherheit', '不确定性')}</a></dt>"
        f"<dd>{t(locale, 'Outcomes not confidently predictable.', '結果を自信を持って予測できない状態。', 'Ergebnisse nicht verlässlich vorhersagbar.', '结果无法可靠预测。')}</dd>"
        f"<dt class='font-semibold mt-4'><a href='complexity.html' class='text-emerald-700 hover:underline'>{t(locale, 'Complexity', '複雑性', 'Komplexität', '复杂性')}</a></dt>"
        f"<dd>{t(locale, 'Dense interactions among variables.', '変数間の密な相互作用。', 'Dichte Wechselwirkungen.', '变量之间高度相互作用。')}</dd>"
        f"<dt class='font-semibold mt-4'><a href='ambiguity.html' class='text-emerald-700 hover:underline'>{t(locale, 'Ambiguity', '曖昧性', 'Mehrdeutigkeit', '模糊性')}</a></dt>"
        f"<dd>{t(locale, 'Multiple plausible interpretations.', '複数の妥当な解釈が共存。', 'Mehrere plausible Deutungen.', '多种合理解释并存。')}</dd>"
        "</dl>"
    )
    main = page_hero(locale, title, desc, "glossary.html") + wrap_body(entries)
    return title, desc, main, None


def build_dim(locale: str, slug: str) -> tuple:
    meta = DIM_META[slug]
    title, desc = meta["title"](locale), meta["desc"](locale)
    paras = DIM_PARAS[slug][locale]
    t_tpl, d, m = dim_page(locale, slug[0].upper(), slug, title, desc, paras)
    return t_tpl, d, m, None


def build_faq(locale: str) -> tuple:
    title = t(locale, "VUCA FAQ", "VUCA FAQ", "VUCA FAQ", "VUCA 常见问题")
    desc = t(locale, "Answers on definition, use, and alternatives.", "定義・活用・代替案への回答。", "Antworten zu Definition, Nutzung, Alternativen.", "关于定义、应用与替代框架的问答。")
    qa = FAQ_ITEMS[locale]
    blocks = []
    entities = []
    for q, a in qa:
        blocks.append(card(f"<h3 class='text-lg font-semibold text-gray-900'>{q}</h3>{p(a)}"))
        entities.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    cites = card(
        h2(t(locale, "Primary sources", "主な出典", "Primärquellen", "主要来源"))
        + ul_items(
            [
                ext(HBR, "HBR: What VUCA Really Means for You"),
                ext(WIKI, "Wikipedia: VUCA"),
                ext(CCL, "CCL: Leadership in uncertain environments"),
                ext(CYNEFIN, "Cynefin.io"),
            ]
        )
    )
    main = page_hero(locale, title, desc) + wrap_body("".join(blocks) + cites)
    extra = {"@type": "FAQPage", "mainEntity": entities}
    return title, desc, main, extra


def build_bibliography(locale: str) -> tuple:
    title = t(locale, "Bibliography", "参考文献", "Bibliographie", "参考书目")
    desc = t(locale, "Linked references used across this knowledge base.", "本ナレッジで用いるリンク付き文献。", "Verlinkte Quellen der Wissensbasis.", "知识库所用链接文献。")
    items = BIB_ITEMS[locale]
    main = page_hero(locale, title, desc) + wrap_body(ul_items([f"{ext(u, lbl)}" for u, lbl in items]))
    return title, desc, main, None


def build_about(locale: str) -> tuple:
    title = t(locale, "About VUCA.cc", "VUCA.ccについて", "Über VUCA.cc", "关于 VUCA.cc")
    desc = t(locale, "Methodology, sourcing, and language policy.", "方法論・出典・言語方針。", "Methodik, Quellen, Sprachpolitik.", "方法论、出处与语言政策。")
    paras = [
        t(
            locale,
            "VUCA.cc is a static reference built for practitioners. Each article is drafted from primary sources "
            "(academic journals, official framework sites, and recognized publishers) and cross-checked for consistency across locales.",
            "VUCA.ccは実務者向け静的リファレンスです。一次資料に基づき各言語で整合を確認します。",
            "VUCA.cc ist eine statische Referenz für Praktiker, basierend auf Primärquellen.",
            "VUCA.cc 是面向实务者的静态参考站，内容依据一手资料并跨语言校对。",
        ),
        t(
            locale,
            "English is the source-of-record for information architecture. Japanese, German, and Simplified Chinese pages "
            "mirror that structure; depth parity is an ongoing program—legacy longform and industry guides are prioritized "
            "for full localization, while newer knowledge stubs continue to expand.",
            "英語が情報設計の基準です。日・独・中は構造をミラーし、長文と産業ガイドの完全ローカライズを優先、新規ナレッジは拡充中です。",
            "Englisch ist die Referenz-IA. JA/DE/ZH spiegeln die Struktur; Tiefenparität ist laufend—Longform und Branchen zuerst, neue Knowledge-Seiten werden ausgebaut.",
            "英语为信息架构基准。日/德/中镜像同一结构；内容深度对齐是持续工作——优先完善长文与行业指南，新知识页持续加厚。",
        ),
        p(f"{t(locale, 'Last content refresh', '最終更新', 'Letzte inhaltliche Aktualisierung', '内容最近更新')}: {LASTMOD}"),
    ]
    return *article(locale, title, desc, paras), None


def build_editorial(locale: str) -> tuple:
    title = t(locale, "Editorial Standards", "編集方針", "Redaktionelle Standards", "编辑标准")
    desc = t(locale, "Quality bar and publishing cadence.", "品質基準と公開ペース。", "Qualitätsmaßstab und Erscheinungsrhythmus.", "质量门槛与发布节奏。")
    paras = [
        t(
            locale,
            "We prioritize primary citations, avoid decorative UI clutter, and keep examples traceable. "
            "Industry and case articles are reviewed quarterly; at least one new case study ships every quarter.",
            "一次出典を優先し、四半期ごとに産業・事例記事を更新、毎四半期少なくとも1事例を追加します。",
            "Primärzitate, quartalsweise Branchen-/Fall-Reviews, mindestens ein neuer Fall pro Quartal.",
            "优先引用一手文献，每季度复审行业与案例稿，每季至少新增一则案例。",
        ),
        t(
            locale,
            "Authority building cadence: refresh dimension examples, keep bibliography links live, and share "
            "comparison tables and templates with educators, leadership communities, and curriculum lists. "
            "run link and SEO parity checks before each publish.",
            "権威構築：次元事例の更新、文献リンク点検、比較表・テンプレの共有。公開前にリンクとSEO整合を点検。",
            "Autoritätsaufbau: Dimensionen aktualisieren, Bibliografie prüfen, Vergleiche/Templates teilen; vor Publish Link- und SEO-Checks.",
            "权威建设节奏：刷新维度案例、核验文献链接、向教育与领导力社群分享对比表与模板；发布前做链接与 SEO 一致性检查。",
        ),
    ]
    return *article(locale, title, desc, paras), None


def build_templates(locale: str) -> tuple:
    title = t(locale, "VUCA Templates", "VUCAテンプレート", "VUCA-Vorlagen", "VUCA 模板")
    desc = t(locale, "Printable checklists for workshops.", "ワークショップ用チェックリスト。", "Druckbare Checklisten.", "可打印研讨清单。")
    c1 = card(
        h2(t(locale, "VUCA scorecard", "VUCAスコアカード", "VUCA-Scorecard", "VUCA 记分卡"))
        + ul_items(
            [
                t(locale, "Rate each dimension 0–2 across strategy, operations, culture.", "各次元を0–2で評価。", "Dimensionen 0–2 bewerten.", "各维度 0–2 评分。"),
                t(locale, "Attach evidence links and owner per row.", "根拠URLと担当者を記入。", "Belege und Owner je Zeile.", "每行附证据与负责人。"),
            ]
        )
        + p(f'<a href="/templates/vuca-scorecard.html" class="text-emerald-700 hover:underline">{t(locale, "Open printable scorecard", "印刷用スコアカード", "Druckbare Scorecard", "打开可打印记分卡")}</a>')
    )
    c2 = card(
        h2(t(locale, "Scenario planning", "シナリオ計画", "Szenarioplanung", "情景规划"))
        + ul_items(
            [
                t(locale, "Name 3–5 scenarios with triggers and leading indicators.", "3–5シナリオとトリガー。", "3–5 Szenarien mit Triggern.", "3–5 个情景及触发指标。"),
                t(locale, "Pre-author spending and staffing envelopes.", "支出・人員の事前承認枠。", "Vorab freigegebene Budgets.", "预授权预算与人力包。"),
            ]
        )
    )
    c3 = card(
        h2(t(locale, "Team agility", "チーム敏捷性", "Team-Agilität", "团队敏捷"))
        + ul_items(
            [
                t(locale, "Weekly decision log: what changed, what we learned.", "週次決定ログ。", "Wöchentliches Entscheidungslog.", "每周决策日志。"),
                t(locale, "WIP limits on cross-functional initiatives.", "横断施策のWIP制限。", "WIP-Limits für Initiativen.", "跨职能举措 WIP 限制。"),
            ]
        )
    )
    main = page_hero(locale, title, desc) + wrap_body(c1 + c2 + c3)
    return title, desc, main, None


def build_org_assessment(locale: str) -> tuple:
    title = t(locale, "Organizational VUCA Diagnostic", "組織VUCA診断", "Organisations-VUCA-Diagnose", "组织 VUCA 诊断")
    desc = t(locale, "Structured checklist with manual scoring—no automated quiz.", "自動採点なしの構造化チェックリスト。", "Strukturierte Checkliste ohne Auto-Quiz.", "结构化清单与手工评分，无自动测验。")
    guide = card(
        h2(t(locale, "Scoring guide", "採点ガイド", "Bewertungsleitfaden", "评分说明"))
        + paras_html(
            [
                t(
                    locale,
                    "There are 16 items (4 per dimension: V, U, C, A). Score each item 0 (absent), 1 (partial), or 2 (consistent). "
                    "Sum each dimension (max 8). 6–8 = strength, 3–5 = gaps, 0–2 = executive attention. Total max 32.",
                    "16項目（各次元4）。各0–2点。次元合計（最大8）：6–8強み、3–5ギャップ、0–2は経営介入。総計最大32。",
                    "16 Items (4 je Dimension). 0–2 pro Item. Dimensionssumme (max. 8): 6–8 stark, 3–5 Lücken, 0–2 Aufmerksamkeit. Gesamt max. 32.",
                    "共 16 项（每维 4 项）。每项 0–2 分。每维合计（满分 8）：6–8 优势，3–5 缺口，0–2 需管理层介入。总分满分 32。",
                )
            ]
        )
    )
    checks = ORG_CHECKLIST[locale]
    body = card(h2(t(locale, "Checklist", "チェックリスト", "Checkliste", "清单")) + ul_items(checks))
    main = page_hero(locale, title, desc) + wrap_body(guide, body)
    return title, desc, main, None


def build_case(locale: str, which: str) -> tuple:
    meta = CASE_META[which]
    title, desc = meta["title"](locale), meta["desc"](locale)
    paras = CASE_BODY[which][locale]
    return article(locale, title, desc, paras, "examples.html")


def write_llms() -> None:
    catalog = """# VUCA.cc

> Professional multilingual knowledge base for VUCA, leadership, and adjacent frameworks (BANI, TUNA, RUPT, Cynefin).

## Primary
- [Home](https://vuca.cc/): Hub
- [What is VUCA](https://vuca.cc/what-is-vuca.html)
- [History](https://vuca.cc/history.html)
- [VUCA Prime](https://vuca.cc/vuca-prime.html)
- [Framework](https://vuca.cc/framework.html)
- [Framework comparison](https://vuca.cc/frameworks-comparison.html)
- [Glossary](https://vuca.cc/glossary.html)
- [FAQ](https://vuca.cc/faq.html)
- [Leadership](https://vuca.cc/leadership.html)
- [Assessment](https://vuca.cc/assessment.html)
- [Org diagnostic](https://vuca.cc/org-assessment.html)
- [Templates](https://vuca.cc/templates.html)
- [Bibliography](https://vuca.cc/bibliography.html)
- [About](https://vuca.cc/about.html)
- [Editorial](https://vuca.cc/editorial.html)

## Dimensions
- /volatility.html /uncertainty.html /complexity.html /ambiguity.html

## Adjacent frameworks
- /vuca-vs-bani.html /tuna.html /rupt.html /cynefin-and-vuca.html

## Industries
- /industry-healthcare.html /industry-finance.html /industry-supply-chain.html /industry-tech.html /industry-education.html

## Languages
English (default), Japanese (/ja/), German (/de/), Simplified Chinese (/zh/) — hreflang on every page.
"""
    (ROOT / "llms.txt").write_text(catalog, encoding="utf-8")


def write_scorecard() -> None:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VUCA Scorecard (Printable)</title>
<meta name="description" content="Printable VUCA organizational scorecard for Volatility, Uncertainty, Complexity, and Ambiguity workshops.">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://vuca.cc/templates/vuca-scorecard.html">
<link rel="stylesheet" href="../css/site.css">
<style>@media print {{ .no-print {{ display: none; }} }}</style>
</head>
<body class="bg-white text-gray-900 p-8 text-sm">
<h1 class="text-3xl font-bold mb-2">VUCA Organizational Scorecard</h1>
<p class="text-gray-600 mb-6">Last updated: {LASTMOD}. Score each practice 0–2; use evidence column for owners and links.</p>
<table class="w-full border border-gray-300">
<thead><tr class="bg-gray-50"><th class="border p-2 text-left">Dimension / practice</th><th class="border p-2">0</th><th class="border p-2">1</th><th class="border p-2">2</th><th class="border p-2 text-left">Evidence / Owner</th></tr></thead>
<tbody>
<tr><td class="border p-2 font-semibold" colspan="5">Volatility</td></tr>
<tr><td class="border p-2">Leading indicators for shocks</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">Buffers on critical paths</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">Rapid-response decision rights</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">Post-shock playbook updates</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2 font-semibold" colspan="5">Uncertainty</td></tr>
<tr><td class="border p-2">Assumptions and kill criteria</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">Three-plus scenarios</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">Experiments with learning logs</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">Forecast ranges (not single points)</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2 font-semibold" colspan="5">Complexity</td></tr>
<tr><td class="border p-2">Dependency maps</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">System metrics over local KPIs</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">Cross-domain impact reviews</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">Interface stewards</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2 font-semibold" colspan="5">Ambiguity</td></tr>
<tr><td class="border p-2">Shared glossary</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">Message interpretation tests</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">Unknown vs unknowable named</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
<tr><td class="border p-2">Conflict forums for contested data</td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td><td class="border p-2"></td></tr>
</tbody></table>
<p class="mt-6 text-gray-700">Per dimension max 8 (4 items × 2). Site diagnostic: <a href="/org-assessment.html">/org-assessment.html</a></p>
<p class="no-print mt-4"><a href="/templates.html" class="text-emerald-700">Back to templates (EN)</a> ·
<a href="/ja/templates.html" class="text-emerald-700">JA</a> ·
<a href="/de/templates.html" class="text-emerald-700">DE</a> ·
<a href="/zh/templates.html" class="text-emerald-700">ZH</a></p>
</body></html>"""
    out = ROOT / "templates" / "vuca-scorecard.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


RENDERERS = {
    "what-is-vuca.html": build_what_is_vuca,
    "history.html": build_history,
    "vuca-prime.html": build_vuca_prime,
    "vuca-vs-bani.html": build_vuca_vs_bani,
    "tuna.html": build_tuna,
    "rupt.html": build_rupt,
    "cynefin-and-vuca.html": build_cynefin,
    "frameworks-comparison.html": build_frameworks_comparison,
    "glossary.html": build_glossary,
    "volatility.html": lambda loc: build_dim(loc, "volatility"),
    "uncertainty.html": lambda loc: build_dim(loc, "uncertainty"),
    "complexity.html": lambda loc: build_dim(loc, "complexity"),
    "ambiguity.html": lambda loc: build_dim(loc, "ambiguity"),
    "faq.html": build_faq,
    "bibliography.html": build_bibliography,
    "about.html": build_about,
    "editorial.html": build_editorial,
    "templates.html": build_templates,
    "org-assessment.html": build_org_assessment,
    "industry-healthcare.html": lambda loc: (*build_industry(loc, "industry-healthcare.html"), None),
    "industry-finance.html": lambda loc: (*build_industry(loc, "industry-finance.html"), None),
    "industry-supply-chain.html": lambda loc: (*build_industry(loc, "industry-supply-chain.html"), None),
    "industry-tech.html": lambda loc: (*build_industry(loc, "industry-tech.html"), None),
    "industry-education.html": lambda loc: (*build_industry(loc, "industry-education.html"), None),
    "case-netflix.html": lambda loc: (*build_case(loc, "netflix"), None),
    "case-toyota.html": lambda loc: (*build_case(loc, "toyota"), None),
}


def main() -> None:
    count = 0
    for loc in LOCS:
        for page in PAGES:
            title, desc, main_html, extra = RENDERERS[page](loc)
            html = wrap_page(loc, page, title, desc, main_html, extra_schema=extra)
            path = page_file(loc, page)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(html, encoding="utf-8")
            count += 1
    write_sitemap(ALL_PAGES)
    write_llms()
    write_scorecard()
    script = Path(__file__).resolve()
    size = script.stat().st_size
    print(f"Generated {count} HTML knowledge pages + scorecard; script {size} bytes")


if __name__ == "__main__":
    main()