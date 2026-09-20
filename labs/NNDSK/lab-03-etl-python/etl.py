"""Lab 03 ETL: extract CSV -> transform (clean, conform) -> load star schema.

Stdlib only (csv, sqlite3). Idempotent: re-running truncates the mart first.
Dirty rows in orders.csv (qty 0, negative qty, unknown product 99) are
quarantined and reported, never loaded.
"""
import csv
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "mart.db"


def extract():
    with open(HERE / "products.csv", newline="", encoding="utf-8") as f:
        products = list(csv.DictReader(f))
    with open(HERE / "orders.csv", newline="", encoding="utf-8") as f:
        orders = list(csv.DictReader(f))
    return products, orders


def transform(products, orders):
    price_by_id = {p["product_id"]: float(p["price"]) for p in products}
    known_ids = set(price_by_id)
    facts, quarantine = [], []
    for o in orders:
        qty = int(o["qty"])
        if o["product_id"] not in known_ids:
            quarantine.append((o, "unknown product_id"))
        elif qty <= 0:
            quarantine.append((o, "qty must be > 0"))
        else:
            facts.append({
                "product_id": int(o["product_id"]),
                "qty": qty,
                "amount": qty * price_by_id[o["product_id"]],
                "order_date": o["order_date"],
            })
    return products, facts, quarantine


def load(products, facts):
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.executescript("""
        CREATE TABLE dim_product(product_key INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL, sku TEXT, name TEXT, category TEXT, price REAL);
        CREATE TABLE dim_date(date_key INTEGER PRIMARY KEY, full_date TEXT UNIQUE,
            year INTEGER, month INTEGER, day INTEGER);
        CREATE TABLE fact_sales(product_key INTEGER REFERENCES dim_product(product_key),
            date_key INTEGER REFERENCES dim_date(date_key), qty INTEGER, amount REAL);
    """)
    key_by_pid = {}
    for p in products:
        cur.execute("INSERT INTO dim_product VALUES (?,?,?,?,?,?)",
                    (int(p["product_id"]), int(p["product_id"]), p["sku"],
                     p["name"], p["category"], float(p["price"])))
        key_by_pid[p["product_id"]] = int(p["product_id"])
    for f in facts:
        y, m, d = map(int, f["order_date"].split("-"))
        date_key = y * 10000 + m * 100 + d
        cur.execute("INSERT OR IGNORE INTO dim_date VALUES (?,?,?,?,?)",
                    (date_key, f["order_date"], y, m, d))
        cur.execute("INSERT INTO fact_sales VALUES (?,?,?,?)",
                    (key_by_pid[str(f["product_id"])], date_key, f["qty"], f["amount"]))
    con.commit()
    counts = {t: cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("dim_product", "dim_date", "fact_sales")}
    con.close()
    return counts


def main():
    products, orders = extract()
    products, facts, quarantine = transform(products, orders)
    counts = load(products, facts)
    print(f"extracted: {len(products)} products, {len(orders)} orders")
    print(f"loaded: {counts}")
    print(f"quarantined: {len(quarantine)} rows")
    for row, reason in quarantine:
        print(f"  SKIP order {row['order_id']}: {reason}")


if __name__ == "__main__":
    main()
