#!/usr/bin/env bash
# Seed the `products` index with sample data via the _bulk API.
set -euo pipefail

ES="${ES_URL:-http://localhost:9200}"
INDEX="${ES_INDEX:-products}"

echo "Creating index $INDEX (ignore 400 if it already exists)..."
curl -s -X PUT "$ES/$INDEX" \
  -H 'Content-Type: application/json' \
  -d '{
    "settings": {"number_of_shards": 1, "number_of_replicas": 0},
    "mappings": {
      "properties": {
        "id": {"type": "keyword"},
        "name": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
        "description": {"type": "text"},
        "price": {"type": "double"},
        "category": {"type": "keyword"}
      }
    }
  }'
echo

echo "Bulk loading documents..."
curl -s -X POST "$ES/$INDEX/_bulk?refresh" \
  -H 'Content-Type: application/x-ndjson' \
  -d '{"index":{"_id":"p1"}}
{"id":"p1","name":"Wireless Headphones","description":"Wireless over-ear headphones with noise cancellation","price":199.99,"category":"audio"}
{"index":{"_id":"p2"}}
{"id":"p2","name":"Bluetooth Speaker","description":"Portable wireless bluetooth speaker with deep bass","price":89.9,"category":"audio"}
{"index":{"_id":"p3"}}
{"id":"p3","name":"Mechanical Keyboard","description":"RGB mechanical keyboard with tactile switches","price":129.0,"category":"computers"}
{"index":{"_id":"p4"}}
{"id":"p4","name":"Wireless Mouse","description":"Ergonomic wireless mouse with silent clicks","price":39.99,"category":"computers"}
{"index":{"_id":"p5"}}
{"id":"p5","name":"Espresso Machine","description":"Compact espresso machine with milk frother","price":249.0,"category":"kitchen"}
{"index":{"_id":"p6"}}
{"id":"p6","name":"Chef Knife","description":"Stainless steel chef knife, razor sharp","price":59.5,"category":"kitchen"}
{"index":{"_id":"p7"}}
{"id":"p7","name":"Running Shoes","description":"Lightweight running shoes for daily training","price":119.95,"category":"sport"}
{"index":{"_id":"p8"}}
{"id":"p8","name":"Yoga Mat","description":"Non-slip yoga mat with carrying strap","price":29.99,"category":"sport"}
'
echo
echo "Count:"
curl -s "$ES/$INDEX/_count?pretty"
