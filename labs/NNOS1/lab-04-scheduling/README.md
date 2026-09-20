# Lab 04 — Scheduling (`nice`, priorities, policies)

Observe the current scheduler policy/priority, change the `nice` value with `getpriority`/`setpriority`, probe real-time policies, and read CPU affinity.

## 1. Theory

- **Scheduling policies (Linux):** `SCHED_OTHER` (default time-sharing, dynamic priority from `nice`), `SCHED_BATCH` (batch workloads), `SCHED_IDLE` (runs only when nothing else wants CPU), real-time `SCHED_FIFO` (run until block/yield/preempted by higher RT priority) and `SCHED_RR` (FIFO + timeslices), `SCHED_DEADLINE` (EDF). Real-time priorities are 1–99; `SCHED_OTHER` always has priority 0.
- **`nice` (-20 … +19):** a hint biasing `SCHED_OTHER` time allocation. Lower = more CPU. Only root may set negative values; anyone may *raise* (lower own priority) — which is why the lab adds +5 and it always succeeds.
- **Privileges:** switching to `SCHED_FIFO`/`SCHED_RR` needs `CAP_SYS_NICE` (root). As a student you get `EPERM` — that error *is* the expected result here.
- **Affinity** (`sched_getaffinity`) tells which CPUs the process may run on.

## 2. Project layout

```
lab-04-scheduling/
  Makefile
  main.c        # policy/priority info + nice bump + RT probe + affinity
  README.md
```

## 3. Run

```bash
cd lab-04-scheduling
make
./lab04
```

## 4. Verify

1. `make` completes with no warnings.
2. Output shows `policy=SCHED_OTHER priority=0`, the min/max priority table, `nice before=N`, `nice after=N+5 ... OK`.
3. `sched_setscheduler(FIFO)` line reports the `EPERM`-style error (or success if run as root — both are accepted and printed).
4. `affinity: K CPU(s) available` with K ≥ 1; exit code `0`.

## 5. Tasks

1. Run two CPU-bound loops with different `nice` values (`nice -n 0` vs `nice -n 10`) and compare wall time with `time`; explain the result.
2. Use `chrt -r -p 1 <pid>` (as root in a VM) to move a process to `SCHED_RR` and observe `sched_getscheduler()` change.
3. Pin the program to one CPU with `taskset -c 0 ./lab04` and check the affinity line prints 1 CPU.
4. Print `sched_rr_get_interval()` for the current policy and explain what a timeslice means for `SCHED_RR` vs `SCHED_FIFO`.
5. (Windows note) Compare with Windows priority classes (`Idle` … `Realtime`) and `Get-Process | Select PriorityClass` — see `labs/NNOS2/lab-02-processes-threads`.
