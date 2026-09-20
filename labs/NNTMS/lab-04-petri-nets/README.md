# Lab 04 — Petri Nets (Engine + Reachability)

Model concurrency as places/transitions/tokens; explore the reachability graph.

## 1. Theory

- **Petri net:** bipartite graph — **places** hold tokens (state), **transitions** fire when all input places have ≥1 token, moving tokens to outputs. Models sync, choice, and parallelism naturally.
- **Firing rule:** transition `t` enabled iff `marking[p] ≥ 1 ∀ p ∈ inputs(t)`; firing decrements inputs, increments outputs.
- **Reachability graph:** all markings reachable from `M0` — answers boundedness (finite?), deadlocks (no enabled transition?), liveness.
- Demo net: tiny order workflow with a parallel branch (payment ∥ packing) joining at ship.

## 2. Project layout

```
lab-04-petri-nets/
  README.md
  petri.py   # net definition + firing engine + BFS reachability explorer
```

## 3. Run

```bash
cd labs/NNTMS/lab-04-petri-nets
python3 petri.py
python3 petri.py --max-states 100
```

## 4. Verify

1. Default run reports a finite reachability set (expected 7 markings), no deadlock before the end place, and the final marking reachable.
2. `python3 petri.py --max-states 100` exits 0 with the same count.
3. `python3 -m py_compile petri.py` passes.

## 5. Tasks

1. Add a choice branch (express vs standard shipping) and count new markings.
2. Introduce a deadlock on purpose (missing token); show the explorer flags it.
3. Check boundedness: add a transition that mints tokens; cap exploration and report.
4. Translate the Lab-04 NAPIS BPMN gateway into a Petri-net conflict and compare.
