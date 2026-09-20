# Lab 01 — Monte Carlo Estimation of Pi

Estimate π by random sampling: throw darts at the unit square, count hits in the quarter circle.

## 1. Theory

- **Monte Carlo:** inscribe a quarter circle (radius 1) in the unit square. `P(hit) = π/4`, so `π ≈ 4·hits/N`.
- **Error:** hits ~ Binomial(N, π/4); std error of the estimate ≈ `4·sqrt(p(1-p)/N)` = O(1/√N). Ten times the accuracy needs 100× samples — the signature Monte Carlo rate.
- Uses only stdlib `random`; seed it (`random.Random(seed)`) for reproducibility. Report estimate ± 95% CI (`±1.96·SE`).

## 2. Project layout

```
lab-01-monte-carlo-pi/
  README.md
  monte_carlo_pi.py   # estimator + CI + convergence table, ASCII output
```

## 3. Run

```bash
cd lab-01-monte-carlo-pi
python3 monte_carlo_pi.py
python3 monte_carlo_pi.py --n 200000 --seed 1
```

## 4. Verify

1. `python3 -m py_compile monte_carlo_pi.py` succeeds.
2. `python3 monte_carlo_pi.py` prints estimates converging toward 3.14159 and `ALL SELF-CHECKS PASSED`.
3. With `--n 200000`, the 95% CI covers math.pi (usually) and width shrinks ~1/√N.

## 5. Tasks

1. Verify the 1/√N rate: compare CI widths at N and 100·N.
2. Add stratified sampling (grid cells) and compare variance vs plain sampling.
3. Estimate `∫₀¹ x² dx` by Monte Carlo; compare with 1/3.
4. Show a bad-PRNG artifact: replace `random()` with a coarse lattice and note the bias.
5. Time scaling: N = 10³..10⁶, confirm linear time, log it in a comment.
