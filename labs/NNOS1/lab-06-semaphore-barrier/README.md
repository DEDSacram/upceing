# Lab 06 — Semaphores + Barrier (producer–consumer, rendezvous)

Bounded-buffer producer–consumer with two counting semaphores + a mutex, then a 3-thread `pthread_barrier_t` rendezvous.

## 1. Theory

- **Counting semaphore** (`sem_init/sem_wait/sem_post`): an integer that blocks at 0. `sem_empty` counts free slots (init = buffer size), `sem_full` counts filled slots (init = 0). Producer waits on `empty` → writes → posts `full`; consumer waits on `full` → reads → posts `empty`. The pair guarantees no overflow and no read of empty cells.
- **Why also a mutex?** Semaphores count *how many* slots are free/filled, but concurrent producers/consumers could still corrupt the `in`/`out` indices — the mutex serialises index + buffer access. (One producer + one consumer could skip it; the lab keeps it for the general pattern.)
- **Barrier** (`pthread_barrier_init/wait/destroy`): N threads block in `wait()` until all N arrive, then all are released — a *rendezvous* for phased computations (e.g. all finish phase 1 before anyone starts phase 2).
- Semaphores vs mutexes vs condition variables: mutex = ownership + mutual exclusion; semaphore = counting/signalling without ownership; condvar = wait-for-predicate inside a monitor.

## 2. Project layout

```
lab-06-semaphore-barrier/
  Makefile
  main.c        # prod/cons (10 items, buf 4) + 3-thread barrier demo
  README.md
```

## 3. Run

```bash
cd lab-06-semaphore-barrier
make
./lab06
```

## 4. Verify

1. `make` completes with no warnings.
2. `producer-consumer: 10 items in order 0..9 -> OK` (order preserved, nothing lost/duplicated).
3. All three `[worker N] passed barrier` lines appear — i.e. no thread proceeded to phase 2 before all finished phase 1.
4. Final line `barrier: all 3 workers rendezvoused -> OK`, exit code `0`.

## 5. Tasks

1. Add a second consumer (2 consumers, 1 producer, split `NITEMS` evenly). What changes in verification?
2. Replace the semaphore pair with a mutex + two condition variables (`not_full`, `not_empty`) and compare code clarity.
3. Make the buffer unbounded (linked list): which semaphore disappears and why?
4. Reuse the barrier in a loop (e.g. 5 iterations of phase 1/barrier/phase 2) — barriers are reusable, unlike one-shot latches.
5. Remove the mutex (keep semaphores) with 2 producers and show index corruption; explain why counting alone is insufficient.
