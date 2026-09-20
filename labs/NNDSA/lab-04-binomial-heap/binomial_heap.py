"""Lab 04 — Simplified binomial heap. Run: python3 binomial_heap.py"""

class _Tree:
    __slots__ = ("key", "order", "kids")
    def __init__(self, key): self.key, self.order, self.kids = key, 0, []
    def link(self, other):  # min-heap link
        if other.key < self.key: return other.link(self)
        self.kids.append(other); self.order += 1
        return self

class BinomialHeap:
    def __init__(self): self.trees = []  # order -> _Tree|None

    def _add_tree(self, t):
        o = t.order
        while o < len(self.trees) and self.trees[o] is not None:
            t = t.link(self.trees[o]); self.trees[o] = None; o += 1
        while len(self.trees) <= o: self.trees.append(None)
        self.trees[o] = t

    def push(self, key):
        self._add_tree(_Tree(key))

    def merge(self, other):
        """Meld other into self (other emptied)."""
        for t in other.trees:
            if t is not None: self._add_tree(t)
        other.trees = []

    def peek(self):
        ks = [t.key for t in self.trees if t]
        return min(ks) if ks else None

    def pop(self):
        idx = min((i for i, t in enumerate(self.trees) if t),
                  key=lambda i: self.trees[i].key, default=None)
        if idx is None: raise IndexError("pop from empty heap")
        t = self.trees[idx]; self.trees[idx] = None
        for k in t.kids: self._add_tree(k)  # children orders distinct -> meld back
        return t.key

    def __len__(self):
        return sum(2 ** t.order for t in self.trees if t)

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    h = BinomialHeap()
    for x in [5, 1, 9, 3, 7, 2]: h.push(x)
    _check(h.peek() == 1, "peek")
    _check(len(h) == 6, "size")
    a, b = BinomialHeap(), BinomialHeap()
    for x in [8, 4]: a.push(x)
    for x in [6, 0]: b.push(x)
    a.merge(b)
    _check(len(b) == 0 and len(a) == 4, "merge empties other")
    got = [a.pop() for _ in range(4)]
    _check(got == [0, 4, 6, 8], f"merge order {got}")
    got = [h.pop() for _ in range(6)]
    _check(got == sorted([5, 1, 9, 3, 7, 2]), f"pop order {got}")
    try:
        BinomialHeap().pop(); _check(False, "empty pop should raise")
    except IndexError: pass
    print("pop order:", got)
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
