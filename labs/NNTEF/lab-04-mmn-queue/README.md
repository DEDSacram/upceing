# Lab 04 — M/M/c Queue (Finite vs Infinite Buffer)

Multi-server queues: Erlang C for infinite buffer, Erlang B/blocking for finite capacity.

## 1. Theory

- **M/M/c:** c servers, rates λ/μ, `a = λ/μ` offered load, `ρ = a/c < 1` stable. **Erlang C** `C(c,a)` = probability an arrival waits; `Wq = C(c,a)/(cμ−λ)`.
- **M/M/c/K** (finite system capacity K): arrivals to a full system are **blocked/lost**. Blocking `P_K` from the truncated birth-death distribution; effective throughput `λ(1−P_K)`.
- Intuition: more servers cut waiting super-linearly at fixed ρ; finite buffers trade loss for bounded delay.

## 2. Project layout

```
lab-04-mmn-queue/
  README.md
  mmc.py   # Erlang B/C formulas + small simulator + self-checks
```

## 3. Run

```bash
cd lab-04-mmn-queue
python3 mmc.py
```

## 4. Verify

1. `python3 -m py_compile mmc.py` succeeds.
2. `python3 mmc.py` prints Erlang C/B table and `ALL SELF-CHECKS PASSED`.
3. c=1 reduces to M/M/1 (`Wq = ρ/(μ−λ)`); K→∞ blocking → 0.

## 5. Tasks

1. Simulate M/M/2 and match simulated Wq to Erlang C within 10%.
2. Find minimal c for `Wq < 0.5` at given λ/μ by search; print the table.
3. Compare finite K = c (loss-only, Erlang B) vs K = 2c delay-loss mix.
4. Show pooling gain: 2× M/M/1 vs 1× M/M/2 at same total capacity.
5. Add costs (server €/h + waiting €/h) and optimize c numerically.
