"""Structural check for the GSN YAML starter (stdlib)."""
import re, sys
from pathlib import Path

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "gsn.yaml"
    text = Path(path).read_text(encoding="utf-8")
    ids = re.findall(r"-\s*id:\s*(\S+)", text)
    dupes = {i for i in ids if ids.count(i) > 1}
    issues = [f"duplicate id {d}" for d in dupes]
    if "TODO" in text:
        issues.append(f"{text.count('TODO')} TODO marker(s) left to fill")
    refs = set(re.findall(r"TODO-[A-Za-z0-9-]+", text))
    for r in refs:
        issues.append(f"dangling ref {r} (TODO node not yet added)")
    goals = re.findall(r"type:\s*Goal", text)
    sols = re.findall(r"type:\s*Solution", text)
    print(f"nodes: {len(ids)} ({len(goals)} goals, {len(sols)} solutions)")
    if issues:
        print("INCOMPLETE:");
        [print(" -", i) for i in issues]
        sys.exit(1)
    print("OK: structure consistent. Review against checklist.md.")

if __name__ == "__main__":
    main()
