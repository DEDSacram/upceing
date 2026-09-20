"""Lab 03 — NFA to DFA subset construction. Run: python3 nfa_to_dfa.py"""
from __future__ import annotations
from itertools import product


class NFA:
    def __init__(self, states, alphabet, start, accepts):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.start = start
        self.accept_states = set(accepts)
        self.trans = {}   # (q, symbol|None) -> set of states; None = epsilon
        for q in self.states:
            for a in list(self.alphabet) + [None]:
                self.trans.setdefault((q, a), set())

    def add(self, q, sym, r):
        self.trans.setdefault((q, sym), set()).add(r)

    def epsilon_closure(self, states):
        stack, out = list(states), set(states)
        while stack:
            q = stack.pop()
            for r in self.trans.get((q, None), ()):
                if r not in out:
                    out.add(r)
                    stack.append(r)
        return frozenset(out)

    def move(self, states, sym):
        out = set()
        for q in states:
            out |= self.trans.get((q, sym), set())
        return frozenset(out)

    def accepts(self, s):
        cur = self.epsilon_closure({self.start})
        for ch in s:
            cur = self.epsilon_closure(self.move(cur, ch))
        return bool(cur & self.accept_states)


def subset_construction(nfa):
    """Return (dfa_states, dfa_delta, dfa_start, dfa_accepts) over frozensets."""
    start = nfa.epsilon_closure({nfa.start})
    states, delta, queue = {start}, {}, [start]
    while queue:
        S = queue.pop()
        for a in nfa.alphabet:
            T = nfa.epsilon_closure(nfa.move(S, a))
            delta[(S, a)] = T
            if T not in states:
                states.add(T)
                queue.append(T)
    accepts = {S for S in states if S & nfa.accept_states}
    return states, delta, start, accepts


def demo_nfa_ends_abb():
    """NFA for (a|b)*abb: guess the last three symbols."""
    n = NFA({0, 1, 2, 3}, {"a", "b"}, 0, {3})
    n.add(0, "a", 0); n.add(0, "b", 0)
    n.add(0, "a", 1); n.add(1, "b", 2); n.add(2, "b", 3)
    return n


def run_dfa(states_delta_start_accepts, s):
    _, delta, start, accepts = states_delta_start_accepts
    cur = start
    for ch in s:
        cur = delta[(cur, ch)]
    return cur in accepts


def _check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    nfa = demo_nfa_ends_abb()
    dfa = subset_construction(nfa)
    states, _, _, _ = dfa
    print(f"NFA states=4, reachable DFA states={len(states)}")
    for s in ["abb", "aabb", "babb", "ab", "abbb", ""]:
        _check(nfa.accepts(s) == run_dfa(dfa, s), f"agree on {s!r}")
        _check(nfa.accepts(s) == s.endswith("abb"), f"language on {s!r}")
    for tup in product("ab", repeat=5):
        s = "".join(tup)
        _check(nfa.accepts(s) == run_dfa(dfa, s), f"sweep mismatch {s!r}")
    print("ALL SELF-CHECKS PASSED")


if __name__ == "__main__":
    main()
