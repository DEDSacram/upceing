# Lab 03 — Architecture Quality Metrics

Compute simple structural quality metrics from a component inventory JSON.

## 1. Theory

- **Coupling (CBO-ish):** number of distinct components a component depends on. High coupling → ripple effects.
- **Instability `I = Ce / (Ca + Ce)`** (Martin): `Ce` = efferent (outgoing) coupling, `Ca` = afferent (incoming). `I→1` = unstable/change-prone, `I→0` = stable/hard to change.
- **Abstractness vs distance (lite):** here replaced by a simple **risk score** = `fan_out * churn * (1 + defect_rate)`.
- Thresholds are team conventions, not laws — this lab uses: `fan_out > 4` smells; `I > 0.7` unstable.

## 2. Project layout

```
lab-03-quality-metrics/
  README.md
  components.json   # sample inventory: {name, depends_on[], churn, defects}
  metrics.py        # computes coupling, instability, risk; prints table + warnings
```

## 3. Run

```bash
cd labs/NAPIS/lab-03-quality-metrics
python3 metrics.py components.json
python3 metrics.py --json components.json
```

## 4. Verify

1. `python3 metrics.py components.json` exits 0 and lists `ShopApp` as highest risk.
2. `python3 metrics.py --json components.json` emits parseable JSON with keys `coupling, instability, risk`.
3. `python3 -m py_compile metrics.py` passes.

## 5. Tasks

1. Add a component with a dependency cycle (`A→B→A`); extend the script to detect and report cycles.
2. Tune thresholds via CLI flags (`--fanout-limit`, `--instability-limit`).
3. Add afferent coupling (`Ca`) column and re-rank by instability.
4. Write 1 paragraph: which component would you refactor first and why (metrics + business risk)?
