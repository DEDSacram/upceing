#!/usr/bin/env bash
# Compare Postgres row count with the Elasticsearch document count.
set -euo pipefail

ES="${ES_URL:-http://localhost:9200}"
INDEX="${ES_INDEX:-products}"
PGURL="${PG_URL:-postgresql://shop:shop@localhost:5432/shop}"

echo "--- Postgres ---"
if command -v psql >/dev/null 2>&1; then
  psql "$PGURL" -c "SELECT count(*) AS pg_count FROM products;"
else
  echo "psql not found, querying via docker compose instead..."
  docker compose exec -T postgres psql -U shop -d shop -c "SELECT count(*) AS pg_count FROM products;"
fi

echo "--- Elasticsearch ---"
curl -s "$ES/$INDEX/_count?pretty"
echo
echo "--- Sample doc ---"
curl -s "$ES/$INDEX/_search?pretty&size=1"
