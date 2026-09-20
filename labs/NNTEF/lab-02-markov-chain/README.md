# Lab 02 — Markov Chain Stationary Distribution (Power Iteration)

Find the long-run distribution of a finite Markov chain by repeated multiplication.

## 1. Theory

- A **stochastic matrix** P has rows summing to 1; `π` is **stationary** if `πP = π`. For an irreducible aperiodic chain, `v·P^k → π` from any start vector (power iteration), geometrically fast (|λ₂|^k).
- Demo: 3-state weather chain (sunny/cloudy/rainy). Iterate until L1 change < tol; cross-check against solving `(Pᵀ−I)π=0` via Gaussian elimination (stdlib).
- **Detailed balance** (reversible chains): `π_i P_ij = π_j P_ji` — optional check for symmetric cases.

## 2. Project layout

```
lab-02-markov-chain/
  README.md
  markov.py   # power iteration + linear-solve check, ASCII output
```

## 3. Run

```bash
cd lab-02-markov-chain
python3 markov.py
```

## 4. Verify

1. `python3 -m py_compile markov.py` succeeds.
2. `python3 markov.py` prints π ≈ stationary vector and `ALL SELF-CHECKS PASSED`.
3. Power iteration and the linear solve agree to 1e-6; `πP − π` residual ≈ 0.

## 5. Tasks

1. Add a periodic 2-state chain (`[[0,1],[1,0]]`); show power iteration oscillates and fix with averaging.
2. Measure convergence rate vs second eigenvalue (estimate |λ₂| from residuals).
3. Simulate a sample path of 50k steps; compare empirical frequencies with π.
4. Implement an absorbing chain and compute absorption probabilities.
5. Test sensitivity: perturb one row by 0.05, report Δπ.
