# Lab 04 — Elasticsearch: Index, Map, Search

## 1. Theory

### Core concepts

| Term | Meaning |
|---|---|
| **Index** | A collection of documents, roughly analogous to a table in SQL. This lab uses one index: `products`. |
| **Document** | A single JSON object stored in an index (here: one product). Each document has a unique `_id`. |
| **Mapping** | The schema of an index: field names and types (`text`, `keyword`, `double`, …). See `src/main/resources/product-mapping.json`. |
| **`text` vs `keyword`** | `text` fields are **analyzed** (tokenized, lowercased) for full-text search; `keyword` fields are stored verbatim for exact matches, sorting and aggregations. `name` in this lab is `text` with a `name.keyword` sub-field so both work. |
| **Analyzer** | Pipeline (character filters → tokenizer → token filters) that turns `Wireless Headphones` into tokens like `[wireless, headphones]`. This lab uses the `standard` analyzer. |
| **Inverted index** | The underlying data structure: a map from each term to the list of documents containing it (e.g. `wireless → [p1, p2, p4]`). That is why full-text (`match`) queries are fast. |

### Query types used here

- **`match`** — analyzes the query string and scores documents containing any/all of the tokens. Use for full-text fields (`description`, `name`).
- **`term`** — no analysis, exact value comparison. Use for `keyword` fields (`category`, `id`).
- **`range`** — numeric/date interval filter (here on `price`).

## 2. Prerequisites

- Docker + Docker Compose
- Java 17, Maven 3.8+

## 3. Run

```bash
cd lab-04-elasticsearch

# 1. Start Elasticsearch (single node, security off, port 9200)
docker compose up -d

# 2. Wait until green/yellow
curl -s http://localhost:9200/_cluster/health?pretty

# 3. Build and run the Java demo (creates index, bulk-loads 8 products, runs 3 queries)
mvn compile exec:java
```

Environment overrides (defaults `localhost:9200`):

```bash
ES_HOST=localhost ES_PORT=9200 mvn compile exec:java
```

## 4. Verify

```bash
# Cluster is up
curl -s http://localhost:9200/ | head -c 300; echo

# Index exists with mapping
curl -s http://localhost:9200/products?pretty | head -n 40

# Document count (expect 8)
curl -s http://localhost:9200/products/_count?pretty

# Full-text search (match): expect p1, p2, p4
curl -s -X POST http://localhost:9200/products/_search?pretty \
  -H 'Content-Type: application/json' \
  -d '{"query": {"match": {"description": "wireless"}}}'

# Exact search (term): expect p1, p2
curl -s -X POST http://localhost:9200/products/_search?pretty \
  -H 'Content-Type: application/json' \
  -d '{"query": {"term": {"category": "audio"}}}'

# Range search: 50 <= price <= 200
curl -s -X POST http://localhost:9200/products/_search?pretty \
  -H 'Content-Type: application/json' \
  -d '{"query": {"range": {"price": {"gte": 50, "lte": 200}}}}'
```

Same operations via the Java client — see:

- `src/main/java/cz/upce/nnpda/es/ProductService.java:24` (`recreateIndex`)
- `src/main/java/cz/upce/nnpda/es/ProductService.java:37` (`bulkIndex`)
- `src/main/java/cz/upce/nnpda/es/ProductService.java:54` (`searchMatch`)
- `src/main/java/cz/upce/nnpda/es/ProductService.java:65` (`searchTerm`)

## 5. Tasks

1. Add 2 new products to `src/main/resources/sample-products.json`, re-run the app, and confirm `_count` grows to 10.
2. Run the `match` query for `keyboard` and the `term` query for `category = kitchen`. Explain why `term` on the analyzed `description` field would return nothing.
3. Add a method `searchByNamePrefix(String prefix)` using a `prefix` query on `name.keyword` or a `match_phrase_prefix` on `name`, and demonstrate it from `EsApp`.
4. (Bonus) Change `description` analyzer to `english` (stemming), recreate the index, and compare results for the query `running` vs `run`.

## 6. Cleanup

```bash
docker compose down        # stop container
docker compose down -v     # also delete indexed data
```
