"""Risk-score calculator for the hazard log (stdlib, tiny YAML-subset parser)."""
import re, sys
from pathlib import Path

def band(score):
    if score >= 17: return "EXTREME"
    if score >= 10: return "HIGH"
    if score >= 5: return "MEDIUM"
    return "LOW"

def parse_hazards(path):
    text = Path(path).read_text(encoding="utf-8")
    hazards, cur = [], None
    for line in text.splitlines():
        m = re.match(r"\s*-\s*id:\s*(\S+)", line)
        if m:
            cur = {"id": m.group(1)}
            hazards.append(cur)
            continue
        m = re.match(r"\s*(title|mitigation):\s*(.+)", line)
        if m and cur is not None:
            cur[m.group(1)] = m.group(2).strip()
            continue
        m = re.match(r"\s*(severity|likelihood|mitigated_likelihood):\s*(\d+)", line)
        if m and cur is not None:
            cur[m.group(1)] = int(m.group(2))
    return hazards

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "hazards.yaml"
    hazards = parse_hazards(path)
    assert len(hazards) >= 5, f"expected >=5 hazards, got {len(hazards)}"
    ok = True
    print(f"{'id':<6}{'hazard':<42}{'S':>3}{'L':>3}{'score':>7}  band  -> residual")
    for h in hazards:
        s, l = h["severity"], h["likelihood"]
        ml = h.get("mitigated_likelihood", l)
        score, res = s * l, s * ml
        status = "OK" if res <= score else "WORSE"
        if res > score: ok = False
        print(f"{h['id']:<6}{h.get('title','')[:41]:<42}{s:>3}{l:>3}{score:>7}  {band(score):<7}-> {res} ({band(res)}) [{status}]")
    print("All mitigations reduce or keep risk." if ok else "WARNING: a mitigation increases risk!")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
