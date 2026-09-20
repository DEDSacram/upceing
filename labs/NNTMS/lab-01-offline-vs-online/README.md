# Lab 01 — Offline vs Online Simulation (Queue)

Discrete-event M/M/1 queue: analytic solution vs event-driven simulation.

## 1. Theory

- **Offline (analytic):** closed-form M/M/1 results — utilization `ρ=λ/μ`, mean wait `Wq=ρ/(μ−λ)`, mean number `Lq=ρ²/(1−ρ)`. Instant, exact under Markov assumptions.
- **Online (event-driven):** simulate arrivals/departures event by event with a PRNG; estimates converge to analytic values as simulated time → ∞.
- **Takeaway:** use analytic for design-space sweeps, simulation when assumptions break (non-exponential, priorities, breakdowns).

## 2. Project layout

```
lab-01-offline-vs-online/
  README.md
  queue_sim.py   # analytic + discrete-event sim, comparison table
```

## 3. Run

```bash
cd labs/NNTMS/lab-01-offline-vs-online
python3 queue_sim.py
python3 queue_sim.py --lam 0.8 --mu 1.0 --t 20000 --seed 7
```

## 4. Verify

1. Default run: simulated `Wq` within 20% of analytic `Wq`.
2. `--t 20000` run is closer to analytic than `--t 500` (convergence).
3. `python3 -m py_compile queue_sim.py` passes.

## 5. Tasks

1. Sweep `ρ ∈ {0.3, 0.6, 0.9}`; plot sim-vs-analytic error vs `ρ`.
2. Replace exponential service with deterministic (`D`): compare M/D/1 sim against `Wq=ρ/(2μ(1−ρ))`.
3. Add a priority class and show where the analytic formula no longer applies.
4. Explain in 3 lines when you would trust the formula over the sim.
