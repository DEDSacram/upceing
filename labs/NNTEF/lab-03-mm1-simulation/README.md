# Lab 03 — M/M/1 Simulation vs Erlang Formulas

Event-driven simulation of a single-server queue; validate against closed-form M/M/1 results.

## 1. Theory

- **M/M/1:** Poisson arrivals (rate λ), exponential service (rate μ), one server, infinite buffer. Traffic intensity `ρ = λ/μ < 1` for stability.
- **Erlang formulas:** `L = ρ/(1−ρ)` (mean in system), `Lq = ρ²/(1−ρ)`, `W = 1/(μ−λ)`, `Wq = ρ/(μ−λ)`, `P(wait) = ρ`. PASTA: arrivals see time averages.
- **Simulation:** next-event loop (arrival vs departure); exponential variates via `-ln(1−U)/rate`. Warm up, then time-average the queue length (area under Q(t) / T) and average waits.

## 2. Project layout

```
lab-03-mm1-simulation/
  README.md
  mm1.py   # simulator + Erlang comparison + self-checks (stdlib + random)
```

## 3. Run

```bash
cd lab-03-mm1-simulation
python3 mm1.py
python3 mm1.py --lam 0.8 --mu 1.0 --n 50000 --seed 3
```

## 4. Verify

1. `python3 -m py_compile mm1.py` succeeds.
2. `python3 mm1.py` prints simulated vs theoretical L/W within tolerance and `ALL SELF-CHECKS PASSED`.
3. Raising λ toward μ visibly inflates W (try `--lam 0.95`).

## 5. Tasks

1. Add warm-up discard (first 10% events) and show bias reduction at high ρ.
2. Plot W vs ρ ∈ {0.1..0.95} as an ASCII curve; overlay theory.
3. Estimate P(wait) from the run; compare with ρ (PASTA check).
4. Replace service with constant times (→ M/D/1) and compare with the M/D/1 formula.
5. Add confidence intervals via 10 independent replications (seed sweep).
