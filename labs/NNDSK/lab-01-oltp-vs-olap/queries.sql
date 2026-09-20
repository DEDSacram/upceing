-- Lab 01 — same question, OLTP vs OLAP shape.
-- Q1 (OLTP): line total per order — joins 3 normalized tables.
SELECT o.id AS order_id, SUM(oi.qty * oi.unit_price) AS total
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
GROUP BY o.id
ORDER BY o.id;

-- Q1 (OLAP): revenue per month — single fact + small date dim, no order join.
SELECT d.year, d.month, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON d.date_key = f.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- Q2 (OLAP): top products by revenue.
SELECT p.name, SUM(f.qty) AS units, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY p.name
ORDER BY revenue DESC
LIMIT 10;
