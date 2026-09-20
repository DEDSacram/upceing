# Lab 01 — Processes (`fork` / `exec` / `wait`)

Parent creates two children with `fork()`; one replaces its image with `exec`, the other computes and exits with a status; the parent reaps both with `wait()`.

## 1. Theory

- **`fork()`** creates a child process as (almost) an exact copy of the parent: same code, copied data/stack/heap, shared file offsets. Return value distinguishes them: `0` in the child, child PID in the parent, `-1` on error.
- **`exec` family** (`execlp`, `execvp`, …) replaces the current process image with a new program. On success it never returns; on failure it returns `-1`. That is why the `perror`/`_exit(127)` after `execlp` only runs on error.
- **`wait()` / `waitpid()`** block until a child changes state and return its PID plus a status. Macros decode it: `WIFEXITED`/`WEXITSTATUS` (normal exit), `WIFSIGNALED`/`WTERMSIG` (killed by signal). A child that is never waited for becomes a **zombie** (dead but still occupying a PID/slot in the process table); an **orphan** (parent died first) is reparented to PID 1/`init`.
- **Copy-on-write:** modern kernels don't physically copy all memory at `fork()`; pages are shared read-only until either side writes.

## 2. Project layout

```
lab-01-processes/
  Makefile
  main.c        # fork x2 -> execlp(echo) + compute/exit(42); parent wait()
  README.md
```

## 3. Run

```bash
cd lab-01-processes
make          # gcc -Wall -Wextra -pthread -o lab01 main.c
./lab01       # or: make run
```

## 4. Verify

1. `make` completes with no warnings.
2. Output contains `[child1]`, `[child2] sum(1..100)=5050`, and two `[parent] child ... exited` lines with statuses `0` (echo) and `42`.
3. Final line: `[parent] all children reaped. No zombies.`
4. Program terminates by itself (no input needed, no hangs).

## 5. Tasks

1. Add a third child that runs `ls -l` via `execvp` with an argument vector.
2. Replace `wait()` with a `waitpid()` loop for a specific PID and print `WIFSIGNALED` handling: kill one child with `kill(pid, SIGTERM)` before it exits.
3. Demonstrate a zombie: `fork()` a child that exits immediately, `sleep(5)` before `wait()`, and observe `Z` state via `ps` from another terminal.
4. Measure `fork()` cost: time 10 000 forks of `/bin/true` vs 10 000 function calls; note the ratio.
5. (Windows note) On Windows there is no `fork()`; the equivalent is `CreateProcess()`. See `labs/NNOS2/lab-02-processes-threads` for the PowerShell side.
