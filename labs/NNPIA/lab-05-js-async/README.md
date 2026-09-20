# Lab 05 — JS async/await + fetch

Plain Node.js exercise: sequential vs parallel fetching, `Promise.all` / `Promise.allSettled`, timeout with `AbortController`, offline fallback. No dependencies.

## 1. Theory

- **`async`/`await`:** an `async` function always returns a `Promise`. `await` pauses *that function* until the promise settles, without blocking the event loop — other work proceeds meanwhile.
- **Sequential vs parallel:** `await` inside a `for` loop runs requests one after another (latency adds up). Mapping URLs to promises first and awaiting `Promise.all(...)` puts all requests in flight at once (latency ≈ slowest single request).
- **`Promise.all` vs `allSettled`:** `all` rejects on the *first* failure (good when every result is required); `allSettled` always resolves with per-item `{status, value/reason}` (good for resilient batches where fallback per item is acceptable).
- **Timeout:** `fetch` has no built-in timeout — wire an `AbortController` signal and `abort()` after N ms; the fetch rejects with an `AbortError`.
- **Errors:** always check `res.ok` — `fetch` only rejects on network failure, not on HTTP 4xx/5xx.

## 2. Project layout

```
lab-05-js-async/
  package.json      # type: module, no dependencies, `npm start`
  async-demo.js     # fetchJson + loadSequential/Parallel/Resilient + main()
```

## 3. Run

```bash
cd lab-05-js-async
node async-demo.js        # works online AND offline (fallback data)
```

## 4. Verify

1. `node --check async-demo.js` passes (syntax clean).
2. `node async-demo.js` prints two users plus a `resilient[0]` line, with or without network.
3. Time the demo online: the `parallel` timer should be well under the sum of two sequential round-trips (add a `console.time` around `loadSequential` to compare).

## 5. Tasks

1. Implement `loadSequential` comparison timing in `main()` and report sequential vs parallel ms in this README.
2. Extend `fetchJson` with a retry (max 3 attempts, exponential backoff) and demonstrate it against an invalid host.
3. Rewrite `loadResilient` using `Promise.all` + per-promise `.catch()` instead of `allSettled`; explain which you prefer in a comment.
4. Add `loadWithLimit(urls, n)` running at most `n` fetches concurrently (no external libs).
