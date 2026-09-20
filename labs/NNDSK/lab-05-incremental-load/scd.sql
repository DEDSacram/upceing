-- Lab 05 — SCD type 1 vs 2 DDL (PostgreSQL).
-- Type 1: overwrite in place (dim_customer, no history).
-- Type 2: versioned rows with validity window (dim_customer_scd2).

CREATE TABLE IF NOT EXISTS dim_customer (
  customer_key SERIAL PRIMARY KEY,
  customer_id  BIGINT NOT NULL UNIQUE,
  name         VARCHAR(100) NOT NULL,
  city         VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_customer_scd2 (
  customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id  BIGINT NOT NULL,
  name         VARCHAR(100) NOT NULL,
  city         VARCHAR(100) NOT NULL,
  valid_from   DATE NOT NULL,
  valid_to     DATE,                       -- NULL = current version
  is_current   BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX IF NOT EXISTS ix_scd2_lookup ON dim_customer_scd2(customer_id, is_current);

-- Current view: the fact table joins here instead of the raw table.
CREATE OR REPLACE VIEW v_dim_customer_current AS
SELECT customer_key, customer_id, name, city
FROM dim_customer_scd2 WHERE is_current;

-- Point-in-time: what did customer 1 look like on 2026-09-02?
-- SELECT * FROM dim_customer_scd2
-- WHERE customer_id = 1 AND valid_from <= DATE '2026-09-02'
--   AND (valid_to IS NULL OR valid_to > DATE '2026-09-02');
