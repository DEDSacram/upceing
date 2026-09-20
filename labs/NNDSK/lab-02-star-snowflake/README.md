# Lab 02 — Star vs Snowflake

One sales mart modelled twice: denormalized `dim_product` (star) vs normalized category hierarchy (snowflake). Same facts, same grain, different dimension shape.

## 1. Theory

- **Star:** dimension attributes live directly in `dim_product` (`category`, `subcategory` inline). Queries need one join; `category` values repeat per product row (storage cost, update anomalies if a category is renamed).
- **Snowflake:** hierarchy normalized into `dim_category` ← `dim_subcategory` ← `dim_product`. No redundancy, single place to rename a category; every query pays extra joins and the optimizer has more tables to plan.
- **Rule of thumb:** prefer star for query speed and simplicity (disk is cheap, BI tools love flat dims); snowflake only when a hierarchy is shared by many dimensions, very large, or updated frequently.
- **Grain unchanged:** both variants keep `fact_sales` at (product × date) grain — the comparison is purely about dimension normalization, never about fact detail.

## 2. Project layout

```
lab-02-star-snowflake/
  docker-compose.yml
  star.sql         # denormalized dim_product + fact
  snowflake.sql    # dim_category/dim_subcategory/dim_product + fact
  queries.sql      # revenue-per-category on star (snowflake version commented) + drill-down
```

## 3. Run

```bash
cd lab-02-star-snowflake
docker compose up -d
psql postgresql://nndsk:nndsk@localhost:5432/nndsk -f star.sql
psql postgresql://nndsk:nndsk@localhost:5432/nndsk -f queries.sql
# separately, on a scratch DB: psql ... -f snowflake.sql (uncomment its query)
docker compose down
```

## 4. Verify

1. `star.sql` and `snowflake.sql` each create `fact_sales` with the same measures (`qty`, `amount`) — diff the fact definitions to confirm.
2. The star query runs with a single join; the snowflake variant (commented) needs three — count `JOIN` keywords.
3. `EXPLAIN` on both (after seeding identical rows) shows fewer nodes for star.

## 5. Tasks

1. Seed 2 categories × 2 subcategories × 2 products in both variants and prove both revenue-per-category queries return identical numbers.
2. Rename a category: count the `UPDATE` statements needed in star (N product rows) vs snowflake (1 row) — document the anomaly.
3. Add a `dim_brand` snowflaked off `dim_product` and show the new query join chain.
4. Decide for a 10M-row `dim_product`: star or snowflake? Justify with storage math (avg. string bytes × rows).
