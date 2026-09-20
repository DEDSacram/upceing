"""Lab 03 — Trie. Run: python3 trie.py"""

class _N:
    __slots__ = ("kids", "word", "freq")
    def __init__(self): self.kids, self.word, self.freq = {}, False, 0

class Trie:
    def __init__(self): self.root = _N()

    def insert(self, w, count=1):
        n = self.root
        for c in w:
            n = n.kids.setdefault(c, _N())
        n.word = True; n.freq += count

    def search(self, w):
        n = self.root
        for c in w:
            n = n.kids.get(c)
            if n is None: return False
        return n.word

    def starts_with(self, pref):
        n = self.root
        for c in pref:
            n = n.kids.get(c)
            if n is None: return []
        out = []
        def dfs(node, cur):
            if node.word: out.append(cur)
            for c, k in sorted(node.kids.items()): dfs(k, cur + c)
        dfs(n, pref)
        return out

    def autocomplete(self, pref, k=5):
        """TODO(4): rank by frequency; currently alphabetical first-k."""
        return self.starts_with(pref)[:k]

    def delete(self, w):
        """TODO(1): unmark + prune. Returns True if word existed."""
        path = []; n = self.root
        for c in w:
            if c not in n.kids: return False
            path.append((n, c)); n = n.kids[c]
        if not n.word: return False
        n.word = False; n.freq = 0
        for parent, c in reversed(path):
            kid = parent.kids[c]
            if kid.kids or kid.word: break
            del parent.kids[c]
        return True

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    t = Trie()
    for w in ["app", "apple", "apply", "apt", "bat", "batch"]:
        t.insert(w)
    _check(t.search("app") and not t.search("ap"), "search")
    _check(t.starts_with("app") == ["app", "apple", "apply"], f"prefix: {t.starts_with('app')}")
    _check(t.autocomplete("ap", 2) == ["app", "apple"], "autocomplete")
    _check(t.delete("apple") and not t.search("apple") and t.search("app"), "delete keeps prefix")
    _check(t.starts_with("app") == ["app", "apply"], "prefix after delete")
    print("autocomplete('bat'):", t.autocomplete("bat"))
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
