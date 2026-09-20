"""Lab 02 — DFA simulator + scanner example. Run: python3 dfa.py"""
from __future__ import annotations


class DFA:
    """Deterministic finite automaton with total transition function."""

    def __init__(self, states, alphabet, delta, start, accepts):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.delta = dict(delta)  # (state, symbol) -> state
        self.start = start
        self.accepts = set(accepts)

    def run(self, s):
        """Return end state; raise ValueError on unknown symbol."""
        q = self.start
        for ch in s:
            if ch not in self.alphabet:
                raise ValueError(f"symbol {ch!r} not in alphabet")
            q = self.delta[(q, ch)]
        return q

    def accepts_input(self, s):
        return self.run(s) in self.accepts

    def complement(self):
        """TODO(2): return DFA with flipped accept set (same transition graph)."""
        return DFA(self.states, self.alphabet, self.delta, self.start,
                   self.states - self.accepts)


def even_zeros_dfa():
    # States: E (even zeros seen), O (odd). Alphabet {0,1}.
    delta = {("E", "0"): "O", ("E", "1"): "E",
             ("O", "0"): "E", ("O", "1"): "O"}
    return DFA({"E", "O"}, {"0", "1"}, delta, "E", {"E"})


def scan_ident_int(s):
    """Toy scanner: IDENT=[A-Za-z_][A-Za-z0-9_]*, INT=[0-9]+, skip whitespace.

    TODO(3): add FLOAT and STRING kinds.
    TODO(4): implement longest-match across kinds.
    """
    toks, i = [], 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c.isalpha() or c == "_":
            j = i
            while j < len(s) and (s[j].isalnum() or s[j] == "_"):
                j += 1
            toks.append(("IDENT", s[i:j]))
            i = j
        elif c.isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            toks.append(("INT", s[i:j]))
            i = j
        else:
            toks.append(("SYM", c))
            i += 1
    return toks


def _check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    d = even_zeros_dfa()
    _check(d.accepts_input(""), "empty has 0 zeros -> accept")
    _check(d.accepts_input("11"), "no zeros -> accept")
    _check(not d.accepts_input("0"), "one zero -> reject")
    _check(d.accepts_input("1010"), "two zeros -> accept")
    c = d.complement()
    _check(c.accepts_input("0") and not c.accepts_input(""), "complement")
    toks = scan_ident_int("x1 = 42 + y;")
    kinds = [k for k, _ in toks]
    _check(kinds[:3] == ["IDENT", "SYM", "INT"], f"scanner: {toks}")
    print("sample tokens:", toks)
    print("ALL SELF-CHECKS PASSED")


if __name__ == "__main__":
    main()
