# Lab 05 — Race Condition → Critical Section (`pthread_mutex`)

4 threads × 200 000 increments of a shared counter: first unprotected (lost updates), then protected by `pthread_mutex_t` (exact result).

## 1. Theory

- **Race condition:** `counter++` compiles to load → add → store. Two threads can load the same value concurrently and both store `value+1` — one update is *lost*. The final result is typically less than expected and differs run to run.
- **Critical section:** the code region touching shared state that must run atomically. `pthread_mutex_lock()` / `pthread_mutex_unlock()` serialise it: at most one thread inside. `PTHREAD_MUTEX_INITIALIZER` statically initialises a default mutex (no `init`/`destroy` needed for this simple case).
- **Mutex discipline:** lock the *shortest* region that covers the shared access; always unlock on every path (or use cleanup handlers); never hold a mutex while doing slow I/O unless necessary (hurts parallelism).
- Note: even when the racy run "accidentally" prints the right number, the program is still wrong — the bug is timing-dependent.

## 2. Project layout

```
lab-05-race-critical/
  Makefile
  main.c        # racy run, then mutex-protected run, compare with expected
  README.md
```

## 3. Run

```bash
cd lab-05-race-critical
make
./lab05
```

## 4. Verify

1. `make` completes with no warnings.
2. `racy:` line shows `LOST UPDATES (race)` (got < 800 000; on rare lucky runs it may match — the message says so).
3. `mutex:` line shows `got 800000, expected 800000 -> OK`.
4. Exit code `0`; runtime is a few seconds at most.

## 5. Tasks

1. Vary `NTHREADS`/`INCR` and plot how the racy deficit grows with thread count.
2. Replace the mutex with `__atomic_fetch_add(&counter, 1, __ATOMIC_SEQ_CST)` (or C11 `atomic_fetch_add`) — exact result without locking; compare runtime.
3. Deliberately deadlock: lock the same non-recursive mutex twice in one thread; observe the hang, then fix with `PTHREAD_MUTEX_ERRORCHECK` (returns `EDEADLK` instead of hanging).
4. Protect a more realistic structure (linked-list push from N threads) with one mutex; then try fine-grained per-node locking and discuss.
5. Explain why `volatile` alone does **not** fix this race (no atomicity, no memory ordering).
