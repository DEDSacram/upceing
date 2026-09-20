#!/usr/bin/env bash
# Example Elasticsearch queries for lab-11. Requires ES on localhost:9200 + articles index.
set -eu
ES=http://localhost:9200

echo "== create index =="
curl -s -X DELETE "$ES/articles" > /dev/null || true
curl -s -X PUT "$ES/articles" -H 'Content-Type: application/json' \
  -d @../src/main/resources/articles-mapping.json | head -c 300; echo

echo; echo "== bulk index =="
curl -s -X POST "$ES/_bulk" -H 'Content-Type: application/x-ndjson' \
  --data-binary @../src/main/resources/articles-bulk.json | head -c 300; echo
curl -s -X POST "$ES/articles/_refresh" > /dev/null

echo; echo "== match =="
curl -s -X GET "$ES/articles/_search" -H 'Content-Type: application/json' -d \
  '{"query": {"match": {"body": "castle"}}}' | head -c 600; echo

echo; echo "== multi_match =="
curl -s -X GET "$ES/articles/_search" -H 'Content-Type: application/json' -d \
  '{"query": {"multi_match": {"query": "hrad", "fields": ["title^2", "body"]}}}' | head -c 600; echo

echo; echo "== fuzzy =="
curl -s -X GET "$ES/articles/_search" -H 'Content-Type: application/json' -d \
  '{"query": {"match": {"title": {"query": "Prag", "fuzziness": "AUTO"}}}}' | head -c 600; echo

echo; echo "== phrase =="
curl -s -X GET "$ES/articles/_search" -H 'Content-Type: application/json' -d \
  '{"query": {"match_phrase": {"body": "largest ancient castle"}}}' | head -c 600; echo

echo; echo "== highlight =="
curl -s -X GET "$ES/articles/_search" -H 'Content-Type: application/json' -d \
  '{"query": {"match": {"body": "vyhledávání"}}, "highlight": {"fields": {"body": {}}}}' | head -c 800; echo

echo; echo "== suggester =="
curl -s -X GET "$ES/articles/_search" -H 'Content-Type: application/json' -d \
  '{"suggest": {"s": {"prefix": "Pra", "completion": {"field": "title_suggest"}}}}' | head -c 600; echo
