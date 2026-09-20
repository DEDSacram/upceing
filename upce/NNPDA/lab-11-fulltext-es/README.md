# Lab 11 — Fulltext Search with Elasticsearch

## Theory

- **Analyzers:** tokenizer (standard splits on word boundaries) +
  filters (lowercase, asciifolding strips diacritics, stop removes
  common words, stemmer reduces to roots). Czech analyzer handles
  `hradu/hradem`; `asciifolding` maps `ř`->`r` for typo tolerance.
- **TF-IDF / BM25:** relevance scoring. TF = term frequency in doc,
  IDF = rarity across corpus. BM25 (ES default) adds length
  normalization and term-frequency saturation. Tune with field boosts
  (`title^2`), `operator: AND`, `fuzziness: AUTO`.
- **Highlighting:** returns matching fragments with `<em>` tags.
- **Suggesters:** completion suggester backed by FST for as-you-type
  autocomplete (`title_suggest` field).

## Run

```bash
cd lab-11-fulltext-es
docker compose up -d
curl localhost:9200
bash scripts/queries.sh
mvn spring-boot:run
curl "localhost:8080/api/search?q=hrad"
curl "localhost:8080/api/search/suggest?q=Pra"
```

## Verify

```bash
curl localhost:9200/articles/_count
curl "localhost:9200/articles/_search?q=castle&pretty"
curl "localhost:8080/api/search?q=vyhledavani"   # asciifolding check
```

## Tasks

1. Start ES, create index from `articles-mapping.json`, bulk-load docs.
2. Run each query in `scripts/queries.sh`; compare match vs multi_match
   vs fuzzy vs phrase scores.
3. Add a document in Czech with diacritics, search without diacritics.
4. Tune boost (`title^2` vs `title^5`), observe ranking changes.
5. Extend `SearchService` with a phrase query endpoint.
