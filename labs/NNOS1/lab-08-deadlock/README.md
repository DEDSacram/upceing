# Lab 08 — Deadlock (dining philosophers → ordered-lock fix + Java monitor)

Naive philosophers deadlock (detected via timed locks, bounded runtime), then a resource-ordering fix lets all eat. `MonitorDining.java` shows the monitor-based variant.

## 1. Theory

- **Coffman's 4 conditions** for deadlock: mutual exclusion, hold-and-wait, no preemption, circular wait. Break any one → no deadlock.
- **Dining philosophers:** 5 philosophers, 5 forks (mutexes). Naive protocol (take left, then right) allows all to hold left and wait for right forever — circular wait. The lab *detects* the embrace with non-blocking `pthread_mutex_trylock()` after a barrier rendezvous (all lefts provably held ⇒ all trylocks fail, deterministically). A real blocking `lock()` at that point would hang forever — which is exactly why the lab uses `trylock` for detection.
- **Fix — resource ordering:** number all resources; every thread acquires them in increasing order. Philosopher 4 takes right-then-left while others take left-then-right, so the wait graph can never contain a cycle. Alternatives: `trylock` + backoff (drop left fork, retry), a waiter semaphore (max 4 seated), or a monitor.
- **Monitor (Java):** `synchronized` methods + `wait()`/`notifyAll()`. The `Table` takes *both* forks atomically — hold-and-wait is impossible by construction, hence deadlock-free.

## 2. Project layout

```
lab-08-deadlock/
  Makefile
  main.c              # naive (timedlock detection) + ordered-lock fix
  MonitorDining.java  # monitor variant (needs a JDK; Windows/Linux)
  README.md
```

## 3. Run

```bash
cd lab-08-deadlock
make
./lab08
# Java variant (on a machine with a JDK):
javac MonitorDining.java && java MonitorDining
```

## 4. Verify

1. `make` completes with no warnings.
2. `naive: 5/5 philosophers starved -> DEADLOCK DEMONSTRATED`.
3. Five `[ordered N] ate` lines, then `ordered: 0/5 starved -> FIX WORKS (all ate)`.
4. Exit code `0`; total runtime ≈ 1 s (no hangs — `trylock` detection never blocks).
5. Java variant (where a JDK exists): `OK: all philosophers ate, no deadlock.`

## 5. Tasks

1. Implement the `trylock` + backoff fix (drop left fork on failure, random short sleep, retry) and compare liveness with ordering.
2. Implement the waiter-semaphore fix (`sem_t seats`, init 4): at most 4 philosophers at the table ⇒ no circular wait. Prove why 4 suffices.
3. Draw the resource-allocation graph for the naive deadlock moment and mark the cycle.
4. Extend `MonitorDining.java` with a `SHUNGRY` print when a philosopher waits > 1 s; run 20 meals and confirm no starvation.
5. Show **livelock**: two philosophers that always back off simultaneously; fix with randomised backoff and explain livelock vs deadlock vs starvation.
