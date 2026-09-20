# Lab 05 — PDA Simulator (Balanced Parentheses)

Simulate a pushdown automaton: a finite control plus a stack. Accept balanced parentheses — beyond DFA power.

## 1. Theory

- A **PDA** = finite control + **stack** (push/pop, LIFO). Transitions depend on (state, input symbol or ε, stack top) and may push a string of symbols.
- Acceptance here: consume all input, end in an accept state (here: stack back to bottom marker `Z`). Nondeterminism can be assumed w.l.o.g. for power, but this lab's PDA is deterministic.
- Canonical demo: `L = {w in {(,)}* : balanced}`. On `(` push; on `)` pop; reject a pop from the bottom marker. This language is context-free but **not regular** (pumping lemma) — so no DFA (Lab 02) can do it.
- PDAs ≡ CFGs in expressive power (every CFL has a PDA and vice versa).

## 2. Project layout

```
lab-05-pda-simulator/
  README.md
  pda.py   # deterministic PDA for balanced parens + trace mode
```

## 3. Run

```bash
cd lab-05-pda-simulator
python3 pda.py
```

## 4. Verify

1. `python3 -m py_compile pda.py` succeeds.
2. `python3 pda.py` prints accept/reject for the sample batch and `ALL SELF-CHECKS PASSED`.
3. `python3 pda.py --trace "(())"` shows push/pop steps.

## 5. Tasks

1. Extend the PDA to three bracket kinds `()`, `[]`, `{}` (push the opener, match on closer).
2. Count nesting depth during simulation; report `max_depth` for each input.
3. Accept by *empty stack* instead of final state; compare the two modes.
4. Show a concrete input where a DFA for "up to k nesting" fails but the PDA succeeds; fix k=2.
5. Sketch (comment) a PDA for `a^n b^n` and test it via a generic transition-table simulator.
