"""Lab 03 — M/M/1 event simulation vs Erlang. Run: python3 mm1.py [--lam L --mu M --n N --seed S]"""
import argparse, random

def erlang(lam, mu):
    rho = lam / mu
    return {"rho": rho, "L": rho / (1 - rho), "Lq": rho**2 / (1 - rho),
            "W": 1 / (mu - lam), "Wq": rho / (mu - lam)}

def simulate(lam, mu, n, seed=0):
    """FCFS single server via Lindley recursion.

    waits[i] = queueing delay (excludes own service); W = Wq + 1/mu.
    """
    rng = random.Random(seed)
    arrs, t = [], 0.0
    for _ in range(n):
        t += rng.expovariate(lam)
        arrs.append(t)
    waits, free = [], 0.0
    for a in arrs:
        s = max(a, free)          # service start
        waits.append(s - a)       # queue wait only
        free = s + rng.expovariate(mu)
    Wq = sum(waits) / n
    W = Wq + 1 / mu               # total sojourn = wait + mean service
    L = lam * W                   # Little's law
    return {"L": L, "W": W, "Wq": Wq, "pwait": sum(1 for x in waits if x > 0) / n}

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lam", type=float, default=0.7)
    ap.add_argument("--mu", type=float, default=1.0)
    ap.add_argument("--n", type=int, default=30000)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    th = erlang(a.lam, a.mu)
    sim = simulate(a.lam, a.mu, a.n, a.seed)
    print(f"rho={th['rho']:.2f} L: sim={sim['L']:.3f} vs theory={th['L']:.3f} | "
          f"W: sim={sim['W']:.3f} vs theory={th['W']:.3f} | "
          f"Wq: sim={sim['Wq']:.3f} vs theory={th['Wq']:.3f} | P(wait)~{sim['pwait']:.3f}")
    _check(abs(sim["L"] - th["L"]) / th["L"] < 0.15, f"L off: {sim['L']} vs {th['L']}")
    _check(abs(sim["W"] - th["W"]) / th["W"] < 0.15, f"W off: {sim['W']} vs {th['W']}")
    _check(abs(sim["pwait"] - th["rho"]) < 0.08, "PASTA P(wait)~rho violated")
    # TODO(2): sweep rho and draw ASCII curve.
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
