# Lab 06 — Dashboard Data (Aggregation + CSV Export)

Four display-ready aggregation queries (KPI cards, trend, share, top-N) in `dashboard.sql` (Postgres) with a runnable SQLite mirror `dashboard.py` exporting each result to `exports/*.csv` for a chart frontend.

## 1. Theory

- **Aggregate at the DB, render in the client:** the dashboard never fetches raw facts — each widget gets one grouped query returning few rows (`GROUP BY` + `ORDER BY` + `LIMIT`). Network payload stays KBs even with billions of fact rows behind it.
- **Display-ready shape:** every query returns a `label` column plus rounded measures, pre-sorted — the frontend maps rows to chart points 1:1 without reshaping.
- **Window functions for shares:** `SUM(SUM(amount)) OVER ()` computes the grand total alongside grouped rows in one pass — percentage share without a second query or client-side math.
- **CSV as contract:** `exports/{kpi,trend,share,top}.csv` is the handoff format — BI tools, spreadsheets, and JS chart libs all ingest it; regenerating the files refreshes the dashboard.

## 2. Project layout

```
lab-06-dashboard-data/
  dashboard.sql   # 4 Postgres queries: kpi, trend, share (window fn), top-10
  dashboard.py    # runnable mirror on in-memory SQLite + CSV export (stdlib only)
  exports/        # created on run: kpi.csv, trend.csv, share.csv, top.csv
```

## 3. Run

```bash
cd lab-06-dashboard-data
python3 dashboard.py
cat exports/trend.csv
psql postgresql://nndsk:nndsk@localhost:5432/nndsk -f dashboard.sql  # needs mart + compose up
```

## 4. Verify

1. `python3 -m py_compile dashboard.py` passes; `python3 dashboard.py` prints 4 export lines and `exports/` holds 4 non-empty CSVs with header rows.
2. `trend.csv` has 2 rows (one per day); `share.csv` categories sum to total revenue (3000+2500+4500 = 10000).
3. `dashboard.sql` parses on Postgres (all four queries execute against the lab-03-loaded mart).

## 5. Tasks

1. Add the `pct` window-function column to `share` in `dashboard.py` (SQLite supports window functions) and assert percentages sum to ~100.
2. Add a week-over-week trend query (`LAG(revenue) OVER (ORDER BY label)`) to both files.
3. Parameterize `dashboard.py` with `--since YYYY-MM-DD` (argparse, still stdlib) filtering all queries.
4. Serve `exports/` with `python3 -m http.server` and sketch (in this README) which chart type each CSV feeds and why.
