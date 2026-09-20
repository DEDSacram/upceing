# Lab 02 — Signals (`sigaction`, handlers, `kill`)

Child sends `SIGUSR1` × 3 and `SIGINT` × 1 to the parent; the parent counts them with a `sigaction()`-installed handler using only async-signal-safe operations.

## 1. Theory

- **Signals** are small async notifications to a process (`SIGINT` = Ctrl+C, `SIGTERM`, `SIGUSR1/2` = user-defined, `SIGCHLD`, …). Default dispositions kill, ignore, or stop the process; a program can install a custom handler, ignore, or block them.
- **`signal()` vs `sigaction()`:** `signal()` is historic and has inconsistent semantics across Unices (handler may reset, syscalls may or may not restart). `sigaction()` is the POSIX-correct API: full control over mask (`sa_mask`) and flags (`SA_RESTART`). This lab uses `sigaction()` only.
- **Async-signal safety:** a handler can interrupt the program anywhere, so it may only call async-signal-safe functions (`write`, `_exit`, … — see `man 7 signal-safety`). `printf()`/`malloc()` are **forbidden** in handlers (deadlock/corruption risk). Communication with main code uses `volatile sig_atomic_t` flags.
- **`kill(pid, sig)`** sends a signal (despite the name). `SIGKILL`/`SIGSTOP` cannot be caught or ignored.

## 2. Project layout

```
lab-02-signals/
  Makefile
  main.c        # sigaction handlers + fork; child kill()s parent; parent counts
  README.md
```

## 3. Run

```bash
cd lab-02-signals
make
./lab02
```

## 4. Verify

1. `make` completes with no warnings.
2. Output shows three `[handler] signal caught` lines plus one more (4 total), then `[parent] SIGUSR1=3 SIGINT=1 child ok`.
3. Final line: `[parent] OK: sigaction handlers work.` and exit code `0` (`echo $?`).
4. Program terminates by itself within ~2 s (bounded wait loop, `waitpid` for child).

## 5. Tasks

1. Add a `SIGALRM` handler via `alarm(2)` and print a message if the child takes too long (real timeout instead of the polling loop).
2. Block `SIGUSR1` with `sigprocmask()` for 1 s while the child sends, then unblock and show the signal was pending (`sigpending()`).
3. Replace the polling loop with `sigsuspend()` — wait atomically for signals without busy-waiting.
4. Install a `SIGCHLD` handler that calls `waitpid(-1, &st, WNOHANG)` in a loop (reaping without blocking the parent).
5. Explain in a comment why `printf()` inside `handler()` would be a bug, and what `SA_RESTART` changes for slow syscalls like `read()`.
