# Lab 06 — Logstash JDBC Sync: Postgres → Elasticsearch

## 1. Theory

### CDC vs polling

| Approach | How it works | Pros | Cons |
|---|---|---|---|
| **Log-based CDC** (e.g. Debezium) | Tails the DB write-ahead log | Near-real-time, captures deletes, low DB load | More moving parts |
| **Polling (this lab)** | Logstash JDBC input re-runs `SELECT … WHERE updated_at > :sql_last_value` on a `schedule` | Simple, no extensions needed | Sync **lag** up to the schedule interval; needs a monotonic `updated_at`; deletes are not propagated unless soft-deleted |

### Key JDBC input options (see `logstash/pipeline/logstash.conf`)

- `schedule => "* * * * *"` — cron, here once per minute.
- `tracking_column => "updated_at"` + `use_column_value => true` — Logstash persists the max seen value in `last_run_metadata_path` and binds it as `:sql_last_value` on the next run. Only newer rows are fetched.
- `tracking_column_type => "timestamp"` — correct comparison for `timestamptz`.
- `jdbc_paging_enabled => true` / `jdbc_page_size => 1000` — pages large result sets instead of loading everything into memory.
- `ORDER BY updated_at ASC` — required so the persisted high-water mark is correct.

### Idempotency

The output sets `document_id => "%{id}"` (the Postgres PK). Re-processing the same row **overwrites** the same ES document instead of creating duplicates — the pipeline is an idempotent upsert. Without `document_id`, every poll would index duplicates.

## 2. Prerequisites

- Docker + Docker Compose (internet access on first build to fetch the Postgres JDBC driver)
- `psql` optional (else `verify.sh` falls back to `docker compose exec`)

## 3. Run

```bash
cd lab-06-logstash-sync

# Build logstash image (installs jdbc plugin + postgres driver) and start all services
docker compose up -d --build

# Follow the sync
docker compose logs -f logstash
```

Logstash polls every minute. Initial sync can take ~1–2 minutes after first start.

## 4. Verify

```bash
./scripts/verify.sh
```

Expected: Postgres `pg_count = 8` and Elasticsearch `_count = 8`.

Manual checks:

```bash
# ES doc count
curl -s http://localhost:9200/products/_count?pretty

# Postgres row count
docker compose exec -T postgres psql -U shop -d shop -c "SELECT count(*) FROM products;"

# Sync-lag test: insert a row, wait <= 70s, re-check _count
docker compose exec -T postgres psql -U shop -d shop \
  -c "INSERT INTO products (name, description, price) VALUES ('Test Item', 'lag probe', 9.99);"
sleep 75
curl -s http://localhost:9200/products/_count?pretty

# Idempotency test: touch a row (bump updated_at without changing data)
docker compose exec -T postgres psql -U shop -d shop \
  -c "UPDATE products SET updated_at = now() WHERE id = 1;"
sleep 75
curl -s http://localhost:9200/products/_count?pretty   # count must NOT grow
```

Full reindex (wipe ES + reset `:sql_last_value`):

```bash
./scripts/reindex.sh
```

## 5. Tasks

1. Insert a new product into Postgres, measure the **sync lag** (time until it appears in `GET /products/_search`), and report it.
2. Update the price of `id = 1` in Postgres. Confirm the ES document is updated in place (same `_id`, new price) — proof of idempotent upsert via `document_id`.
3. Change the Logstash `schedule` to every 10 seconds (`*/10 * * * * *`), restart, and re-measure the lag. What is the trade-off of a tighter schedule?
4. (Bonus) Add a `category TEXT` column to `schema.sql` + pipeline `statement`, run `reindex.sh`, and build the Lab-05 Lens chart on top of the synced index.

## 6. Cleanup

```bash
docker compose down        # stop containers
docker compose down -v     # also delete pg + es + logstash data
```
