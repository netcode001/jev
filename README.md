# Jev Hub

Unofficial information hub for **Jev**, the "System One" AI model by TypeSafe —
a model that reads a text state plus typed questions and returns choices,
scores, or probabilities with confidence estimates. It never generates text.

**Live site: https://jev-ai.live**

## What you'll find on the site

- **Get Access guide** — Jev AI sign up is open (no waitlist, no invite code):
  register at console.typesafe.ai with $5 free credit, or connect via
  Vercel AI Gateway / Cloudflare Workers AI → https://jev-ai.live/get-access/
- **Free Playground** — BYOK: bring your API key, run real Jev decisions in
  the browser. 5 sponsored plays/day even without a key → https://jev-ai.live/playground/
- **Pricing comparison** — $0.042/1M input, output unmetered, vs LLM rates
  (self-reported figures marked) → https://jev-ai.live/pricing/
- **Jev vs LLMs** — decision table: when a typed-decision model beats a
  chat model (and when it doesn't) → https://jev-ai.live/vs-llm/
- **News timeline** — auto-updated daily from HN, Reddit and official sources
  → https://jev-ai.live/news/

## Tech stack

Python static-site generator (single `build.py`) deployed on Cloudflare Pages,
with a scheduled GitHub Action that fetches and republishes Jev news 3x/day.
Bilingual (EN / 中文).

## Related

- Listed in [awesome-jev](https://github.com/heyjunpenn/awesome-jev)
  (Demos & playgrounds)

> Not affiliated with TypeSafe AI. All vendor-reported figures are marked as
> self-reported on the site.
