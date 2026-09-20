# Lab 05 — Application Portfolio Analysis (TIME)

Score an application portfolio CSV into Gartner TIME quadrants (Tolerate / Invest / Migrate / Eliminate).

## 1. Theory

- **Application portfolio management:** inventory all apps, score business value vs technical health, decide per-quadrant strategy.
- **TIME quadrants:** high value + high health = **Invest**; high value + low health = **Migrate**; low value + high health = **Tolerate**; low value + low health = **Eliminate**.
- **Scoring here:** `value` (0–10, business fit) and `health` (0–10, tech quality) come from the CSV; threshold default 5.0 (median split). Cost is reported, not scored — used to prioritize Eliminate candidates by savings.

## 2. Project layout

```
lab-05-portfolio-analysis/
  README.md
  portfolio.csv    # sample: name,value,health,annual_cost
  portfolio.py     # scores quadrants, prints table + summary
```

## 3. Run

```bash
cd labs/NAPIS/lab-05-portfolio-analysis
python3 portfolio.py portfolio.csv
python3 portfolio.py --threshold 6 portfolio.csv
```

## 4. Verify

1. `python3 portfolio.py portfolio.csv` lists all 8 apps with correct quadrants (LegacyPayroll → Eliminate, ShopApp → Invest).
2. Summary counts add up to the row count and total Eliminate savings are printed.
3. `python3 -m py_compile portfolio.py` passes.

## 5. Tasks

1. Add a `risk` column and re-score: any app with `risk > 7` is forced to Migrate/Eliminate regardless of quadrant.
2. Plot value vs health scatter (matplotlib or ASCII) with quadrant lines.
3. Add a `--format json` export for downstream dashboards.
4. Write a 1-page rationalization plan: which 2 apps to kill first, savings, migration target.
