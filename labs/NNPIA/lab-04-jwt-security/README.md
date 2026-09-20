# Lab 04 — JWT Security Skeleton + Password Encoder

Stateless JWT auth skeleton: `JwtUtil` (jjwt HS256), `JwtFilter` (`OncePerRequestFilter`), `SecurityConfig` (stateless, `/auth/**` public), BCrypt password demo, and tests.

## 1. Theory

- **JWT structure:** `header.payload.signature` (base64url). The server signs the payload with a secret; anyone can read it, but only the secret holder can mint valid tokens. The filter therefore *verifies the signature* — never trusts the payload alone.
- **Stateless auth flow:** `POST /auth/register` stores a BCrypt hash (never plaintext) → `POST /auth/login` checks `encoder.matches()` and returns a signed token → client sends `Authorization: Bearer <token>` → `JwtFilter` validates and publishes an `Authentication` into the `SecurityContextHolder` → controller sees an authenticated principal. No server-side session (`SessionCreationPolicy.STATELESS`).
- **Filter position:** `addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)` runs JWT validation before Spring's form-login filter, so bearer tokens authenticate API calls.
- **BCrypt:** adaptive hash with salt + cost factor. `matches()` re-hashes the candidate with the stored salt and compares — timing-safe; identical passwords produce different hashes.

## 2. Project layout

```
lab-04-jwt-security/
  pom.xml                                             # web + security + jjwt 0.12.5
  src/main/java/cz/upce/nnpia/lab04/
    App.java
    security/{JwtUtil,JwtFilter}.java                 # token mint/verify + Bearer filter (skeleton)
    config/SecurityConfig.java                        # BCrypt bean, stateless chain
    auth/AuthController.java                          # /auth/register, /auth/login, /api/hello
  src/test/java/.../{JwtUtilTest,PasswordEncoderTest}.java
```

## 3. Run

```bash
cd lab-04-jwt-security
mvn test
mvn spring-boot:run
# in another terminal:
curl -X POST localhost:8080/auth/register -H 'Content-Type: application/json' -d '{"username":"ada","password":"s3cret-pw!"}'
TOKEN=$(curl -s -X POST localhost:8080/auth/login -H 'Content-Type: application/json' -d '{"username":"ada","password":"s3cret-pw!"}' | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
curl localhost:8080/api/hello -H "Authorization: Bearer $TOKEN"   # -> authenticated ok
curl localhost:8080/api/hello                                     # -> 403/401
```

## 4. Verify

1. `mvn test` green: JWT round-trip keeps the username, tampered token rejected, BCrypt hashes and verifies.
2. `/api/hello` without a token is rejected; with the login token returns `authenticated ok`.
3. Wrong password on `/auth/login` returns `401`.

## 5. Tasks

1. Finish the `JwtFilter` skeleton: load real authorities (e.g. `ROLE_USER`) from a user store and assert they appear in `SecurityContextHolder` in a MockMvc test with `SecurityMockMvcRequestPostProcessors.jwt()`.
2. Add token expiry test: generate a token with 1 ms validity, sleep, assert `valid()` is false.
3. Replace the in-memory `users` map with the JPA `Customer`/user entity from lab-03.
4. Move the JWT secret to `application.properties` (`@Value("${jwt.secret}")`) and document why hardcoded secrets are unsafe.
