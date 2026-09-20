# Lab 03 — Trie (Prefix Tree)

A character tree for autocomplete, spell-check prefixes, and counting words with a prefix.

## 1. Theory

- A **trie** stores keys character by character; each node = one prefix. Insert/search/delete cost O(L) in key length, independent of dictionary size.
- Nodes carry `children` (dict char -> node), `is_word`, and optionally `count` (words in subtree) for prefix counting and autocomplete ranking.
- Trade-off vs hash set: trie supports prefix queries (`starts_with`, autocomplete) but uses more memory (one node per distinct prefix). Compress chains -> radix/Patricia tree.

## 2. Project layout

```
lab-03-trie/
  README.md
  trie.py   # Trie with insert/search/starts_with/autocomplete + self-checks
```

## 3. Run

```bash
cd lab-03-trie
python3 trie.py
```

## 4. Verify

1. `python3 -m py_compile trie.py` succeeds.
2. `python3 trie.py` prints autocomplete suggestions and `ALL SELF-CHECKS PASSED`.
3. `starts_with("app")` returns all inserted `app*` words.

## 5. Tasks

1. Implement `delete(word)` (unmark + prune dead nodes); test deleting a prefix of another word.
2. Add `count_prefix(p)` using subtree counts maintained on insert.
3. Implement wildcard search `search("c.t")` (`.` = any char).
4. Add top-k autocomplete ordered by inserted frequency.
5. Compare memory/time of trie vs `set` for 10k random words; note results in a comment.
