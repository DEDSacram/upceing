# Lab 02 — KMP String Search

Linear-time substring search via the prefix (failure) function — no re-scanning.

## 1. Theory

- Naive search is O(n·m): after a mismatch it re-scans. **KMP** precomputes the **prefix function** `pi[i]` = length of the longest proper prefix of `pattern[:i+1]` that is also a suffix. On mismatch at `j`, jump to `j = pi[j-1]` instead of restarting.
- Total time O(n + m), extra memory O(m). The prefix function itself is built in O(m) with the same fallback trick.
- Use when: same pattern searched repeatedly, streaming input, or worst-case guarantees matter (naive degrades on `a^n` vs `a^m b`).

## 2. Project layout

```
lab-02-kmp-search/
  README.md
  kmp.py   # prefix function + kmp_search + naive baseline, assert self-checks
```

## 3. Run

```bash
cd lab-02-kmp-search
python3 kmp.py
```

## 4. Verify

1. `python3 -m py_compile kmp.py` succeeds.
2. `python3 kmp.py` prints match positions and `ALL SELF-CHECKS PASSED`.
3. KMP and naive agree on all test cases, including overlapping matches.

## 5. Tasks

1. Return overlapping matches (e.g. `"aa"` in `"aaa"` -> `[0, 1]`); add a test.
2. Count character comparisons of KMP vs naive on `text="a"*5000+"b"`, `pat="a"*100+"b`.
3. Implement Boyer-Moore-Horspool and benchmark all three on random text.
4. Make search streaming (generator yielding positions chunk by chunk).
5. Explain in a comment why `pi` fallback keeps the scan linear.
