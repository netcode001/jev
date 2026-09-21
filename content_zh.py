# -*- coding: utf-8 -*-
"""Chinese (Simplified) page content for Jev Hub."""

from datetime import date

CRUMB_HOME = [("首页", "/zh/")]


def faq_html_and_schema():
    groups = {}
    for cat, q, a in FAQS:
        groups.setdefault(cat, []).append((q, a))
    titles = {"basics": "基础认知", "access": "获取接入", "pricing": "价格", "technical": "技术细节", "trust": "可信度与来源"}
    html, schema_entities = [], []
    for cat, qs in groups.items():
        html.append(f'<h2 id="{cat}">{titles[cat]}</h2>')
        for q, a in qs:
            html.append(f'<details><summary>{q}</summary><div class="a">{a}</div></details>')
            schema_entities.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a.replace("<strong>", "").replace("</strong>", "")}})
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": schema_entities}
    return "\n".join(html), schema


NEWS = [
    ("2026-09-21", "Jev 全面开放：取消 waitlist，注册即送 $5 额度",
     "TypeSafe 完全取消排队，console.typesafe.ai 开放注册，新用户送 $5 额度（约 1.2 亿输入 tokens）。Vercel、Cloudflare 渠道路径不变。",
     "console.typesafe.ai / 36kr"),
    ("2026-09-18", "第三方分析提醒：Jev 评测数据需谨慎看待",
     "多家独立媒体（The Tech Society、DataCamp、dev.to）汇总了 Jev 的数据并指出：4 工作流基准由厂商自行设计运行，「准确率」是与 GPT-6 Astra、Claude Fable 5.1 共识标签的一致性，并非真实标准答案。所有分析都建议先在自己的业务流量上实测。",
     "digitalstrategy-ai.com"),
    ("2026-09-17", "TypeSafe 36 小时内放行 14 万 waitlist 用户",
     "上线后的需求洪峰中，TypeSafe 表示已在一个半昼夜间把 14 万排队用户全部放行，并建议新用户先用 Vercel AI Gateway。同期流传的生产数据包括：调度流程成本下降 71%、总耗时下降 90%；另有 1,018 篇论文分类仅花 $0.08、单篇中位延迟 256ms。",
     "marketbrief.now"),
    ("2026-09-16", "Jev 上架 Vercel AI Gateway",
     "Vercel CEO 确认 Jev 已通过 Vercel AI Gateway 提供（模型 ID：typesafe-ai/jev），并报告路由场景下 p95 响应最快提升 18 倍。这是目前绕开官方 waitlist 的最快路径。",
     "vercel.com / x.com"),
    ("2026-09-16", "Cloudflare、OpenRouter、LangChain 首日同步接入",
     "Cloudflare Workers AI 上线 typesafe/jev（32K 上下文），OpenRouter 上线 typesafe/jev-1.13（64K 上下文，输入 $0.042/1M、输出免费），LangChain 发布基于 langchain-typesafe 包的评测框架指南。",
     "openrouter.ai"),
    ("2026-09-15", "发布日：TypeSafe 推出 System One Models 与 Jev",
     "TypeSafe AI 发布 Jev：一个不生成文本、只返回类型化决策（Choice、Score、Noul）+ 校准置信度的新模型。官方口径：System One 工作流上比前沿 LLM 快 193.6 倍、便宜 444.6 倍；输入 $0.042/1M tokens、输出免费；结构上保证 0% 格式错误。",
     "typesafe.ai"),
]

FAQS = [
    ("basics", "Jev 是什么？一句话说明",
     "Jev 是 TypeSafe 推出的「System One」AI 模型：你输入一段文本（state）和若干带类型的问题，它返回选项、评分或真/假概率，并附带置信度——它永远不会生成自由文本。"),
    ("basics", "Jev 的三种题型是什么？",
     "<strong>Choice</strong>（从你定义的选项中选一个）、<strong>Score</strong>（低/中/高/危急这类有序评分）、<strong>Noul</strong>（TypeSafe 自创的类型：一个陈述为真的概率，例如 0.95）。多个问题可以合并进同一次请求。"),
    ("basics", "为什么叫「System One」模型？",
     "借用卡尼曼《思考，快与慢》的概念：System 1 是快速、直觉式的判断。Jev 负责处理海量的快速有限判断（路由、评分、审批），让「System 2」式的慢思考——前沿 LLM 或人类——只花在真正重要的地方。"),
    ("basics", "Jev 能替代 ChatGPT 或 Claude 吗？",
     "不能。Jev 不会写文章、写邮件、做摘要，也无法开放式推理。它是补充角色：接管 LLM 技术栈里的结构化判断环节，让昂贵的生成模型少被调用。"),
    ("access", "必须等 TypeSafe 官方 waitlist 吗？",
     "不用了。2026 年 9 月 20 日起 Jev 全面开放、取消排队：直接在 console.typesafe.ai 注册，新用户送 $5 额度（约 1.2 亿 tokens）。Vercel AI Gateway（typesafe-ai/jev）与 Cloudflare Workers AI（typesafe/jev）也可直接调用。"),
    ("access", "有免费的网页试用吗？",
     "有。获批用户可使用 console.typesafe.ai/playground：左侧粘贴文本作为 state，用大白话写问题，选好题型，点运行——一秒内返回带置信度的结果。Choice、Score、Noul 可以混在一次运行里。"),
    ("access", "官方提供哪些 SDK？",
     "TypeSafe 官方提供 Python 和 JavaScript/TypeScript SDK，另有框架集成：Vercel AI SDK（@ai-sdk/typesafe）和 LangChain（langchain-typesafe 包）。"),
    ("access", "速率限制是多少？",
     "早期访问默认约为每秒 25 万 tokens、每分钟 1200 次请求，企业协议可提升。这是上线初期数字，可能调整。"),
    ("pricing", "Jev 多少钱？",
     "参考价：输入 $0.042 / 100 万 tokens（约 $42 / 10 亿），输出完全免费——因为返回的是紧凑的类型化决策而非长文本。按 state 长度不同，单次决策成本大约在 $0.0001 或更低。"),
    ("pricing", "输出真的免费？",
     "是的。所有渠道输出都按 $0 计费。输出是紧凑的类型化决策（一个选项、一个评分、一个概率），不是生成的 token 流。"),
    ("pricing", "和 LLM 比价格差多少？",
     "TypeSafe 称 $0.042/1M 的输入价约为「Claude Fable 5.1」的 1/238，约为 GPT-5.6 Terra（$2.00/1M）的 1/48——而且这些模型还要收 $2–$12/1M 的输出费，Jev 一分不收。完整对比见价格页。"),
    ("pricing", "这个激进定价会变吗？",
     "会——TypeSafe 自己也很坦率：无法证明定价没有补贴，长期可持续性有待验证，但它预计价格只会降不会涨。当前价格是发布期数字，不是保证。本站动态页会自动追踪价格变化。"),
    ("technical", "Jev 不能做什么？",
     "不能生成文本或解释；只支持文本输入（暂不支持图片/音频）；不能做算术和日期计算（交给代码）；上下文窗口 64K（Cloudflare 为 32K）；对无关上下文敏感——发送前请清理 state 中的噪音。"),
    ("technical", "「零幻觉」是真的吗？",
     "准确地说：它不可能产生文本幻觉，因为它根本不生成文本；schema 保证使它只能返回你定义过的选项（结构性 0% 格式错误）。但「格式有效的答案」仍可能是「错误答案」且带着高置信度——自动化之前先在自己的数据上校准阈值。"),
    ("technical", "API 长什么样？",
     "一次 HTTP 调用：POST https://api.typesafe.ai/v1/systemone（model: jev-latest），body 里带 state 字符串和类型化问题字典，响应返回每个答案及其概率。可复制粘贴的快速上手见「获取方式」页。"),
    ("technical", "Jev 速度有多快？",
     "官方口径端到端 70–500ms，社区实测约 200–260ms 中位延迟。TypeSafe 的头条数字是：System One 工作流上比文本生成模型快 193.6 倍。"),
    ("trust", "Jev 的评测数据可信吗？",
     "当作「有前景但未经独立验证」来看。4 工作流基准（67.8% 准确率、$0.0004/例）由 TypeSafe 设计并运行，打分对象是与 GPT-6 Astra、Claude Fable 5.1 共识标签的一致性——TypeSafe 自己承认这偏向 OpenAI 和 Anthropic。目前尚无中立框架的独立复现。"),
    ("trust", "openjev 是什么？",
     "一个开源社区项目，通过读取小开源模型 logits 上的类型化选项概率，复刻了 Jev 的接口模式——说明「类型化决策」这一原语的生命周期可能超过任何单一厂商。"),
    ("trust", "TypeSafe AI 是谁？",
     "TypeSafe AI 是一家初创公司，围绕名为 RLCD（Reinforcement Learning for Calibrated Decisions，面向校准决策的强化学习）的新训练算法打造了 Jev。2026 年 9 月发布后几天内 waitlist 人数超过 14 万。"),
    ("trust", "Jev Hub 的信息从哪来？",
     "来自 TypeSafe 官网与文档、各渠道商列表（OpenRouter、Cloudflare、Vercel）、Hacker News 与 Reddit 讨论、以及独立媒体分析——每条动态都附来源链接。厂商自报的数据我们一律标注，并随新信息自动更新本站。"),
]


PAGES = {}

# ---- index ----
PAGES["index"] = {
    "title": "Jev AI 中文站：价格、获取方式、评测与动态追踪 | Jev Hub",
    "desc": "关于 TypeSafe AI 旗下 System One 模型 Jev 的独立中文信息站：它是什么、各渠道价格、带保留意见的评测数据、开放注册与免费额度的接入路径，以及自动更新的最新动态。",
    "crumb": [("首页", None)],
    "schema": [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Jev Hub", "url": "https://jevhub.ai/zh/",
         "description": "Jev（TypeSafe AI System One 模型）中文追踪站。", "inLanguage": "zh"},
        {"@context": "https://schema.org", "@type": "Organization", "name": "Jev Hub",
         "url": "https://jev-ai.live/zh/", "logo": "https://jev-ai.live/og/zh-index.png",
         "slogan": "把 Jev AI 讲清楚：价格、接入、评测与动态，一站看完"},
    ],
    "body": """
<div class="hero">
  <div class="eyebrow"><span class="dot"></span> SYSTEM ONE MODEL · BY TYPESAFE AI · 2026</div>
  <h1>Jev AI <span class="accent">一次讲清</span>：价格、接入、评测与动态。</h1>
  <p class="lede">Jev 不写文字，它返回<strong>带校准置信度的类型化决策</strong>。2026 年 9 月 15 日发布，几天内 14 万多人排队——9 月 20 日起全面开放：无需排队，注册送 $5 额度。这个站持续回答：它是什么、多少钱、怎么用上。</p>
  <div class="hero-cta">
    <a class="btn btn-primary" href="/zh/get-access/">免费开始 — 送 $5 额度</a>
    <a class="btn btn-ghost" href="/zh/what-is-jev/">Jev 是什么？</a>
  </div>
  <div class="stat-grid">
    <div class="stat"><div class="num">193.6x</div><div class="lbl">比前沿 LLM 更快（厂商自报）</div></div>
    <div class="stat"><div class="num">444.6x</div><div class="lbl">单位工作流成本更低（厂商自报）</div></div>
    <div class="stat"><div class="num alt">$0.042</div><div class="lbl">每 100 万输入 tokens，输出免费</div></div>
    <div class="stat"><div class="num warn">$5</div><div class="lbl">注册即送额度 — 全面开放，无需排队</div></div>
  </div>
</div>

<section>
  <div class="kicker">01 · 什么是 Jev</div>
  <h2>30 秒看懂 Jev</h2>
  <p>Jev 读取一段文本（<strong>state</strong>）加上你定义的问题，返回三种类型化答案之一——从你的选项中选一个的 <strong>Choice</strong>、有序 <strong>Score</strong> 评分、或 <strong>Noul</strong> 真/假概率——每个都带置信度。因为答案格式在架构层就固定了，它不可能编造文本，运行速度比聊天模型快 20–200 倍、成本低 40–400 倍。你的代码设定置信度阈值：Jev 有把握就自动执行，没把握就升级给人工或前沿 LLM。</p>
  <p><a href="/zh/what-is-jev/">阅读完整解读 →</a></p>
</section>

<section>
  <div class="kicker">02 · 最新动态</div>
  <h2>Jev 动态，每日追踪</h2>
  <div class="timeline">
    {NEWS_PREVIEW}
  </div>
  <p><a href="/zh/news/">查看完整时间线 →</a></p>
</section>

<section>
  <div class="kicker">03 · 接入</div>
  <h2>今天就能用上 Jev</h2>
  <p>Jev 已于 9 月 20 日全面开放、排队取消。可以直接注册，也可以走渠道商：</p>
  <div class="card-grid">
    <a class="card" href="/zh/get-access/#console"><span class="tag">已开放</span><h2>TypeSafe 控制台</h2><p>console.typesafe.ai — 注册送 $5 额度（约 1.2 亿 tokens），含 Playground 与 API key。</p></a>
    <a class="card" href="/zh/get-access/#vercel"><span class="tag">最快</span><h2>Vercel AI Gateway</h2><p>typesafe-ai/jev — 发布当天上线，Vercel 用户无需单独注册。</p></a>
    <a class="card" href="/zh/get-access/#cloudflare"><span class="tag">边缘</span><h2>Cloudflare Workers AI</h2><p>typesafe/jev — 32K 上下文，边缘节点运行，按请求计费。</p></a>
  </div>
</section>

<section>
  <div class="kicker">04 · 价格</div>
  <h2>价格速览</h2>
  <div class="table-wrap">
    <table>
      <thead><tr><th></th><th>Jev</th><th>典型聊天 LLM</th></tr></thead>
      <tbody>
        <tr><td><strong>输入</strong></td><td class="mono good">$0.042 / 1M tokens</td><td class="mono">$0.25 – $3.00 / 1M tokens</td></tr>
        <tr><td><strong>输出</strong></td><td class="mono good">$0（免费）</td><td class="mono">$2 – $15 / 1M tokens</td></tr>
        <tr><td><strong>延迟</strong></td><td class="mono good">70–500 ms</td><td class="mono">2 – 80 s</td></tr>
        <tr><td><strong>返回内容</strong></td><td>类型化决策 + 置信度</td><td>自由文本</td></tr>
      </tbody>
    </table>
  </div>
  <p><a href="/zh/pricing/">完整渠道对比 + 成本计算器 →</a></p>
</section>

<section>
  <div class="kicker">05 · 开始探索</div>
  <h2>站点导航</h2>
  <div class="card-grid">
    <a class="card" href="/zh/what-is-jev/"><span class="tag">指南</span><h2>Jev 是什么？</h2><p>System One 模型详解：题型原语、架构、评测数据与诚实的局限性。</p></a>
    <a class="card" href="/zh/use-cases/"><span class="tag">打法</span><h2>10 个使用场景</h2><p>路由、工单分诊、护栏、RAG 过滤——附社区真实数据。</p></a>
    <a class="card" href="/zh/vs-llm/"><span class="tag">决策</span><h2>Jev vs 大模型</h2><p>什么时候便宜的类型化模型赢，什么时候仍需要前沿 LLM。</p></a>
    <a class="card" href="/zh/ecosystem/"><span class="tag">生态</span><h2>生态项目</h2><p>openjev、jev-ultrafast、pg-jev 等十余个社区项目。</p></a>
    <a class="card" href="/zh/faq/"><span class="tag">答疑</span><h2>常见问题</h2><p>20 个问题直接回答：接入、价格、限制、哪些数字别轻信。</p></a>
    <a class="card" href="/"><span class="tag">English</span><h2>English version</h2><p>The full English edition, kept in sync with this site.</p></a>
  </div>
</section>
""",
}

# ---- what-is-jev ----
PAGES["what-is-jev"] = {
    "title": "Jev 是什么？TypeSafe System One 模型完整解读（2026）",
    "desc": "Jev 完整中文指南：System One 模型原理、Choice/Score/Noul 三种题型、RLCD 训练方法、带保留意见的评测数据、价格与局限性。",
    "crumb": CRUMB_HOME + [("Jev 是什么", None)],
    "schema": [{
        "@context": "https://schema.org", "@type": "Article",
        "headline": "Jev 是什么？TypeSafe System One 模型完整解读",
        "datePublished": "2026-09-20", "dateModified": date.today().isoformat(),
        "author": {"@type": "Organization", "name": "Jev Hub"},
        "publisher": {"@type": "Organization", "name": "Jev Hub"},
        "about": {"@type": "SoftwareApplication", "name": "Jev", "applicationCategory": "AI Model"},
    }],
    "body": """
<p class="updated">最后更新：2026-09-20 · 来源：typesafe.ai、渠道商列表、独立媒体（文中附链接）</p>
<h1>Jev 是什么？TypeSafe System One 模型完整解读</h1>
<p class="lede">Jev 是 TypeSafe AI 于 2026 年 9 月 15 日发布的全新模型品类——<strong>System One Models</strong>——的第一个成员。它不生成文本，而是针对你的输入回答带类型的问题，返回附带校准置信度的结构化决策。这篇指南讲清它的工作原理、能做什么不能做什么，以及哪些说法你应该亲自验证。</p>

<div class="toc"><div class="t">本页目录</div>
<ol>
  <li><a href="#tldr">太长不看版</a></li>
  <li><a href="#problem">聊天模型的问题</a></li>
  <li><a href="#how">Jev 怎么工作</a></li>
  <li><a href="#primitives">三种题型原语</a></li>
  <li><a href="#benchmarks">评测数据——及其水分</a></li>
  <li><a href="#pricing">价格速览</a></li>
  <li><a href="#limits">局限性</a></li>
  <li><a href="#mental">正确的心智模型</a></li>
  <li><a href="#access">怎么试用</a></li>
</ol></div>

<h2 id="tldr">太长不看版</h2>
<ul>
  <li><strong>是什么：</strong>一个返回类型化决策（选项、评分或真/假概率）+ 置信度的模型——绝不输出自由文本。</li>
  <li><strong>为什么重要：</strong>在结构化决策工作流上比前沿 LLM 快约 193.6 倍、便宜约 444.6 倍（TypeSafe 自报数字），因为没有逐 token 的串行生成。</li>
  <li><strong>价格：</strong>输入 $0.042 / 1M tokens，输出免费。</li>
  <li><strong>现状：</strong>已全面开放（2026-09-20 起）——console.typesafe.ai 注册送 $5 额度，或经 Vercel / Cloudflare 渠道调用。</li>
  <li><strong>注意：</strong>评测为厂商自跑、无独立复现；格式正确的答案仍可能带着高置信度出错。</li>
</ul>

<h2 id="problem">聊天模型的问题</h2>
<p>RLHF 时代的 LLM 为「产出人类喜欢的文字」而优化。这让它们在遵循指令上超越人类——但作为软件组件却不可靠：模式坍缩、过度自信、编造自由文本、每个答案都裹着散文。如果你的应用真正需要的是「这张工单属于这 4 类中的哪一类」或「这个来源是否支持这个论断」，聊天模型是一条昂贵又嘈杂的路径，只为得到一个比特的答案。</p>
<p>TypeSafe 的赌注是：人们目前交给 LLM 的相当大一部分工作，其实是<strong>披着聊天外衣的结构化决策</strong>——这部分理应拥有自己的模型品类，原生地被机器消费。</p>

<h2 id="how">Jev 怎么工作</h2>
<h3>输入：state + 类型化问题</h3>
<p>一次 HTTP 请求包含 <strong>state</strong>（待判断的文本块——工单、段落、日志）和一个或多个<strong>问题</strong>，每个问题有固定的答案类型。响应在单次调用中返回所有答案及概率。</p>
<pre><code>{
  <span class="c-key">"state"</span>: <span class="c-str">"我的 Stripe 账户连了 3 天一直失败，我正在丢单。"</span>,
  <span class="c-key">"questions"</span>: {
    <span class="c-key">"urgency"</span>:   { <span class="c-key">"type"</span>: <span class="c-str">"noul"</span>,   <span class="c-key">"statement"</span>: <span class="c-str">"这条消息表达了紧急感。"</span> },
    <span class="c-key">"category"</span>:  { <span class="c-key">"type"</span>: <span class="c-str">"choice"</span>, <span class="c-key">"options"</span>: [<span class="c-str">"账务"</span>, <span class="c-str">"技术"</span>, <span class="c-str">"销售"</span>, <span class="c-str">"垃圾信息"</span>] },
    <span class="c-key">"frustration"</span>:{ <span class="c-key">"type"</span>: <span class="c-str">"score"</span>,  <span class="c-key">"scale"</span>: [<span class="c-str">"低"</span>, <span class="c-str">"中"</span>, <span class="c-str">"高"</span>, <span class="c-str">"危急"</span>] }
  }
}</code></pre>
<h3>训练：RLCD，而非 RLHF</h3>
<p>TypeSafe 为 Jev 设计了新架构、新采样器和名为 <strong>RLCD（Reinforcement Learning for Calibrated Decisions，面向校准决策的强化学习）</strong>的训练算法。优化目标是校准度——0.9 就应该真的代表 90% 概率——而不是人类对生成文风的偏好。这也是它无法输出无效答案的原因：输出形状在架构层固定，不靠提示词工程约束。</p>
<h3>输出：决策 + 置信度阈值</h3>
<p>策略由你的代码决定：高于 0.9 自动执行，0.6–0.9 之间升级给人工，再低就回退到前沿 LLM。TypeSafe 的原话：「在代码中组合这些决策来构建更大的工作流，由你掌控智能的使用方式。」</p>

<h2 id="primitives">三种题型原语</h2>
<div class="table-wrap">
<table>
  <thead><tr><th>原语</th><th>返回</th><th>示例问题</th></tr></thead>
  <tbody>
    <tr><td><strong>Choice</strong></td><td>选项之一 + 概率</td><td>「这张工单属于哪类？」→ 账务（0.91）</td></tr>
    <tr><td><strong>Score</strong></td><td>有序评分 + 概率</td><td>「这个告警多严重？」→ 高（0.87）</td></tr>
    <tr><td><strong>Noul</strong></td><td>陈述为真的概率</td><td>「这段话是否否认了它引用的论断？」→ 0.95</td></tr>
  </tbody>
</table>
</div>
<p>三种题型可共享同一次请求——常见做法是「投机式扇出」：把可能需要的所有问题一次性问出去，由代码挑选相关答案，因为输入是唯一计费项，多问几个问题几乎不增加成本。</p>

<h2 id="benchmarks">评测数据——及其水分</h2>
<p>TypeSafe 在 4 个工作流（安全事件响应、agent 轨迹可观测、发票处理、客服）上做了自建评测：</p>
<div class="table-wrap">
<table>
  <thead><tr><th>模型</th><th>准确率*</th><th>单例成本</th><th>延迟</th></tr></thead>
  <tbody>
    <tr><td><strong>Jev</strong></td><td class="mono">67.8%</td><td class="mono good">$0.0004</td><td class="mono good">0.4 s</td></tr>
    <tr><td>GPT-5.6 Terra</td><td class="mono">67.9%</td><td class="mono">$0.0304</td><td class="mono">10.1 s</td></tr>
    <tr><td>Claude Sonnet 5</td><td class="mono">67.8%</td><td class="mono">$0.117</td><td class="mono">78 s</td></tr>
    <tr><td>Claude Opus 5</td><td class="mono">73.1%</td><td class="mono">$0.1761</td><td class="mono">37.8 s</td></tr>
    <tr><td>GPT-5.6 Sol</td><td class="mono">74.1%</td><td class="mono">$0.0836</td><td class="mono">23.3 s</td></tr>
  </tbody>
</table>
</div>
<div class="callout warn"><div class="t">看星号再看表格</div>
<ul>
  <li><strong>*「准确率」是一致性，不是真值。</strong>共识标签由 GPT-6 Astra 与 Claude Fable 5.1 生成——它衡量的是与两个前沿模型的一致程度，TypeSafe 也承认这偏向 OpenAI 和 Anthropic。</li>
  <li><strong>厂商自跑。</strong>工作流、评测框架、运行全部由 TypeSafe 完成，尚无中立框架的独立复现。</li>
  <li><strong>「0% 错误」是结构性的。</strong>「零幻觉」「0% 格式错误」源自 schema 保证，不是测量结果。格式有效的答案仍可能是带高置信度的错误答案——这正是发布后 Hacker News 讨论最激烈的点。</li>
  <li><strong>社区共识：</strong>先在自己的流量上评测，再决定是否依赖这些数字。</li>
</ul>
</div>

<h2 id="pricing">价格速览</h2>
<div class="table-wrap">
<table>
  <thead><tr><th></th><th>Jev</th><th>GPT-5.6 Terra</th><th>Claude Sonnet 5</th></tr></thead>
  <tbody>
    <tr><td>输入 / 1M tokens</td><td class="mono good">$0.042</td><td class="mono">$2.00</td><td class="mono">$3.00</td></tr>
    <tr><td>输出 / 1M tokens</td><td class="mono good">$0</td><td class="mono">$12.00</td><td class="mono">$15.00</td></tr>
    <tr><td>单决策例成本</td><td class="mono good">~$0.0004</td><td class="mono">$0.0304</td><td class="mono">$0.117</td></tr>
  </tbody>
</table>
</div>
<p>各渠道逐一报价和可交互的成本计算器见<a href="/zh/pricing/">价格页</a>。</p>

<h2 id="limits">局限性</h2>
<ul>
  <li><strong>不能生成文本。</strong>写不了文章、邮件、聊天回复——任何面向人的文字仍需 LLM。</li>
  <li><strong>只支持文本。</strong>暂不支持图片、音频输入。</li>
  <li><strong>64K 上下文</strong>（Cloudflare 为 32K），长文档需先分块或摘要。</li>
  <li><strong>不算算术、不处理日期。</strong>计数、求和、日期差交给代码。</li>
  <li><strong>对上下文敏感。</strong>发送前清理 state 里的追踪头、HTML 样板和无关元数据。</li>
  <li><strong>可能自信地错。</strong>校准有帮助，但错误答案也可能带高置信度。自动化前先用历史数据回归测试概率。</li>
  <li><strong>早期访问的经济性。</strong>价格和速率限制可能变化；TypeSafe 自己说无法证明定价没有补贴。</li>
</ul>

<h2 id="mental">正确的心智模型</h2>
<p>Jev 不是更便宜的 LLM，而是<strong>一个恰好有智能的类型化函数调用</strong>：直接返回代码可用的值，附带置信度。有了它，很多只为「在字符串输出中活下来并做校验」而存在的代码就不需要存在了。发布几天内，开源项目 <a href="/zh/ecosystem/">openjev</a> 就在小开源模型上复刻了这套接口模式——说明这个原语的生命周期可能超过任何单一厂商。</p>

<h2 id="access">怎么试用</h2>
<p>从零代码到完整 API 的三条路径，我们在<a href="/zh/get-access/">获取方式指南</a>里逐步讲清——包括送 $5 额度的官方直注路径与 Vercel / Cloudflare 渠道。什么时候该用 Jev、什么时候该用前沿模型，见 <a href="/zh/vs-llm/">Jev vs 大模型</a>；具体工作流见<a href="/zh/use-cases/">使用场景</a>。</p>
""",
}

# ---- pricing ----
PAGES["pricing"] = {
    "title": "Jev 价格（2026）：每 token、每决策成本与 LLM 对比",
    "desc": "Jev 输入 $0.042/1M tokens、输出免费。对比全部渠道（Vercel、Cloudflare、Vivgrid），看真实单决策成本，并用计算器估算你的账单。",
    "crumb": CRUMB_HOME + [("价格", None)],
    "schema": [],
    "body": """
<p class="updated">最后更新：2026-09-20 · 价格已于当日对照各渠道商列表核验</p>
<h1>Jev 价格：到底要花多少钱（2026）</h1>
<p class="lede">Jev 的参考价是<strong>输入 $0.042 / 100 万 tokens（约 $42 / 10 亿）</strong>，且在所有渠道<strong>输出完全免费</strong>——因为模型返回的是紧凑的类型化决策，不是生成的文字。本页追踪每个渠道的费率、换算成真实的单决策成本，并让你直接算出自己的账单。</p>

<h2>官方定价</h2>
<div class="table-wrap">
<table>
  <thead><tr><th>项目</th><th>费率</th><th>说明</th></tr></thead>
  <tbody>
    <tr><td>输入 tokens</td><td class="mono good">$0.042 / 1M</td><td>唯一计费项</td></tr>
    <tr><td>输出 tokens</td><td class="mono good">$0</td><td>「便宜到不用计量」——答案是类型化决策，不是文本</td></tr>
    <tr><td>上下文窗口</td><td class="mono">64,000</td><td>Cloudflare 为 32,000；state 必须放得下</td></tr>
    <tr><td>典型单次决策</td><td class="mono">~$0.0001</td><td>官方基准例 $0.000081；厂商评测口径 $0.0004/例</td></tr>
  </tbody>
</table>
</div>
<div class="callout"><div class="t">量级参照</div>
<p>TypeSafe 的 $0.042/1M 输入价约为<strong>「Claude Fable 5.1」的 1/238</strong>、约为 <strong>GPT-5.6 Terra（$2.00/1M）的 1/48</strong>——而且这些模型还要收 $2–$12/1M 的输出费，Jev 从不收。</p></div>

<h2>渠道对比</h2>
<p>Jev 由四家公开渠道商加 TypeSafe 自家控制台提供服务。同一个模型，上下文上限不同：</p>
<div class="table-wrap">
<table>
  <thead><tr><th>渠道</th><th>模型 ID</th><th>输入 / 1M</th><th>输出 / 1M</th><th>上下文</th><th>要排队吗</th></tr></thead>
  <tbody>
    <tr><td>TypeSafe 控制台</td><td class="mono">jev-latest</td><td class="mono">$0.042</td><td class="mono">$0</td><td class="mono">64K</td><td>要（早期访问）</td></tr>
    <tr><td>Vercel AI Gateway</td><td class="mono">typesafe-ai/jev</td><td class="mono">$0.042</td><td class="mono">$0</td><td class="mono">64K</td><td class="good">不用</td></tr>
    <tr><td>Cloudflare Workers AI</td><td class="mono">typesafe/jev</td><td class="mono">$0.042</td><td class="mono">$0</td><td class="mono">32K</td><td class="good">不用</td></tr>
    <tr><td>Vivgrid</td><td class="mono">jev</td><td class="mono">$0.042</td><td class="mono">$0</td><td class="mono">64K</td><td class="good">不用</td></tr>
  </tbody>
</table>
<p class="updated">注：发布周有多篇报道称 Jev 已上 OpenRouter，但目前未在其列——使用前请以渠道商自己的模型列表为准。</p>
</div>

<h2>成本计算器</h2>
<p>估算你的月账单。Jev 只收输入；聊天模型两端都收（LLM 按每次决策约 60 个输出 tokens 估算）：</p>
<div class="calc">
  <label for="calc-decisions">每月决策次数</label>
  <input type="number" id="calc-decisions" value="100000" min="1"/>
  <label for="calc-tokens">每次决策的输入 tokens（state + 问题）</label>
  <input type="number" id="calc-tokens" value="800" min="10"/>
  <div class="calc-results">
    <div class="calc-row best"><span class="name">Jev（输入 $0.042/1M，输出免费）</span><span class="val" id="r-jev">—</span></div>
    <div class="calc-row"><span class="name">GPT-5 mini（输入 $0.25 / 输出 $2.00）</span><span class="val" id="r-mini">—</span></div>
    <div class="calc-row"><span class="name">Claude Sonnet 5（输入 $3.00 / 输出 $15.00）</span><span class="val" id="r-sonnet">—</span></div>
    <div class="calc-row"><span class="name">对比 GPT-5 mini 节省</span><span class="val" id="r-save">—</span></div>
  </div>
  <p class="calc-note">费率来自渠道商列表（2026 年 9 月）。实际单次决策成本取决于你的 state 长度——state 越精简越省。</p>
</div>

<h2>真实成本记录</h2>
<ul>
  <li><strong>1,018 篇论文分类</strong>总共 $0.08，单篇中位延迟 256ms（社区报告，2026 年 9 月）。</li>
  <li><strong>生产调度流程：</strong>决策环节切到 Jev 后成本下降 71%、总耗时下降 90%。</li>
  <li><strong>订单流基准（独立测试）：</strong>实时数据上每 1,000 次决策 $0.039，中位延迟 0.49 秒。</li>
  <li><strong>视频辩论打分（jevmeter）：</strong>每句话都打分，总共约 $0.05。</li>
</ul>

<h2>这个价格可持续吗？</h2>
<p>TypeSafe 在这点上异常坦率：<strong>无法证明定价没有补贴</strong>，长期可持续性有待验证——但它预计价格只降不涨。把当前费率当作发布期数字看待。我们的<a href="/zh/news/">动态追踪</a>盯着渠道商列表，有任何变化会自动标记。</p>

<h2>什么决定你的真实成本</h2>
<ul>
  <li><strong>state 长度是大头。</strong>成本随输入 tokens 线性增长，300 tokens 的精简 state 比 800 tokens 的臃肿 state 便宜约 2.7 倍。</li>
  <li><strong>加问题几乎免费。</strong>问题搭同一请求的便车；投机式扇出几乎不增加账单。</li>
  <li><strong>干净的 state 胜过便宜的模型。</strong>剔除 HTML 样板和元数据既省 tokens 又提升准确率——TypeSafe 查询设计指南里的「双赢」建议。</li>
</ul>
""",
}

# ---- use-cases ----
PAGES["use-cases"] = {
    "title": "Jev 的 10 个使用场景（附真实数据，2026）",
    "desc": "Jev 实战打法与社区实测数据：agent 护栏、模型路由、RAG 过滤、工单分诊、内容审核、LLM-as-judge、线索评分等。",
    "crumb": CRUMB_HOME + [("使用场景", None)],
    "schema": [],
    "body": """
<p class="updated">最后更新：2026-09-20 · 社区数据由项目作者自行报告</p>
<h1>Jev 的 10 个真实可用的场景</h1>
<p class="lede">下面每个场景都依赖同样三样东西：<strong>类型化的答案</strong>、<strong>置信度数字</strong>，以及低到可以对「全量数据」而非「抽样数据」运行的定价。只要答案已经存在于你发送的 state 里，Jev 就是提取它的最便宜方式。</p>
<div class="callout warn"><div class="t">一条铁律</div>
<p>Jev 擅长<strong>分类，不擅长预测</strong>。「这条线索是不是我们的目标行业？」是 Jev 的问题；「这条线索会不会成交？」不是——在短周期预测测试里，Jev 和掷硬币没区别（LLM 也一样）。</p></div>

<h2>1. Agent 护栏</h2>
<p>在 AI agent 删除文件、发送消息或执行命令之前，用 Jev 按你的规则对动作评级：<em>拒绝 / 询问 / 允许</em>。检查成本低到可以在<strong>每次</strong>动作前都跑一遍，而不是为了省钱跳过。社区项目 <a href="/zh/ecosystem/">jev-guard</a> 演示了这一模式。</p>

<h2>2. 模型路由</h2>
<p>请求到达昂贵模型之前，先让 Jev 问一句：简单还是困难。简单的走便宜模型，困难的走贵的。Vercel 报告用 Jev 做路由后 <strong>p95 响应最快提升 18 倍</strong>——它很可能成为 agent 技术栈的默认第一跳。</p>

<h2>3. RAG 过滤</h2>
<p>检索管线总会拉回没用的文档。用一次 Jev 调用给每篇召回文档与真实问题的相关性打分，弱结果在到达「写答案的模型」之前就被丢弃——答案更好，浪费的 tokens 更少。</p>

<h2>4. 客服工单分诊</h2>
<p>工单、邮件、告警、日志都涌向同一处，处理前先要分类。一次 Jev 请求同时选出类别、评出严重度、标记紧急度。过去需要人工初筛的队列实现了自动分诊。</p>

<h2>5. 大规模内容审核</h2>
<p>按你的业务类目给评论、评价、私信分类并设置信度阈值——高置信度的大多数自动处理，拿不准的少数升级给人工。</p>

<h2>6. LLM-as-judge，但不付 LLM 的账单</h2>
<p>当 AI 生成的文本把论断和来源配对时，让 Jev 检查来源是否真的支持论断。再叫一个完整模型来「复核」会让成本翻倍，还可能犯自己的错；一个类型化的问题只核查那个具体事实。</p>

<h2>7. 线索评分</h2>
<p>一次调用同时给线索打上目标行业匹配度、意向强度、垃圾概率——再把结论喂进广告平台的反馈回路。结构化决策的成本让「每条线索都打分」在任何量级下都可行。</p>

<h2>8. 搜索词挖掘</h2>
<p>把成千上万条搜索词报告分类为品牌 / 竞品 / 通用 / 无关，自动挖掘否定关键词。过去只能抽样的决策，现在可以全量覆盖。</p>

<h2>9. 实时界面</h2>
<p>Steve Krouse 的 <a href="/zh/ecosystem/">Typewriter</a> 在你打字的同时实时更新 16 个 Jev 判断。当一次决策只要 200ms 和 ~$0.0001，界面本身就可以「由判断构成」，而不只是展示判断。</p>

<h2>10. 语义搜索与语料 Map-Reduce</h2>
<p>以「全语料覆盖」可承受的成本对文档进行过滤、打分和映射——社区演示对 1,018 篇论文完成分类，<strong>总共 $0.08</strong>，中位延迟 256ms。</p>

<h2>Jev 生态：star 最多的社区项目</h2>
<p>真实仓库，按 GitHub star 排序（截至 2026-09-21）。完整目录见<a href="/zh/ecosystem/">生态页</a>。</p>
<div class="card-grid">
  <a class="card gh-card" href="https://github.com/OpenByteInc/QuantDinger" rel="nofollow noopener" target="_blank"><img loading="lazy" src="https://opengraph.githubassets.com/1/OpenByteInc/QuantDinger" alt="QuantDinger on GitHub"/><span class="tag">11.8k stars</span><h3>QuantDinger</h3><p>开源 AI 交易操作系统，集成 Jev System One——Agent 循环内高频的分类/路由/评分调用由 Jev 完成。</p></a>
  <a class="card gh-card" href="https://github.com/jaredpalmer/kev" rel="nofollow noopener" target="_blank"><img loading="lazy" src="https://opengraph.githubassets.com/1/jaredpalmer/kev" alt="kev on GitHub"/><span class="tag">1.0k stars</span><h3>kev</h3><p>基于 Qwen3.5 的迷你 Jev 类决策模型家族，可以自己训练、自己跑——System One 的开源版本。</p></a>
  <a class="card gh-card" href="https://github.com/reticlehq/reticle" rel="nofollow noopener" target="_blank"><img loading="lazy" src="https://opengraph.githubassets.com/1/reticlehq/reticle" alt="Reticle on GitHub"/><span class="tag">776 stars</span><h3>Reticle</h3><p>AI Agent 能生成代码，却难以理解代码——Reticle 把 Jev 式类型化理解带进它们构建的东西。</p></a>
  <a class="card gh-card" href="https://github.com/devagrawal09/jev-review" rel="nofollow noopener" target="_blank"><img loading="lazy" src="https://opengraph.githubassets.com/1/devagrawal09/jev-review" alt="jev-review on GitHub"/><span class="tag">410 stars</span><h3>jev-review</h3><p>基于 Jev 的分阶段代码评审工作流，带本地仪表盘。</p></a>
  <a class="card gh-card" href="https://github.com/itsmostafa/typesafe-mcp" rel="nofollow noopener" target="_blank"><img loading="lazy" src="https://opengraph.githubassets.com/1/itsmostafa/typesafe-mcp" alt="typesafe-mcp on GitHub"/><span class="tag">136 stars</span><h3>typesafe-mcp</h3><p>MCP 连接器，让任意 AI Agent 直接调用 Jev。</p></a>
  <a class="card gh-card" href="https://github.com/0xNatoshi/jev-codex-router" rel="nofollow noopener" target="_blank"><img loading="lazy" src="https://opengraph.githubassets.com/1/0xNatoshi/jev-codex-router" alt="jev-codex-router on GitHub"/><span class="tag">88 stars</span><h3>jev-codex-router</h3><p>由 Jev 驱动的 Codex 逐轮模型与推理路由。</p></a>
</div>

<h2>Jev 不适合哪里</h2>
<ul>
  <li><strong>一切生成任务：</strong>回复、摘要、代码补丁——继续用你的 LLM。</li>
  <li><strong>预测：</strong>价格、流失、销量——答案不在输入里，这个价位的模型也没有优势。</li>
  <li><strong>复合推理：</strong>拆成原子级的直觉问题、在代码里组合，而不是问一个含糊的超级问题。</li>
</ul>
<p>决策边界的更多讨论见 <a href="/zh/vs-llm/">Jev vs 大模型</a>。</p>
""",
}

# ---- get-access ----
PAGES["get-access"] = {
    "title": "如何获取 Jev 使用权限（2026）：开放注册、$5 免费额度与渠道路径",
    "desc": "Jev 已全面开放、无需排队。直接在 console.typesafe.ai 注册并领取 $5 免费额度，或经 Vercel AI Gateway、Cloudflare Workers AI 调用——附 5 分钟快速上手。",
    "crumb": CRUMB_HOME + [("获取方式", None)],
    "schema": [],
    "body": """
<p class="updated">最后更新：2026-09-20</p>
<h1>如何获取 Jev 使用权限</h1>
<p class="lede"><strong>Jev 已于 2026 年 9 月 20 日全面开放——排队取消。</strong>在 console.typesafe.ai 注册即送 $5 额度（约 1.2 亿输入 tokens）。也可以走 Vercel、Cloudflare 渠道，调用的都是同一个模型。</p>

<h2 id="console">方式一：TypeSafe 官方直注（已开放）</h2>
<ol>
  <li>打开 <a href="https://console.typesafe.ai" rel="nofollow noopener" target="_blank">console.typesafe.ai</a> 注册——无需排队、无需邀请。</li>
  <li>新账户赠送 <strong>$5 免费额度</strong>——按 $0.042/1M 计价约等于 1.2 亿输入 tokens。</li>
  <li>控制台内含网页 Playground、API key 管理与用量看板。</li>
</ol>

<h2 id="vercel">方式二：Vercel AI Gateway（Vercel 用户免注册）</h2>
<p>发布当天 Jev 即进入 Vercel AI Gateway，模型 ID 为 <span class="mono">typesafe-ai/jev</span>。如果你本来就在 Vercel 上开发，无需单独注册——用现有账户直接调用。价格与 TypeSafe 原生 $0.042/1M 一致。</p>

<h2 id="cloudflare">方式三：Cloudflare Workers AI</h2>
<p>Cloudflare 上线了 <span class="mono">typesafe/jev</span>，按请求在边缘计费。注意这里的上下文窗口是 <strong>32K</strong>（不是 64K）——长文本先分块。</p>

<h2 id="openrouter">关于 OpenRouter 的说明</h2>
<div class="callout warn"><div class="t">目前未见上架</div>
<p>发布周有多篇报道称 Jev 已上 OpenRouter，但其公开模型 API 目前查不到任何 TypeSafe 条目。动手前请以渠道商自己的模型列表为准——当前可靠的路径是 TypeSafe 控制台、Vercel AI Gateway 与 Cloudflare Workers AI。</p></div>

<h2>5 分钟快速上手</h2>
<h3>1. 先玩 Playground（零代码）</h3>
<p>打开 <span class="mono">console.typesafe.ai/playground</span>：粘贴文本作为 state，用大白话写问题，选题型（Choice / Score / Noul），点运行。亚秒级返回，带置信度。官方入门例：粘贴「我的 Stripe 账户连了 3 天一直失败，我正在丢单」，问「这条消息表达了紧急感吗？」</p>
<h3>2. 调 API</h3>
<pre><code>curl https://api.typesafe.ai/v1/systemone \\
  -H <span class="c-str">"Authorization: Bearer $JEV_API_KEY"</span> \\
  -d '{
    <span class="c-key">"model"</span>: <span class="c-str">"jev-latest"</span>,
    <span class="c-key">"state"</span>: <span class="c-str">"结账页只在 Safari 上报 500。"</span>,
    <span class="c-key">"questions"</span>: {
      <span class="c-key">"category"</span>: { <span class="c-key">"type"</span>: <span class="c-str">"choice"</span>,
                    <span class="c-key">"options"</span>: [<span class="c-str">"账务"</span>, <span class="c-str">"技术"</span>, <span class="c-str">"销售"</span>] }
    }
  }'</code></pre>
<h3>3. 用 SDK</h3>
<p>官方 Python 与 JavaScript/TypeScript SDK 已提供，另有 <span class="mono">langchain-typesafe</span> 包和 Vercel AI SDK 集成（<span class="mono">@ai-sdk/typesafe</span>）。TypeScript 的 evaluate 模式：</p>
<pre><code><span class="c-key">import</span> { evaluate } <span class="c-key">from</span> <span class="c-str">'@typesafe-ai/sdk'</span>;

<span class="c-key">const</span> verdict = <span class="c-key">await</span> <span class="c-fn">evaluate</span>({
  model: <span class="c-str">'typesafe-ai/jev'</span>,
  state: ticketText,
  questions: {
    category: { type: <span class="c-str">'choice'</span>, options: [<span class="c-str">'billing'</span>,<span class="c-str">'technical'</span>,<span class="c-str">'sales'</span>,<span class="c-str">'spam'</span>] },
  },
});

<span class="c-com">// 策略由你的代码决定：</span>
<span class="c-key">if</span> (verdict.category.value === <span class="c-str">'spam'</span> &amp;&amp; verdict.confidence &gt; 0.90) archive(ticketText);</code></pre>

<h2>速率限制与生产建议</h2>
<ul>
  <li>早期访问默认：约 <strong>25 万 tokens/秒</strong>、约 <strong>1200 请求/分钟</strong>；企业档可提升。</li>
  <li>state 保持精简——剔除 HTML 和元数据。省 tokens，也更准。</li>
  <li>问题拆成原子的；概率在代码里组合。</li>
  <li>自动化前先在 100–500 条历史样本上做校准回归测试。</li>
</ul>
<p>不知道先做什么？从<a href="/zh/use-cases/">工单分诊或邮件路由</a>开始——风险低、见效快。也先看看<a href="/zh/vs-llm/">什么时候根本不该用 Jev</a>。</p>
""",
}

# ---- vs-llm ----
PAGES["vs-llm"] = {
    "title": "Jev vs 大模型：什么时候用哪个（2026 诚实指南）",
    "desc": "用 Jev 还是用聊天大模型？路由、分类、生成三类工作流的决策表，混合架构模式，以及双方诚实的局限。",
    "crumb": CRUMB_HOME + [("Jev vs 大模型", None)],
    "schema": [],
    "body": """
<p class="updated">最后更新：2026-09-20</p>
<h1>Jev vs 大模型：什么时候用哪个</h1>
<p class="lede"><strong>一句话答案：</strong>如果答案已经存在于输入中、且正确答案是已知选项之一，用 Jev。如果答案需要被「写出来」——文章、代码、摘要、方案——用 LLM。大多数真实系统两者都要。</p>

<h2>正面对比</h2>
<div class="table-wrap">
<table>
  <thead><tr><th></th><th>Jev（System One）</th><th>聊天 LLM（GPT / Claude / Gemini）</th></tr></thead>
  <tbody>
    <tr><td>返回内容</td><td>类型化决策 + 置信度</td><td>自由文本</td></tr>
    <tr><td>输入价 / 1M</td><td class="mono good">$0.042</td><td class="mono">$0.25 – $3.00+</td></tr>
    <tr><td>输出价 / 1M</td><td class="mono good">$0</td><td class="mono">$2 – $15+</td></tr>
    <tr><td>延迟</td><td class="mono good">70–500 ms</td><td class="mono">2 – 80 s</td></tr>
    <tr><td>文本幻觉</td><td class="good">结构性不可能</td><td class="bad">固有风险</td></tr>
    <tr><td>无效答案格式</td><td class="good">0%（schema 保证）</td><td class="bad">实测 0.58% – 45.5%</td></tr>
    <tr><td>能写文字吗</td><td class="bad">永远不能</td><td class="good">这正是它的本职</td></tr>
    <tr><td>开放式推理</td><td class="bad">不能</td><td class="good">能</td></tr>
    <tr><td>图片 / 音频输入</td><td class="bad">不支持（纯文本）</td><td class="good">通常支持</td></tr>
    <tr><td>上下文窗口</td><td class="mono">64K（Cloudflare 32K）</td><td class="mono">128K – 1M+</td></tr>
  </tbody>
</table>
</div>

<h2>决策表</h2>
<div class="table-wrap">
<table>
  <thead><tr><th>工作负载</th><th>赢家</th><th>原因</th></tr></thead>
  <tbody>
    <tr><td>工单 / 邮件分诊</td><td class="good">Jev</td><td>类目有限、量巨大、成本敏感</td></tr>
    <tr><td>Agent 工具调用审批</td><td class="good">Jev</td><td>每次调用都该查；$0.0001 的检查好过被跳过的检查</td></tr>
    <tr><td>简单/困难请求路由</td><td class="good">Jev</td><td>把贵的 tokens 留给真正需要的请求</td></tr>
    <tr><td>RAG 相关性过滤</td><td class="good">Jev</td><td>生成之前先打分再丢弃</td></tr>
    <tr><td>撰写回复与摘要</td><td class="good">LLM</td><td>生成是 LLM 的本职</td></tr>
    <tr><td>多步开放式推理</td><td class="good">LLM</td><td>Jev 只做有限判断</td></tr>
    <tr><td>「价格/流失/销量会怎么走？」</td><td class="warn-c">都别用</td><td>预测的答案不在输入里；实测约等于掷硬币</td></tr>
    <tr><td>算术与日期计算</td><td class="warn-c">普通代码</td><td>数学别交给任何模型</td></tr>
  </tbody>
</table>
</div>

<h2>混合架构（生产系统的真实样子）</h2>
<pre><code>请求进入（webhook / 表单 / 工单）
        │
        ▼
  Jev 决策层                ~200ms，~$0.0001
  （类别 · 紧急度 · 是否垃圾 · 路由？）
        │
        ├─ 高置信 + 标准动作 ──────► 确定性代码执行
        ├─ 低置信 / 复杂 ──────────► 升级给人工
        └─ 需要生成 ───────────────► 前沿 LLM
                                        │
                                        ▼
                          可选：Jev QA 复核（验证论断）</code></pre>
<p>这个模式把控制流留在你的代码库里，避免脆弱的多轮提示词循环，消灭 schema 校验错误，把昂贵的前沿推理留给真正需要的请求。LangChain 的官方指南也是同样定位：Jev 是 <strong>LLM 的补充，不是替代</strong>。</p>

<h2>Jev 不能做什么（对自己诚实）</h2>
<ul>
  <li>没有文字、没有解释、没有共情——任何面向人的文字都需要 LLM。</li>
  <li>没有开放式推理；它做判断，不做推演。</li>
  <li>纯文本输入；64K 上下文；不算数学、不处理日期。</li>
  <li>格式正确的答案仍可能带着高置信度出错——先在自己的数据上校准。</li>
  <li>评测是厂商自跑的；进入生产信任前先用自己的流量验证。</li>
</ul>

<h2>结论</h2>
<p>这笔交易的实质是<strong>用少量精度换一两个数量级的成本</strong>：在有限工作流上，Jev 与中档前沿模型的差距只有一两个点，成本却低 1–2 个数量级。让便宜的裁判无处不在，让昂贵的思考者偶尔出场。用你的真实业务量跑一下<a href="/zh/pricing/">成本计算器</a>，再从<a href="/zh/use-cases/">场景打法</a>里挑第一个落地的工作流。</p>
""",
}

# ---- news ----
PAGES["news"] = {
    "title": "Jev 动态与更新——自动追踪时间线（2026）",
    "desc": "关于 Jev 的每一条重要更新：发布新闻、接入政策变化、渠道上架、价格变化、评测分析与社区项目——自动追踪，持续更新。",
    "crumb": CRUMB_HOME + [("动态", None)],
    "schema": [],
    "body": """
<p class="updated">最后更新：2026-09-20 · 本页随新信源出现自动刷新</p>
<h1>Jev 动态与更新</h1>
<p class="lede">关于 Jev 值得知道的一切，按时间排列：官方公告、渠道上架、独立分析、社区里程碑。每条附来源链接；厂商自报数据均已标注。</p>
<div class="timeline">
{NEWS_FULL}
</div>
""",
}

# ---- ecosystem ----
PAGES["ecosystem"] = {
    "title": "Jev 生态项目目录：开源项目与社区工具",
    "desc": "Jev 项目大全：openjev、jev-ultrafast、jev-guard、pg-jev、HA-Jev、jevmeter 等——各自做什么、谁在维护。",
    "crumb": CRUMB_HOME + [("生态项目", None)],
    "schema": [],
    "body": """
<p class="updated">最后更新：2026-09-20 · 项目介绍来自公开演示与作者发文</p>
<h1>Jev 生态</h1>
<p class="lede">发布几天之内，开发者们就开始基于 Jev 的类型化决策原语构建东西了——agent、护栏、数据库过滤器、游戏，甚至接口本身的开源复刻。这个目录收录值得关注的那些。</p>

<h2>开源复刻</h2>
<div class="card-grid">
  <div class="card"><span class="tag">参考实现</span><h2>openjev</h2><p>通过读取小开源模型 logits 上的类型化选项概率，复刻 Jev 接口模式。这是社区对「这是耐用的原语还是厂商包装」的回答——显然耐用。</p></div>
</div>

<h2>Agent 类</h2>
<div class="card-grid">
  <div class="card"><span class="tag">浏览器</span><h2>jev-ultrafast</h2><p>Browser Use 的 agent 以 Jev 为决策层——7.1 秒完成苏黎世→伦敦的 Google 机票搜索。</p></div>
  <div class="card"><span class="tag">手机</span><h2>mobile-jev</h2><p>Droidrun 的手机 agent 在真机 Android 上操作 Uber：约 21 秒完成 9 个动作（未完成下单）。</p></div>
  <div class="card"><span class="tag">电脑操作</span><h2>typesafe-computer-use</h2><p>电脑操作 agent，Jev 作为每个动作的廉价守门人。</p></div>
  <div class="card"><span class="tag">游戏</span><h2>heist-one</h2><p>在抢劫游戏 demo 中由 Jev 驱动守卫 AI——是决策，不是脚本。</p></div>
</div>

<h2>基础设施与工具</h2>
<div class="card-grid">
  <div class="card"><span class="tag">安全</span><h2>jev-guard</h2><p>执行前对每个 agent 工具调用按你的规则评级：拒绝 / 询问 / 允许。</p></div>
  <div class="card"><span class="tag">数据库</span><h2>pg-jev</h2><p>通过 Jev 决策为 Postgres 查询增加自然语言过滤。</p></div>
  <div class="card"><span class="tag">智能家居</span><h2>HA-Jev</h2><p>把 Jev 答案变成 Home Assistant 实体，驱动智能家居逻辑。</p></div>
  <div class="card"><span class="tag">媒体</span><h2>jevmeter</h2><p>给视频辩论的每一句话打分，总共约 $0.05。</p></div>
  <div class="card"><span class="tag">实时 UI</span><h2>Typewriter</h2><p>Steve Krouse 的实时打字 demo——你边打字，16 个 Jev 判断边实时更新。</p></div>
  <div class="card"><span class="tag">实验</span><h2>jev-trader</h2><p>市场信号实验。独立测试显示 Jev 在短周期预测上与掷硬币无异——参见<a href="/zh/use-cases/">那条铁律</a>。</p></div>
</div>

<h2>想被收录？</h2>
<p>用 Jev 做了东西？它大概率会出现在 Hacker News 或 X 上——我们的追踪器会从那里自动发现并收录到这里，也可以直接把链接发给我们。</p>
""",
}

# ---- faq ----
_faq_body, _faq_schema = faq_html_and_schema()
PAGES["faq"] = {
    "title": "Jev 常见问题：关于 TypeSafe System One 模型的 20 个问答",
    "desc": "关于 Jev 的直接答案：它是什么、开放接入、价格、速率限制、零幻觉保证、评测可信度，以及信息来源。",
    "crumb": CRUMB_HOME + [("常见问题", None)],
    "schema": [_faq_schema],
    "body": """
<p class="updated">最后更新：2026-09-20</p>
<h1>Jev 常见问题：20 个问答，直接说清</h1>
<p class="lede">人们真正在问的关于 Jev 的一切，不带营销滤镜地回答。凡属 TypeSafe 自己的说法，我们会注明。</p>
""" + _faq_body,
}

# live 数据覆盖（由 update_news.py 写入；来源标题保持原文，摘要说明为英文社区内容）
import json as _json, os as _os
_news_file = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data", "news.json")
if _os.path.exists(_news_file):
    _live = _json.load(open(_news_file, encoding="utf-8"))
    NEWS = [
        (i["date"], i["title"],
         i["summary"] + (f' <a href="{(i.get("url") or "").replace("&", "&amp;")}">查看原文 →</a>' if i.get("url") else ""),
         i["source"])
        for i in _live
    ]
    from datetime import date as _date
    PAGES["news"]["body"] = PAGES["news"]["body"].replace(
        "最后更新：2026-09-20", f"最后更新：{_date.today().isoformat()}")

# news 页 ItemList schema：给 Google 富数据 + 新鲜度信号
if _os.path.exists(_news_file):
  PAGES["news"]["schema"] = [{
    "@context": "https://schema.org", "@type": "ItemList",
    "name": "Jev news timeline",
    "itemListElement": [
        {"@type": "ListItem", "position": i + 1,
         "name": i2["title"], "url": i2.get("url") or "https://jev-ai.live/news/"}
          for i, i2 in enumerate(_live[:20])
      ],
  }]

NEWS_PREVIEW = "".join(
    f'<div class="tl-item"><div class="date">{d}</div><h3>{t}</h3><p>{s}</p><div class="src">来源：{src}</div></div>'
    for d, t, s, src in NEWS[:3]
)
PAGES["index"]["body"] = PAGES["index"]["body"].replace("{NEWS_PREVIEW}", NEWS_PREVIEW)

NEWS_FULL = "".join(
    f'<div class="tl-item"><div class="date">{d}</div><h3>{t}</h3><p>{s}</p><div class="src">来源：{src}</div></div>'
    for d, t, s, src in NEWS
)
PAGES["news"]["body"] = PAGES["news"]["body"].replace("{NEWS_FULL}", NEWS_FULL)
