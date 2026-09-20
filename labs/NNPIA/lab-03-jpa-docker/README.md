# Lab 03 — JPA Entity + Repository + Docker Postgres

`Customer` entity with a Spring Data derived query, Postgres via `docker-compose` for runtime, H2 for tests so `mvn test` works without Docker.

## 1. Theory

- **JPA entity:** a POJO annotated with `@Entity` whose fields map to table columns. `@Id` + `@GeneratedValue(IDENTITY)` delegates key generation to the DB (`BIGSERIAL`). The protected no-arg constructor is required by the JPA provider (Hibernate instantiates via reflection).
- **Repository:** `JpaRepository<Customer, Long>` gives CRUD + paging for free. `findByEmail` is a *derived query* — Spring parses the method name into `... where email = ?`. No SQL written by hand.
- **Two data sources, two configs:** `src/main/resources/application.properties` points at Postgres (`ddl-auto=validate`, schema owned by `schema.sql`); `src/test/resources/application.properties` overrides with H2 in-memory + `create-drop`, so tests never need Docker.
- **`@DataJpaTest`:** slices the context to JPA only (entities, repositories, in-memory DB), rolls each test back in a transaction. Fast, isolated persistence tests.

## 2. Project layout

```
lab-03-jpa-docker/
  pom.xml                                    # data-jpa + postgres (runtime) + h2/test (test)
  docker-compose.yml                         # postgres:16, db nnpia / user nnpia
  src/main/java/cz/upce/nnpia/lab03/
    App.java  Customer.java  CustomerRepository.java
  src/main/resources/{application.properties,schema.sql}
  src/test/{java/.../CustomerRepositoryTest.java,resources/application.properties}
```

## 3. Run

```bash
cd lab-03-jpa-docker
docker compose up -d
psql postgresql://nnpia:nnpia@localhost:5432/nnpia -f src/main/resources/schema.sql
mvn test                  # H2-backed, works WITHOUT Docker
mvn spring-boot:run       # needs Postgres up
docker compose down
```

## 4. Verify

1. `mvn test` is green without Docker running (proves the H2 test config is picked up).
2. With Postgres up, `psql ... -c "\d customers"` shows the table; `SELECT * FROM customers;` reflects saved rows.
3. Stop Docker and re-run `mvn test` — still green (test isolation from infrastructure).

## 5. Tasks

1. Add `List<Customer> findByNameContainingIgnoreCase(String part)` and a `@DataJpaTest` covering it.
2. Add a `POST /api/customers` controller on top of the repository (reuse lab-02 validation) with a MockMvc test.
3. Change `ddl-auto` to `update`, restart, and explain in a comment why `validate` + `schema.sql` is safer for production.
4. Add a unique-email test: saving two customers with the same email must throw `DataIntegrityViolationException`.
