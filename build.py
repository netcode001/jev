#!/usr/bin/env python3
"""Jev Hub static site generator.
Outputs clean-URL static HTML to site/ — deployable to Vercel / Cloudflare Pages / Netlify as-is.
"""
import json
import os
import shutil
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_en import PAGES as PAGES_EN
from content_zh import PAGES as PAGES_ZH

# TODO: replace with the real domain after registration
SITE_URL = "https://jev-ai.live"
TODAY = date.today().isoformat()
# IndexNow key (Bing/Seznam/Yandex instant indexing). File served at /{KEY}.txt
INDEXNOW_KEY = "a3f8c2e91b7d4f6e8c5a2d7b9e4f1c38"
BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
OG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "og")

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='6' fill='%230E1726'/%3E"
           "%3Ctext x='16' y='22' font-family='monospace' font-size='16' font-weight='700' "
           "fill='%23E85D3D' text-anchor='middle'%3EJ%3C/text%3E%3C/svg%3E")

FONT_LINKS = ('  <link rel="preconnect" href="https://fonts.googleapis.com"/>\n'
              '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>\n'
              '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap"/>\n')

GA_ID = "G-W8YTRRNG9P"
GA_SNIPPET = ('  <script async src="https://www.googletagmanager.com/gtag/js?id=' + GA_ID + '"></script>\n'
              '  <script>\n'
              '    window.dataLayer = window.dataLayer || [];\n'
              '    function gtag(){dataLayer.push(arguments);}\n'
              "    gtag('js', new Date());\n"
              "    gtag('config', '" + GA_ID + "');\n"
              '  </script>\n')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "style.css"), encoding="utf-8") as _f:
    CSS_CONTENT = _f.read()

LOCALES = {
    "en": {
        "brand": "jev<span>.hub</span>",
        "nav": {
            "what-is-jev": "What is Jev", "pricing": "Pricing",
            "use-cases": "Use Cases", "get-access": "Get Access", "playground": "Playground",
            "news": "News", "ecosystem": "Ecosystem", "faq": "FAQ",
        },
        "home_label": "Home", "nav_cta": "Get API Key",
        "footer_about": ("Jev Hub is an independent information hub for Jev, the System One "
                         "model by TypeSafe AI. We track pricing, benchmarks, access paths, ecosystem "
                         "projects and news — updated automatically."),
        "footer_cols": [
            ("Learn", [("What is Jev", "/what-is-jev/"), ("Jev vs LLMs", "/vs-llm/"), ("Use Cases", "/use-cases/"), ("FAQ", "/faq/")]),
            ("Data", [("Pricing", "/pricing/"), ("News", "/news/"), ("Ecosystem", "/ecosystem/")]),
            ("Access", [("Get Access", "/get-access/"), ("Playground", "/playground/"), ("TypeSafe AI (official)", "https://typesafe.ai")]),
        ],
        "disclaimer": ("Jev Hub is not affiliated with, endorsed by, or sponsored by TypeSafe AI. "
                       "\"Jev\" and \"TypeSafe\" are trademarks of their respective owners. Benchmark and "
                       "pricing figures are self-reported by vendors unless stated otherwise and may "
                       "change without notice. Content is informational, not investment or procurement advice."),
        "lang_name": "English", "lang_self": "EN",
        "dir_prefix": "",
    },
    "zh": {
        "brand": "jev<span>.hub</span>",
        "nav": {
            "what-is-jev": "Jev 是什么", "pricing": "价格",
            "use-cases": "使用场景", "get-access": "获取方式", "playground": "在线试玩",
            "news": "动态", "ecosystem": "生态项目", "faq": "常见问题",
        },
        "home_label": "首页", "nav_cta": "获取 API Key",
        "footer_about": ("Jev Hub 是关于 TypeSafe AI 旗下 System One 模型 Jev 的独立第三方信息站，"
                         "自动追踪价格、评测数据、获取路径、生态项目与最新动态。"),
        "footer_cols": [
            ("了解", [("Jev 是什么", "/zh/what-is-jev/"), ("Jev vs 大模型", "/zh/vs-llm/"), ("使用场景", "/zh/use-cases/"), ("常见问题", "/zh/faq/")]),
            ("数据", [("价格对比", "/zh/pricing/"), ("最新动态", "/zh/news/"), ("生态项目", "/zh/ecosystem/")]),
            ("接入", [("获取方式", "/zh/get-access/"), ("在线试玩", "/zh/playground/"), ("TypeSafe AI 官网", "https://typesafe.ai")]),
        ],
        "disclaimer": ("Jev Hub 与 TypeSafe AI 无隶属、背书或赞助关系。\"Jev\"\"TypeSafe\" 为其各自所有者的商标。"
                       "除特别注明外，评测与价格数据均为厂商自报，可能随时调整。内容仅供参考，不构成投资或采购建议。"),
        "lang_name": "简体中文", "lang_self": "中文",
        "dir_prefix": "zh/",
    },
}


def page_url(lang, slug):
    base = SITE_URL + ("/zh/" if lang == "zh" else "/")
    return base if slug == "index" else base + slug + "/"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def breadcrumb_html(crumb, locale):
    items = []
    for i, (name, href) in enumerate(crumb):
        cur = ' aria-current="page"' if i == len(crumb) - 1 else ""
        link = f'<a href="{href}">{esc(name)}</a>' if href else esc(name)
        items.append(f"<li{cur}>{link}</li>")
    return f'<nav class="breadcrumb" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def breadcrumb_schema(crumb):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, **({"item": SITE_URL + href if href.startswith("/") else href} if href else {})}
            for i, (name, href) in enumerate(crumb)
        ],
    }


def render_page(lang, slug, page, all_pages):
    loc = LOCALES[lang]
    crumb = page.get("crumb") or [(loc["home_label"], "/" if lang == "en" else "/zh/")]
    canonical = page_url(lang, slug)
    og_image = f"{SITE_URL}/og/{lang}-{slug}.png"
    en_url, zh_url = page_url("en", slug), page_url("zh", slug)
    hreflang = (
        f'  <link rel="alternate" hreflang="en" href="{en_url}"/>\n'
        f'  <link rel="alternate" hreflang="zh" href="{zh_url}"/>\n'
        f'  <link rel="alternate" hreflang="x-default" href="{en_url}"/>\n'
    )
    schemas = list(page.get("schema", [])) + [breadcrumb_schema(crumb)]
    ld = "".join(
        f'  <script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
        for s in schemas
    )
    nav_links = []
    for s, label in loc["nav"].items():
        href = "/" if s == "index" else f"/{loc['dir_prefix']}{s}/" if lang == "zh" else f"/{s}/"
        cur = ' aria-current="page"' if s == slug else ""
        nav_links.append(f'<a href="{href}"{cur}>{label}</a>')
    lang_other = "/zh/" if lang == "en" else "/"
    cols = "".join(
        f'<div><h3>{t}</h3><ul>' + "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in links) + "</ul></div>"
        for t, links in loc["footer_cols"]
    )
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{esc(page['title'])}</title>
  <meta name="description" content="{esc(page['desc'])}"/>
  <link rel="canonical" href="{canonical}"/>
{hreflang}  <meta name="robots" content="index, follow, max-image-preview:large"/>
  <meta property="og:type" content="website"/>
  <meta property="og:site_name" content="Jev Hub"/>
  <meta property="og:title" content="{esc(page['title'])}"/>
  <meta property="og:description" content="{esc(page['desc'])}"/>
  <meta property="og:url" content="{canonical}"/>
  <meta property="og:image" content="{og_image}"/>
  <meta property="og:image:width" content="1200"/>
  <meta property="og:image:height" content="630"/>
  <meta property="og:locale" content="{'en_US' if lang == 'en' else 'zh_CN'}"/>
  <meta property="og:locale:alternate" content="{'zh_CN' if lang == 'en' else 'en_US'}"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{esc(page['title'])}"/>
  <meta name="twitter:description" content="{esc(page['desc'])}"/>
  <meta name="twitter:image" content="{og_image}"/>
  <link rel="alternate" type="application/rss+xml" title="Jev Hub — Jev news &amp; updates" href="{SITE_URL}/feed.xml"/>
  <link rel="icon" href="{FAVICON}"/>
{FONT_LINKS}{GA_SNIPPET}  <style>
{CSS_CONTENT}
  </style>
{ld}</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="{lang_other if slug == 'index' else ('/' if lang == 'en' else '/zh/')}"><span class="mark">J</span>jev.hub</a>
    <nav class="main-nav" aria-label="Main">{''.join(nav_links)}</nav>
    <a class="nav-cta" href="{'/get-access/' if lang == 'en' else '/zh/get-access/'}">{loc['nav_cta']}</a>
    <div class="lang-switch"><a href="{lang_other}" hreflang="{ 'zh' if lang == 'en' else 'en' }">{ '中文' if lang == 'en' else 'EN' }</a></div>
  </div>
</header>
<main class="{'wrap wide' if page.get('wide') else 'wrap narrow'}">
<article>
  {page['body']}
</article>
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <h3>Jev Hub</h3>
        <p style="font-size:13.5px">{loc['footer_about']}</p>
      </div>
      {cols}
    </div>
    <p class="disclaimer">{loc['disclaimer']}</p>
    <p class="mono" style="margin-top:14px">© 2026 Jev Hub · Data last updated 2026-09-20 · <a href="/sitemap.xml">Sitemap</a></p>
  </div>
</footer>
</body>
</html>
"""


def rewrite_internal_links(html, prefix):
    """Rewrite root-absolute hrefs (/zh/xxx/) into relative paths so links
    work on file://, the local preview server, and the deployed site alike."""
    import re

    def repl(m):
        raw = m.group(1)
        if raw.startswith("/"):  # protocol-relative URL, leave untouched
            return m.group(0)
        path, anchor = raw, ""
        if "#" in raw:
            path, anchor = raw.split("#", 1)
            anchor = "#" + anchor
        path = path.rstrip("/")
        if path == "":
            target = "index.html"
        else:
            target = path + "/index.html"
        return f'href="{prefix}{target}{anchor}"'

    return re.sub(r'href="/([^"]*)"', repl, html)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_rss():
    """RSS 2.0 feed from data/news.json (fallback: curated NEWS from content_en)."""
    import html as _html
    from email.utils import format_datetime
    from datetime import datetime, timezone
    news_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "news.json")
    items = []
    if os.path.exists(news_file):
        with open(news_file, encoding="utf-8") as f:
            items = json.load(f)
    else:
        from content_en import NEWS as _news
        items = [{"date": d, "title": t, "summary": s, "source": src, "url": None}
                 for d, t, s, src in _news]
    e = _html.escape
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0"><channel>',
        '<title>Jev Hub — Jev news &amp; updates</title>',
        f'<link>{SITE_URL}/news/</link>',
        '<description>Auto-tracked news about Jev, the System One model by TypeSafe AI: '
        'launches, provider listings, price changes, benchmarks and ecosystem projects.</description>',
        '<language>en</language>',
        f'<lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>',
    ]
    for i in items[:30]:
        link = i.get("url") or f"{SITE_URL}/news/"
        try:
            dt = datetime.strptime(i.get("date", "2026-09-15"), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            pubdate = format_datetime(dt)
        except ValueError:
            pubdate = format_datetime(datetime.now(timezone.utc))
        desc = e(i.get("summary", ""))
        if i.get("url"):
            desc += f'  Source: {e(i.get("source", ""))}'
        parts += [
            '<item>',
            f'<title>{e(i["title"])}</title>',
            f'<link>{e(link)}</link>',
            f'<guid isPermaLink="true">{e(link)}</guid>',
            f'<pubDate>{pubdate}</pubDate>',
            f'<description>{desc}</description>',
            '</item>',
        ]
    parts.append('</channel></rss>')
    write(os.path.join(BUILD_DIR, "feed.xml"), "\n".join(parts))


def build():
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR)
    shutil.copytree(ASSETS_DIR, os.path.join(BUILD_DIR, "assets"))
    # OG share images (PNG, generated separately by gen_og.py)
    if os.path.isdir(OG_DIR):
        shutil.copytree(OG_DIR, os.path.join(BUILD_DIR, "og"))
    # IndexNow key file (site ownership proof for Bing/Seznam/Yandex)
    write(os.path.join(BUILD_DIR, f"{INDEXNOW_KEY}.txt"), INDEXNOW_KEY)

    # cost calculator script — injected into both pricing pages
    calc_js = """
<script>
(function () {
  var d = document.getElementById('calc-decisions'),
      t = document.getElementById('calc-tokens');
  if (!d || !t) return;
  function fmt(v) { return '$' + v.toFixed(2); }
  function run() {
    var n = Math.max(1, parseFloat(d.value) || 0),
        k = Math.max(10, parseFloat(t.value) || 0),
        mIn = n * k;  // input tokens per month
    var jev = mIn / 1e6 * 0.042;
    var mini = mIn / 1e6 * 0.25 + n * 60 / 1e6 * 2.00;
    var sonnet = mIn / 1e6 * 3.00 + n * 60 / 1e6 * 15.00;
    document.getElementById('r-jev').textContent = fmt(jev) + ' /mo';
    document.getElementById('r-mini').textContent = fmt(mini) + ' /mo';
    document.getElementById('r-sonnet').textContent = fmt(sonnet) + ' /mo';
    document.getElementById('r-save').textContent = (mini > 0 ? (100 - jev / mini * 100).toFixed(1) : '0') + '%';
  }
  d.addEventListener('input', run);
  t.addEventListener('input', run);
  run();
})();
</script>"""
    for lang_pages in (PAGES_EN, PAGES_ZH):
        lang_pages["pricing"]["body"] += calc_js

    for lang, pages in (("en", PAGES_EN), ("zh", PAGES_ZH)):
        for slug, page in pages.items():
            html = render_page(lang, slug, page, pages)
            # safety net: any hardcoded legacy domain in content falls back to SITE_URL
            html = html.replace("https://jevhub.ai", SITE_URL)
            rel = "index.html" if slug == "index" else f"{slug}/index.html"
            if lang == "zh":
                rel = f"zh/{rel}"
            depth = rel.count("/")  # directories above this file
            prefix = "../" * depth
            html = rewrite_internal_links(html, prefix)
            write(os.path.join(BUILD_DIR, rel), html)

    # 404
    notfound = PAGES_EN["index"]
    html404 = render_page("en", "index", dict(notfound, title="404 — Page not found | Jev Hub",
                              body="<div class='hero'><h1>404</h1><p class='sub'>This page does not exist. <a href='/'>Back to Jev Hub</a></p></div>"),
                          PAGES_EN).replace("https://jevhub.ai", SITE_URL)
    write(os.path.join(BUILD_DIR, "404.html"), rewrite_internal_links(html404, ""))

    # sitemap.xml with hreflang alternates
    urls = []
    for slug in PAGES_EN:
        en_url, zh_url = page_url("en", slug), page_url("zh", slug)
        alt = (
            f'<xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>'
            f'<xhtml:link rel="alternate" hreflang="zh" href="{zh_url}"/>'
            f'<xhtml:link rel="alternate" hreflang="x-default" href="{en_url}"/>'
        )
        urls.append(f"  <url><loc>{en_url}</loc><lastmod>{TODAY}</lastmod><xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"{en_url}\"/>{alt}</url>")
        urls.append(f"  <url><loc>{zh_url}</loc><lastmod>{TODAY}</lastmod>{alt}</url>")
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
               'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    write(os.path.join(BUILD_DIR, "sitemap.xml"), sitemap)

    write(os.path.join(BUILD_DIR, "robots.txt"),
          f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")

    count = sum(len(p) for p in (PAGES_EN, PAGES_ZH))
    build_rss()
    print(f"Built {count} pages + sitemap.xml + robots.txt + feed.xml -> {BUILD_DIR}")


if __name__ == "__main__":
    build()
