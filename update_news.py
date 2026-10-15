#!/usr/bin/env python3
"""Jev Hub auto-update pipeline.

Fetches live sources for Jev (TypeSafe AI System One model) news and pricing,
dedupes against data/news.json, appends new items, and snapshots prices into
data/price.json. Run before `python3 build.py` to refresh the site.

Sources:
  - Hacker News (Algolia API)          -> community stories about Jev / TypeSafe
  - GitHub topic:jev                   -> new ecosystem repos (needs GITHUB_TOKEN for reliability)
  - OpenRouter models API              -> provider pricing for typesafe/jev*
  - Reddit r/LLMDevs                   -> community threads (best-effort)

All sources fail soft: one broken source never blocks the rest.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.parse
from datetime import date, datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
NEWS_FILE = os.path.join(DATA_DIR, "news.json")
PRICE_FILE = os.path.join(DATA_DIR, "price.json")
TODAY = date.today().isoformat()
UA = {"User-Agent": "jev-hub/1.0 (Jev news tracker)"}


NET_FAILS = 0  # incremented on every unreachable source (used by the guards in main())


def http_json(url, timeout=15, headers=None):
    global NET_FAILS
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except Exception:
        NET_FAILS += 1
        raise


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"  ! could not parse {os.path.basename(path)}: {e}", file=sys.stderr)
    return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- sources

RELEVANT = re.compile(r"\bjev\b|typesafe|system one", re.IGNORECASE)
LAUNCH_DAY = "2026-09-14"  # Jev launch — anything dated before this is a different "typesafe"/"jev"


def is_current(item_date):
    return (item_date or TODAY) >= LAUNCH_DAY


def fetch_hn(news):
    """Recent HN stories mentioning jev/typesafe, newest first."""
    new_items = []
    for q in ("jev", "typesafe ai"):
        api = ("https://hn.algolia.com/api/v1/search_by_date?"
               + urllib.parse.urlencode({"query": q, "tags": "story", "hitsPerPage": 30}))
        try:
            data = http_json(api)
        except Exception as e:
            print(f"  - HN query '{q}' failed: {e}")
            continue
        for h in data.get("hits", []):
            title = (h.get("title") or "").strip()
            if not title or not RELEVANT.search(title):
                continue
            object_id = h.get("objectID")
            url = h.get("url") or f"https://news.ycombinator.com/item?id={object_id}"
            if any(i.get("url") == url for i in news):
                continue
            pts, cs = h.get("points") or 0, h.get("num_comments") or 0
            created = (h.get("created_at") or "")[:10] or TODAY
            if not is_current(created):
                continue
            new_items.append({
                "date": created,
                "title": title,
                "summary": f"Hacker News discussion — {pts} points, {cs} comments. "
                           f"Community reaction and first-hand usage reports in the thread.",
                "source": "news.ycombinator.com",
                "url": url,
                "added": TODAY,
            })
    print(f"  - HN: {len(new_items)} new item(s)")
    return new_items


def fetch_github(news):
    """Repos tagged topic:jev, recently updated/created."""
    headers = {}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"token {os.environ['GITHUB_TOKEN']}"
    api = ("https://api.github.com/search/repositories?q="
           + urllib.parse.urlencode({"q": "topic:jev", "sort": "updated", "per_page": 20}))
    try:
        data = http_json(api, headers=headers)
    except Exception as e:
        print(f"  - GitHub failed (rate limit? set GITHUB_TOKEN): {e}")
        return []
    new_items = []
    for r in data.get("items", []):
        full = r.get("full_name", "")
        if any(i.get("url", "").endswith(full) for i in news):
            continue
        desc = (r.get("description") or "").strip()
        stars = r.get("stargazers_count", 0)
        created_repo = (r.get("created_at") or TODAY)[:10]
        if not is_current(created_repo):
            continue
        new_items.append({
            "date": created_repo,
            "title": f"New ecosystem project: {full}",
            "summary": (desc or "No description yet.") + f" — {stars}★ on GitHub.",
            "source": "github.com",
            "url": r.get("html_url"),
            "added": TODAY,
        })
    print(f"  - GitHub: {len(new_items)} new repo(s)")
    return new_items


def fetch_openrouter():
    """Pricing snapshot for any typesafe/jev* model on OpenRouter."""
    try:
        data = http_json("https://openrouter.ai/api/v1/models", timeout=20)
    except Exception as e:
        print(f"  - OpenRouter failed: {e}")
        return None
    models = [m for m in data.get("data", [])
              if "jev" in m.get("id", "").lower() or "jev" in (m.get("name") or "").lower()]
    if not models:
        print("  - OpenRouter: no jev model listed yet")
        return None
    snap = {"date": TODAY, "models": []}
    for m in models:
        p = m.get("pricing") or {}
        # OpenRouter prices are per-token strings; normalize to per-million
        def per_m(v):
            try:
                return round(float(v) * 1_000_000, 6)
            except (TypeError, ValueError):
                return None
        snap["models"].append({
            "id": m.get("id"),
            "input_per_mtok": per_m(p.get("prompt")),
            "output_per_mtok": per_m(p.get("completion")),
            "context": m.get("context_length"),
        })
    print(f"  - OpenRouter: {len(snap['models'])} jev model(s) priced")
    return snap


def fetch_reddit(news):
    """Recent r/LLMDevs+r/LocalLLaMA threads about Jev.

    DISABLED by default: as of 2026-09 Reddit returns HTTP 403 to every
    anonymous request (any User-Agent, any endpoint: www/api/old), so the
    source is dead weight and would only pollute the failure guards. Set
    REDDIT_ENABLED=1 once OAuth credentials are wired in."""
    if os.environ.get("REDDIT_ENABLED") != "1":
        print("  - Reddit: skipped (anonymous access blocked by Reddit; set REDDIT_ENABLED=1 to force)")
        return []
    new_items = []
    for sub in ("LLMDevs", "LocalLLaMA"):
        api = (f"https://www.reddit.com/r/{sub}/search.json?"
               + urllib.parse.urlencode({"q": "jev typesafe", "sort": "new", "limit": 15}))
        try:
            data = http_json(api, headers={"User-Agent": UA["User-Agent"]})
        except Exception as e:
            print(f"  - Reddit r/{sub} failed: {e}")
            continue
        for c in data.get("data", {}).get("children", []):
            d = c.get("data", {})
            title = (d.get("title") or "").strip()
            if not RELEVANT.search(title):
                continue
            url = "https://www.reddit.com" + d.get("permalink", "")
            if any(i.get("url") == url for i in news):
                continue
            rd_date = datetime.fromtimestamp(d.get("created_utc", 0), tz=timezone.utc).date().isoformat()
            if not is_current(rd_date):
                continue
            new_items.append({
                "date": rd_date,
                "title": title,
                "summary": f"Reddit r/{sub} thread — {d.get('num_comments', 0)} comments.",
                "source": f"reddit.com/r/{sub}",
                "url": url,
                "added": TODAY,
            })
    print(f"  - Reddit: {len(new_items)} new thread(s)")
    return new_items


# ------------------------------------------------------- editor comments

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"


def _deepseek_comment(title, summary, source):
    """One original editorial sentence (en + zh) for a news item."""
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        return None
    prompt = (
        "You are the editor of an independent tracker site for the Jev AI model "
        "(a typed-decision model by TypeSafe AI). Write ONE original editorial "
        "sentence (20-35 words) about the news item below: what it means for "
        "developers using Jev, what is genuinely notable, or a caveat. Never "
        "restate the title, never use filler like 'the community discussed'. "
        "Then write the same sentence in natural Simplified Chinese. "
        'Reply with strict JSON only: {"en": "...", "zh": "..."}\n\n'
        f"Title: {title}\nSummary: {summary}\nSource: {source}"
    )
    body = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 300,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")
    req = urllib.request.Request(DEEPSEEK_URL, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    })
    from concurrent.futures import ThreadPoolExecutor

    def _call():
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
        parsed = json.loads(data["choices"][0]["message"]["content"])
        en = (parsed.get("en") or "").strip()
        zh = (parsed.get("zh") or "").strip()
        return (en, zh) if en and zh else None

    # hard wall-clock guard: a slow-trickling response defeats socket timeouts
    with ThreadPoolExecutor(1) as ex:
        fut = ex.submit(_call)
        try:
            return fut.result(timeout=45)
        except Exception as e:
            print(f"  - editor comment failed for '{title[:48]}': {type(e).__name__}")
            fut.cancel()
            return None


def commentate(news):
    """Attach unique editorial comments to items missing one (newest first,
    backfills older boilerplate entries too). Hard budget of 12 calls per run."""
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("  - editor comments: skipped (DEEPSEEK_API_KEY not set)")
        return news, 0
    budget = 8
    changed = 0
    for i in news:  # newest-first
        if budget <= 0:
            break
        if i.get("comment_en") and i.get("comment_zh"):
            continue
        result = _deepseek_comment(i.get("title", ""), i.get("summary", ""), i.get("source", ""))
        if result:
            i["comment_en"], i["comment_zh"] = result
            changed += 1
            budget -= 1
    if changed:
        print(f"  - editor comments: {changed} written")
    return news, changed


# ---------------------------------------------------------------- main

def dedupe(items):
    seen, out = set(), []
    for i in items:
        key = i.get("url") or i.get("title", "").lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(i)
    return out


def main():
    news = load_json(NEWS_FILE, [])
    price_hist = load_json(PRICE_FILE, [])
    print(f"[{TODAY}] update start — {len(news)} existing news items")

    fresh = []
    fresh += fetch_hn(news)
    fresh += fetch_github(news)
    fresh += fetch_reddit(news)

    snap = fetch_openrouter()
    if snap and price_hist and snap["models"] == price_hist[-1].get("models"):
        print("  - OpenRouter: pricing unchanged, no new snapshot")
        snap_recorded = False
    else:
        snap_recorded = bool(snap)

    if fresh or snap_recorded:
        if snap_recorded:
            price_hist.append(snap)
            save_json(PRICE_FILE, price_hist)
        # also surface a price event as a news item
        if snap_recorded and len(price_hist) > 1:
            fresh.append({
                "date": TODAY,
                "title": "Jev pricing changed on OpenRouter",
                "summary": f"Latest listing: {json.dumps(snap['models'])}",
                "source": "openrouter.ai",
                "url": "https://openrouter.ai/models",
                "added": TODAY,
            })
        news = dedupe(fresh + news)  # newest first by fetch order; sorted below
        news.sort(key=lambda i: i.get("date", ""), reverse=True)

    news, commented = commentate(news)
    if fresh or snap_recorded or commented:
        save_json(NEWS_FILE, news)
        print(f"[{TODAY}] wrote {len(fresh)} new item(s), {commented} editor comment(s) "
              f"-> data/news.json ({len(news)} total), price snapshots: {len(price_hist)}")
    else:
        print(f"[{TODAY}] no changes; data files untouched")

    # --- guards: a silently broken feed must show up as a RED run -------------
    # Without these, a blocked network or a changed API looks exactly like a
    # quiet news day: green run, "no changes", stale site for days on end.
    newest = max((i.get("date", "") for i in news), default="")[:10]
    if newest:
        try:
            age = (date.today() - date.fromisoformat(newest)).days
        except ValueError:
            age = 0
        print(f"  - freshness: newest item {newest} ({age} day(s) old)")
        if age > 3:
            print(f"ERROR: news feed is stale — newest item is {age} days old. "
                  f"Check the fetch sources (blocked network / changed API).")
            return 1
    if NET_FAILS >= 3 and not fresh:
        print(f"ERROR: {NET_FAILS} source request(s) failed and nothing was "
              f"fetched — all sources look unreachable.")
        return 1

    # signal for build script
    return 0


if __name__ == "__main__":
    sys.exit(main())
