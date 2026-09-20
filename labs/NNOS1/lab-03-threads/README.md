# Lab 03 — Threads (pthreads + reentrancy pitfall)

`strtok()` vs `strtok_r()` pitfall demo plus 4 pthreads tokenising strings concurrently with the reentrant variant.

## 1. Theory

- **Threads** share one address space (code, heap, globals) but have private stacks and registers. `pthread_create()` starts one, `pthread_join()` waits for it and collects its return value. No `wait()`-style zombies if joined or detached.
- **Reentrancy:** a function is *reentrant* if it can be safely re-entered (second call before the first finished) — no hidden shared state. `strtok()` keeps a static internal pointer to "current position", so interleaved tokenisation of two strings (or two threads) corrupts both. `strtok_r()` (the `_r` = reentrant) stores that state in caller-provided memory (`saveptr`), so each thread/string is independent.
- Siblings of the same idea: `strerror` → `strerror_r`, `localtime` → `localtime_r`, `rand` → `rand_r`. Rule of thumb: on Linux, prefer the `_r` variant in threaded code, or protect the non-reentrant one with a mutex (serialises, hurts parallelism).
- `printf()` is thread-safe (no data corruption) but output lines from different threads can interleave.

## 2. Project layout

```
lab-03-threads/
  Makefile
  main.c        # strtok pitfall + fix, then NTHREADS x strtok_r workers
  README.md
```

## 3. Run

```bash
cd lab-03-threads
make
./lab03
```

## 4. Verify

1. `make` completes with no warnings.
2. Pitfall section prints `t1=alpha t2=one t3=two` (wrong — wanted `beta`), fix section prints `t1=alpha t2=one t3=beta` (correct).
3. Four `[thread N] ... -> N tokens` lines appear, then `total tokens=13 (expected 3+3+3+4=13): OK`.
4. Exit code `0`, program terminates without hangs.

## 5. Tasks

1. Make the pitfall multithreaded: two threads calling `strtok()` on different strings in a loop; observe corrupted token streams, then fix with `strtok_r()`.
2. Replace the per-thread `printf()` with accumulation into a shared array (one slot per thread, no lock needed) and print serially after `pthread_join()`.
3. Pass a `struct` argument (string + delimiter + result slot) to workers instead of a global table.
4. Add `pthread_detach()` variant: when is detach preferable to join?
5. (Challenge) Show `errno` clobbering: call a failing syscall in one thread while another reads `errno`; explain why glibc makes `errno` thread-local.
