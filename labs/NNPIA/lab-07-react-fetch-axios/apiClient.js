// apiClient.js — the SAME API surface implemented twice: native fetch vs axios.
// `fetchImpl` / `http` are injectable so the demo + tests use mockApi.js
// while production passes the real `fetch` / axios instance.

export class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

function throwIfHttpError(res, data) {
  if (!res.ok) throw new ApiError(res.status, data?.message ?? `HTTP ${res.status}`);
  return data;
}

// ---- fetch variant (zero dependencies) ----
export function createFetchClient(fetchImpl) {
  const base = "/api/products";
  return {
    async list() {
      const res = await fetchImpl(base);
      return throwIfHttpError(res, await res.json());
    },
    async get(id) {
      const res = await fetchImpl(`${base}/${id}`);
      return throwIfHttpError(res, await res.json());
    },
    async create(product) {
      const res = await fetchImpl(base, { method: "POST", body: JSON.stringify(product) });
      return throwIfHttpError(res, await res.json());
    },
  };
}

// ---- axios variant (needs `npm install`; same behavior, leaner error mapping) ----
// import axios from "axios";
// export function createAxiosClient(http = axios.create({ baseURL: "/api" })) {
//   const wrap = (p) =>
//     p.then((r) => r.data).catch((e) => {
//       throw new ApiError(e.response?.status ?? 0, e.response?.data?.message ?? e.message);
//     });
//   return {
//     list: () => wrap(http.get("/products")),
//     get: (id) => wrap(http.get(`/products/${id}`)),
//     create: (product) => wrap(http.post("/products", product)),
//   };
// }

// ---- axios-equivalent against the mock (runnable without installing axios) ----
export function createMockAxiosLikeClient() {
  // Mirrors the axios variant's error mapping (status 0 = network failure).
  const wrap = async (p) =>
    p.then((data) => data).catch((e) => {
      throw new ApiError(e.status ?? 0, e.message);
    });
  const asAxiosStyle = async (res) => {
    const data = await res.json();
    if (!res.ok) throw { status: res.status, message: data.message };
    return data;
  };
  // NOTE: needs mockFetch injected by the caller (see demo.js).
  return (fetchImpl) => ({
    list: async () => wrap(asAxiosStyle(await fetchImpl("/api/products"))),
    get: async (id) => wrap(asAxiosStyle(await fetchImpl(`/api/products/${id}`))),
    create: async (product) =>
      wrap(asAxiosStyle(await fetchImpl("/api/products", { method: "POST", body: JSON.stringify(product) }))),
  });
}
