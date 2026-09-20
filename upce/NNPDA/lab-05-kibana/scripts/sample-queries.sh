#!/usr/bin/env bash
# Run a set of sample queries against the `products` index.
set -euo pipefail

ES="${ES_URL:-http://localhost:9200}"
INDEX="${ES_INDEX:-products}"

q() {
  echo "=== $1 ==="
  curl -s -X POST "$ES/$INDEX/_search?pretty" -H 'Content-Type: application/json' -d "$2"
  echo
}

q "match: description=wireless" '{"query":{"match":{"description":"wireless"}}}'
q "term: category=audio" '{"query":{"term":{"category":"audio"}}}'
q "range: 50<=price<=200" '{"query":{"range":{"price":{"gte":50,"lte":200}}},"sort":[{"price":"desc"}]}'
q "aggs: avg price by category" '{"size":0,"aggs":{"by_category":{"terms":{"field":"category"},"aggs":{"avg_price":{"avg":{"field":"price"}}}}}}'
