"""Lab 05 — SCD type 1 vs type 2 + incremental load demo (stdlib sqlite3).

Day 1: Ada lives in Pardubice. Day 2: she moves to Prague.
Type 1 overwrites (history lost); Type 2 closes the old version and opens
a new one (history preserved). Re-running day 2 changes nothing (idempotent).
"""
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.executescript("""
    CREATE TABLE dim_customer_scd1(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
    CREATE TABLE dim_customer_scd2(customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL, name TEXT, city TEXT,
        valid_from TEXT NOT NULL, valid_to TEXT, is_current INTEGER NOT NULL);
    CREATE TABLE stg_loaded(batch TEXT PRIMARY KEY);
""")

DAY1 = [("Ada", "Pardubice"), ("Bob", "Prague")]
DAY2 = [("Ada", "Prague"), ("Bob", "Prague")]  # Ada moved


def load_scd1(day, rows):
    for i, (name, city) in enumerate(rows, start=1):
        cur.execute("INSERT INTO dim_customer_scd1 VALUES (?,?,?) "
                    "ON CONFLICT(customer_id) DO UPDATE SET city=excluded.city",
                    (i, name, city))
    cur.execute("INSERT OR IGNORE INTO stg_loaded VALUES (?)", (f"scd1-{day}",))


def load_scd2(day, rows):
    if cur.execute("SELECT 1 FROM stg_loaded WHERE batch=?",
                   (f"scd2-{day}",)).fetchone():
        return  # already applied -> incremental, idempotent
    for i, (name, city) in enumerate(rows, start=1):
        cur_row = cur.execute("SELECT customer_key, city FROM dim_customer_scd2 "
                              "WHERE customer_id=? AND is_current=1", (i,)).fetchone()
        if cur_row is None:
            cur.execute("INSERT INTO dim_customer_scd2 "
                        "(customer_id,name,city,valid_from,valid_to,is_current) "
                        "VALUES (?,?,?,?,NULL,1)",
                        (i, name, city, day))
        elif cur_row[1] != city:
            cur.execute("UPDATE dim_customer_scd2 SET valid_to=?, is_current=0 "
                        "WHERE customer_key=?", (day, cur_row[0]))
            cur.execute("INSERT INTO dim_customer_scd2 "
                        "(customer_id,name,city,valid_from,valid_to,is_current) "
                        "VALUES (?,?,?, ?,NULL,1)", (i, name, city, day))
    cur.execute("INSERT INTO stg_loaded VALUES (?)", (f"scd2-{day}",))


load_scd1("2026-09-01", DAY1)
load_scd2("2026-09-01", DAY1)
load_scd1("2026-09-02", DAY2)
load_scd2("2026-09-02", DAY2)
load_scd2("2026-09-02", DAY2)  # replay -> no-op
con.commit()

print("SCD1 (history lost — Ada only in Prague):")
for row in cur.execute("SELECT * FROM dim_customer_scd1 ORDER BY customer_id"):
    print(" ", row)
print("SCD2 (history kept — Ada twice, old version closed):")
for row in cur.execute("SELECT customer_id,name,city,valid_from,valid_to,is_current "
                       "FROM dim_customer_scd2 ORDER BY customer_id, valid_from"):
    print(" ", row)
print("point-in-time (Ada on 2026-09-01):",
      cur.execute("SELECT city FROM dim_customer_scd2 WHERE customer_id=1 "
                  "AND valid_from<='2026-09-01' AND (valid_to IS NULL OR valid_to>'2026-09-01')")
      .fetchone()[0])
con.close()
