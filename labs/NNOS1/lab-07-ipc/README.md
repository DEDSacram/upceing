# Lab 07 — IPC (pipe + `socketpair`)

Parent↔child communication over an anonymous pipe (one-way message) and over a Unix-domain `socketpair` (bidirectional ping–pong).

## 1. Theory

- **Anonymous pipe** (`pipe()`): two fds, `fd[0]` read end, `fd[1]` write end; unidirectional, exists only between related processes (inherited across `fork()`). Each side **must close the end it doesn't use** — otherwise the reader never sees EOF and `read()` blocks forever. Writes up to `PIPE_BUF` (4 KiB) are atomic.
- **`socketpair(AF_UNIX, SOCK_STREAM, 0, sv)`**: two connected bidirectional sockets, also inherited across `fork()`. Full-duplex (both sides read+write), message boundaries not preserved with `SOCK_STREAM` (it's a byte stream, like TCP).
- **When to use what:** pipe = simple one-way producer→consumer (shell `|`); socketpair = bidirectional parent↔child RPC; named FIFO = unrelated processes via filesystem; POSIX message queues / Unix sockets = unrelated processes with names; shared memory = highest throughput, needs external synchronisation.
- Blocking semantics: `read()` on an empty pipe whose write end is still open blocks; once all write ends close, it returns 0 (EOF).

## 2. Project layout

```
lab-07-ipc/
  Makefile
  main.c        # demo_pipe() + demo_socketpair(), both fork-based
  README.md
```

## 3. Run

```bash
cd lab-07-ipc
make
./lab07
```

(On Windows lab machines the same ideas map to anonymous/named pipes — `CreatePipe`, `\\.\pipe\…`; see `labs/NNOS2`.)

## 4. Verify

1. `make` completes with no warnings.
2. Output contains `[pipe] child received: "hello through the pipe"` and `[socketpair] child received: "ping"` + `[socketpair] parent received: "pong"`.
3. Final line `pipe=OK socketpair=OK`, exit code `0`; no hangs (both children reaped with `waitpid`).

## 5. Tasks

1. Send a `struct` (e.g. `{int id; char text[32];}`) through the pipe; handle short reads with a `read_full()` loop.
2. Keep both `socketpair` ends open and implement 5 rounds of ping–pong in a loop.
3. Replace the anonymous pipe with a named FIFO (`mkfifo`): two unrelated processes (two terminals) talking to each other.
4. Compare with POSIX message queues (`mq_open/mq_send/mq_receive`, needs `-lrt` on older glibc): send priority-tagged messages.
5. Make the read end non-blocking (`O_NONBLOCK`) and handle `EAGAIN` with `poll()`/`select()`.
