-- Lab 06 — dashboard feeding queries (PostgreSQL on the lab-01/03 mart).
-- Each query returns display-ready rows: labels, rounded numbers, explicit ORDER BY.

-- KPI cards: total revenue, units, order days, avg daily revenue.
SELECT COUNT(*) AS kpi_days,
       SUM(amount) AS kpi_revenue,
       SUM(qty) AS kpi_units,
       ROUND(AVG(amount), 2) AS kpi_avg_daily
FROM (SELECT date_key, SUM(amount) AS amount, SUM(qty) AS qty
      FROM fact_sales GROUP BY date_key) d;

-- Revenue trend per day (line chart).
SELECT d.full_date AS label, SUM(f.amount) AS revenue, SUM(f.qty) AS units
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
GROUP BY d.full_date
ORDER BY d.full_date;

-- Revenue share per category (pie/donut chart).
SELECT p.category AS label,
       SUM(f.amount) AS revenue,
       ROUND(100.0 * SUM(f.amount) / SUM(SUM(f.amount)) OVER (), 1) AS pct
FROM fact_sales f
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY p.category
ORDER BY revenue DESC;

-- Top 10 products (bar chart / table).
SELECT p.name AS label, SUM(f.qty) AS units, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY p.name
ORDER BY revenue DESC
LIMIT 10;
