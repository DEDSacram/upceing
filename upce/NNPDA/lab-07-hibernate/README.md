# Lab 07 — Hibernate ORM

Plain Hibernate (no Spring): `SessionFactory`, `Session`, entity lifecycle, HQL, lazy vs eager loading.

## Theory

### Session / SessionFactory
- `SessionFactory` — heavyweight, thread-safe, one per database. Built once at startup (`HibernateUtil`).
- `Session` — short-lived, single-threaded unit of work. Opened per operation/transaction, always closed (`try-with-resources`).
- Transaction pattern: `openSession()` -> `beginTransaction()` -> work -> `commit()` / `rollback()` -> `close()`.

### Entity states
| State | Meaning |
|---|---|
| Transient | `new Book()` — unknown to Hibernate, no id. |
| Persistent | Attached to an open `Session` (`persist()`, `get()`). Changes are tracked (dirty checking) and flushed on commit. |
| Detached | Was persistent, session closed. Has an id but changes are ignored. Re-attach with `merge()`. |
| Removed | `session.remove(entity)` — scheduled for deletion on commit. |

See `App.demonstrateEntityStates()` for a runnable demo.

### HQL
- Object-oriented query language: `from Book b where b.author.name = :name`.
- Operates on entities/fields, not tables/columns. Supports named parameters, joins, aggregates (`select count(b)`).
- `JOIN FETCH` eagerly loads a lazy association in one query.

### Lazy vs eager + N+1
- `@ManyToOne(fetch = LAZY)` (default for collections is also lazy): the association is a proxy, loaded only when touched.
- Naive loop: 1 query for all books + N queries for each author = **N+1 selects**. Enable `show_sql` and count them.
- Fix: `select b from Book b join fetch b.author` — one query with a SQL join.
- `@OneToMany` here is lazy by default (good). Never switch collections to `EAGER` globally — fetch explicitly per query instead.

## Project layout
- `HibernateUtil` — singleton `SessionFactory`.
- `entity/Author`, `entity/Book` — `@OneToMany` / `@ManyToOne` bidirectional mapping.
- `dao/BookDao` — CRUD + HQL (`findByAuthorName`, `findAllWithAuthors`, `findAllNaive`).
- `App` — demo: create, read, HQL, update, entity states, N+1, delete.
- `hibernate.cfg.xml` — H2 by default; PostgreSQL block commented.
- `import.sql` — seed data.

## Run
```bash
cd lab-07-hibernate
mvn compile exec:java
```

## Verify
```bash
mvn test
```
Tests (`BookDaoTest`) run against an isolated H2 database: save/find, HQL filter, fetch join, update + delete.

Use PostgreSQL instead:
1. Create database `lab07`.
2. Uncomment the PostgreSQL block in `src/main/resources/hibernate.cfg.xml` and comment out the H2 block.
3. `mvn compile exec:java`

## Tasks
1. Add a `findBooksCheaperThan(double maxPrice)` HQL query + test.
2. Add `@NamedQuery` `Book.findByYear` and use it from the DAO.
3. Measure N+1: run `findAllNaive()` vs `findAllWithAuthors()` with `show_sql=true` and count `select` statements.
4. Change `Book.author` to `EAGER`, re-run, and explain in one paragraph why explicit `JOIN FETCH` is preferable.
5. Add optimistic locking with `@Version` on `Book` and write a test that triggers `OptimisticLockException`.
