# Lab 08 — Spring Data JPA

JPA on top of Spring Boot: entities, repositories, JPQL, transactions.

## Theory

### JPA vs Hibernate
- **JPA** (`jakarta.persistence`) is a specification: annotations (`@Entity`, `@ManyToOne`), `EntityManager`, JPQL.
- **Hibernate** is the most common JPA *provider* (implementation). Spring Boot uses Hibernate by default under the hood.
- Lab 07 used the native Hibernate API (`SessionFactory`); here you use the portable JPA API via Spring Data.

### EntityManager
- JPA counterpart of Hibernate `Session`. Manages the persistence context (first-level cache, dirty checking).
- In Spring you rarely touch it directly — repositories/services do — but it is available via `@PersistenceContext`.
- States (transient / managed / detached / removed) mirror Lab 07.

### JPQL vs Criteria
- **JPQL**: string queries over entities (`select p from Product p where p.price < :max`). Readable, used with `@Query`.
- **Criteria API**: type-safe programmatic queries (`CriteriaBuilder`, `Root<Product>`). Verbose but refactor-safe and good for dynamic filters.
- **Derived queries**: method names parsed by Spring Data (`findByCategoryName`, `findByPriceBetween`) — no query string at all.

### Repositories
- Extend `JpaRepository<Product, Long>` to get CRUD + paging + sorting for free.
- Add derived methods or `@Query` methods for custom searches.
- Tested with `@DataJpaTest`: in-memory DB, transactional rollback per test, `EntityManager` available.

### Transactions
- `@Transactional` on service methods: all writes commit together or roll back together.
- Read-only operations do not need it; multi-write use cases (create product + category) do.
- `ProductService.createWithCategory()` shows a transaction spanning `EntityManager.persist()` + repository `save()`.

## Project layout
- `JpaApplication` — Spring Boot entry point.
- `entity/Category`, `entity/Product` — `@OneToMany` / `@ManyToOne` + Bean Validation.
- `repository/ProductRepository` — derived queries + `@Query` JPQL.
- `service/ProductService` — `@Transactional` business logic, validation.
- `controller/ProductController` — minimal REST (`/api/products`).
- `application.properties` — H2 default; PostgreSQL block commented.
- `data.sql` — seed data.

## Run
```bash
cd lab-08-jpa
mvn spring-boot:run
# REST on http://localhost:8082/api/products
```

## Verify
```bash
mvn test
```
`ProductRepositoryTest` (`@DataJpaTest`) covers derived queries, `@Query` JPQL, and case-insensitive search.

Curl smoke test (app running):
```bash
curl http://localhost:8082/api/products
curl "http://localhost:8082/api/products?q=mouse"
```

## Tasks
1. Add `findByStockGreaterThanEqualOrderByPriceAsc` and test it.
2. Add a paginated query `Page<Product> findByCategoryName(String name, Pageable pageable)`; write a test with `PageRequest.of(0, 2)`.
3. Write a Criteria API query (via `JpaSpecificationExecutor` or `EntityManager`) for dynamic price/stock filtering.
4. Add a `@Modifying` bulk update (`update stock where ...`) and explain why it bypasses the persistence context.
5. Switch to PostgreSQL (see properties comment) and run the app + tests against it.
