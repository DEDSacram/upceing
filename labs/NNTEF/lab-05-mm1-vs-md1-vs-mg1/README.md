# Lab 05 — M/M/1 vs M/D/1 vs M/G/1 Comparison

Same arrival rate, same mean service — but service *variability* drives waiting. Pollaczek–Khinchine makes it exact.

## 1. Theory

- **M/G/1 P–K formula:** `Wq = λ·E[S²] / (2(1−ρ))`. Only the second moment of service matters.
- Special cases: M/M/1 (exponential, `E[S²]=2/μ²`) → `Wq = ρ/(μ−λ)`; **M/D/1** (deterministic, `E[S²]=1/μ²`) → exactly **half** of M/M/1.
- Experiment: fix λ, mean service; simulate exponential / deterministic / hyperexponential service; rank Wq and compare with P–K.

## 2. Project layout

```
lab-05-mm1-vs-md1-vs-mg1/
  README.md
  compare.py   # Lindley simulation for 3 service laws + P-K check (random only)
```

## 3. Run

```bash
cd lab-05-mm1-vs-md1-vs-mg1
python3 compare.py
python3 compare.py --rho 0.8 --n 40000 --seed 5
```

## 4. Verify

1. `python3 -m py_compile compare.py` succeeds.
2. `python3 compare.py` prints `Wq(M/D/1) < Wq(M/M/1) < Wq(hyper)` and `ALL SELF-CHECKS PASSED`.
3. Each simulated Wq is within 15% of its P–K prediction.

## 5. Tasks

1. Add Erlang-2 service (CoV < 1); confirm it sits between D and M.
2. Sweep ρ ∈ {0.3, 0.5, 0.7, 0.9}; draw ASCII curves theory vs sim.
3. Derive in a comment why deterministic service halves M/M/1 waiting.
4. Test robustness: Pareto service with infinite variance (sim Wq explodes).
5. Repeat with 10 seeds; report mean ± CI per discipline.
