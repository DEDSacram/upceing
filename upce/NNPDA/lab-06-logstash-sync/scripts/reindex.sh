#!/usr/bin/env bash
# Full reindex: wipe the ES index and reset Logstash's jdbc last-run marker
# so the next scheduled run re-reads ALL rows.
set -euo pipefail

ES="${ES_URL:-http://localhost:9200}"
INDEX="${ES_INDEX:-products}"

echo "Deleting index $INDEX (full reindex on next Logstash run)..."
curl -s -X DELETE "$ES/$INDEX?pretty"
echo

echo "Resetting Logstash tracking metadata (sql_last_value)..."
docker compose exec -T logstash rm -f /usr/share/logstash/data/.logstash_jdbc_last_run_products || true

echo "Restarting logstash to pick up the schedule immediately..."
docker compose restart logstash

echo "Done. Watch progress with: docker compose logs -f logstash"
echo "Then run ./scripts/verify.sh"
