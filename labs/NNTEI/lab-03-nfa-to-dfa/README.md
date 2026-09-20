# Lab 03 — NFA to DFA (Subset Construction)

Convert nondeterministic automata to deterministic ones via the powerset construction.

## 1. Theory

- An **NFA** adds choice: from `(q, a)` there can be 0..n successors, plus **epsilon moves** (no input consumed). An NFA accepts if *some* path consumes the input and ends in `F`.
- **Epsilon-closure** `E(S)`: all states reachable from `S` using only epsilon moves.
- **Subset construction:** DFA states are *sets* of NFA states. Start = `E({q0})`; `D(S,a) = E(move(S,a))`. Accept iff the set contains an NFA accept state. Worst case 2^n DFA states, often far fewer reachable in practice.
- Consequence: NFA ≡ DFA in power (both = regular languages); NFA is just exponentially more concise for some languages.

## 2. Project layout

```
lab-03-nfa-to-dfa/
  README.md
  nfa_to_dfa.py   # NFA class, epsilon-closure, subset construction, demo NFA for (a|b)*abb
```

## 3. Run

```bash
cd lab-03-nfa-to-dfa
python3 nfa_to_dfa.py
```

## 4. Verify

1. `python3 -m py_compile nfa_to_dfa.py` succeeds.
2. `python3 nfa_to_dfa.py` prints the DFA state count and `ALL SELF-CHECKS PASSED`.
3. The NFA and the constructed DFA agree on a brute-force sweep of all strings up to length 6.

## 5. Tasks

1. Add epsilon transitions to the demo NFA (e.g. optional `a`) and re-run the agreement sweep.
2. Implement DFA minimization (table-filling / Hopcroft lite) and report states before/after.
3. Build an NFA for `(a|b)*a(a|b){2}` via Thompson-style helpers and convert it.
4. Measure reachable DFA states vs the 2^n bound for n = 3,4,5 on a family of your choice.
5. Show an NFA where the minimal DFA really is exponentially bigger (or argue why one from theory qualifies).
