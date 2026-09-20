# Lab 04 — CFG Derivation (Trees, CNF Check)

Derive strings from context-free grammars, print derivation trees, and check Chomsky Normal Form.

## 1. Theory

- A **CFG** is `(V, Sigma, R, S)`: variables, terminals, productions `A -> alpha`, start symbol. One **derivation step** rewrites a single variable using a rule; a **leftmost derivation** always rewrites the leftmost variable.
- A **parse/derivation tree** has variables at inner nodes and terminals at leaves; its yield is the derived string. Ambiguous grammars admit ≥2 trees for one string.
- **Chomsky Normal Form (CNF):** every rule is `A -> BC` (two variables), `A -> a` (one terminal), or `S -> ε`. Any ε/cycle-free CFG can be converted to CNF — the shape CKY parsing (and many proofs) assume.
- CFGs ⊃ regular languages (e.g. `a^n b^n` is context-free but not regular).

## 2. Project layout

```
lab-04-cfg-derivation/
  README.md
  cfg.py   # Grammar class, leftmost derivation, tree printer, CNF checker
```

## 3. Run

```bash
cd lab-04-cfg-derivation
python3 cfg.py
```

## 4. Verify

1. `python3 -m py_compile cfg.py` succeeds.
2. `python3 cfg.py` prints a derivation of `(())`, a tree, CNF verdicts, and `ALL SELF-CHECKS PASSED`.

## 5. Tasks

1. Add grammar for `a^n b^n`; derive `aaabbb` and print the tree.
2. Show ambiguity: two trees for `a+a*a` under the expression grammar; then fix it with precedence layers.
3. Implement ε-rule elimination (one step) and re-run the CNF check.
4. Implement a CYK recognizer for CNF grammars and test membership of 10 strings.
5. Write the CNF conversion of `S -> aSb | ε` step by step in a comment.
