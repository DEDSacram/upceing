#!/usr/bin/env python3
"""Linux-verifiable twin of Parse-Log.ps1: count log lines by severity."""
import re
import sys
from collections import Counter

path = sys.argv[1] if len(sys.argv) > 1 else "sample.log"
counts = Counter()
errors = []
try:
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.search(r"\b(INFO|WARN|ERROR)\b", line)
            if m:
                counts[m.group(1)] += 1
                if m.group(1) == "ERROR":
                    errors.append(line.rstrip())
except FileNotFoundError:
    print(f"File not found: {path}", file=sys.stderr)
    sys.exit(1)

print(f"=== Summary for {path} ===")
for level in ("ERROR", "INFO", "WARN"):
    print(f"{level:5}: {counts.get(level, 0)}")
if errors:
    print("=== ERROR lines ===")
    print("\n".join(errors))
