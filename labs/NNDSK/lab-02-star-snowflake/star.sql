-- Lab 02 — STAR variant: denormalized dim_product (category attributes inline).
-- Target: PostgreSQL, sqlite-compatible (SERIAL -> INTEGER PRIMARY KEY AUTOINCREMENT).

CREATE TABLE IF NOT EXISTS dim_product (
  product_key SERIAL PRIMARY KEY,
  sku         VARCHAR(30) NOT NULL,
  name        VARCHAR(100) NOT NULL,
  category    VARCHAR(50) NOT NULL,
  subcategory VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_sales (
  product_key INTEGER NOT NULL REFERENCES dim_product(product_key),
  date_key    INTEGER NOT NULL,
  qty         INT NOT NULL,
  amount      NUMERIC(12,2) NOT NULL
);
