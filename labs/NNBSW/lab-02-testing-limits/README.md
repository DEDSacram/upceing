# Lab 02 — Testing Limits (Mutation-Testing Mini-Demo)

Shows what coverage hides: seeded mutants that pass a weak suite but fail a strong one.

## 1. Theory

- **Coverage** measures executed lines, not checked behaviour. 100% line coverage can still miss off-by-one or operator bugs.
- **Mutation testing:** seed small faults (mutants: `>`→`>=`, `+`→`-`, constant changes) into code under test; a good suite **kills** mutants (≥1 test fails). **Mutation score = killed / total**.
- **Competent-programmer hypothesis:** real faults are small syntactic slips — mutants approximate them.
- Demo target: `is_safe_speed(speed, limit)` with boundary semantics `speed <= limit`. Mutants flip the boundary and arithmetic.

## 2. Project layout

```
lab-02-testing-limits/
  README.md
  mutation_demo.py   # target function + mutants + weak/strong suites + scorer
```

## 3. Run

```bash
cd labs/NNBSW/lab-02-testing-limits
python3 mutation_demo.py
python3 mutation_demo.py --suite strong
```

## 4. Verify

1. `python3 mutation_demo.py` prints weak-suite score < strong-suite score (weak leaves survivors).
2. Strong suite kills all mutants (score 1.00) — the boundary test `limit` itself is the key case.
3. `python3 -m py_compile mutation_demo.py` passes.

## 5. Tasks

1. Add a mutant (`speed < limit - 1`) and check which suite kills it.
2. Add a mutant on a new function (e.g. `brake_distance`) with its own tests.
3. Measure: how many tests does the strong suite need for score 1.0? Remove redundant ones.
4. Write 3 lines: why is mutation score a better safety argument than line coverage?
