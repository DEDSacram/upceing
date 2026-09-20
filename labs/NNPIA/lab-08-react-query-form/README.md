# Lab 08 — React Query + Hook Form Pattern

Server-state caching (React Query) + uncontrolled forms (Hook Form) pattern starter. The framework-free core (`queryLogic.js`) runs with plain node; `.jsx`/hook files are read-first and need `npm install` only inside a real app.

## 1. Theory

- **Server state vs client state:** server data (product list) is cached, shared, stale-prone — React Query owns it (`useQuery` cache + background refetch). Form draft state is local, transient — Hook Form owns it. Mixing the two (e.g. product list in `useState`) causes stale UI and duplicate fetching logic.
- **Query keys:** `productKeys.all = ["products"]`, `detail(id) = ["products", id]` — the cache identity. Invalidating `["products"]` refetches list *and* details (prefix match).
- **Optimistic update:** `onMutate` snapshots cache, writes the guessed result instantly, returns context; `onError` rolls back from context; `onSettled` invalidates to fetch server truth. UI feels instant yet stays correct.
- **Hook Form:** uncontrolled inputs (refs, not `useState` per keystroke) → fewer re-renders; `register` attaches validation; `handleSubmit` gates `onSubmit`; server errors (e.g. 400 `ApiError` from lab-07) render via a `serverError` prop.

## 2. Project layout

```
lab-08-react-query-form/
  package.json        # @tanstack/react-query, react-hook-form, axios (app use only)
  queryLogic.js       # runnable core: keys, stale policy, optimisticUpdate + self-check
  useProducts.js      # useQuery/useMutation pattern (commented imports, read-first)
  ProductForm.jsx     # Hook Form pattern (commented, read-first)
```

## 3. Run

```bash
cd lab-08-react-query-form
node queryLogic.js          # self-check, no install
node --check useProducts.js
npm install                 # only when wiring into a real React app
```

## 4. Verify

1. `node --check queryLogic.js && node --check useProducts.js` pass.
2. `node queryLogic.js` prints `queryLogic self-check: OK` (optimistic apply + rollback + stale policy asserted).
3. After `npm install` in a sandbox app: submitting `ProductForm` with empty name shows `name is required` without any network call.

## 5. Tasks

1. Add `useProduct(id)` detail query with `staleTime: 60_000` and an `enabled: !!id` guard; explain the guard in a comment.
2. Extend `optimisticUpdate` for deletions (remove by id) with a node assertion.
3. Wire `ProductForm`'s `onSubmit` to `useCreateProduct().mutateAsync` and map `ApiError(400)` field messages via `setError`.
4. Compare `staleTime` vs `gcTime` in this README with an experiment note (when does background refetch fire?).
