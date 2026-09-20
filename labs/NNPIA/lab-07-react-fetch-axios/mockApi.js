// mockApi.js — in-memory fake transport. Both client variants below talk to
// this instead of the network, so `node demo.js` works offline and tests are hermetic.
// Swap `mockFetch` for global `fetch` (and axios instance for real axios) in production.

export const DB = [
  { id: 1, name: "Keyboard" },
  { id: 2, name: "Mouse" },
];

function ok(data, status = 200) {
  return { ok: true, status, json: async () => data };
}
function fail(status, message) {
  return { ok: false, status, json: async () => ({ message }) };
}

/** Drop-in replacement for `fetch(url, opts)` used by the demo. */
export async function mockFetch(url, { method = "GET", body } = {}) {
  const id = Number(url.split("/").pop());
  await new Promise((r) => setTimeout(r, 5)); // fake latency
  if (url.endsWith("/boom")) throw new Error("network down");
  if (method === "GET" && Number.isNaN(id)) return ok([...DB]);
  if (method === "GET") {
    const found = DB.find((p) => p.id === id);
    return found ? ok({ ...found }) : fail(404, "not found");
  }
  if (method === "POST") {
    const parsed = JSON.parse(body);
    if (!parsed.name) return fail(400, "name required");
    const created = { id: Math.max(...DB.map((p) => p.id)) + 1, ...parsed };
    DB.push(created);
    return ok(created, 201);
  }
  return fail(405, "method not allowed");
}
