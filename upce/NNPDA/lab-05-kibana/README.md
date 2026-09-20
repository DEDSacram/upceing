# Lab 05 — Kibana: Discover, Visualize, Dashboard

## 1. Theory

- **Kibana** is the UI for the Elastic Stack: search, charts and dashboards over Elasticsearch indices.
- **Discover** — interactive document search/filter for an index. Uses KQL/Kuery (`category: audio and price > 50`).
- **Data view (formerly "index pattern")** — a named pointer to one or more indices (e.g. `products-*`) that Kibana apps use. Without a data view, Discover/Visualize see nothing.
- **Visualize / Lens** — drag-and-drop chart builder. A Lens visualization stores its config as a saved object.
- **Dashboard** — a layout of visualizations + filters, also stored as saved objects (importable NDJSON, see `kibana/dashboard.ndjson`).
- **DevTools Console** — in-browser editor for raw REST calls to Elasticsearch (`GET /products/_count`, …). Samples in `kibana/devtools-console.txt`.

## 2. Prerequisites

- Docker + Docker Compose

## 3. Run

```bash
cd lab-05-kibana

docker compose up -d

# Wait for both services
curl -s http://localhost:9200/_cluster/health?pretty
curl -s http://localhost:5601/api/status | head -c 300; echo

# Seed sample data (creates `products` index + 8 docs)
./scripts/seed.sh

# Run sample queries from the shell (same queries as DevTools)
./scripts/sample-queries.sh
```

Open Kibana: **http://localhost:5601**

## 4. Verify

```bash
curl -s http://localhost:9200/products/_count?pretty
curl -s http://localhost:5601/api/status | grep -o '"level":"[^"]*"'
```

In the browser:

1. DevTools (`/app/dev_tools#/console`) — paste queries from `kibana/devtools-console.txt`, all should return `200 OK`.
2. Confirm `GET /products/_count` returns `8`.

## 5. Tasks (do in Kibana UI)

1. **Create a data view**: Stack Management → Data Views → Create `products-*` (or `products`), no time field → open it in **Discover** and find the 3 `wireless` products with `description : *wireless*`.
2. **Lens chart**: Visualizations → Create → Lens → data view `products-*` → Bar chart, X = Top values of `category`, Y = Average of `price`. Save as `Products - avg price by category`.
3. **Dashboard**: Dashboards → Create → add your Lens chart → save as `Products overview`. Optional: import the provided sample objects via Stack Management → Saved Objects → Import `kibana/dashboard.ndjson`.
4. **KQL exercise**: in Discover, run `category: audio and price > 50` — expect 2 hits. Then `category: kitchen or category: sport` — expect 4 hits.

### Screenshots checklist (submit these)

- [ ] Discover showing the data view + a KQL query with hits.
- [ ] Lens chart (avg price by category).
- [ ] Dashboard containing the chart.
- [ ] DevTools Console with one successful `_search` response.

## 6. Cleanup

```bash
docker compose down        # stop containers
docker compose down -v     # also delete ES data
```
