# Lab 03 — ETL in Plain Python (stdlib only)

Extract CSV → transform (validate, conform) → load a SQLite star-schema mart. Fully runnable, no Docker. Dirty rows are quarantined, never silently loaded.

## 1. Theory

- **ETL stages:** *Extract* reads source systems without modifying them (here two CSVs); *Transform* cleans and conforms (types, business rules, surrogate keys, date keys); *Load* writes the mart in one transaction. Failures quarantine rows with reasons instead of aborting or corrupting the mart.
- **Conformed dimensions:** `dim_product`/`dim_date` use surrogate keys and canonical formats (`YYYY-MM-DD`, `YYYYMMDD` date key) so every fact joins consistently.
- **Idempotent load:** the script deletes `mart.db` first — re-running from scratch always yields the same mart. Real pipelines use staging tables + `MERGE` instead of full wipe (see lab-05).
- **Data quality gates:** `qty > 0`, known `product_id`, `amount = qty × price` derived (never trusted from source). 3 of 8 order rows are dirty by design.

## 2. Project layout

```
lab-03-etl-python/
  products.csv   # 4 products (clean)
  orders.csv     # 8 orders, 3 dirty (qty 0, qty -1, unknown product 99)
  etl.py         # extract/transform/load + quarantine report, stdlib only
  mart.db        # created on run (gitignored)
```

## 3. Run

```bash
cd lab-03-etl-python
python3 etl.py
sqlite3 mart.db "SELECT d.full_date, p.name, f.qty, f.amount FROM fact_sales f JOIN dim_product p ON p.product_key=f.product_key JOIN dim_date d ON d.date_key=f.date_key ORDER BY d.full_date;"
```

## 4. Verify

1. `python3 -m py_compile etl.py` passes; `python3 etl.py` prints `loaded: {'dim_product': 4, 'dim_date': 3, 'fact_sales': 5}` and 3 `SKIP` lines (orders 106/107/108).
2. Re-run: identical output (idempotent).
3. Spot-check: `2 × Keyboard @1500 = 3000` appears for 2026-09-01.

## 5. Tasks

1. Add an `amount` cross-check: if the CSV ever carries its own amount column, quarantine on mismatch > 0.01.
2. Add `dim_customer` + `customers.csv` and extend facts with `customer_key`.
3. Switch the load to incremental: keep `mart.db`, skip already-loaded `order_id`s (store them in a `stg_loaded` table) — compare with lab-05.
4. Emit a data-quality summary CSV (`order_id,reason`) instead of printing to stdout.
