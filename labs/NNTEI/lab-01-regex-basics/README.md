# Lab 01 — Regex Basics (`re` module)

Hands-on regular expressions with Python's stdlib `re`: matching, groups, and a tiny tokenizer.

## 1. Theory

- A **regular expression** denotes a regular language: literals, concatenation, alternation (`|`), Kleene star (`*`), plus (`+`), option (`?`), character classes (`[0-9]`, `\d`, `\w`), anchors (`^`, `$`), and groups `(...)`.
- Python `re` functions: `re.match` (start of string), `re.search` (anywhere), `re.fullmatch` (whole string), `re.findall`/`re.finditer` (all matches), `re.sub` (replace).
- **Greedy vs lazy:** `.*` grabs as much as possible; `.*?` grabs as little as possible. Prefer explicit classes (`[^"]*`) for quoted strings.
- **Groups:** `(...)` captures; `(?:...)` is non-capturing; `(?P<name>...)` is named. Use raw strings `r"..."` so backslashes survive.
- Regexes recognize exactly the regular languages (= what a DFA can do) — Labs 02–03 build the automata underneath.

## 2. Project layout

```
lab-01-regex-basics/
  README.md
  regex_basics.py   # patterns + tokenizer + assert self-checks (stdlib only)
```

## 3. Run

```bash
cd lab-01-regex-basics
python3 regex_basics.py
```

## 4. Verify

1. `python3 -m py_compile regex_basics.py` succeeds.
2. `python3 regex_basics.py` prints `ALL SELF-CHECKS PASSED`.
3. `python3 -c "import re; print(re.fullmatch(r'[a-z]+@[a-z]+\.[a-z]{2,}', 'a@b.cz'))"` shows a match object.

## 5. Tasks

1. Extend `is_email()` to accept dots/pluses (`j.smith+tag@example.com`) without accepting `a@b` or `@x.cz`.
2. Write `is_ipv4()` (four 0–255 octets) and add 4 asserts.
3. Add a `STRING` token (`"..."` with escapes) to the tokenizer; handle `\"` correctly.
4. Compare greedy vs lazy on `"<a><b>"` with `<.*>` vs `<.*?>` and note the outputs.
5. Implement `find_numbers()` returning floats incl. negatives/exponents; add tests.
