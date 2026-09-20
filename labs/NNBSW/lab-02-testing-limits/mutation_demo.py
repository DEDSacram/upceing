"""Mutation-testing mini-demo (stdlib only)."""
import argparse

def is_safe_speed(speed, limit):
    """Original: safe iff speed <= limit and both non-negative."""
    if speed < 0 or limit < 0:
        return False
    return speed <= limit

# (name, mutated function)
MUTANTS = [
    ("M1: <= to <", lambda s, l: (False if s < 0 or l < 0 else s < l)),
    ("M2: <= to >=", lambda s, l: (False if s < 0 or l < 0 else s >= l)),
    ("M3: drop neg-check", lambda s, l: s <= l),
    ("M4: limit+1", lambda s, l: (False if s < 0 or l < 0 else s <= l + 1)),
    ("M5: and to or", lambda s, l: (False if (s < 0 and l < 0) else s <= l)),
]

WEAK_SUITE = [(10, 50, True), (100, 50, False)]  # no boundary, no negatives
STRONG_SUITE = [(10, 50, True), (100, 50, False), (50, 50, True),
                (51, 50, False), (-1, 50, False), (10, -5, False)]

def score(fn, suite):
    kills = []
    for name, mut in MUTANTS:
        killed = any(mut(s, l) != exp for s, l, exp in suite if fn is None or True)
        # sanity: original must pass the suite
        kills.append((name, killed))
    return kills

def suite_passes_original(suite):
    return all(is_safe_speed(s, l) == exp for s, l, exp in suite)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", choices=["weak", "strong", "both"], default="both")
    args = ap.parse_args()
    suites = {"weak": WEAK_SUITE, "strong": STRONG_SUITE}
    todo = ["weak", "strong"] if args.suite == "both" else [args.suite]
    for name in todo:
        suite = suites[name]
        assert suite_passes_original(suite), f"original fails {name} suite!"
        kills = score(is_safe_speed, suite)
        killed = sum(1 for _, k in kills if k)
        print(f"--- {name} suite ({len(suite)} tests) ---")
        for mname, k in kills:
            print(f"  {'KILLED' if k else 'SURVIVED'}  {mname}")
        print(f"  mutation score: {killed}/{len(kills)} = {killed/len(kills):.2f}\n")

if __name__ == "__main__":
    main()
