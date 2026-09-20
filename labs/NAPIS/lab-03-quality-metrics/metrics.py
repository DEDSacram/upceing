"""Architecture quality metrics from a component JSON (stdlib only)."""
import argparse, json, sys

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["components"]

def compute(components):
    names = {c["name"] for c in components}
    # afferent: how many depend on me
    ca = {n: 0 for n in names}
    for c in components:
        for d in c.get("depends_on", []):
            if d in ca:
                ca[d] += 1
    rows = []
    for c in components:
        name = c["name"]
        ce = len(c.get("depends_on", []))
        a = ca[name]
        instability = ce / (a + ce) if (a + ce) else 0.0
        churn = c.get("churn", 0)
        defects = c.get("defects", 0)
        risk = ce * churn * (1 + defects / 10.0)
        rows.append({"name": name, "fan_out_Ce": ce, "fan_in_Ca": a,
                      "instability": round(instability, 3), "risk": round(risk, 2)})
    rows.sort(key=lambda r: r["risk"], reverse=True)
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="components JSON")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()
    rows = compute(load(args.input))
    if args.as_json:
        print(json.dumps(rows, indent=2))
        return
    print(f"{'component':<12}{'Ce':>4}{'Ca':>4}{'I':>7}{'risk':>10}  flags")
    for r in rows:
        flags = []
        if r["fan_out_Ce"] > 4:
            flags.append("HIGH-FANOUT")
        if r["instability"] > 0.7:
            flags.append("UNSTABLE")
        print(f"{r['name']:<12}{r['fan_out_Ce']:>4}{r['fan_in_Ca']:>4}{r['instability']:>7}{r['risk']:>10}  {' '.join(flags)}")

if __name__ == "__main__":
    main()
