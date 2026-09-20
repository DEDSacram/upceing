"""Lab 01 — Regex basics. Stdlib only. Run: python3 regex_basics.py"""
import re

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
INT = re.compile(r"[+-]?\d+")
FLOAT = re.compile(r"[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?")

TOKEN_SPEC = [
    ("NUMBER", r"\d+(?:\.\d+)?"),
    ("IDENT", r"[A-Za-z_]\w*"),
    ("OP", r"[+\-*/=();]"),
    ("SKIP", r"\s+"),
]


def is_email(s):
    """TODO(1): tighten/loosen this pattern, keep self-checks green."""
    return EMAIL.fullmatch(s) is not None


def find_numbers(s):
    """Return list of ints/floats found in s."""
    # TODO(5): extend to exponents via FLOAT; currently handles plain decimals.
    return [float(m.group(0)) if "." in m.group(0) else int(m.group(0))
            for m in re.finditer(r"[+-]?\d+(?:\.\d+)?", s)]


def tokenize(s):
    """Tiny tokenizer for identifiers/numbers/operators. Returns [(kind, text)]."""
    master = "|".join(f"(?P<{name}>{pat})" for name, pat in TOKEN_SPEC)
    out = []
    for m in re.finditer(master, s):
        kind = m.lastgroup
        if kind != "SKIP":
            out.append((kind, m.group()))
    return out


def _check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    _check(is_email("student@upce.cz"), "valid email rejected")
    _check(not is_email("a@b"), "short TLD accepted")
    _check(not is_email("@x.cz"), "missing local part accepted")
    _check(re.fullmatch(r"\d{3}-\d{3}-\d{3}", "123-456-789"), "phone pattern")
    _check(re.sub(r"\s+", " ", "a  b\t c") == "a b c", "sub collapse")
    m = re.match(r"(?P<y>\d{4})-(?P<m>\d{2})", "2026-09-20")
    _check(m and m.group("y") == "2026", "named group")
    _check("<a><b>" and re.findall(r"<.*?>", "<a><b>") == ["<a>", "<b>"], "lazy match")
    _check(re.findall(r"<.*>", "<a><b>") == ["<a><b>"], "greedy match")
    _check(find_numbers("n=-3, pi=3.14") == [-3, 3.14], "find_numbers")
    toks = tokenize("x = 12 + y2;")
    _check(toks[0] == ("IDENT", "x") and ("NUMBER", "12") in toks, f"tokenizer: {toks}")
    # Optional TODO exercises (uncomment as you implement):
    # from regex_basics import ...  # noqa
    print("ALL SELF-CHECKS PASSED")


if __name__ == "__main__":
    main()
