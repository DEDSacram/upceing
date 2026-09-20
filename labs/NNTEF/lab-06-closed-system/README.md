# Lab 06 — Closed Queueing System (Machine Repair / M/M/1//N)

Finite population: N machines break down, R repairmen fix them. Throughput saturates — add repairmen only up to the knee.

## 1. Theory

- **Machine-repair model M/M/R//N:** N machines, each up-machine fails after Exp(λ); R repairmen each repair at Exp(μ); down machines wait. Population is *finite*, so arrivals slow as more machines are down (no ρ<1 stability condition needed).
- **Birth-death solution:** states 0..N down; birth `λ_k = (N−k)λ`, death `μ_k = min(k,R)μ`. Solve `p_k` recursively, then `L` (down), `W` (via Little on throughput `λ_eff = Σλ_k p_k`), availability `A = 1 − L/N`.
- Experiment: sweep R = 1..3, show waiting collapse; compare with simulation sketch.

## 2. Project layout

```
lab-06-closed-system/
  README.md
  closed.py   # birth-death solver + sweeps + self-checks (stdlib only)
```

## 3. Run

```bash
cd lab-06-closed-system
python3 closed.py
```

## 4. Verify

1. `python3 -m py_compile closed.py` succeeds.
2. `python3 closed.py` prints availability/L per R and `ALL SELF-CHECKS PASSED`.
3. Probabilities sum to 1; more repairmen never hurt availability.

## 5. Tasks

1. Event-simulate the repair shop; match L within 10% of the solver.
2. Add costs (downtime €/h vs repairman €/h); find optimal R.
3. Sweep N = 5..50 at fixed R; show the saturation knee in throughput.
4. Compare λ_eff vs offered N·λ; explain the "finite population" damping in a comment.
5. Extend to two failure modes (fast/slow repair) via a 2-D state sketch.
