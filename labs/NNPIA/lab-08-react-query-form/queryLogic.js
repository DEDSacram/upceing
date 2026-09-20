// queryLogic.js — framework-free core of the React Query pattern.
// Runnable + testable with plain node: cache key factory, stale-time policy,
// and optimistic-update helper. The .jsx files consume these.

export const productKeys = {
  all: ["products"],
  detail: (id) => ["products", id],
};

/** Central stale-time policy: list 30s, detail 60s. */
export function staleTimeFor(key) {
  return key.length === 1 ? 30_000 : 60_000;
}

/**
 * Optimistic-update helper: applies `updater` to cached `oldData`,
 * returns { optimistic, rollback } for onMutate/onError handlers.
 */
export function optimisticUpdate(oldData, updater) {
  const optimistic = updater(structuredClone(oldData ?? []));
  return { optimistic, rollback: () => oldData };
}

// --- runnable self-check (node queryLogic.js) ---
import { strict as assert } from "node:assert";

const prev = [{ id: 1, name: "Keyboard" }];
const { optimistic, rollback } = optimisticUpdate(prev, (d) => {
  d.push({ id: 2, name: "Mouse" });
  return d;
});
assert.equal(optimistic.length, 2);
assert.equal(rollback().length, 1, "rollback restores previous cache");
assert.deepEqual(staleTimeFor(productKeys.all), 30_000);
assert.deepEqual(staleTimeFor(productKeys.detail(1)), 60_000);
console.log("queryLogic self-check: OK");
