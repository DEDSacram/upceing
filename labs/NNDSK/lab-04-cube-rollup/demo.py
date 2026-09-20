"""Lab 04 — ROLLUP/CUBE equivalent runnable in SQLite.

SQLite has no ROLLUP/CUBE/GROUPING SETS, so each grouping is a GROUP BY
query combined with UNION ALL. Same numbers as cube.sql; NULL marks
the aggregated-away level (COALESCE it to 'ALL' for display).
"""
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.executescript("""
    CREATE TABLE sales(month INT, category TEXT, amount REAL);
    INSERT INTO sales VALUES
      (9,'Peripherals',3000),(9,'Peripherals',2500),(9,'Displays',4500),
      (10,'Peripherals',2200),(10,'Displays',9000);
""")

print("== ROLLUP(month, category): detail + month subtotal + grand total ==")
for row in cur.execute("""
    SELECT month, category, SUM(amount) FROM sales GROUP BY month, category
    UNION ALL
    SELECT month, NULL, SUM(amount) FROM sales GROUP BY month
    UNION ALL
    SELECT NULL, NULL, SUM(amount) FROM sales
    ORDER BY 1, 2
"""):
    print(row)

print("== CUBE(month, category): + category subtotals ==")
for row in cur.execute("""
    SELECT month, category, SUM(amount) FROM sales GROUP BY month, category
    UNION ALL
    SELECT month, NULL, SUM(amount) FROM sales GROUP BY month
    UNION ALL
    SELECT NULL, category, SUM(amount) FROM sales GROUP BY category
    UNION ALL
    SELECT NULL, NULL, SUM(amount) FROM sales
    ORDER BY 1, 2
"""):
    print(row)

print("== GROUPING SETS((month),(category),()): no detail rows ==")
for row in cur.execute("""
    SELECT month, NULL, SUM(amount) FROM sales GROUP BY month
    UNION ALL
    SELECT NULL, category, SUM(amount) FROM sales GROUP BY category
    UNION ALL
    SELECT NULL, NULL, SUM(amount) FROM sales
    ORDER BY 1, 2
"""):
    print(row)

con.close()
