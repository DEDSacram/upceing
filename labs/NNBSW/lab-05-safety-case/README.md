# Lab 05 — Safety Case (GSN Template)

Write a Goal Structuring Notation safety case: claims, arguments, evidence, assumptions.

## 1. Theory

- **Safety case** = structured argument that a system is acceptably safe in its context (required by EN 50129, ISO 26262, DO-178C).
- **GSN elements:** Goal (claim), Strategy (argument approach), Solution (evidence: test report, proof), Context (operating envelope), Assumption, Justification. Arrows: `supportedBy` (goal→strategy/solution), `inContextOf`.
- **Argument pattern:** top goal "Crossing is acceptably safe" → strategy "argue over hazards" → sub-goals per hazard (H-01..H-05 from Lab 01) → solutions (test/proof/analysis reports).
- A safety case is only as strong as its weakest evidence link — every goal must bottom out in a Solution, every Assumption must be validated.

## 2. Project layout

```
lab-05-safety-case/
  README.md
  gsn.yaml          # GSN tree starter (goals/strategies/solutions; 2 TODO sub-goals)
  checklist.md      # review checklist (independent reviewer questions)
  check.py          # structural check: ids unique, every goal grounded, no dangling refs
```

## 3. Run

```bash
cd labs/NNBSW/lab-05-safety-case
python3 check.py gsn.yaml
```

## 4. Verify

1. `python3 check.py gsn.yaml` exits 0 after TODOs are filled (starter reports the 2 missing sub-goals).
2. Every Goal traces to ≥1 Solution (directly or via children); every `supportedBy` target exists.
3. Reviewer can answer all `checklist.md` questions from `gsn.yaml` alone.

## 5. Tasks

1. Fill the 2 TODO sub-goals (H-04, H-05) with strategies + solutions pointing at Lab 01/02/04 evidence.
2. Add an Assumption (e.g. "train speed ≤ 160 km/h") and a validation Solution.
3. Add a counter-evidence node (a failed test) and show how the case handles it.
4. Swap reviews with a peer using `checklist.md`; record findings.
