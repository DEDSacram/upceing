"""Lab 07 — Amortized dynamic array experiment. Run: python3 amortized.py"""
import time

class DynArray:
    def __init__(self, grow):
        self.grow = grow  # fn(cap) -> new cap
        self.cap, self.n, self.copies = 1, 0, 0
        self.a = [None] * 1
    def append(self, x):
        if self.n == self.cap:
            new = max(self.n + 1, self.grow(self.cap))
            b = [None] * new
            for i in range(self.n): b[i] = self.a[i]
            self.copies += self.n
            self.a, self.cap = b, new
        self.a[self.n] = x; self.n += 1

def trial(grow, n=100_000):
    d = DynArray(grow)
    t = time.perf_counter()
    for i in range(n): d.append(i)
    dt = time.perf_counter() - t
    assert list(d.a[:d.n]) == list(range(n))
    return dt, d.copies / n, d.cap

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    rows = [
        ("double x2", lambda c: c * 2),
        ("x1.5", lambda c: int(c * 1.5) + 1),
        ("+1000", lambda c: c + 1000),
    ]
    print(f"{'growth':>10} {'ms':>8} {'copies/app':>10} {'final cap':>10}")
    res = {}
    for name, g in rows:
        dt, cpa, cap = trial(g)
        res[name] = cpa
        print(f"{name:>10} {dt*1e3:>8.1f} {cpa:>10.2f} {cap:>10}")
    _check(res["double x2"] < 3.0, f"doubling copies/append {res['double x2']}")
    _check(res["double x2"] < res["+1000"], "doubling should beat +1000")
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
