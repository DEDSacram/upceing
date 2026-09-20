# NNPDA Coursework Pack

Labs, runnable code, and docs for 13 topics. English, Maven, Java 17, Spring Boot 3.2.5.

## Map

| # | Topic | Folder |
|---|-------|--------|
| 1 | JDBC | `lab-01-jdbc/` |
| 2 | REST web services | `lab-02-rest/` |
| 3 | SOAP web services | `lab-03-soap/` |
| 4 | Elasticsearch basics | `lab-04-elasticsearch/` |
| 5 | Kibana | `lab-05-kibana/` |
| 6 | DB sync with Logstash (JDBC → ES) | `lab-06-logstash-sync/` |
| 7 | Hibernate | `lab-07-hibernate/` |
| 8 | JPA | `lab-08-jpa/` |
| 9 | Spring / Spring Boot | `lab-09-springboot/` |
| 10 | Application servers (jar vs war, Tomcat/WildFly, nginx) | `lab-10-appservers/` |
| 11 | Full-text search in Elasticsearch | `lab-11-fulltext-es/` |
| 12 | Docker virtualization | `lab-12-docker/` |
| 13 | Oracle Spatial + MapBuilder/MapViewer | `lab-13-oracle-spatial/` |

Each lab has its own `README.md` with theory, run steps, verify steps, and tasks.

## Prerequisites

- JDK 17, Maven 3.9+
- Docker + Docker Compose plugin
- curl, bash

## Quick start

```bash
# 1. JDBC (needs Postgres)
cd lab-01-jdbc
docker compose up -d
mvn test
mvn exec:java

# 2. REST
cd ../lab-02-rest
mvn spring-boot:run   # :8081

# 3. SOAP
cd ../lab-03-soap
mvn spring-boot:run   # :8082/ws/countries.wsdl

# 4-6. Search stack
cd ../lab-04-elasticsearch && docker compose up -d
cd ../lab-05-kibana && docker compose up -d        # :5601
cd ../lab-06-logstash-sync && docker compose up -d

# 7-9. ORM stack
cd ../lab-07-hibernate && mvn test
cd ../lab-08-jpa && mvn test && mvn spring-boot:run
cd ../lab-09-springboot && mvn test && mvn spring-boot:run  # :8083

# 10-13
cd ../lab-10-appservers && docker compose up --build
cd ../lab-11-fulltext-es && docker compose up -d && bash scripts/queries.sh
cd ../lab-12-docker && bash scripts/build.sh && bash scripts/run.sh
cd ../lab-13-oracle-spatial && docker compose up -d
```

## Suggested study order

1 → 7 → 8 → 9 → 2 → 3 → 10 → 12 → 4 → 11 → 5 → 6 → 13

JDBC → ORM → Boot → HTTP services → deployment → search → geo.

See `docs/` for cross-cutting notes.
