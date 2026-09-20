# Lab 06 — B-tree (In-Memory)

A multiway balanced search tree: the structure behind database indexes and filesystems.

## 1. Theory

- A **B-tree** of minimum degree `t` keeps  t-1..2t-1 keys per node (root: 1..2t-1) and all leaves at equal depth. Het.
- **Search** is linear-in-node (or binary) descent, O(log n) node visits. **Insert** splits full nodes top-down on the way (`split_child`), so recursion never backtracks. **Delete** borrows/merges to keep nodes ≥ t-1 keys (this lab: delete scaf-folded as TODO with a working simple path).
- Node size ≈ disk page: one node = one I/O. Large fan-out keeps the tree shallow (3 levels hold millions of keys).

## 2. Project layout

```
lab-06-btree/
  README.md
  btree.py   # BTree(t) with insert/search + traversal + self-checks
```

## 3. Run

```bash
cd lab-06-btree
python3 btree.py
```

## 4. Verify

1. `python3 -m py_compile btree.py` succeeds.
2. `python3 btree.py` prints sorted traversal and `ALL SELF-CHECKS PASSED`.
3. All 200 inserted keys are found; inorder output is sorted.

## 5. Tasks

1. Finish full `delete` (borrow from sibling / merge) and test with randomized op sequences vs `set`.
2. Add `range_query(lo, hi)` (sorted list of keys in interval).
3. Count node visits for search hits vs misses; show shallowness for n = 100k.
4. Parameter sweep: compare height for t = 2, 8, 32 on the same key set.
5. Persist nodes to files (one file per node id) to mimic disk pages; measure I/Os per op.
