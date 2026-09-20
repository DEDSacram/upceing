# Course guide

## How labs connect

- **JDBC (1)** is the foundation. Everything else (Hibernate, JPA, Logstash JDBC input) builds on SQL + transactions.
- **Hibernate (7) → JPA (8) → Spring Boot (9)** is one progression: native ORM → standard API → full stack.
- **REST (2) vs SOAP (3)**: same domain (books/countries) implemented twice so you can compare.
- **ES basics (4) → Full-text (11) → Kibana (5) → Logstash (6)**: store → analyze → visualize → sync.
- **App servers (10) + Docker (12)**: how to ship labs 2/3/9.
- **Oracle Spatial (13)**: standalone geo extension; uses JDBC (1) + Docker (12).

## Exam checkpoints

1. JDBC: `PreparedStatement`, transaction isolation, connection pooling.
2. REST: verbs, status codes, validation, `Location` header.
3. SOAP: XSD contract-first, WSDL, envelope.
4. ES: index/mapping/document, inverted index.
5. Kibana: data view, Lens, dashboard.
6. Logstash: polling vs CDC, `tracking_column`, `document_id`.
7. Hibernate: session states, lazy/eager, HQL, N+1.
8. JPA: `EntityManager`, JPQL, derived queries, `@Transactional`.
9. Boot: DI, auto-config, profiles, actuator.
10. Servers: jar vs war, embedded vs standalone, reverse proxy.
11. Full-text: analyzers, BM25, fuzziness, highlight.
12. Docker: layers, multi-stage, volumes, networks, compose.
13. Spatial: `SDO_GEOMETRY`, SRID, R-tree index, themes.

## Common ports

| Service | Port |
|---------|------|
| lab-02 REST | 8081 |
| lab-03 SOAP | 8082 |
| lab-09 Boot | 8083 |
| Postgres | 5432 |
| Elasticsearch | 9200 |
| Kibana | 5601 |
| Oracle XE | 1521 |
