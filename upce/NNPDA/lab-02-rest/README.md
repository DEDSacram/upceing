# Lab 02 — REST API (Spring Boot)

In-memory CRUD REST service for books with validation, proper HTTP codes and pagination.

## 1. Theory

- **REST** = resource-oriented style over HTTP. Resources (`/api/books`) are manipulated with verbs; representations are JSON.
- **HTTP verbs:** `GET` (read, safe/idempotent), `POST` (create, not idempotent), `PUT` (full replace, idempotent), `PATCH` (partial update), `DELETE` (remove, idempotent).
- **Status codes used here:**
  - `200 OK` — GET/PUT success
  - `201 Created` + `Location` header — POST success
  - `204 No Content` — DELETE success
  - `400 Bad Request` — validation errors, bad `page`/`size`
  - `404 Not Found` — unknown book id
- **Validation:** `spring-boot-starter-validation` + `@Valid` on `@RequestBody`; violations are mapped to a uniform `ApiError` by `GlobalExceptionHandler`.
- **Pagination:** `GET /api/books?page=0&size=10`, sorted by id ascending.

## 2. Run

```bash
cd lab-02-rest
mvn spring-boot:run
# server on http://localhost:8081
```

## 3. Verify (curl)

```bash
# list (paginated)
curl -s 'http://localhost:8081/api/books?page=0&size=10'

# get one
curl -s http://localhost:8081/api/books/1

# create (201 + Location)
curl -i -X POST http://localhost:8081/api/books \
  -H 'Content-Type: application/json' \
  -d '{"title":"Domain-Driven Design","author":"Eric Evans","isbn":"978-0321125217","publishedYear":2003}'

# update
curl -s -X PUT http://localhost:8081/api/books/1 \
  -H 'Content-Type: application/json' \
  -d '{"title":"Effective Java 3rd","author":"Joshua Bloch","isbn":"978-0134685991","publishedYear":2018}'

# delete (204)
curl -i -X DELETE http://localhost:8081/api/books/2

# validation error (400)
curl -s -X POST http://localhost:8081/api/books \
  -H 'Content-Type: application/json' \
  -d '{"title":"","author":"","isbn":"bad","publishedYear":1000}'

# not found (404)
curl -s http://localhost:8081/api/books/999999
```

Or open `http/requests.http` in IntelliJ / VS Code REST Client and run the requests.

## 4. Tests

```bash
mvn test
```

`BookControllerTest` (MockMvc) covers list, pagination, full create→get→update→delete lifecycle, 404 and 400 cases.

## 5. Tasks

1. Add `GET /api/books/search?author=...` filtering by author substring (case-insensitive).
2. Add `PATCH /api/books/{id}` for partial updates (ignore `null` fields).
3. Return pagination metadata (`page`, `size`, `total`) instead of a bare array — keep backward compatibility via a new endpoint or wrapper object.
4. Add OpenAPI docs (`springdoc-openapi-starter-webmvc-ui`) and expose Swagger UI; link it here.
5. Persist books with Spring Data JPA + H2/Postgres instead of the `ConcurrentHashMap`.
