"""Lab 02 — KMP search. Run: python3 kmp.py"""

def prefix_function(p):
    pi = [0] * len(p)
    for i in range(1, len(p)):
        j = pi[i - 1]
        while j > 0 and p[i] != p[j]:
            j = pi[j - 1]
        if p[i] == p[j]:
            j += 1
        pi[i] = j
    return pi

def kmp_search(text, pat):
    """Return all start positions (incl. overlaps). TODO(1): kept — overlaps included."""
    if not pat: return []
    pi = prefix_function(pat)
    out, j = [], 0
    for i, ch in enumerate(text):
        while j > 0 and ch != pat[j]:
            j = pi[j - 1]
        if ch == pat[j]:
            j += 1
        if j == len(pat):
            out.append(i - j + 1)
            j = pi[j - 1]  # allow overlaps
    return out

def naive_search(text, pat):
    if not pat: return []
    return [i for i in range(len(text) - len(pat) + 1) if text[i:i+len(pat)] == pat]

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    _check(prefix_function("ababaca") == [0, 0, 1, 2, 3, 0, 1], "prefix fn")
    cases = [("ababa", "aba", [0, 2]), ("aaa", "aa", [0, 1]),
             ("hello", "ll", [2]), ("abc", "d", []), ("aaaa", "a", [0, 1, 2, 3])]
    for t, p, want in cases:
        got = kmp_search(t, p)
        _check(got == want, f"kmp({t!r},{p!r})={got} want {want}")
        _check(naive_search(t, p) == want, f"naive({t!r},{p!r})")
    big_t, big_p = "a" * 2000 + "b", "a" * 50 + "b"
    _check(kmp_search(big_t, big_p) == naive_search(big_t, big_p) == [1950], "adversarial")
    print("kmp sample:", kmp_search("ababcababcabc", "ababc"))
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
