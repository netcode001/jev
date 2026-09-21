// Pages Function: POST /api/systemone
// Proxy to https://api.typesafe.ai/v1/systemone — fallback for browsers
// blocked by CORS on the direct api.typesafe.ai call. The key is forwarded
// as-is and never stored or logged.
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

async function onRequestPost({ request }) {
  const auth = request.headers.get("Authorization") || "";
  if (!auth.startsWith("Bearer ")) {
    return new Response(JSON.stringify({ error: "Missing Bearer token" }), {
      status: 401,
      headers: cors({ "Content-Type": "application/json" }),
    });
  }
  let body;
  try {
    body = await request.text();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid request body" }), {
      status: 400,
      headers: cors({ "Content-Type": "application/json" }),
    });
  }
  let r;
  try {
    r = await fetch(UPSTREAM, {
      method: "POST",
      headers: { Authorization: auth, "Content-Type": "application/json" },
      body,
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: "Upstream request failed" }), {
      status: 502,
      headers: cors({ "Content-Type": "application/json" }),
    });
  }
  const text = await r.text();
  return new Response(text, {
    status: r.status,
    headers: cors({ "Content-Type": r.headers.get("Content-Type") || "application/json" }),
  });
}

async function onRequestOptions() {
  return new Response(null, { status: 204, headers: cors() });
}
