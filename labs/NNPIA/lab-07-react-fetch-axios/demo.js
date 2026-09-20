// demo.js — exercises both client variants against mockApi.js. Plain node, no install.
import { mockFetch } from "./mockApi.js";
import { createFetchClient, createMockAxiosLikeClient, ApiError } from "./apiClient.js";

const fetchClient = createFetchClient(mockFetch);
const axiosLike = createMockAxiosLikeClient()(mockFetch);

console.log("fetch list:", JSON.stringify(await fetchClient.list()));
console.log("axios-like list:", JSON.stringify(await axiosLike.list()));
console.log("fetch create:", JSON.stringify(await fetchClient.create({ name: "Monitor" })));

for (const [label, fn] of [
  ["fetch 404", () => fetchClient.get(999)],
  ["axios-like 404", () => axiosLike.get(999)],
]) {
  try {
    await fn();
    console.log(label, ": UNEXPECTED SUCCESS");
  } catch (e) {
    console.log(`${label}: ApiError status=${e instanceof ApiError ? e.status : "?"} msg=${e.message}`);
  }
}

try {
  await createFetchClient(() => mockFetch("/api/products/boom")).list();
} catch (e) {
  console.log("network failure surfaces as:", e.message);
}
