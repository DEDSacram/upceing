# Lab 04 — CUBE / ROLLUP / GROUPING SETS

Multi-level aggregations in one pass (Postgres `cube.sql`) plus a SQLite-runnable equivalent (`demo.py`, stdlib only — SQLite lacks these constructs, so `UNION ALL` emulates them).

## 1. Theory

- **The problem:** subtotals per month + per category + grand total naively need 4 queries and 4 scans. `CUBE`/`ROLLUP` compute all groupings in one scan.
- **`ROLLUP (a, b, c)`:** hierarchical — `(a,b,c)`, `(a,b)`, `(a)`, `()`. Use for drill-down hierarchies (year → month → category): 4 groupings, not 8.
- **`CUBE (a, b)`:** all 2ⁿ combinations — `(a,b)`, `(a)`, `(b)`, `()`. Use when every slice matters (month totals AND category totals AND grand total).
- **`GROUPING SETS`:** hand-picked list, e.g. `((month), (category), ())` skips detail rows entirely — cheapest when you only need the margins.
- **`GROUPING()`:** distinguishes "NULL because subtotal" from "NULL in data" (returns 1 for aggregated-away columns); `COALESCE(col, 'ALL')` for display.
- **SQLite gap:** SQLite supports plain `GROUP BY` only — `demo.py` unions one `GROUP BY` per grouping, identical numbers, N scans instead of one.

## 2. Project layout

```
lab-04-cube-rollup/
  docker-compose.yml
  cube.sql    # ROLLUP + CUBE + GROUPING SETS + GROUPING() on the mart (Postgres)
  demo.py     # same groupings via UNION ALL on in-memory SQLite (runnable anywhere)
```

## 3. Run

```bash
cd lab-04-cube-rollup
python3 demo.py                                     # works everywhere, no Docker
docker compose up -d                                # Postgres variants:
psql postgresql://nndsk:nndsk@localhost:5432/nndsk -f cube.sql
```

## 4. Verify

1. `python3 -m py_compile demo.py` passes; `python3 demo.py` prints 3 sections: ROLLUP 7 rows (4 detail + 2 month subtotals + grand), CUBE 9 rows, GROUPING SETS 5 rows.
2. Grand total is identical in all three sections (21200).
3. On Postgres, `GROUPING(month, category)` is 0 on detail rows, >0 on subtotal rows.

## 5. Tasks

1. Add a 3-column `ROLLUP(year, month, category)` to `cube.sql` and count groupings (answer: 4); then `CUBE` the same 3 columns (answer: 8) — document the blowup.
2. Extend `demo.py` with `COALESCE` display labels (`ALL`) and assert the grand total equals 21200.
3. Rewrite the CUBE query with `GROUPING SETS` enumerating all 4 combos explicitly; verify identical output.
4. Benchmark on the lab-03 mart: time `CUBE` vs 4 separate `GROUP BY` queries with `EXPLAIN ANALYZE` and note the winner.
