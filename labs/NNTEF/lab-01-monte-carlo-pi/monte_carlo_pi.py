"""Lab 01 — Monte Carlo pi. Run: python3 monte_carlo_pi.py [--n N --seed S]"""
import argparse, math, random

def estimate(n, seed=0):
    rng = random.Random(seed)
    hits = sum(1 for _ in range(n) if (x := rng.random())**2 + rng.random()**2 <= 1.0)
    p = hits / n
    est = 4 * p
    se = 4 * math.sqrt(p * (1 - p) / n)
    return est, se, hits

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=50000)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    print(f"{'N':>8} {'est':>8} {'95% CI half-width':>18}")
    for n in (1000, 10000, a.n):
        est, se, _ = estimate(n, a.seed)
        print(f"{n:>8} {est:>8.4f} {1.96*se:>18.4f}")
    est, se, _ = estimate(a.n, a.seed)
    # TODO(1): verify CI width ratio ~ sqrt(100)=10 between N and 100N.
    _check(abs(est - math.pi) < 4 * se + 0.02, f"far from pi: {est}")
    e1, s1, _ = estimate(2000, 123)
    e2, _, _ = estimate(2000, 123)
    _check(e1 == e2, "seeded runs must reproduce")
    print(f"final: pi~{est:.5f} +- {1.96*se:.5f} (true {math.pi:.5f})")
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
