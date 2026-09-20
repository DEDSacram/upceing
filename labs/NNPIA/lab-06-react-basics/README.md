# Lab 06 — React Basics (no build)

Minimal JSX/props/state starter as static files. No npm, no Vite, no build step to *read* the code; open `index.html` in a browser to run it (CDN React + Babel standalone).

## 1. Theory

- **Component:** a function returning UI (JSX). React re-calls it whenever its state/props change and reconciles the DOM diff.
- **Props:** read-only inputs from the parent (`label`, `start`, `step`). Data flows down; a component must never mutate its props.
- **State (`useState`):** per-component-instance mutable memory (`count`, `name`). `setCount` schedules a re-render — the variable itself updates only on the next render, so prefer the updater form `setCount(c => c + step)`.
- **`key` in lists:** `key={c.label}` tells the reconciler which rendered item corresponds to which data item, so state isn't mixed up on reorder.
- **Controlled input:** `<input value={name} onChange={...}>` — React state is the single source of truth for the field value.

## 2. Project layout

```
lab-06-react-basics/
  index.html     # CDN React 18 + Babel standalone, mounts <App />
  Counter.jsx    # props + useState + events starter
  App.jsx        # composition + list rendering + controlled input starter
```

No `package.json`: nothing to install, nothing to build.

## 3. Run

```bash
cd lab-06-react-basics
python3 -m http.server 8000   # or any static server; file:// also works
# open http://localhost:8000 in a browser (needs network for the CDN scripts)
```

## 4. Verify

1. The page shows `Hello, NNPIA!`, a name input, and two counters.
2. Typing in the input updates the heading live (controlled input works).
3. `+1`/`+5` increment their own counter only; `reset` restores `start` (independent state per instance).

## 5. Tasks

1. Add a `step` selector to `Counter` (buttons 1/5/10) storing step in state.
2. Add a `TodoList` component: input + add button, list with delete per item (use stable `key`s, not array indices — explain why in a comment).
3. Lift state up: move both counters' counts into `App` and show their sum; note when lifting is worth it.
4. Convert `Counter` to TypeScript-style prop documentation via `Counter.propTypes`-like JSDoc comments.
