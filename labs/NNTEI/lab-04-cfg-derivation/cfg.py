"""Lab 04 — CFG derivation, trees, CNF check. Run: python3 cfg.py"""
from __future__ import annotations


class Grammar:
    def __init__(self, variables, terminals, rules, start):
        self.V = set(variables)
        self.T = set(terminals)
        self.rules = list(rules)  # (lhs, rhs_tuple)
        self.start = start

    def leftmost_derive(self, target, max_steps=50):
        """BFS for a leftmost derivation of `target` (list of sentential forms)."""
        start = ([self.start], [f"start: {self.start}"])
        queue = [start]
        while queue:
            form, hist = queue.pop(0)
            if all(s in self.T for s in form):
                if "".join(form) == target:
                    return hist + [f"yield: {target}"]
                continue
            if len(hist) > max_steps:
                continue
            i = next(k for k, s in enumerate(form) if s in self.V)
            for lhs, rhs in self.rules:
                if lhs == form[i]:
                    new = form[:i] + list(rhs) + form[i + 1:]
                    queue.append((new, hist + [f"{lhs} -> {''.join(rhs) or 'e'}  :: {''.join(new)}"]))
        return None

    def derivation_tree(self, target):
        """Return an ASCII tree of one leftmost derivation (naive: reuse BFS parents)."""
        # Simple approach: derive then nest by re-parsing with rules is overkill;
        # we pretty-print the sentential-form chain as an indented tree sketch.
        hist = self.leftmost_derive(target)
        if hist is None:
            return f"<no derivation for {target!r}>"
        return "\n".join(("  " * min(k, 6) + h) for k, h in enumerate(hist))

    def is_cnf(self):
        """Check Chomsky Normal Form. Returns (ok, reasons)."""
        reasons = []
        for lhs, rhs in self.rules:
            if len(rhs) == 1 and rhs[0] in self.T:
                continue
            if len(rhs) == 2 and all(s in self.V for s in rhs):
                continue
            if lhs == self.start and len(rhs) == 0:
                continue
            reasons.append(f"rule {lhs} -> {''.join(rhs) or 'e'} violates CNF")
        return (not reasons), reasons


def balanced_parens_grammar():
    V, T, S = {"S"}, {"(", ")"}, "S"
    rules = [("S", ("(", "S", ")")), ("S", ("S", "S")), ("S", ())]
    return Grammar(V, T, rules, S)


def cnf_sample_grammar():
    V, T, S = {"S", "A", "B"}, {"a", "b"}, "S"
    return Grammar(V, T, [("S", ("A", "B")), ("A", ("a",)), ("B", ("b",))], S)


def _check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    g = balanced_parens_grammar()
    hist = g.leftmost_derive("(())")
    _check(hist is not None, "no derivation for (())")
    print("\n".join(hist[:6]))
    print("--- tree sketch ---")
    print(g.derivation_tree("(())"))
    ok, _ = g.is_cnf()
    _check(not ok, "parens grammar with S->SS should not be CNF")
    ok2, _ = cnf_sample_grammar().is_cnf()
    _check(ok2, "S->AB sample should be CNF")
    print("ALL SELF-CHECKS PASSED")


if __name__ == "__main__":
    main()
