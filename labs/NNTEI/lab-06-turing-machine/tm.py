"""Lab 06 — Turing machine simulator + unary adder. Run: python3 tm.py"""
from __future__ import annotations

L, R = "L", "R"


class TM:
    def __init__(self, transitions, start, accept, reject, blank="_"):
        self.d = dict(transitions)  # (q, sym) -> (q2, write, move)
        self.start, self.accept, self.reject, self.blank = start, accept, reject, blank

    def run(self, tape_str, max_steps=100_000):
        tape = {i: ch for i, ch in enumerate(tape_str)}
        q, head, steps = self.start, 0, 0
        while steps < max_steps:
            if q == self.accept:
                return ("ACCEPT", self._dump(tape), steps)
            if q == self.reject:
                return ("REJECT", self._dump(tape), steps)
            sym = tape.get(head, self.blank)
            key = (q, sym)
            if key not in self.d:
                return ("REJECT", self._dump(tape), steps)
            q, write, move = self.d[key]
            tape[head] = write
            head += 1 if move == R else -1
            steps += 1
        return ("TIMEOUT", self._dump(tape), steps)

    def _dump(self, tape):
        cells = [k for k, v in tape.items() if v != self.blank]
        if not cells:
            return ""
        lo, hi = min(cells), max(cells)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1))


def unary_adder():
    """Adds 1^n + 1^m -> 1^(n+m). States: scan, carry/return, cleanup."""
    d = {}
    d[("q0", "1")] = ("q0", "1", R)
    d[("q0", "+")] = ("q1", "1", R)   # turn + into 1 ...
    d[("q1", "1")] = ("q1", "1", R)
    d[("q1", "_")] = ("q2", "_", L)   # ... then erase one 1 at the end
    d[("q2", "1")] = ("qa", "_", R)
    return TM(d, "q0", "qa", "qr")


def _check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    tm = unary_adder()
    for tape_in, want in [("111+11", "11111"), ("1+1", "11"), ("111+1", "1111")]:
        status, out, steps = tm.run(tape_in)
        _check(status == "ACCEPT" and out == want, f"{tape_in} -> {out} ({status})")
        print(f"{tape_in:10} -> {out:10} steps={steps}")
    print("--- scaling (linear check) ---")
    for n in (5, 10, 20, 40):
        _, _, steps = tm.run("1" * n + "+" + "1" * n)
        print(f"n={n:3} steps={steps}")
    print("ALL SELF-CHECKS PASSED")


if __name__ == "__main__":
    main()
