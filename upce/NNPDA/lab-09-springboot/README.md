# Lab 09 — Spring Boot Layers (port 8083)

Full layered app: controller -> service -> repository -> entity, with DTOs, validation,
`@ConfigurationProperties`, profiles, Actuator, and tests.

## Theory

### IoC / DI
- **IoC**: the container creates and wires beans; your code declares dependencies instead of `new`-ing them.
- **DI**: dependencies arrive via constructor injection (`TaskController(TaskService)`). Constructor injection is preferred: immutable, testable.
- Stereotypes: `@RestController`, `@Service`, `@Repository`, `@Component` + `@SpringBootApplication` component scan.

### Auto-configuration
- Starters (`starter-web`, `starter-data-jpa`, `starter-validation`, `starter-actuator`) pull in curated dependencies.
- `@SpringBootApplication` = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`.
- Auto-config reads `application.yml`: DataSource, JPA, Jackson, validation, Actuator endpoints. Custom knobs via `AppProperties` (`app.*`).

### Layers
| Layer | Class | Responsibility |
|---|---|---|
| Controller | `TaskController`, `HelloController` | HTTP <-> DTO, status codes, no business logic |
| Service | `TaskService` | Business rules, transactions, entity <-> DTO mapping |
| Repository | `TaskRepository` | Persistence only (derived queries) |
| Entity/DTO | `Task`, `TaskDto` | DB shape vs API contract + validation |

- `GlobalExceptionHandler` maps `NoSuchElementException` -> 404, validation -> 400.

### Profiles
- Default profile: H2 in-memory, `ddl-auto=create-drop`.
- `postgres` profile (bottom of `application.yml`): real PostgreSQL, `ddl-auto=validate`.
- Run: `SPRING_PROFILES_ACTIVE=postgres mvn spring-boot:run`.

### Actuator
- Exposed: `health`, `info`, `metrics` (see `management.*` in yml).
- `GET /actuator/health` for liveness checks.

### Testing
- `TaskServiceTest` (`@SpringBootTest` + `@Transactional`): service rules, rollback per test.
- `TaskControllerTest` (`MockMvc`): status codes, JSON shape, validation + 404 handling.

## Run
```bash
cd lab-09-springboot
mvn spring-boot:run
# http://localhost:8083
```

## Verify
```bash
mvn test
```

## Curl examples (port 8083)
```bash
curl http://localhost:8083/api/hello
curl http://localhost:8083/actuator/health

curl http://localhost:8083/api/tasks
curl "http://localhost:8083/api/tasks?done=false"
curl "http://localhost:8083/api/tasks?q=spring"

curl -X POST http://localhost:8083/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Buy milk","description":"2 litres"}'

curl -X PUT http://localhost:8083/api/tasks/1 \
  -H 'Content-Type: application/json' \
  -d '{"title":"Learn Spring Boot","description":"Finish Lab 09","done":true}'

curl -X PATCH http://localhost:8083/api/tasks/1/toggle
curl -X DELETE http://localhost:8083/api/tasks/1 -i

# validation error (400):
curl -X POST http://localhost:8083/api/tasks \
  -H 'Content-Type: application/json' -d '{"title":""}' -i
```

## Tasks
1. Add `GET /api/tasks?sort=title,asc` style sorting via `Pageable`.
2. Add a `dueDate` field to `Task`/`TaskDto` with `@Future` validation + a query `findByDueDateBefore`.
3. Restrict Actuator: expose only `health` in the `postgres` profile.
4. Add `POST /api/tasks/bulk` that creates N tasks in one transaction and rolls back if any item is invalid.
5. Write a `@WebMvcTest(TaskController.class)` slice test with a mocked `TaskService`.
