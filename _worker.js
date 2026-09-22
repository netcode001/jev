// Cloudflare Pages advanced-mode worker.
// Serves static assets and proxies /api/systemone to api.typesafe.ai.
// Two modes:
//   - BYOK: request carries an Authorization header -> forwarded as-is
//     (fallback for browsers blocked by CORS on the direct call).
//   - Free trial: no Authorization -> injects $TYPESAFE_API_KEY (env var,
//     never stored in the repo) after rate limiting:
//       per-IP 5 plays/day, site-wide 500 plays/day, state <= 20k chars.
// Counters use the Cache API (same-colo consistent, no KV binding needed).

const UPSTREAM = "https://api.typesafe.ai/v1/systemone";
const FREE_PER_IP = 5;
const FREE_DAILY_SITE = 500;
const MAX_STATE_CHARS = 20000;
const MAX_QUESTIONS = 8;

function cors(extra = {}) {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Authorization, Content-Type",
    "Access-Control-Max-Age": "86400",
    ...extra,
  };
}

function json(body, status) {
  return new Response(JSON.stringify(body), {
    status,
    headers: cors({ "Content-Type": "application/json" }),
  });
}

async function sha1Hex(s) {
  const buf = await crypto.subtle.digest("SHA-1", new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

// Cache-API counter: match -> n+1 -> put. Best-effort (races may undercount
// under heavy concurrency) which is fine for an abuse guard.
async function bumpCount(cache, key, max) {
  const u = "https://counter.jev-ai.internal/" + key;
  let n = 0;
  const hit = await cache.match(u);
  if (hit) {
    const v = parseInt(await hit.text(), 10);
    if (!isNaN(v)) n = v;
  }
  if (n >= max) return { count: n, ok: false };
  n += 1;
  const res = new Response(String(n), {
    headers: { "Cache-Control": "public, max-age=86400" },
  });
  await cache.put(u, res.clone());
  return { count: n, ok: true };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/systemone") {
      return handleProxy(request, env);
    }
    return env.ASSETS.fetch(request);
  },
};

async function handleProxy(request, env) {
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors() });
  }
  if (request.method !== "POST") {
    return json({ error: "Method not allowed" }, 405);
  }

  let body;
  try {
    body = await request.text();
  } catch {
    return json({ error: "Invalid request body" }, 400);
  }
  if (body.length > 300000) return json({ error: "Payload too large" }, 413);

  const auth = request.headers.get("Authorization") || "";
  const headers = { Authorization: auth, "Content-Type": "application/json" };
  let freeRemaining = null;

  if (!auth) {
    // ---- free trial mode: rate-limit, then inject the site key ----
    const siteKey = env.TYPESAFE_API_KEY;
    if (!siteKey) {
      return json({ error: "free_trial_unavailable", message: "Free trial is not configured yet — bring your own key from console.typesafe.ai ($5 free credit)." }, 503);
    }
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const d = dayKey();
    const cache = caches.default;

    const site = await bumpCount(cache, "free-site-" + d, FREE_DAILY_SITE);
    if (!site.ok) {
      return json({ error: "rate_limited", message: "The free trial quota is exhausted for today. You can still run unlimited decisions with your own key." }, 429);
    }
    const ipHash = await sha1Hex(ip);
    const ipr = await bumpCount(cache, "free-ip-" + ipHash + "-" + d, FREE_PER_IP);
    if (!ipr.ok) {
      return json({ error: "rate_limited", message: "You have used all " + FREE_PER_IP + " free plays for today. Come back tomorrow, or sign up at console.typesafe.ai for $5 in free credit and run with your own key." }, 429);
    }
    freeRemaining = FREE_PER_IP - ipr.count;
    headers.Authorization = "Bearer " + siteKey;
  }

  // sanity-check before paying for the upstream call
  let payload;
  try {
    payload = JSON.parse(body);
  } catch {
    return json({ error: "Invalid JSON" }, 400);
  }
  const stateStr = typeof payload.state === "string" ? payload.state : JSON.stringify(payload.state || "");
  if (stateStr.length > MAX_STATE_CHARS) {
    return json({ error: "state_too_large", message: "Free trial limit is " + MAX_STATE_CHARS + " characters of state." }, 413);
  }
  const qn = payload.questions ? Object.keys(payload.questions).length : 0;
  if (!qn || qn > MAX_QUESTIONS) {
    return json({ error: "bad_questions", message: "Provide between 1 and " + MAX_QUESTIONS + " questions." }, 422);
  }

  let r;
  try {
    r = await fetch(UPSTREAM, { method: "POST", headers, body });
  } catch (e) {
    return json({ error: "Upstream request failed" }, 502);
  }
  const text = await r.text();
  const out = cors({ "Content-Type": r.headers.get("Content-Type") || "application/json" });
  if (freeRemaining !== null) {
    out["X-Free-Remaining"] = String(freeRemaining);
    out["Access-Control-Expose-Headers"] = "X-Free-Remaining";
  }
  return new Response(text, { status: r.status, headers: out });
}
