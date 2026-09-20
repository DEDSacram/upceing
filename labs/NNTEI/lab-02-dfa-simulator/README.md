# Lab 02 — DFA Simulator + Scanner Example

Build a deterministic finite automaton class and use it as a tiny lexical scanner.

## 1. Theory

- A **DFA** is `(Q, Sigma, delta, q0, F)`: finite states, alphabet, total transition function, start state, accept states.
- A string is **accepted** iff following `delta` from `q0` ends in `F`. DFAs recognize exactly the **regular languages**; they run in O(n) time, O(1) memory.
- **Scanner idea:** run several DFAs (or one combined DFA) over the input; longest-match / priority decides the token. Keywords are just extra accept states checked against a table.
- Non-regular languages (e.g. `a^n b^n`, balanced parens) need a stack (PDA, Lab 05) or more.

## 2. Project layout

```
lab-02-dfa-simulator/
  README.md
  dfa.py   # DFA class + even-zeros DFA + identifier/integer scanner demo
```

## 3. Run

```bash
cd lab-02-dfa-simulator
python3 dfa.py
```

## 4. Verify

1. `python3 -m py_compile dfa.py` succeeds.
2. `python3 dfa.py` prints `ALL SELF-CHECKS PASSED` plus a tokenized sample line.
3. Change an accept state and confirm a self-check fails (then revert).

## 5. Tasks

1. Add a DFA for "ends with `01`" over `{0,1}` (3 states) with tests.
2. Implement `DFA.complement()` (flip `F`) and test on the even-zeros DFA.
3. Extend the scanner with `FLOAT` and `STRING` token kinds.
4. Implement longest-match scanning (current demo is greedy per-char class) and show a case where it matters.
5. Prove/argue why `a^n b^n` cannot be done with any DFA (pumping-lemma sketch in a comment).
