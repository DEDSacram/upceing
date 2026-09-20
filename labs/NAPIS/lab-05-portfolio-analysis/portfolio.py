"""TIME quadrant scoring for an app portfolio CSV (stdlib only)."""
import argparse, csv, sys

def quadrant(value, health, t):
    if value >= t and health >= t:
        return "Invest"
    if value >= t and health < t:
        return "Migrate"
    if value < t and health >= t:
        return "Tolerate"
    return "Eliminate"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csvfile")
    ap.add_argument("--threshold", type=float, default=5.0)
    args = ap.parse_args()
    rows = list(csv.DictReader(open(args.csvfile, encoding="utf-8")))
    counts = {}
    savings = 0
    print(f"{'app':<15}{'value':>7}{'health':>8}{'cost':>10}  quadrant")
    for r in rows:
        v, h, c = float(r["value"]), float(r["health"]), float(r["annual_cost"])
        q = quadrant(v, h, args.threshold)
        counts[q] = counts.get(q, 0) + 1
        if q == "Eliminate":
            savings += c
        print(f"{r['name']:<15}{v:>7.1f}{h:>8.1f}{c:>10.0f}  {q}")
    print(f"\nThreshold: {args.threshold}")
    print("Summary:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"Eliminate savings potential: {savings:.0f}/year")

if __name__ == "__main__":
    main()
