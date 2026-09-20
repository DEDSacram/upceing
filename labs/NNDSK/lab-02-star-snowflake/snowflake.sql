-- Lab 02 — SNOWFLAKE variant: category hierarchy normalized out of dim_product.
-- Same grain, same facts; only the dimension shape differs.

CREATE TABLE IF NOT EXISTS dim_category (
  category_key SERIAL PRIMARY KEY,
  category     VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_subcategory (
  subcategory_key SERIAL PRIMARY KEY,
  category_key    INTEGER NOT NULL REFERENCES dim_category(category_key),
  subcategory     VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_product (
  product_key     SERIAL PRIMARY KEY,
  sku             VARCHAR(30) NOT NULL,
  name            VARCHAR(100) NOT NULL,
  subcategory_key INTEGER NOT NULL REFERENCES dim_subcategory(subcategory_key)
);

CREATE TABLE IF NOT EXISTS fact_sales (
  product_key INTEGER NOT NULL REFERENCES dim_product(product_key),
  date_key    INTEGER NOT NULL,
  qty         INT NOT NULL,
  amount      NUMERIC(12,2) NOT NULL
);
