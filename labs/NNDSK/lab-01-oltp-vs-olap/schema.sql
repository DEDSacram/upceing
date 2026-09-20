-- Lab 01 — OLTP shop (normalized) + OLAP star schema (denormalized).
-- Target: PostgreSQL. SQLite-compatible except BIGSERIAL -> INTEGER PRIMARY KEY
-- AUTOINCREMENT (noted inline); NUMERIC works in both.

-- ============ OLTP: normalized shop (3NF, write-optimized) ============
CREATE TABLE IF NOT EXISTS customers (
  id    BIGSERIAL PRIMARY KEY,
  name  VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS products (
  id    BIGSERIAL PRIMARY KEY,
  sku   VARCHAR(30) NOT NULL UNIQUE,
  name  VARCHAR(100) NOT NULL,
  price NUMERIC(10,2) NOT NULL CHECK (price >= 0)
);

CREATE TABLE IF NOT EXISTS orders (
  id          BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customers(id),
  ordered_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS order_items (
  order_id   BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id BIGINT NOT NULL REFERENCES products(id),
  qty        INT NOT NULL CHECK (qty > 0),
  unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
  PRIMARY KEY (order_id, product_id)
);

-- ============ OLAP: star schema mart (read-optimized) ============
CREATE TABLE IF NOT EXISTS dim_customer (
  customer_key SERIAL PRIMARY KEY,
  customer_id  BIGINT NOT NULL,          -- natural key from OLTP
  name         VARCHAR(100) NOT NULL,
  email        VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_product (
  product_key SERIAL PRIMARY KEY,
  product_id  BIGINT NOT NULL,
  sku         VARCHAR(30) NOT NULL,
  name        VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_date (
  date_key SMALLINT PRIMARY KEY,         -- e.g. YYYYMMDD truncated to INT range of demo
  full_date DATE NOT NULL UNIQUE,
  year      SMALLINT NOT NULL,
  month     SMALLINT NOT NULL,
  day       SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_sales (
  customer_key BIGINT NOT NULL REFERENCES dim_customer(customer_key),
  product_key  BIGINT NOT NULL REFERENCES dim_product(product_key),
  date_key     SMALLINT NOT NULL REFERENCES dim_date(date_key),
  qty          INT NOT NULL,
  amount       NUMERIC(12,2) NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_fact_sales_date ON fact_sales(date_key);
