# Lab 06 — Optimistic Synchronization (Time Warp Toy)

Execute speculatively, roll back on stragglers with anti-messages — single-process simulation of the idea.

## 1. Theory

- **Optimistic (Time Warp, Jefferson):** LPs never block — they process events as they arrive, even speculatively past not-yet-received messages.
- **Straggler:** a message arrives with timestamp `<` local clock → causality violated → **rollback**: restore last checkpoint with time ≤ straggler, re-execute, send **anti-messages** to cancel already-sent downstream effects.
- **GVT (Global Virtual Time):** min over LP clocks + in-flight timestamps; state older than GVT can be garbage-collected (fossil collection). This toy keeps full history instead.
- Trade-off vs Lab 05: no blocking, but rollback cost; wins when cross-events are rare.

## 2. Project layout

```
lab-06-optimistic-sync/
  README.md
  timewarp.py   # one LP with speculative execution, checkpoints, straggler rollbacks
```

## 3. Run

```bash
cd labs/NNTMS/lab-06-optimistic-sync
python3 timewarp.py
python3 timewarp.py --stragglers 8 --seed 2
```

## 4. Verify

1. Default run prints `rollbacks > 0`, `anti-messages > 0`, and final state equals the sequential reference (sorted-order) result.
2. `--stragglers 0` yields zero rollbacks and the same final state.
3. `python3 -m py_compile timewarp.py` passes.

## 5. Tasks

1. Sweep stragglers `{0, 2, 8, 20}`; plot rollbacks and re-executed events.
2. Implement GVT + fossil collection (drop checkpoints older than GVT).
3. Add a second LP with cross-traffic and count cascaded rollbacks.
4. Write 5 lines: for which workload would you pick Time Warp over conservative (Lab 05)?
