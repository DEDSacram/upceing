"""Lab 06 — Closed machine-repair M/M/R//N solver. Run: python3 closed.py"""

def solve(N, R, lam, mu):
    birth = [((N - k) * lam) for k in range(N + 1)]
    death = [0.0] + [min(k, R) * mu for k in range(1, N + 1)]
    p = [1.0] * (N + 1)
    for k in range(1, N + 1):
        p[k] = p[k - 1] * birth[k - 1] / death[k]
    s = sum(p); p = [x / s for x in p]
    L = sum(k * x for k, x in enumerate(p))
    lam_eff = sum(birth[k] * p[k] for k in range(N + 1))
    W = L / lam_eff if lam_eff else 0.0
    return {"p": p, "L": L, "W": W, "avail": 1 - L / N, "lam_eff": lam_eff}

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    N, lam, mu = 8, 0.1, 1.0
    prev = -1
    for R in (1, 2, 3):
        r = solve(N, R, lam, mu)
        _check(abs(sum(r["p"]) - 1) < 1e-9, "probs sum")
        _check(r["avail"] >= prev - 1e-12, "more repairmen hurt?")
        prev = r["avail"]
        print(f"R={R}: L={r['L']:.3f} W={r['W']:.3f} avail={r['avail']:.4f} lam_eff={r['lam_eff']:.3f}")
    r1 = solve(N, 1, lam, mu)
    _check(0 < r1["L"] < N and r1["W"] > 0, "sanity")
    # single machine closed form: up-fraction = mu/(lam+mu)
    s1 = solve(1, 1, lam, mu)
    _check(abs(s1["avail"] - mu / (lam + mu)) < 1e-9, "N=1 closed form")
    # TODO(1): event simulation cross-check.
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
