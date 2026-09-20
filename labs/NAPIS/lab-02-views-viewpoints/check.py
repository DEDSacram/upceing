"""Completeness check for the viewpoint matrix (stdlib, minimal YAML scan)."""
import re, sys
from pathlib import Path

def load(p):
    return Path(p).read_text(encoding="utf-8")

def main():
    base = Path(__file__).parent
    vp = load(base / "viewpoints.yaml")
    st = load(base / "stakeholders.yaml")
    issues = []
    for needle, fname in (("TODO", "viewpoints.yaml"),):
        if "TODO" in vp:
            n = vp.count("TODO")
            issues.append(f"{fname}: {n} TODO marker(s) left to fill")
    # every coverage line must have a non-TODO view
    for m in re.finditer(r"^\s*(\S+):\s*\[(.*)\]", vp, re.M):
        concern, views = m.group(1), m.group(2)
        if concern in ("id", "name", "notation", "concerns", "viewpoint", "stakeholders", "answers", "influence", "interest", "role"):
            continue
        if "TODO" in views or not views.strip():
            issues.append(f"coverage '{concern}' has no concrete view")
    if "TODO" in st:
        issues.append(f"stakeholders.yaml: {st.count('TODO')} TODO marker(s) left")
    stakeholders = re.findall(r"-\s*id:\s*(\S+)", st)
    if len(stakeholders) < 5:
        issues.append(f"only {len(stakeholders)} stakeholders, need >= 5")
    if issues:
        print("INCOMPLETE:")
        for i in issues:
            print(" -", i)
        sys.exit(1)
    print(f"OK: matrix starter consistent ({len(stakeholders)} stakeholders). Fill TODOs to complete the lab.")

if __name__ == "__main__":
    main()
