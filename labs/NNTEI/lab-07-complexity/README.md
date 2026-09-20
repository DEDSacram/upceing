# Lab 07 — Complexity: P vs Exponential Brute Force

Feel the P vs NP gap: polynomial algorithms scale; exponential brute force hits a wall.

## 1. Theory

- **P** = decidable in polynomial time on a deterministic TM. **EXP** = exponential time. (NP = polynomial-time *verifiable*.)
- Demo pair on the same problem (Subset Sum): brute force tries all 2^n subsets — O(2^n); dynamic programming over the target sum runs in O(n·S) (**pseudopolynomial**: polynomial in n and the *value* S, exponential in the *bit-length* of S).
- Timing method: `time.perf_counter()` around repeats; take the best of K runs to reduce noise. Keep n small (≤ 22) so brute force finishes.
- Takeaway: an exponential curve doubles per +1 n; a polynomial curve barely moves. That wall is why complexity classes matter in practice.

## 2. Project layout

```
lab-07-complexity/
  README.md
  complexity.py   # subset-sum brute force vs DP + timing table (stdlib only, ASCII)
```

## 3. Run

```bash
cd lab-07-complexity
python3 complexity.py
```

## 4. Verify

1. `python3 -m py_compile complexity.py` succeeds.
2. `python3 complexity.py` prints a timing table where brute-force ms roughly double per row and `ALL SELF-CHECKS PASSED`.
3. Both solvers agree on all self-check instances.

## 5. Tasks

1. Add a memoized (top-down DP) solver and time it against bottom-up.
2. Plot the table as ASCII bars (no matplotlib — stdlib only) and paste it here.
3. Find the largest n your machine brute-forces in < 5 s; record it.
4. Show a "hard" instance (large S) where DP degrades; explain pseudopolynomial in a comment.
5. Implement 2-SAT (linear, in P) vs brute-force 2-SAT and time both for n = 10..20.
