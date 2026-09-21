// Cloudflare Pages _worker.js (advanced mode)
// - POST /api/systemone  -> proxy to https://api.typesafe.ai/v1/systemone
//   (fallback for browsers blocked by CORS on the direct call;
//    the API key is forwarded as-is, never stored or logged)
// - everything else      -> serve static assets as usual
const UPSTREAM = "https://api.typesafe.ai/v1/systemone";

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

async function handleProxy(request) {
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors() });
  }
  if (request.method !== "POST") {
    return json({ error: "Method not allowed" }, 405);
  }
  const auth = request.headers.get("Authorization") || "";
  if (!auth.startsWith("Bearer ")) {
    return json({ error: "Missing Bearer token" }, 401);
  }
  let body;
  try {
    body = await request.text();
  } catch {
    return json({ error: "Invalid request body" }, 400);
  }
  let r;
  try {
    r = await fetch(UPSTREAM, {
      method: "POST",
      headers: { Authorization: auth, "Content-Type": "application/json" },
      body,
    });
  } catch (e) {
    return json({ error: "Upstream request failed" }, 502);
  }
  const text = await r.text();
  return new Response(text, {
    status: r.status,
    headers: cors({ "Content-Type": r.headers.get("Content-Type") || "application/json" }),
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/systemone") {
      return handleProxy(request);
    }
    return env.ASSETS.fetch(request);
  },
};
