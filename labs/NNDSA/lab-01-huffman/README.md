# Lab 01 — Huffman Coding (Encode/Decode)

Optimal prefix codes via greedy bottom-up merging: frequent symbols get short codes.

## 1. Theory

- A **prefix code** assigns bit strings so no code is a prefix of another — decodable left-to-right with a binary tree (left = 0, right = 1).
- **Huffman algorithm:** repeatedly merge the two lowest-frequency nodes (priority queue, O(n log n)); the merged weight is the sum. Result minimizes expected code length `sum(p_i * len_i)` among all prefix codes (optimal for symbol-by-symbol coding).
- **Entropy bound:** `H <= L < H + 1` for the optimal prefix code (H = Shannon entropy in bits). Compression ratio depends on skew of frequencies.
- Encode = table lookup per symbol; decode = walk tree per bit. Store the code table (or tree) alongside the payload.

## 2. Project layout

```
lab-01-huffman/
  README.md
  huffman.py   # tree build, encode/decode, round-trip self-checks (stdlib only)
```

## 3. Run

```bash
cd lab-01-huffman
python3 huffman.py
```

## 4. Verify

1. `python3 -m py_compile huffman.py` succeeds.
2. `python3 huffman.py` prints code table, bit counts, and `ALL SELF-CHECKS PASSED`.
3. Round-trip `decode(encode(s)) == s` holds for all sample strings.

## 5. Tasks

1. Handle the single-symbol edge case (assign code `"0"`); add a test.
2. Report compression ratio vs fixed 8-bit encoding on a skewed input.
3. Compare Huffman length against entropy `H` on the sample frequencies.
4. Implement canonical Huffman codes from code lengths; verify decode still works.
5. Encode a real text file given on the command line and print before/after bit counts.
