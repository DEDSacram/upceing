// Lab 05 — async/await + fetch exercise. Runnable with plain node (>=18).
// Demonstrates: sequential vs parallel awaits, Promise.all, timeout via
// AbortController, and graceful fallback when the network is unavailable.

const API = "https://jsonplaceholder.typicode.com/users";

const FALLBACK_USERS = [
  { id: 1, name: "Ada Lovelace", email: "ada@example.com" },
  { id: 2, name: "Grace Hopper", email: "grace@example.com" },
];

/** fetch with a timeout; rejects on HTTP error or abort. */
export async function fetchJson(url, { timeoutMs = 5000 } = {}) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, { signal: ctrl.signal });
    if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}

/** Sequential: simple but pays full latency of each request. */
export async function loadSequential(urls) {
  const out = [];
  for (const u of urls) out.push(await fetchJson(u));
  return out;
}

/** Parallel: all requests in flight at once. */
export async function loadParallel(urls) {
  return Promise.all(urls.map((u) => fetchJson(u)));
}

/** Parallel with per-request fallback so one failure never kills the batch. */
export async function loadResilient(urls, fallback) {
  const settled = await Promise.allSettled(urls.map((u) => fetchJson(u)));
  return settled.map((r) => (r.status === "fulfilled" ? r.value : fallback));
}

async function main() {
  const urls = [`${API}/1`, `${API}/2`];

  // Parallel load; fall back to local data offline so the demo always prints.
  let users;
  try {
    console.time("parallel");
    users = await loadParallel(urls);
    console.timeEnd("parallel");
    console.log("source: network");
  } catch (err) {
    console.warn("network unavailable (%s), using fallback data", err.message);
    users = FALLBACK_USERS;
  }
  for (const u of users) console.log(`- ${u.id}: ${u.name} <${u.email}>`);

  // Resilient variant: never throws, substitutes fallback per failed request.
  const resilient = await loadResilient(
    ["https://invalid.invalid/users/1", `${API}/1`],
    { id: -1, name: "fallback", email: "fallback@example.com" },
  ).catch(() => [FALLBACK_USERS[0]]);
  console.log("resilient[0]:", JSON.stringify(resilient[0]));
}

main();
