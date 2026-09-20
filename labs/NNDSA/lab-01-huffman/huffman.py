"""Lab 01 — Huffman encode/decode. Stdlib only. Run: python3 huffman.py"""
import heapq, math
from collections import Counter

class Node:
    __slots__ = ("freq", "sym", "left", "right")
    def __init__(self, freq, sym=None, left=None, right=None):
        self.freq, self.sym, self.left, self.right = freq, sym, left, right
    def __lt__(self, other):
        return self.freq < other.freq

def build_tree(freq):
    pq = [Node(f, s) for s, f in freq.items()]
    heapq.heapify(pq)
    if len(pq) == 1:  # TODO(1): single-symbol edge — handled here with dummy sibling
        only = heapq.heappop(pq)
        return Node(only.freq, None, only, Node(0, None))
    while len(pq) > 1:
        a = heapq.heappop(pq); b = heapq.heappop(pq)
        heapq.heappush(pq, Node(a.freq + b.freq, None, a, b))
    return pq[0]

def build_codes(root):
    codes = {}
    def dfs(n, prefix):
        if n.sym is not None:
            codes[n.sym] = prefix or "0"
            return
        if n.left: dfs(n.left, prefix + "0")
        if n.right: dfs(n.right, prefix + "1")
    dfs(root, "")
    return codes

def encode(s, codes):
    return "".join(codes[c] for c in s)

def decode(bits, root):
    out, n = [], root
    for b in bits:
        n = n.left if b == "0" else n.right
        if n.sym is not None:
            out.append(n.sym); n = root
    return "".join(out)

def entropy(freq):
    tot = sum(freq.values())
    return -sum((f / tot) * math.log2(f / tot) for f in freq.values())

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    for s in ["hello world", "aaaaabbbcc", "x", "mississippi", ""]:
        if not s: continue
        freq = Counter(s)
        root = build_tree(freq)
        codes = build_codes(root)
        bits = encode(s, codes)
        _check(decode(bits, root) == s, f"round-trip failed for {s!r}")
    freq = Counter("aaaaabbbcc")
    H = entropy(freq)
    avg = sum(freq[c] * len(build_codes(build_tree(freq))[c]) for c in freq) / sum(freq.values())
    print("codes:", build_codes(build_tree(freq)))
    print(f"entropy={H:.3f} avg_len={avg:.3f} (expect H <= avg < H+1)")
    _check(H <= avg < H + 1, "entropy bound violated")
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
