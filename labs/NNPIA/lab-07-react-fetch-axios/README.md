# Lab 07 — fetch vs axios + Error Handling

Same product API implemented twice (native `fetch`, axios pattern) against a mocked transport with unified `ApiError` handling. Demo runs with plain node, no install.

## 1. Theory

- **`fetch` quirks:** never rejects on HTTP 4xx/5xx (check `res.ok` yourself); request body must be `JSON.stringify`d manually; no timeout/interceptors built in. Zero dependencies, full control.
- **axios value-add:** rejects on non-2xx automatically, serializes/deserializes JSON, supports instances with `baseURL`, timeouts, and request/response interceptors (ideal for attaching JWT tokens globally). Costs a dependency.
- **Mocked transport:** both clients take their transport as a parameter (`fetchImpl` / axios instance), so the demo and tests inject `mockFetch` instead of the network. Same technique as constructor injection in lab-01, applied to JS.
- **Unified errors:** both variants normalize failures to `ApiError(status, message)` — network failure becomes `status 0`. UI code catches one type regardless of the underlying client.

## 2. Project layout

```
lab-07-react-fetch-axios/
  package.json     # axios listed (only needed for the real axios variant)
  mockApi.js       # in-memory fake fetch transport (offline-safe)
  apiClient.js     # createFetchClient + axios variant (commented, needs npm i) + runnable axios-like mirror
  demo.js          # exercises both variants, prints results + error mapping
```

## 3. Run

```bash
cd lab-07-react-fetch-axios
node demo.js            # no install needed (mock transport)
npm install && node -e "import('./apiClient.js').then(m => console.log(Object.keys(m)))"  # optional real axios
```

## 4. Verify

1. `node --check mockApi.js && node --check apiClient.js && node --check demo.js` all pass.
2. `node demo.js` prints product lists from both variants, a created product, `ApiError status=404` for both missing-product calls, and a network-failure line.
3. Uncomment the real axios variant after `npm install` and point it at a test URL — error shape must stay `ApiError`.

## 5. Tasks

1. Add `update(id, product)` (PUT) and `remove(id)` (DELETE) to both clients + mock transport, with demo lines.
2. Add a request interceptor equivalent for the fetch client that injects `Authorization: Bearer <token>`.
3. Implement timeout support in `createFetchClient` via `AbortController` (reuse lab-05) mapping aborts to `ApiError(0, ...)`.
4. Write a node:test script asserting both clients behave identically (list/get/create/404 cases).
