"""Lab 05 — PDA simulator for balanced parentheses. Run: python3 pda.py [--trace EXPR]"""
import sys


class PDA:
    """Deterministic PDA for balanced parens over {(,)} with bottom marker Z."""

    def __init__(self):
        self.bottom = "Z"

    def run(self, s, trace=False):
        stack = [self.bottom]
        depth, max_depth = 0, 0
        for i, ch in enumerate(s):
            if ch == "(":
                stack.append("(")
                depth += 1
                max_depth = max(max_depth, depth)
            elif ch == ")":
                if stack[-1] != "(":
                    if trace:
                        print(f"step {i}: reject ')' with top {stack[-1]!r}")
                    return False
                stack.pop()
                depth -= 1
            else:
                if trace:
                    print(f"step {i}: illegal symbol {ch!r}")
                return False
            if trace:
                print(f"step {i}: read {ch!r} stack={''.join(stack)}")
        ok = len(stack) == 1
        if trace:
            print(f"end: stack={''.join(stack)} accept={ok} max_depth={max_depth}")
        return ok


def _check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    pda = PDA()
    if len(sys.argv) == 3 and sys.argv[1] == "--trace":
        print("accept:", pda.run(sys.argv[2], trace=True))
        return
    cases = {"": True, "()": True, "(())": True, "()()": True,
             "(()())": True, "(": False, ")": False, ")(": False, "(()": False}
    for s, want in cases.items():
        got = pda.run(s)
        _check(got == want, f"PDA({s!r})={got}, want {want}")
        print(f"{'ACCEPT' if got else 'REJECT':6} {s!r}")
    print("ALL SELF-CHECKS PASSED")


if __name__ == "__main__":
    main()
