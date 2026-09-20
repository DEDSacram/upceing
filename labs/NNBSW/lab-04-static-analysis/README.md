# Lab 04 — Static Analysis (Toy C Checker)

A tiny Python analyzer that flags banned/suspicious C patterns in sample files.

## 1. Theory

- **Static analysis** reasons about code without running it: pattern matching (lint), dataflow (taint), abstract interpretation (value ranges).
- **Safety-critical C (MISRA C):** bans `gets`, unbounded `strcpy/strcat/sprintf`, unchecked `malloc` return, `system()`, dynamic recursion without bound.
- This toy checker is regex-based (like a baby `grep`+rules engine): each rule has id, severity, pattern, rationale. Real tools (Cppcheck, Coverity, CodeQL) add parsing + dataflow; the rule-catalog idea is the same.
- Expect **false positives/negatives** — tune rules, then confirm by reading.

## 2. Project layout

```
lab-04-static-analysis/
  README.md
  analyzer.py      # rule engine: scans .c files, reports findings with line numbers
  samples/
    unsafe.c       # 5 seeded violations (must all be flagged)
    safe.c         # clean file (must report 0 findings)
```

## 3. Run

```bash
cd labs/NNBSW/lab-04-static-analysis
python3 analyzer.py samples/unsafe.c samples/safe.c
python3 analyzer.py --strict samples/unsafe.c
```

## 4. Verify

1. `unsafe.c` yields ≥5 findings covering rules `BANNED-GETS`, `UNBOUNDED-COPY`, `UNCHECKED-MALLOC`, `SHELL-EXEC`, `SPRINTF`.
2. `safe.c` yields 0 findings.
3. `--strict` exits non-zero when any finding exists.

## 5. Tasks

1. Add rule `NO-ASSERT-SIDE-EFFECT` flagging `assert(x++)`-style side effects.
2. Add rule for unchecked `scanf` return value; seed a violation and confirm detection.
3. Measure false positives: run on any local `.c` file and triage 3 findings.
4. Write 3 lines: what can this regex checker never catch that dataflow analysis can?
