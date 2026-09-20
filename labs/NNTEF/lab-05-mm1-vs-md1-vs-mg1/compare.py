"""Lab 05 — M/M/1 vs M/D/1 vs M/G/1. Run: python3 compare.py [--rho R --n N --seed S]"""
import argparse, random

def pk_wq(lam, es, es2):
    rho = lam * es
    return lam * es2 / (2 * (1 - rho))

def lindley(lam, sampler, n, seed):
    rng = random.Random(seed)
    waits, free, t = [], 0.0, 0.0
    for _ in range(n):
        t += rng.expovariate(lam)
        s = max(t, free)
        waits.append(s - t)
        free = s + sampler(rng)
    return sum(waits) / n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rho", type=float, default=0.7)
    ap.add_argument("--n", type=int, default=30000)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    mu = 1.0; lam = a.rho * mu
    laws = {
        "M/D/1": (lambda r: 1 / mu, 1 / mu**2),
        "M/M/1": (lambda r: r.expovariate(mu), 2 / mu**2),
        "M/G/1-hyper": (lambda r: r.expovariate(2 * mu) if r.random() < 0.5 else r.expovariate(2 * mu / 3), None),
    }
    # E[S^2] of the mixture: 0.5*(2/(2mu)^2... compute numerically-free closed form:
    es2_hyper = 0.5 * (2 / (2 * mu) ** 2) + 0.5 * (2 / (2 * mu / 3) ** 2)
    es2 = {"M/D/1": 1 / mu**2, "M/M/1": 2 / mu**2, "M/G/1-hyper": es2_hyper}
    print(f"rho={a.rho} lam={lam}")
    sims = {}
    for name, (samp, _) in laws.items():
        wq = lindley(lam, samp, a.n, a.seed)
        th = pk_wq(lam, 1 / mu, es2[name])
        sims[name] = wq
        print(f"  {name:>12}: sim Wq={wq:.3f} theory={th:.3f}")
        assert abs(wq - th) / th < 0.20, f"{name} off theory"
    assert sims["M/D/1"] < sims["M/M/1"] < sims["M/G/1-hyper"], f"order violated: {sims}"
    # TODO(1): add Erlang-2 law between D and M.
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
