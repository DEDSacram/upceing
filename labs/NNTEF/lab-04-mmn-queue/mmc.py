"""Lab 04 — M/M/c Erlang B/C. Run: python3 mmc.py"""
import math

def erlang_b(c, a):
    inv = 1.0
    for k in range(1, c + 1):
        inv = 1.0 + k / a * inv
    return 1.0 / inv

def erlang_c(c, a):
    # C(c,a) = B / (1 - rho*(1 - B)), rho = a/c  (Ross, Stochastic Processes)
    b = erlang_b(c, a)
    rho = a / c
    return b / (1.0 - rho * (1.0 - b)) if a < c else 1.0

def mmc_wq(c, lam, mu):
    a = lam / mu
    assert a < c, "unstable"
    return erlang_c(c, a) / (c * mu - lam)

def mmck_blocking(c, K, lam, mu):
    """Blocking prob for M/M/c/K (K = system capacity)."""
    a = lam / mu
    assert K >= c
    p0inv = sum(a**k / math.factorial(k) for k in range(c))
    p0inv += sum(a**k / (math.factorial(c) * c**(k - c)) for k in range(c, K + 1))
    p0 = 1 / p0inv
    return p0 * a**K / (math.factorial(c) * c**(K - c))

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    _check(abs(erlang_b(1, 0.5) - 0.5 / 1.5) < 1e-9, "ErlangB c=1")
    _check(abs(mmc_wq(1, 0.7, 1.0) - 0.7 / 0.3) < 1e-9, "c=1 == M/M/1")
    w1, w2 = mmc_wq(1, 0.7, 1.0), mmc_wq(2, 1.4, 1.0)
    print(f"M/M/1 Wq={w1:.3f} vs M/M/2 (same rho) Wq={w2:.3f} (pooling wins)")
    _check(w2 < w1, "pooling should win")
    b = mmck_blocking(2, 2, 1.0, 1.0)
    _check(0 < b < 1, "blocking range")
    print(f"ErlangC(2, a=1.0)={erlang_c(2, 1.0):.4f} ErlangB(2,1.0)={erlang_b(2, 1.0):.4f} block(K=2)={b:.4f}")
    _check(mmck_blocking(2, 200, 1.0, 1.0) < 1e-3, "large K -> ~0 blocking")
    # TODO(1): event simulation of M/M/2 cross-check.
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
