# Lab 01 — JDBC (PostgreSQL + HikariCP)

Plain JDBC CRUD with `HikariCP`, `PreparedStatement`, and explicit transactions.

## 1. Theory

- **JDBC** is the low-level Java API for relational databases (`Connection`, `Statement`, `ResultSet`).
- **DriverManager vs DataSource:**
  - `DriverManager.getConnection(url, user, pass)` opens a new physical connection every time. Simple but slow, no pooling.
  - `DataSource` (here HikariCP) is a factory of pooled connections. `getConnection()` borrows from the pool and `close()` returns the connection to the pool. Always prefer `DataSource` in real apps.
- **Statement vs PreparedStatement:**
  - `Statement` concatenates SQL strings — vulnerable to SQL injection, no precompilation.
  - `PreparedStatement` uses `?` placeholders, precompiled by the DB, safe against injection, faster for repeated use. This lab uses `PreparedStatement` everywhere.
- **Transactions:** a group of statements that succeed or fail together (ACID). With JDBC: `setAutoCommit(false)` → statements → `commit()`, on error `rollback()`. `App.rollbackDemo()` shows a duplicate-email insert rolling back the whole transaction.
- **Resources:** always use try-with-resources for `Connection`/`Statement`/`ResultSet`.

## 2. Project layout

```
lab-01-jdbc/
  pom.xml
  docker-compose.yml
  src/main/java/cz/upce/nnpda/jdbc/{App,DbConfig,Student,StudentDao}.java
  src/main/resources/{schema.sql,data.sql}
  src/test/java/.../StudentDaoTest.java
```

## 3. Run

```bash
cd lab-01-jdbc

# start Postgres
docker compose up -d

# init schema + seed (optional, App also creates the table)
psql postgresql://nnpda:nnpda@localhost:5432/nnpda -f src/main/resources/schema.sql
psql postgresql://nnpda:nnpda@localhost:5432/nnpda -f src/main/resources/data.sql

# build + unit tests (H2, no Postgres needed)
mvn test

# run demo (needs Postgres up)
mvn compile exec:java
# or: DB_URL=jdbc:postgresql://localhost:5432/nnpda DB_USER=nnpda DB_PASS=nnpda mvn compile exec:java
```

Environment overrides: `DB_URL`, `DB_USER`, `DB_PASS` (defaults to `jdbc:postgresql://localhost:5432/nnpda` / `nnpda` / `nnpda`).

## 4. Verify

1. `mvn test` is green (3 H2-backed tests).
2. `mvn compile exec:java` prints INSERT → FIND ALL → UPDATE → TRANSACTION commit → rollback demo → DELETE.
3. `psql postgresql://nnpda:nnpda@localhost:5432/nnpda -c "SELECT * FROM students;"` shows remaining rows.

## 5. Tasks

1. Add `findByEmail(String email)` to `StudentDao` and cover it with a test.
2. Add a paginated `findAll(int limit, int offset)` using `LIMIT ? OFFSET ?`.
3. Rewrite `deleteAll()` with `PreparedStatement`/`TRUNCATE` and explain the difference in a comment.
4. Implement a money-transfer style transaction across two rows (two `UPDATE`s in one commit) and a test that forces rollback.
5. Compare `DriverManager` vs HikariCP: measure 1000x `findAll()` with each and note timings in this README.
