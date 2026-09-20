-- Lab 02 — same question on both variants: revenue per category.
-- STAR: one join (fact -> dim_product).
SELECT p.category, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY p.category
ORDER BY revenue DESC;

-- SNOWFLAKE: three joins (fact -> product -> subcategory -> category).
-- SELECT c.category, SUM(f.amount) AS revenue
-- FROM fact_sales f
-- JOIN dim_product p ON p.product_key = f.product_key
-- JOIN dim_subcategory s ON s.subcategory_key = p.subcategory_key
-- JOIN dim_category c ON c.category_key = s.category_key
-- GROUP BY c.category
-- ORDER BY revenue DESC;

-- Drill-down (star): category -> subcategory revenue.
SELECT p.category, p.subcategory, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_product p ON p.product_key = f.product_key
GROUP BY p.category, p.subcategory
ORDER BY p.category, revenue DESC;
