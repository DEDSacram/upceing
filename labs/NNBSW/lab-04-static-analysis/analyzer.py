"""Toy static analyzer for banned C patterns (stdlib, regex rules)."""
import argparse, re, sys
from pathlib import Path

RULES = [
    ("BANNED-GETS", "error", r"\bgets\s*\(", "gets() is unbuffered — use fgets (MISRA/CERT)."),
    ("UNBOUNDED-COPY", "error", r"\b(strcpy|strcat)\s*\(", "unbounded copy — use strncpy/strncat with size."),
    ("SPRINTF", "warning", r"\bsprintf\s*\(", "sprintf may overflow — use snprintf."),
    ("SHELL-EXEC", "error", r"\bsystem\s*\(", "shell execution — avoid in safety code."),
    ("UNCHECKED-MALLOC", "warning", r"\bmalloc\s*\(", "check for NULL after malloc (heuristic)."),
]

def strip_comments(src):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"//.*", "", src)
    return src

def has_null_check(src):
    return ("== NULL" in src or "!= NULL" in src or "if (p" in src or "if(p" in src)

def analyze(path):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    code = strip_comments(text)
    findings = []
    lines = code.splitlines()
    for rid, sev, pat, why in RULES:
        rx = re.compile(pat)
        for i, line in enumerate(lines, 1):
            if rx.search(line):
                if rid == "UNCHECKED-MALLOC" and has_null_check(code):
                    continue  # file does check malloc somewhere -> suppress heuristic
                findings.append((i, rid, sev, line.strip()[:90], why))
    return findings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    total = 0
    for f in args.files:
        findings = analyze(f)
        total += len(findings)
        print(f"== {f}: {len(findings)} finding(s)")
        for ln, rid, sev, line, why in sorted(findings):
            print(f"  line {ln}: [{sev}] {rid}: {line}")
            print(f"           -> {why}")
    if args.strict and total:
        sys.exit(1)

if __name__ == "__main__":
    main()
