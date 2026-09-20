"""Lab 06 — In-memory B-tree. Run: python3 btree.py"""

class Node:
    def __init__(self, leaf=True):
        self.keys = []; self.kids = []; self.leaf = leaf

class BTree:
    def __init__(self, t=3):
        assert t >= 2
        self.t, self.root = t, Node()

    def search(self, k, n=None):
        n = n or self.root
        i = 0
        while i < len(n.keys) and k > n.keys[i]: i += 1
        if i < len(n.keys) and k == n.keys[i]: return True
        return False if n.leaf else self.search(k, n.kids[i])

    def _split(self, p, i):
        t = self.t; full = p.kids[i]
        mid = full.keys[t - 1]
        right = Node(leaf=full.leaf)
        right.keys = full.keys[t:]
        full.keys = full.keys[:t - 1]
        if not full.leaf:
            right.kids = full.kids[t:]; full.kids = full.kids[:t]
        p.kids.insert(i + 1, right); p.keys.insert(i, mid)

    def insert(self, k):
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            nr = Node(leaf=False); nr.kids = [r]; self.root = nr
            self._split(nr, 0)
        self._ins(self.root, k)

    def _ins(self, n, k):
        if k in n.keys: return
        if n.leaf:
            i = 0
            while i < len(n.keys) and n.keys[i] < k: i += 1
            n.keys.insert(i, k)
            return
        i = len(n.keys)
        while i > 0 and k < n.keys[i - 1]: i -= 1
        if len(n.kids[i].keys) == 2 * self.t - 1:
            self._split(n, i)
            if k > n.keys[i]: i += 1
        self._ins(n.kids[i], k)

    def inorder(self):
        out = []
        def dfs(n):
            for i, k in enumerate(n.keys):
                if not n.leaf: dfs(n.kids[i])
                out.append(k)
            if not n.leaf: dfs(n.kids[-1])
        dfs(self.root); return out

    def height(self):
        h, n = 0, self.root
        while True:
            h += 1
            if n.leaf: return h
            n = n.kids[0]

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    bt = BTree(t=3)
    keys = [(7 * i + 3) % 200 for i in range(200)]
    for k in keys: bt.insert(k)
    want = sorted(set(keys))
    _check(bt.inorder() == want, "inorder sorted")
    for k in want: _check(bt.search(k), f"missing {k}")
    _check(not bt.search(10 ** 9), "phantom found")
    print(f"n={len(want)} height={bt.height()} (expect <= 4 for t=3)")
    _check(bt.height() <= 5, "too deep")
    print("inorder head:", bt.inorder()[:8])
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
