# Lab 02 — REST Controller + DTO + Validation

`GET`/`POST` controller with a validated DTO and a `MockMvc` slice test. In-memory store, no DB.

## 1. Theory

- **`@RestController` = `@Controller` + `@ResponseBody`:** the return value is serialized to JSON (Jackson) instead of resolving a view. `@RequestMapping("/api/products")` sets the base path.
- **DTO (Data Transfer Object):** `ProductDto` is the API contract, separate from any domain/entity class. It carries only what the API needs and owns the validation rules, so internal model changes don't leak to clients.
- **Bean Validation:** `@NotBlank`, `@Size`, `@Min` on DTO fields + `@Valid` on the `@RequestBody` parameter. Spring validates before the method body runs; violations throw `MethodArgumentNotValidException`.
- **`@RestControllerAdvice`:** centralizes error mapping. `GlobalExceptionHandler` turns validation failures into HTTP 400 with a `{field: message}` JSON body instead of a default HTML error page.
- **`@WebMvcTest`:** loads only the web slice (controller + advice + Jackson + validation), not the full context. `MockMvc` performs fake HTTP calls without starting a server — fast and hermetic.

## 2. Project layout

```
lab-02-rest-controller/
  pom.xml                                             # web + validation + starter-test
  src/main/java/cz/upce/nnpia/lab02/
    App.java
    dto/ProductDto.java                               # @NotBlank name, @Min price
    controller/ProductController.java                 # GET list, GET by id, POST create
    exception/GlobalExceptionHandler.java             # 400 {field: message}
  src/test/java/.../ProductControllerTest.java        # MockMvc: create+read, 400s, 404
```

## 3. Run

```bash
cd lab-02-rest-controller
mvn test
mvn spring-boot:run
curl -X POST localhost:8080/api/products -H 'Content-Type: application/json' -d '{"name":"Keyboard","price":1500}'
curl localhost:8080/api/products
curl -X POST localhost:8080/api/products -H 'Content-Type: application/json' -d '{"name":"","price":-1}'  # -> 400
```

## 4. Verify

1. `mvn test` is green (4 MockMvc tests).
2. `POST` valid JSON returns `201` with an assigned `id`; `GET /api/products/{id}` returns it.
3. `POST {"name":"","price":-1}` returns `400` with `name` and `price` keys; `GET` of an unknown id returns `404`.

## 5. Tasks

1. Add `PUT /api/products/{id}` (full update, `@Valid`, 404 when missing) and cover it with a MockMvc test.
2. Add `DELETE /api/products/{id}` returning `204`, plus a test that `GET` afterwards is `404`.
3. Add `@Size(max = 100)` behavior proof: post a 101-char name, assert `400` and the `name` key.
4. Paginate `GET /api/products` with `?page=&size=` query params and test the second page.
