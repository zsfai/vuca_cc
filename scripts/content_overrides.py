#!/usr/bin/env python3
"""Locale depth + meta overrides applied by generate_knowledge_base."""
from __future__ import annotations


def apply(ns: dict) -> None:
    """Mutate INDUSTRY_CONTENT / DIM_PARAS / CASE_BODY in the caller namespace."""
    industry = ns["INDUSTRY_CONTENT"]
    for slug, locs in INDUSTRY_EXTRA.items():
        industry[slug].update(locs)

    dim = ns["DIM_PARAS"]
    for slug, locs in DIM_PARAS_EXTRA.items():
        dim[slug].update(locs)

    cases = ns["CASE_BODY"]
    for slug, locs in CASE_BODY_EXTRA.items():
        cases[slug].update(locs)

    meta = ns["DIM_META"]
    t = ns["t"]
    meta["volatility"]["desc"] = lambda locale, _t=t: _t(
        locale,
        "Volatility means rapid, large swings in conditions and metrics—and how leaders buffer recovery time.",
        "変動性とは条件・指標の急速かつ大きな振れであり、回復時間をどう確保するかが焦点です。",
        "Volatilität meint schnelle, starke Schwankungen—und wie Führung Erholungszeit absichert.",
        "易变性指条件与指标的快速大幅波动，以及领导者如何缩短冲击后的恢复时间。",
    )
    meta["uncertainty"]["desc"] = lambda locale, _t=t: _t(
        locale,
        "Uncertainty is when credible probabilities are unavailable and decisions need staged commitments.",
        "不確実性とは信頼できる確率が得られず、段階的コミットメントが必要な状態です。",
        "Unsicherheit: fehlende verlässliche Wahrscheinlichkeiten und gestufte Verpflichtungen.",
        "不确定性指缺乏可信概率估计，因而需要分阶段承诺的决策情境。",
    )
    meta["complexity"]["desc"] = lambda locale, _t=t: _t(
        locale,
        "Complexity arises from many interacting parts with nonlinear effects across teams and systems.",
        "複雑性は多数の相互作用と非線形効果がチームやシステムを横断して生じる状態です。",
        "Komplexität entsteht durch viele Wechselwirkungen mit nichtlinearen Effekten über Systeme hinweg.",
        "复杂性来自大量相互作用与非线性效应，并跨团队与系统传导。",
    )
    meta["ambiguity"]["desc"] = lambda locale, _t=t: _t(
        locale,
        "Ambiguity means signals allow multiple valid readings—language, culture, or incomplete data.",
        "曖昧性とは、言語・文化・不完全データにより複数の妥当な読み取りが可能な状態です。",
        "Mehrdeutigkeit: Signale lassen mehrere gültige Deutungen zu—Sprache, Kultur oder Lücken.",
        "模糊性指信号可有多种有效解读——来自语言、文化或不完整数据。",
    )

    case_meta = ns["CASE_META"]
    case_meta["netflix"]["desc"] = lambda locale, _t=t: _t(
        locale,
        "How Netflix pivoted from DVD mailers to streaming under volatile technology and licensing shifts.",
        "Netflixが技術・ライセンス変動下でDVD配送からストリーミングへ転換した事例。",
        "Wie Netflix unter Technologie- und Lizenzvolatilität vom DVD-Versand zum Streaming wechselte.",
        "Netflix 如何在技术与授权易变下，从 DVD 邮递转向流媒体。",
    )
    case_meta["toyota"]["desc"] = lambda locale, _t=t: _t(
        locale,
        "Toyota lean practice, resilience design, and response to global supply shocks.",
        "トヨタのリーン、レジリエンス設計、世界的供給ショックへの対応。",
        "Toyotas Lean-Praxis, Resilienzdesign und Reaktion auf globale Supply-Schocks.",
        "丰田的精益实践、韧性设计与全球供应冲击应对。",
    )


INDUSTRY_EXTRA = {
    "finance": {
        "ja": """金融機関は金利・スプレッドの変動、規制アジェンダの不確実性、貸借対照表連鎖が増幅する複雑性、数字発表後も残る評判ナラティブの曖昧さの中で稼働します。リテール銀行は預金ベータが一夜で再価格付けされるときに変動性を感じ、資産運用はストレス下で流動性窓が狭まるときにそれを見ます。

不確実性は戦略計画サイクルを支配します。監督当局は資本バッファー変更を示唆し、気候ストレステストは進化し、デジタル資産ルールは複数法域で草案のままです。財務は金利パスをモデル化しつつ、政治ショックが四半期半ばで優先度を並べ替えます。

複雑性は構造的です。住宅ローン商品は販売行為、資金デスク、リスクウェイト、サービサー、投資家報告に触れます。不正対策と協調せず承認速度だけを上げると、数四半期後に損失が膨らみます。

曖昧性は顧客信頼に表れます。同じAPR開示でも人口層で読み方が違い、ESGラベルは定義が複数あります。コンプライアンスとマーケティングが同じ言葉を異なる意図で使うことがあります。

強靭な銀行は取引・流動性・オペリスクを一本のタイムラインで結ぶ統合リスク・テレメトリに投資します。シナリオ演習にはサイバー停止、突然の預金流出、相関市場ギャップを含めます。

資本・流動性バッファは変動性の吸収材ですが、スプレッドシート信仰ではなくガバナンス所有であるべきです。取締役会は指名された決裁権に紐づくトリガー閾値を見るべきです。

不確実性ツールには段階的商品ローンチ、フィンテックとのサンドボックス連携、技術投資のリアルオプション価格付けがあります。資金投入前に撤退基準を文書化します。

複雑性実務は新規APIチャネルごとのアーキテクチャ審査と、AML・行為監視への明示的データ系譜を意味します。曖昧性実務は顧客文書の平易言語テストと、開場前の危機ナラティブに関する会長級合意を意味します。

異業種波及は金融にとってサプライチェーン問題です。物流企業が破綻すると貿易金融エクスポージャが跳ねます。ティア1以外までカウンターパーティマップを維持してください。

次の一手：主要収益施策3件に四次元スキャンを行い、既存KPIを紐づけ、失敗予測の四半期学習ログを公開してください。これは静的計画より、不確実性下の組織的理解を育てます。

財務とリスク委員会は、変動性が日中限度を破ったときのコミュニケーションを予行演習すべきです—誰が取引を止め、誰が規制当局に説明し、支店がどう承認済みスクリプトを受け取るか。事後にはどの前提が崩れたかをタグ付けするポストトレード分析を組み合わせ、相関ブックの複雑性をサイロ化したダッシュボードに隠さないようにします。

ウェルスと保険アームはリテールとブランド曖昧性を共有します。SNSが内部メモの部分スクショを広げるとき、チャネル横断の危機言語の同期が重要です。""",
        "zh": """金融机构置身 VUCA：利率与利差波动、监管议程带来的不确定性、资产负债表联动放大的复杂性，以及数字公布后仍存的声誉叙事模糊。零售银行在存款定价一夜重定锚时感到易变性；资管在压力市况下流动性窗口变窄时看到它。

不确定性主导战略规划周期。监管暗示资本缓冲变化、气候压力测试持续演进、数字资产规则在多法域仍处草案。司库在建模利率路径的同时，政治冲击会在季度中途重排优先级。

复杂性是结构性的：一款房贷同时牵动销售行为、资金台、风险权重、服务商与投资者披露。未与反欺诈协同就只优化审批速度，可能在数季后放大损失。

模糊性出现在客户信任上。相同 APR 披露在不同人群中读法不同，ESG 标签定义多元。合规与市场可能用同一词汇表达不同意图。

有韧性的银行投资统一风险遥测——将交易、流动性与操作事件放在同一时间线。情景演练应包含网络中断、突发存款外流与相关性市场缺口。

资本与流动性缓冲是易变性吸收器，但须由治理主体拥有，而非表格崇拜。董事会应看到与命名决策权绑定的触发阈值。

不确定性工具包括分阶段产品上线、与金融科技的沙盒合作，以及对技术押注的实物期权定价。出资前先写明终止标准。

复杂性实务意味着每个新 API 渠道做架构审查，并明确流入反洗钱与行为监测的数据血缘。模糊性实务意味着对客户信函做通俗语言测试，并在开市前就危机叙事达成主席级对齐。

跨业传染对金融是供应链问题：物流企业失败时，贸易融资敞口会跳升。将交易对手图谱维护到一级以外。

行动建议：对三大营收举措做四维扫描、映射现有 KPI，并发布季度预测失误学习日志——这比再写一份静态计划更能建立不确定下的组织理解。

财务与风险委员会应预演易变性突破日间限额时的沟通——谁可停止交易、谁向监管汇报、分行如何收到核准话术。配合交易后分析标注哪些假设失败，使相关账簿的复杂性可见而非藏在孤岛仪表盘里。

财富与保险条线与零售共享品牌模糊性——当社交媒体传播内部备忘录的局部截图时，跨渠道危机口径同步至关重要。""",
    },
    "supply-chain": {
        "ja": """グローバル・サプライチェーンは運賃急騰、港湾労働争議、二次サプライヤーの静かな破綻、サステナビリティ規制の一夜での解釈変更など、VUCAが集中します。変動性はスポットコンテナ運賃や航空サーチャージとして現れ、四半期の粗利ガイダンスを消し得ます。

不確実性は、小売パートナーからのデータ共有が減る需要予測、週次更新の制裁リスト、回収に数年かかるニアショア判断にあります。

複雑性はBOM、デュアルソーシング規則、品質保留、逆方向に働く金融プログラムの網です。金属のコストダウンが三ノード先の組立不良率を上げることがあります。

曖昧性はESGスコア、不可抗力条項、遅延に関する顧客コミュニケーションの定義ズレとして現れます。現場と法務は合意したつもりでも、顧客には混線したメッセージが届くことがあります。

リーダーは在庫・入庫物流・サプライヤー健全性を融合するコントロールタワーを作ります。ERPスナップショットだけでは足りず、支払ストレスや工場地域の社会センチメントなど先行指標が必要です。

デュアルソーシングは互換仕様で設計すれば変動性ヘッジになりますが、さもなければレジリエンスなく複雑性だけが増えます。運河閉鎖、半導体配分ショック、関税急変をシナリオに含めます。

高変動下では年次戦略より半年ごとのネットワーク設計レビューが有効です。特急判断のウォールームには財務を同席させ、マージン影響をリアルタイムで把握します。

数字化は助けになりますが、部品番号の重複や不完全BOMが分析を歪めます。マスターデータ・スチュワードが標準を強制するまでデータ曖昧性は残ります。

地域・品目のVUCAヒートマップをサービスレベル指標に結び、制裁と気象モデルの不確実性モニタリング担当を置いてください。仕様を設計・品質と共著するサプライヤー育成資金は曖昧性を下げ、メール論争より共有テスト治具の方が効きます。

混乱後の振り返りでは、変動性（価格急騰）と複雑性（ルート変更）を分け、次のプレイブックが正しい根本原因を狙うようにします。気候変動性を四半期レビューの第一級シナリオに格上げしてください。在庫配置は複雑性レバーです。財務とオペは少なくとも二つの変動レジームで総着地コストを四半期ごとにモデル化します。強制労働デューデリジェンスは国ごとの文書基準差で曖昧性を生み、中央監査プレイブックと地域別付録で現場とコンプライアンスを揃えます。""",
        "de": """Globale Lieferketten bündeln VUCA: Frachtspitzen, Hafenstreiks, stille Tier-2-Ausfälle und ESG-Regeln, die Beschaffung über Nacht umdeuten. Volatilität zeigt sich in Spot-Containerraten und Luftfrachtzuschlägen, die Quartalsmargenführung löschen können.

Unsicherheit sitzt in Nachfrageprognosen bei weniger Retail-Daten, wöchentlich aktualisierten Sanktionslisten und Nearshoring mit mehrjährigen Paybacks.

Komplexität ist das Netz aus Stücklisten, Dual-Sourcing-Regeln, Quality Holds und Finanzprogrammen mit gegenläufigen Anreizen. Ein Cost-down bei Metallen kann Ausschuss drei Knoten weiter erhöhen.

Mehrdeutigkeit entsteht, wenn ESG-Scores, Force-Majeure-Klauseln und Kundenkommunikation zu Verspätungen inkonsistente Definitionen nutzen. Operations und Legal glauben aligned zu sein, während Kunden gemischte Botschaften hören.

Führung baut Control Towers, die Bestand, Inbound und Lieferantengesundheit verbinden—nicht nur ERP-Snapshots. Frühindikatoren: Zahlungstress der Lieferanten und soziales Sentiment in Fabrikregionen.

Dual Sourcing puffert Volatilität nur mit austauschbaren Specs; sonst verdoppelt es Komplexität ohne Resilienz. Szenarien: Kanalsperren, Halbleiterzuteilung, Zollschocks. Netzwerk-Reviews alle sechs Monate schlagen Jahresstrategien bei hoher Volatilität.

War Rooms brauchen Finance, damit Eilentscheidungen Margeneffekte sofort sehen. Digitalisierung hilft, doch doppelte Teilenummern und Teil-BOMs verzerren Analysen, bis Master-Data-Stewards Standards durchsetzen.

Starten Sie mit einer VUCA-Heatmap nach Region und Commodity, koppeln Sie an Service-Level-Metriken und benennen Sie Owner für Sanktions- und Wettermodelle. Supplier-Development-Fonds reduzieren Mehrdeutigkeit, wenn Specs gemeinsam mit Engineering und Quality entstehen.

Nach Störungen: blameless Retros, die Volatilität (Preisspitzen) von Komplexität (Routing) trennen. Klimavolatilität gehört als First-Class-Szenario in Quartalsreviews. Bestandspositionierung ist ein Komplexitätshebel; Finance und Operations modellieren Total Landed Cost unter mindestens zwei Volatilitätsregimen. Forced-Labor-Diligence erzeugt Mehrdeutigkeit bei unterschiedlichen Dokumentstandards—zentrale Audit-Playbooks mit lokalen Annexen halten Compliance und Operations aligned.""",
        "zh": """全球供应链集中体现 VUCA：运价飙升、港口劳资行动、二级供应商隐性失败，以及可持续规则一夜之间改写采购含义。易变性可见于即期集装箱价格与空运附加费，足以抹掉季度毛利指引。

不确定性存在于零售伙伴数据分享变少时的需求预测、每周更新的制裁清单，以及回收期长达数年的回流决策。

复杂性是物料清单、双源规则、质量冻结与相互矛盾的财务激励交织的网络。金属降本项目可能在三个节点之外抬高装配不良率。

当 ESG 评分、不可抗力条款与延期客户沟通使用不一致定义时，模糊性出现。运营与法务自以为对齐，客户却听到混杂信息。

领导者建设融合库存、入库物流与供应商健康度的控制塔——不只是 ERP 快照。领先指标包括供应商支付压力与工厂地区的社会情绪。

双源只有在可互换规格下才是易变性对冲，否则只增加复杂性而无韧性。情景应覆盖运河中断、芯片配给冲击与关税突变。高波动时，每半年的网络设计审视优于年度战略。跨职能作战室需要财务在场，以便实时理解加急对毛利的影响。

数字化有帮助，但重复料号与残缺 BOM 会扭曲分析，直到主数据 steward 强制标准。按区域与品类绘制 VUCA 热图，绑定服务水平指标，并指定制裁与气象模型的监测负责人。

与工程、质量共写规格的供应商发展资金可降低模糊性；共享测试夹具胜过邮件争论公差。冲击后做无指责复盘，区分易变性（价格飙升）与复杂性（路由变更），使下一版手册对准正确根因。

气候易变性应作为一级情景进入季度经营回顾。库存布点是复杂性杠杆——靠近客户吸收波动但提高过时风险，中央枢纽简化计划但拉长交期。财务与运营应至少按两种波动体制季度建模总到岸成本。强迫劳动尽职调查因各国文件标准不同引入模糊性；用中央审计手册加地方附件对齐合规与运营。""",
    },
    "tech": {
        "ja": """テック企業はプロダクト半減期の短縮、プラットフォーム規則の変化、セキュリティ脅威がロードマップを四半期ごとに描き直すため、VUCAを増幅します。変動性はクラウド費用の振れ、人材市場の急騰、競争位置を一夜でリセットするモデル公開サイクルとして現れます。

不確実性はAI規制、OSSライセンス論争、予算明確化まで待つエンタープライズ購買にあります。複雑性はマイクロサービス、データパイプライン、Entitlement、サポート階層にまたがり、オンコールも分断されます。価格変更一つが請求、営業報酬、カスタマーサクセス手順に波及します。

曖昧性はポジショニングで常態です。誰もがAIリーダーを名乗り、安全・プライバシー約束の解釈は地域で異なります。強いエンジニアリング組織はFeature flagと段階ロールアウトという変動バッファを、トレードオフを明示するエラーバジェットと組み合わせます。

不確実性下の探索トラックは期間上限と成功指標の事前登録が必要です。ADRは境界の理由を残し複雑性負債を抑えます。包摂的デザインレビューはUX文言と同意フローの曖昧さを下げます。利用変動が収益連動SLAを脅かすとき、信頼性は取締役会議題になります。

第三者リスクには古典的SaaSだけでなくAIサブプロセッサとデータ所在地チェーンを含めます。四半期ごとにプラットフォーム戦略のVUCAレビューを行い、各次元を既存のSRE・プロダクト発見・広報指標に結びます。

セキュリティと信頼性は別チェックリストではなく変動性問題としてボードに見せます。インシデント頻度、パッチ遅延、顧客可視ダウンタイムを収益ガイダンスと同じスライドに載せます。人材変動性にはプリンシパル級の後継計画と組織改編前のナレッジ移管が必要で、さもなければ複雑性負債が新チーム名の下に再出現します。

商況リーダーは価格実験を変動トリガーに揃えます。クラウド費用やモデル訓練費が月次バンドを超えたら、財務とプロダクトの共同承認まで広範値引きを自動停止し、粗利ガードレールの曖昧さを防ぎます。OSSプログラムオフィスは承認ライセンス行列とマージ時の自動スキャンで法務曖昧性を下げます。

サポート滞留、エスカレーション率、公開イシュースレッドなどの信頼指標をデプロイ頻度の横に置き、対外メッセージの曖昧性が解約変動になる前に捕捉します。マルチクラウド契約は不確実性ベットであり、退出コスト・移植テスト・データ重力の前提を署名前に文書化し、更新期に請求複雑性が財務を驚かせないようにします。""",
        "de": """Technologieunternehmen verstärken VUCA, weil Produkthalbwertszeiten schrumpfen, Plattformregeln wechseln und Security-Bedrohungen Roadmaps vierteljährlich neu zeichnen. Volatilität zeigt sich in Cloud-Kosten, Talentmärkten und Modell-Release-Zyklen, die Wettbewerbspositionen über Nacht resetten.

Unsicherheit sitzt in KI-Regulierung, OSS-Lizenzdebatten und Enterprise-Käufern, die Commitments verzögern. Komplexität spannt Microservices, Datenpipelines, Entitlements und Support-Tiers—mit getrennten On-call-Rotationen. Eine Preisänderung kann Billing, Sales Comp und Customer-Success-Playbooks durchlaufen.

Mehrdeutigkeit ist in der Positionierung üblich: jeder Vendor beansprucht AI-Leadership; Kunden deuten Safety- und Privacy-Versprechen regional unterschiedlich. Starke Engineering-Orgs kombinieren Feature Flags und gestufte Rollouts mit Error Budgets, die Trade-offs explizit machen.

Discovery-Tracks unter Unsicherheit brauchen Dauer-Caps und vorregistrierte Erfolgsmetriken. ADRs senken Komplexitätsschulden. Inklusive Design-Reviews senken UX-/Consent-Mehrdeutigkeit. Plattformreliabilität wird Board-Thema, wenn Nutzungsvolatilität umsatzgebundene SLAs bedroht.

Third-Party-Risk muss KI-Subprozessoren und Datenresidenzketten einschließen. Führen Sie quartalsweise VUCA-Reviews der Plattformstrategie durch und koppeln Sie Dimensionen an SRE-, Discovery- und Comms-KPIs.

Boards sollten Security und Reliability als Volatilitätsprobleme sehen: Incident-Frequenz, Patch-Latenz und kundensichtbare Ausfälle gehören auf dieselbe Folie wie Revenue Guidance. Talentvolatilität braucht Nachfolgepläne für Principal Engineers und Wissensübergabe vor Reorgs.

Commercial Leaders koppeln Pricing-Experimente an Volatilitätstrigger—bei Überschreiten von Cloud- oder Training-Kostenbändern pausieren automatische Gates breite Rabatte bis Finance und Product gemeinsam freigeben. OSS-Program Offices halten eine License-Matrix und automatisierte Scans. Trust-Metriken stehen neben Deployment Frequency. Multi-Cloud-Commitments sind Unsicherheitswetten—Exit-Kosten und Portabilitätstests vor Mehrjahresspends dokumentieren.""",
        "zh": """科技公司因产品半衰期缩短、平台规则变化与安全威胁按季度重画路线图而放大 VUCA。易变性体现为云支出波动、人才市场飙升，以及一夜重置竞争位势的模型发布周期。

不确定性在于 AI 监管、开源许可争议，以及企业买家等待预算清晰后再承诺。复杂性跨越微服务、数据管道、授权体系与支持分层——各自独立值班。一次定价变更可波及计费、销售提成与客户成功手册。

定位上的模糊性很常见：人人自称 AI 领先，客户对安全与隐私承诺的解读因地区而异。强工程组织把特性开关、灰度发布与显式权衡的错误预算结合，作为易变性缓冲。

不确定下的探索轨道应设时长上限与预设成功指标。架构决策记录通过写明边界理由降低复杂性债务。包容性设计评审降低 UX 文案与同意流程的模糊性。用量波动威胁收入挂钩 SLA 时，可靠性成为董事会议题。

第三方风险须纳入 AI 子处理者与数据驻留链，而非仅经典 SaaS。每季度对平台战略做 VUCA 审视，并将各维映射到已有的 SRE、产品发现与传播指标。

董事会应将安全与可靠性视为易变性问题：事故频率、补丁延迟、客户可见停机应与收入指引同页。人才易变性需要首席工程师继任计划与重组前的知识移交，否则复杂性债务会在新团队名下重现。

商业负责人应将定价实验与易变触发对齐——云成本或模型训练支出月度越界时，自动闸门暂停大规模折扣，直至财务与产品共同签核。开源项目办公室以统一许可矩阵与每次合并的自动扫描降低法律模糊性。将支持积压、升级率与公开问题线程等信任指标放在部署频率旁。多云承诺是不确定性押注——在签署多年支出前记录退出成本、可移植性测试与数据重力假设。""",
    },
    "education": {
        "ja": """教育システムは人口動態、財政ルール、技術採用、カリキュラム価値をめぐる公共議論からVUCAに直面します。変動性は入学数の振れ、代替教員の供給、評価・認証政策の急変として現れます。

不確実性は長期資本計画に影響します。ハイブリッドは続くか、雇用主は技能をどう認定するか、どの助成金が予算サイクルを生き残るか。

複雑性は学務、学生支援、IT、施設が局所最適する一方で学生は一つの旅路として体験するときに生じます。LMS導入は教育法、アクセシビリティ、プライバシー、ヘルプデスク負荷を同時に触ります。

厳密さ・公正・コンピテンシーといった言葉には曖昧さが残り、目標には合意しても定義では割れます。強靭な機関は透明な入学シナリオを公開し、緊縮トリガーをアメニティより教育の質の保護に結びます。

横断カリキュラム委員会が依存をマップし、一般教育の変更が専攻パスを壊さないようにします。デジタルエクイティは端末物流・帯域・サポート時間を一体で動かします。争議・天候休校・論争時の広報手順が曖昧さを減らします。企業連携には入学コミットとデータ利用の不確実性条項を含めます。

本サイトの組織診断とシナリオテンプレートで、学務・事務ユニットの準備度を四半期ごとに採点してください。認証サイクルは不確実性のマイルストーンです。証拠収集を早期に始め、成果物をVUCA次元にタグ付けすると審査側に体系的準備が見えます。

教職員の共有ガバナンスは、組合契約・州の命令・寄付者期待が重なるときの曖昧さを下げます。危機前に意思決定原則を公開し、暫定リーダーが圧力下で政策を発明しないようにします。学生成功アナリティクスは「リスク」ラベルの意味がアドバイザー・教務・奨学金で異なると曖昧性を増幅します。運用定義を公開し、学期ごとにモデルを監査してください。

コミュニティカレッジと研究大学では変動プロファイルが異なるため、異種機関のテンプレをそのまま持ち込まずVUCAプレイブックをカスタムします。非常勤雇用サイクルの変動性指標（充足率、休講数、単位スループット）を明示し、学期末サーベイ前に教学インパクトを見える化します。

同窓会・財団関係は危機広報に複雑性を加えます。論争的講演や研究発表向けの事前合意ステートメントがニュースサイクル圧縮時の場当たり曖昧性を減らします。留学生フローは変動ドライバーのままです。ビザ政策の不確実性を入学シナリオと住居計画に入れ、補助サービスが曖昧な政策窓で過剰建設しないようにします。設備更新委員会は遅延保全バックログを建物システムの複雑性マップに結び、同一ベンダー連鎖を変動情報付きポートフォリオとして順序付けます。""",
        "de": """Bildungssysteme erleben VUCA durch demografischen Wandel, Finanzierungsregeln, Technologieadoption und öffentliche Debatten über Curriculum-Werte. Volatilität zeigt sich in Einschreibungsschwankungen, Vertretungsengpässen und abrupten Assessment-/Akkreditierungspolitiken.

Unsicherheit trifft langfristige Kapitalpläne: Bleibt Hybrid, wie zertifizieren Arbeitgeber Skills, welche Grants überleben Budgetzyklen?

Komplexität entsteht, wenn Fakultäten, Student Services, IT und Facilities lokal optimieren, während Studierende eine Journey erleben. Ein LMS-Rollout berührt Didaktik, Accessibility, Privacy und Helpdesk gleichzeitig.

Mehrdeutigkeit umgibt Begriffe wie Rigor, Equity und Kompetenz. Resiliente Institutionen publizieren transparente Einschreibungsszenarien und koppeln Austerity-Trigger an Unterrichtsqualität vor Amenities.

Curriculum-Gremien mappen Abhängigkeiten. Digitale Equity braucht Geräte, Bandbreite und Supportstunden gemeinsam. Kommunikations-Playbooks senken Mehrdeutigkeit bei Streiks, Wetterschließungen oder Kontroversen. Arbeitgeberpartnerschaften brauchen Unsicherheitsklauseln zu Einschreibung und Datennutzung.

Nutzen Sie Organisationsdiagnose und Szenario-Vorlagen dieser Website für Quartals-Scores. Akkreditierungszyklen sind Unsicherheitsmeilensteine—Evidenz früh sammeln und Artefakte an VUCA-Dimensionen taggen.

Shared Governance senkt Mehrdeutigkeit, wenn Tarifverträge, Landesvorgaben und Spendererwartungen überlappen. Veröffentlichen Sie Entscheidungsprinzipien vor Krisen. Student-Success-Analytics verstärken Mehrdeutigkeit, wenn „at-risk“ unterschiedlich definiert ist—Operational Definitions publizieren und Modelle je Term auditieren.

Community Colleges und Forschungsunis haben unterschiedliche Volatilitätsprofile—Playbooks anpassen. Adjunct-Hiring-Volatilität braucht Metriken (Fill Rates, Absagen, Credit-Hour-Throughput). Alumni-/Foundation-Relationen erhöhen Kommunikationskomplexität; vorverhandelte Holding Statements helfen. Internationale Studierendenströme bleiben Volatilitätstreiber—Visapolitik in Einschreibungs- und Wohnszenarien einspeisen. Kapitalplanung sollte Instandhaltungsrückstände an Komplexitätskarten von Gebäudesystemen koppeln und unter volatilitätsinformiertem Portfolio sequenzieren.""",
        "zh": """教育系统因人口结构变化、经费规则、技术采纳与课程价值的公共争论而面对 VUCA。易变性体现为招生波动、代课供给以及评估与认证政策突变。

不确定性影响长期资本规划：混合式教学会否延续、雇主如何认证技能、哪些拨款能跨过预算周期。

当教务、学生服务、IT 与后勤各自局部最优，而学生体验是一条旅程时，复杂性出现。学习管理系统上线同时牵动教学法、无障碍、隐私与服务台负荷。

严谨、公平、能力等词汇仍存模糊——目标可共识，定义却易分裂。有韧性的院校公开招生情景，并将紧缩触发优先绑定教学质量而非配套设施。

跨学科课程委员会应绘制依赖，避免通识改动破坏专业路径。数字公平需设备物流、带宽与支持时段同步推进。罢工、天气停课或舆论争议时的传播手册可降低模糊性。校企合作应包含招生承诺与数据使用的不确定性条款。

请用本站组织诊断与情景模板，每季度评估教学与行政单元准备度。认证周期是不确定性里程碑——尽早收集证据，并将材料按 VUCA 维度标注，便于评审看到系统准备。

教职工共享治理可在工会合同、州指令与捐赠人期望重叠时降低模糊性；危机前公布决策原则，避免临时负责人在压力下发明政策。学生成功分析若「风险」标签在顾问、教务与资助办含义不同，会放大模糊性——公布操作定义并每学期审计模型。

社区学院与研究型大学的易变画像不同，勿照搬异类机构模板，应定制 VUCA 手册。兼职聘用周期需要显式易变指标（满班率、停课数、学分吞吐），以便在学期末调查前看见教学影响。校友与基金会关系增加危机传播复杂性；对争议演讲或研究成果预备统一口径。国际学生流动仍是易变驱动——将签证政策不确定性写入招生与住宿情景。基建委员会应将延迟维护积压映射到楼宇系统复杂性图，并在波动知情的组合下排序同一供应商链条。""",
    },
}

DIM_PARAS_EXTRA = {
    "volatility": {
        "ja": [
            "変動性は、重要変数がどれだけ速く・大きく動くかを示します。市場価格、投入コスト、人材供給、サイバーリスクは四半期のあいだに急変し得ます。変動性そのものは機会にもなり得ますが、硬直した計画を罰します。",
            "リーダーは余力（スラック）、供給の多元化、意思決定サイクルに合わせた監視頻度で対応します。財務バッファ、モジュール型プロダクト、クロストレーニングされたチームはショック後の回復時間を短縮します。",
            "単なる季節性との違いは振幅の予測困難さです。ダッシュボードは水準だけでなく変化率を追跡し、閾値超過時の決裁権を事前に決めておいてください。",
        ],
        "de": [
            "Volatilität beschreibt, wie schnell und wie stark zentrale Variablen schwanken. Märkte, Inputkosten, Personalverfügbarkeit und Cyberrisiken können innerhalb eines Quartals springen. Volatilität ist nicht per se negativ—sie belohnt vorbereitete Organisationen—bestraft aber starre Pläne.",
            "Antworten sind Pufferressourcen, diversifizierte Lieferanten und Überwachungsrhythmen, die zu Entscheidungszyklen passen. Finanzpuffer, modulare Produktarchitekturen und cross-trainierte Teams verkürzen die Erholungszeit nach Schocks.",
            "Unterscheiden Sie Volatilität von Saisonalität: volatile Regime zeigen unvorhersagbare Amplitude. Dashboards sollten Änderungsraten tracken, nicht nur Niveaus, und Schwellen mit klaren Entscheidungsrechten verbinden.",
        ],
        "zh": [
            "易变性描述关键变量变化的速度与幅度。市场、成本、人才供给与网络风险都可能在一个季度内急剧波动。易变本身未必负面——对有准备的组织可成机会——但会惩罚僵化计划。",
            "领导者以冗余资源、供应多元化，以及匹配决策周期的监测节奏应对。财务缓冲、模块化产品架构与交叉培训团队可缩短冲击后的恢复时间。",
            "易变不同于单纯季节性：易变区间的振幅难以预测。仪表盘应追踪变化率而非仅看水平，并事先约定阈值触发后的决策权。",
        ],
    },
    "uncertainty": {
        "ja": [
            "不確実性は、結果の幅が広く確率そのものが争点になるときに現れます。規制草案、地政学シフト、新興技術が典型例です。",
            "探索型計画、実物オプション、段階投資はコミットメントリスクを下げます。前提を記録した意思決定ログを残し、事実が変わったときに再訪できるようにします。",
            "定量モデルと定性シナリオを併用してください。モデルが食い違うときは合意を強要せず、相違点を文書化します。",
        ],
        "de": [
            "Unsicherheit entsteht, wenn die Ergebnisspanne groß und Wahrscheinlichkeiten umstritten sind. Regulatorische Entwürfe, geopolitische Verschiebungen und neue Technologien landen oft hier.",
            "Discovery-driven Planning, Real Options und gestufte Investments senken Commitment-Risiko. Ein Entscheidungslog mit Annahmen erlaubt Neubewertung, wenn Fakten wechseln.",
            "Kombinieren Sie quantitative Modelle mit qualitativen Szenarien. Bei Modellkonflikten dokumentieren Sie die Differenz statt Konsens zu erzwingen.",
        ],
        "zh": [
            "当结果区间很宽、概率本身存在争议时，就是不确定性。监管草案、地缘变化与新兴技术常落在这里。",
            "探索式规划、实物期权与分阶段投资可降低承诺风险。维护记录假设的决策日志，事实变化时可回头修订。",
            "将定量模型与定性情景并用。模型不一致时记录分歧，而不是强行统一口径。",
        ],
    },
    "complexity": {
        "ja": [
            "複雑性は相互依存を増幅します。一つの方針変更が部門横断のインセンティブを組み替えます。医療パス、プラットフォーム生態系、グローバル供給網が典型です。",
            "システムマップ、境界付き実験、ネットワーク・スチュワードが有効です。グラフ上の隣接部門へ失敗を押し出す局所KPI最適化を避けてください。",
            "拡大前に小さな安全失敗可能なプローブを使います。複雑性は英雄的単一計画より学習を報います。",
        ],
        "de": [
            "Komplexität vervielfacht Abhängigkeiten: eine Policy-Änderung verdrahtet Anreize über Abteilungen hinweg. Klinische Pfade, Plattform-Ökosysteme und globale Liefernetze sind klassische Beispiele.",
            "Systemkarten, begrenzte Experimente und Network Stewards helfen. Vermeiden Sie lokale KPIs, die Scheitern an Nachbarn im Netzwerk exportieren.",
            "Nutzen Sie kleine safe-to-fail-Proben vor dem Skalieren. Komplexität belohnt Lernende, nicht Hero-Pläne.",
        ],
        "zh": [
            "复杂性放大相互依赖：改一项政策会重接跨部门激励。临床路径、平台生态与全球供应网是典型场景。",
            "系统图、边界清晰的实验与网络 steward 有帮助。避免用局部 KPI 把失败导出给邻接环节。",
            "放大前先做可安全失败的小探针。复杂性奖励学习，而不是单一英雄式计划。",
        ],
    },
    "ambiguity": {
        "ja": [
            "曖昧性とは、言語・文化・不完全データにより複数の妥当な物語が残る状態です。合併、AI倫理、対外広報がしばしばここに入ります。",
            "ファシリテートされた対話、ナラティブテスト、用語の明示的定義が摩擦を減らします。アジリティや変革など多義語には共有用語集を用意します。",
            "リーダーは未知と不可知を分けて示します。聴衆ごとに必要な安心の質が異なります。",
        ],
        "de": [
            "Mehrdeutigkeit bedeutet, dass Sprache, Kultur oder unvollständige Daten mehrere plausible Deutungen zulassen. Mergers, KI-Ethik und öffentliche Botschaften sitzen oft hier.",
            "Moderierter Dialog, Narrative-Tests und klare Begriffsdefinitionen reduzieren Reibung. Legen Sie Glossare für überladene Wörter wie Agilität oder Transformation an.",
            "Führungskräfte sollten Unbekanntes von Unwissbarem trennen—unterschiedliche Publika brauchen unterschiedliche Sicherheit.",
        ],
        "zh": [
            "模糊性指语言、文化或不完整数据使多种合理解释并存。并购、AI 伦理与对外传播常落在这里。",
            "引导式对话、叙事测试与明确术语定义可降低摩擦。对「敏捷」「转型」等多义词应维护共享术语表。",
            "领导者应区分未知与不可知——不同受众需要不同层面的说明与安抚。",
        ],
    },
}

CASE_BODY_EXTRA = {
    "netflix": {
        "ja": [
            "Netflixは技術・ライセンス市場の変動性の事例です。経営陣は短期の粗利圧力を受け入れつつ、ブロードバンド普及に早期ベットし、ストリーミング能力を蓄積しました。",
            "スタジオ契約の不確実性はオリジナル投資を後押ししました。コストは上がりますが、曖昧な更新条件への依存は下がります。",
            "CDN・エンコード・パーソナライズなど複雑なプラットフォーム運用には、サービス所有が明確なモジュール型チームが必要でした。",
        ],
        "de": [
            "Netflix zeigt Volatilität in Technologie- und Lizenzmärkten. Die Führung setzte früh auf Breitband und nahm kurzfristigen Margendruck in Kauf, um Streaming-Kompetenz aufzubauen.",
            "Unsicherheit bei Studioverträgen trieb Investitionen in Originals—teurer, aber weniger abhängig von mehrdeutigen Verlängerungen.",
            "Komplexe Plattformoperationen (CDN, Encoding, Personalisierung) brauchten modulare Teams mit klarer Service-Ownership.",
        ],
        "zh": [
            "Netflix 体现了技术与授权市场的易变性。管理层早期押注宽带普及，承受短期毛利压力以积累流媒体能力。",
            "片厂合同的不确定性推动自制内容投资——成本上升，但对模糊续约条款的依赖下降。",
            "CDN、编码与个性化等复杂平台运营，需要服务所有权清晰的模块化团队。",
        ],
    },
    "toyota": {
        "ja": [
            "トヨタのリーンは現場の複雑性を抑えつつ問題を素早く可視化します。世界的供給混乱の後、重要半導体にはジャストインタイムと戦略在庫の再バランスを図りました。",
            "地政学の曖昧さに対しては調達多角化を進め、規制当局と労働組合へ一貫した説明を維持しました。変動性（供給ショック）と複雑性（工程相互依存）を分けて学習することが次のプレイブックを強くします。",
        ],
        "de": [
            "Toyotas Lean puffert Komplexität in der Fertigung und macht Probleme schnell sichtbar. Nach globalen Lieferstörungen balancierte das Unternehmen Just-in-time mit strategischen Halbleiterbeständen.",
            "Geopolitische Mehrdeutigkeit erforderte diversifizierte Beschaffung und konsistente Kommunikation gegenüber Regulierern und Gewerkschaften.",
        ],
        "zh": [
            "丰田精益在抑制车间复杂性的同时快速暴露问题。全球供应冲击后，对关键芯片在准时制与战略库存之间再平衡。",
            "地缘模糊性推动采购多元化，并对监管与工会保持一致表述。把易变性（供应冲击）与复杂性（工序相互依赖）分开学习，能强化下一版行动手册。",
        ],
    },
}
