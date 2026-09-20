# Lab 02 — Processes & Threads (Windows + Linux try-out)

Inspect Windows processes/threads with PowerShell; try the equivalent Linux concepts locally with `proc_threads.c`.

## 1. Theory

- **Windows process model:** a process is a container (address space, handles, token) — execution happens in *threads*. Tools: Task Manager, `tasklist`, `Get-Process` (CPU, WorkingSet64, HandleCount, PriorityClass). No `fork()`; new processes come from `CreateProcess()`.
- **Threads:** listed per process via `$proc.Threads` (Id, StartTime, ThreadState, PriorityLevel). State/WaitReason show what a thread is blocked on — the analogue of Linux `wchan`/`/proc/<pid>/task/<tid>/status`.
- **Priorities:** Windows *priority classes* (`Idle`, `BelowNormal`, `Normal`, `AboveNormal`, `High`, `Realtime`) × thread relative levels; Linux uses `nice` (-20…19) + real-time policies. See `labs/NNOS1/lab-04-scheduling` for the Linux side.
- **Affinity:** `$proc.ProcessorAffinity` (bitmask) ≈ Linux `sched_getaffinity` / `taskset`.
- **Linux try-out:** `proc_threads.c` spawns 3 pthreads and enumerates `/proc/self/task` (each thread = TID + `comm` name), the same idea as `$proc.Threads`.

## 2. Project layout

```
lab-02-processes-threads/
  Get-ProcessesThreads.ps1  # top CPU/mem processes + thread table + own affinity (run on Windows)
  proc_threads.c            # Linux try-out: pthreads + /proc/self/task listing (runs here)
  README.md
```

## 3. Run

```powershell
# On a student Windows machine:
powershell -ExecutionPolicy Bypass -File Get-ProcessesThreads.ps1 -Top 10 -Name svchost
```

```bash
# On Linux (verifiable here):
cd lab-02-processes-threads
gcc -Wall -Wextra -pthread -o proc_threads proc_threads.c
./proc_threads
```

## 4. Verify

1. On Windows: top-CPU and top-memory tables print; thread table for the named process appears (or a clear warning if the name doesn't exist); own `PriorityClass`/`ProcessorAffinity` print.
2. On Linux: `./proc_threads` lists ≥ 4 TIDs and ends with `total threads=N (expected >= 4): OK`, exit code `0`.
3. You can explain the mapping: `Get-Process` ≙ `ps`, `.Threads` ≙ `/proc/<pid>/task`, `PriorityClass` ≙ `nice`, `ProcessorAffinity` ≙ `taskset`.

## 5. Tasks

1. On Windows: find the PID with the largest `WorkingSet64`; list its threads sorted by `StartTime`.
2. Change a process priority: `$p = Get-Process -Name notepad; $p.PriorityClass = 'High'` — observe effect and revert; why is `Realtime` dangerous?
3. Limit a process to one CPU via `$p.ProcessorAffinity = 1` and compare with Linux `taskset -c 0`.
4. Extend `proc_threads.c` to also print each thread's state from `/proc/self/task/<tid>/status` (`State:` line).
5. Explain handles (`HandleCount`) vs Linux file descriptors: what counts as a "handle" that has no fd analogue (e.g. registry keys, tokens)?
