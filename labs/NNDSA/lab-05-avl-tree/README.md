# Lab 05 — AVL Tree

A self-balancing BST: O(log n) insert/search/delete via rotations.

## 1. Theory

- **BST invariant:** left subtree keys < node < right subtree keys. Degenerates to O(n) if keys arrive sorted.
- **AVL invariant:** balance factor `bf = height(L) - height(R)` in `{-1, 0, +1}` at every node. Violation after insert/delete is fixed with rotations: LL -> right rotate, RR -> left rotate, LR/RL -> double rotate.
- Heights are stored per node and updated bottom-up; each op costs O(log n) with ≤ 2 rotations on insert.
- Check both the BST order and the bf invariant in tests — one without the other hides bugs.

## 2. Project layout

```
lab-05-avl-tree/
  README.md
  avl.py   # AVL with insert/delete/search + invariant checker
```

## 3. Run

```bash
cd lab-05-avl-tree
python3 avl.py
```

## 4. Verify

1. `python3 -m py_compile avl.py` succeeds.
2. `python3 avl.py` prints inorder traversal, height, and `ALL SELF-CHECKS PASSED`.
3. Inserting 1..1000 keeps height ≤ ~1.44·log2(n) (printed).

## 5. Tasks

1. Implement `delete(key)` for the two-children case via successor swap (scaffold present).
2. Add `kth_smallest(k)` using subtree sizes.
3. Add `rank(key)` (count of keys < key).
4. Compare height vs an unbalanced BST on sorted input 1..500.
5. Make `search` iterative and count comparisons vs expected log2(n).
