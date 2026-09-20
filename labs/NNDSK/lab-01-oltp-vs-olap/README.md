# Lab 01 — OLTP vs OLAP

One shop modelled twice: normalized OLTP for transactions, star-schema OLAP mart for analytics. Postgres via `docker-compose`.

## 1. Theory

- **OLTP (Online Transaction Processing):** normalized (3NF) tables, one fact per row, many small writes, row-level locking, current state only. Optimized for `INSERT`/`UPDATE` integrity: no duplication, FK constraints enforce consistency (`order_items` PK on `(order_id, product_id)` prevents double lines).
- **OLAP (Online Analytical Processing):** star schema — one central fact table (`fact_sales`: only keys + measures `qty`/`amount`) surrounded by denormalized dimensions (`dim_*`: descriptive attributes). Optimized for big read scans: fewer joins, integer surrogate keys, bitmap/index-friendly.
- **Surrogate vs natural keys:** dimensions use generated `*_key` (stable, small, immune to source-system key changes); the OLTP `customer_id` is kept alongside as the natural key for ETL traceability.
- **Why both:** running `SUM(amount) GROUP BY month` over normalized `orders ⨝ order_items` re-joins millions of rows per query; the mart pre-joins dimensions once at load time (ETL), so each analytic query scans one narrow fact table.

## 2. Project layout

```
lab-01-oltp-vs-olap/
  docker-compose.yml   # postgres:16, db/user nndsk
  schema.sql           # OLTP shop + OLAP star (Postgres; SQLite notes inline)
  queries.sql          # Q1 OLTP vs OLAP + top-products query
```

## 3. Run

```bash
cd lab-01-oltp-vs-olap
docker compose up -d
psql postgresql://nndsk:nndsk@localhost:5432/nndsk -f schema.sql
psql postgresql://nndsk:nndsk@localhost:5432/nndsk -f queries.sql
docker compose down
```

## 4. Verify

1. `\dt` shows `customers, products, orders, order_items` (OLTP) plus `dim_customer, dim_product, dim_date, fact_sales` (OLAP).
2. All three queries in `queries.sql` execute without error (empty results are fine — no seed data yet; lab-03 loads data).
3. `\d fact_sales` shows FKs to all three dimensions and the `ix_fact_sales_date` index.

## 5. Tasks

1. Seed 3 customers / 3 products / 2 orders by hand and run both Q1 variants; compare row counts and explain why they match.
2. Add `dim_store(store_key, city, region)` + `store_key` in `fact_sales`; note what changes in existing queries (nothing — star extensibility).
3. Write the OLTP equivalent of the top-products query (3-table join) and compare its plan (`EXPLAIN`) with the OLAP version.
4. Convert `schema.sql` to SQLite (`BIGSERIAL` → `INTEGER PRIMARY KEY AUTOINCREMENT`, drop `TIMESTAMPTZ`) and document each change.
