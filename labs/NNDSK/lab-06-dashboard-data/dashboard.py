"""Lab 06 — dashboard data: aggregate queries + CSV export (stdlib only).

Builds a demo mart in-memory, runs the same four dashboard queries as
dashboard.sql (Postgres), and exports each result to exports/*.csv —
the files a frontend chart library would consume.
"""
import csv
import sqlite3
from pathlib import Path

EXPORTS = Path(__file__).parent / "exports"
EXPORTS.mkdir(exist_ok=True)

con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.executescript("""
    CREATE TABLE dim_date(date_key INT PRIMARY KEY, full_date TEXT, year INT, month INT);
    CREATE TABLE dim_product(product_key INT PRIMARY KEY, name TEXT, category TEXT);
    CREATE TABLE fact_sales(product_key INT, date_key INT, qty INT, amount REAL);
    INSERT INTO dim_date VALUES (20260901,'2026-09-01',2026,9),(20260902,'2026-09-02',2026,9);
    INSERT INTO dim_product VALUES (1,'Keyboard','Peripherals'),(2,'Mouse','Peripherals'),(3,'Monitor','Displays');
    INSERT INTO fact_sales VALUES (1,20260901,2,3000),(2,20260901,5,2500),(3,20260902,1,4500);
""")

QUERIES = {
    "kpi": """SELECT COUNT(*) AS days, SUM(amount) AS revenue, SUM(qty) AS units
              FROM (SELECT date_key, SUM(amount) AS amount, SUM(qty) AS qty
                    FROM fact_sales GROUP BY date_key)""",
    "trend": """SELECT d.full_date AS label, SUM(f.amount) AS revenue, SUM(f.qty) AS units
                FROM fact_sales f JOIN dim_date d ON d.date_key=f.date_key
                GROUP BY d.full_date ORDER BY d.full_date""",
    "share": """SELECT p.category AS label, SUM(f.amount) AS revenue
                FROM fact_sales f JOIN dim_product p ON p.product_key=f.product_key
                GROUP BY p.category ORDER BY revenue DESC""",
    "top": """SELECT p.name AS label, SUM(f.qty) AS units, SUM(f.amount) AS revenue
              FROM fact_sales f JOIN dim_product p ON p.product_key=f.product_key
              GROUP BY p.name ORDER BY revenue DESC LIMIT 10""",
}

for name, sql in QUERIES.items():
    rows = cur.execute(sql).fetchall()
    cols = rows[0].keys() if rows else []
    with open(EXPORTS / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows([tuple(r) for r in rows])
    print(f"{name}.csv: {len(rows)} row(s) -> {EXPORTS / f'{name}.csv'}")

con.close()
