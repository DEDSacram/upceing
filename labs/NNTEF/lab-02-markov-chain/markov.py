"""Lab 02 — Markov stationary distribution. Run: python3 markov.py"""
P = [[0.7, 0.2, 0.1],
     [0.3, 0.5, 0.2],
     [0.2, 0.3, 0.5]]

def step(v, M):
    n = len(v)
    return [sum(v[i] * M[i][j] for i in range(n)) for j in range(n)]

def power_iteration(M, tol=1e-10, maxit=10000):
    n = len(M)
    v = [1 / n] * n
    for k in range(1, maxit + 1):
        w = step(v, M)
        if sum(abs(a - b) for a, b in zip(w, v)) < tol:
            return w, k
        v = w
    raise RuntimeError("no convergence")

def solve_stationary(M):
    """Gaussian elimination on (P^T - I) with sum(pi)=1 constraint."""
    n = len(M)
    A = [[M[j][i] - (1.0 if i == j else 0.0) for j in range(n)] for i in range(n)]
    A[-1] = [1.0] * n
    b = [0.0] * (n - 1) + [1.0]
    # eliminate
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(A[r][col]))
        A[col], A[piv] = A[piv], A[col]; b[col], b[piv] = b[piv], b[col]
        for r in range(n):
            if r != col and A[r][col] != 0:
                f = A[r][col] / A[col][col]
                A[r] = [a - f * c for a, c in zip(A[r], A[col])]
                b[r] -= f * b[col]
    return [b[i] / A[i][i] for i in range(n)]

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    pi, iters = power_iteration(P)
    ref = solve_stationary(P)
    res = [abs(a - b) for a, b in zip(step(pi, P), pi)]
    print(f"pi={[round(x, 4) for x in pi]} iters={iters} residual={max(res):.2e}")
    _check(abs(sum(pi) - 1) < 1e-9 and all(x > 0 for x in pi), "not a distribution")
    _check(max(abs(a - b) for a, b in zip(pi, ref)) < 1e-6, f"solvers disagree {ref}")
    _check(max(res) < 1e-8, "pi*P != pi")
    # TODO(3): simulate path and compare empirical frequencies.
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
