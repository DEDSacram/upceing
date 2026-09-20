# Lab 05 — Conservative Synchronization (Two LPs + Lookahead)

Chandy–Misra–Bryant style: LPs block until safe, using lookahead to guarantee no stragglers.

## 1. Theory

- **Parallel discrete-event simulation** splits the model into Logical Processes (LPs) with separate clocks exchanging timestamped events.
- **Conservative (CMB) protocol:** an LP processes its next event at time `t` only when it can prove no smaller-timestamp event will ever arrive — via per-channel FIFO + **lookahead** `L` (min service/promise time): safe time = `min over channels (last_received + L)`.
- **Lookahead trade-off:** larger `L` → less blocking, more parallelism; `L=0` → deadlock-prone (needs null messages).
- Demo: two tandem queue LPs (LP0 → LP1); LP1 may only advance to `t` when `t ≤ LP0_clock + lookahead`.

## 2. Project layout

```
lab-05-conservative-sync/
  README.md
  conservative.py   # two-LP sim with null-message clocks, deadlock/blocked counters
```

## 3. Run

```bash
cd labs/NNTMS/lab-05-conservative-sync
python3 conservative.py
python3 conservative.py --lookahead 2.0 --seed 5
```

## 4. Verify

1. Default run completes all events with zero causality violations and prints blocked-vs-progress stats.
2. Larger `--lookahead` reduces blocked rounds vs `--lookahead 0.1`.
3. `python3 -m py_compile conservative.py` passes.

## 5. Tasks

1. Sweep lookahead `{0.1, 0.5, 1.0, 2.0}`; plot blocked rounds vs lookahead.
2. Break it: set lookahead to 0 and inject simultaneous timestamps; explain the deadlock.
3. Add a third LP (LP1 → LP2 chain) and re-derive the safe-time rule.
4. Compare wall-clock event order against a sequential reference run.
