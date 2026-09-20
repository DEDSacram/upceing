-- Lab 04 — ROLLUP / CUBE / GROUPING SETS on fact_sales (PostgreSQL).
-- Assumes lab-01/03 mart shape: fact_sales(product_key, date_key, qty, amount).

-- Revenue by (month, category) + month subtotals + grand total.
SELECT d.year, d.month, p.category, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY ROLLUP (d.year, d.month, p.category)
ORDER BY d.year, d.month, p.category;

-- All combinations of (month, category): CUBE.
SELECT d.month, p.category, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY CUBE (d.month, p.category)
ORDER BY d.month, p.category;

-- Hand-picked groupings only: per-month, per-category, grand total.
SELECT d.month, p.category, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY GROUPING SETS ((d.month), (p.category), ())
ORDER BY d.month, p.category;

-- Tell detail rows apart from subtotal rows: GROUPING() = 1 means "aggregated away".
SELECT d.month, p.category, SUM(f.amount) AS revenue,
       GROUPING(d.month, p.category) AS grp
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY CUBE (d.month, p.category)
ORDER BY grp, d.month;
