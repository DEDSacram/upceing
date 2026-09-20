"""Lab 05 — AVL tree. Run: python3 avl.py"""
import math

class N:
    __slots__ = ("k", "l", "r", "h")
    def __init__(self, k): self.k, self.l, self.r, self.h = k, None, None, 1

def _h(n): return n.h if n else 0
def _upd(n): n.h = 1 + max(_h(n.l), _h(n.r))
def _bf(n): return _h(n.l) - _h(n.r)
def _rotR(y):
    x = y.l; y.l = x.r; x.r = y; _upd(y); _upd(x); return x
def _rotL(x):
    y = x.r; x.r = y.l; y.l = x; _upd(x); _upd(y); return y
def _bal(n):
    _upd(n); b = _bf(n)
    if b > 1:
        if _bf(n.l) < 0: n.l = _rotL(n.l)
        return _rotR(n)
    if b < -1:
        if _bf(n.r) > 0: n.r = _rotR(n.r)
        return _rotL(n)
    return n

class AVL:
    def __init__(self): self.root = None
    def insert(self, k): self.root = self._ins(self.root, k)
    def _ins(self, n, k):
        if not n: return N(k)
        if k < n.k: n.l = self._ins(n.l, k)
        elif k > n.k: n.r = self._ins(n.r, k)
        else: return n
        return _bal(n)
    def search(self, k):
        n = self.root
        while n:
            if k == n.k: return True
            n = n.l if k < n.k else n.r
        return False
    def delete(self, k): self.root = self._del(self.root, k)
    def _del(self, n, k):
        if not n: return None
        if k < n.k: n.l = self._del(n.l, k)
        elif k > n.k: n.r = self._del(n.r, k)
        else:
            if not n.l: return n.r
            if not n.r: return n.l
            # TODO(1): two-children via successor swap:
            m = n.r
            while m.l: m = m.l
            n.k = m.k; n.r = self._del(n.r, m.k)
        return _bal(n) if n else None
    def inorder(self):
        out = []
        def dfs(n):
            if n: dfs(n.l); out.append(n.k); dfs(n.r)
        dfs(self.root); return out

def check(n, lo=-float("inf"), hi=float("inf")):
    if not n: return True, 0
    assert lo < n.k < hi, f"BST violated at {n.k}"
    okl, hl = check(n.l, lo, n.k); okr, hr = check(n.r, n.k, hi)
    assert abs(hl - hr) <= 1, f"AVL violated at {n.k}"
    assert n.h == 1 + max(hl, hr), f"height stale at {n.k}"
    return okl and okr, n.h

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    t = AVL()
    for x in [10, 4, 15, 2, 7, 12, 20, 1, 3, 6, 8]:
        t.insert(x)
    _check(t.inorder() == sorted([10, 4, 15, 2, 7, 12, 20, 1, 3, 6, 8]), "inorder")
    _check(t.search(7) and not t.search(99), "search")
    check(t.root)
    t.delete(4); t.delete(15)
    _check(t.inorder() == sorted(set([10, 4, 15, 2, 7, 12, 20, 1, 3, 6, 8]) - {4, 15}), "delete")
    check(t.root)
    big = AVL()
    for x in range(1, 1001): big.insert(x)
    bound = 1.44 * math.log2(1001) + 2
    print(f"n=1000 height={big.root.h} bound~{bound:.1f}")
    _check(big.root.h <= bound, "AVL height bound")
    print("inorder head:", t.inorder()[:5], "height:", t.root.h)
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
