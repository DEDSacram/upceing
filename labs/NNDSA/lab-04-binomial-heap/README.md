# Lab 04 — Binomial Heap (Simplified)

A mergeable priority queue: insert/push fast, meld two heaps in O(log n).

## 1. Theory

- A **binomial heap** is a forest of binomial trees `B_k` (2^k nodes), at most one tree per order — like binary digits of n. Min-heap order within each tree.
- **Insert** = meld a single-node heap: O(log n) amortized O(1). **Meld** = binary addition of tree lists with carry: O(log n). **Extract-min** = remove min root, meld its children back: O(log n).
- This lab's simplified version keeps the meldable forest + lazy `push/pop/merge`; decrease-key is a TODO.
- Use when: merging queues often (Dijkstra variants, event simulation) — binary heaps meld in O(n).

## 2. Project layout

```
lab-04-binomial-heap/
  README.md
  binomial_heap.py   # BinomialHeap with push/pop/peek/merge + self-checks
```

## 3. Run

```bash
cd lab-04-binomial-heap
python3 binomial_heap.py
```

## 4. Verify

1. `python3 -m py_compile binomial_heap.py` succeeds.
2. `python3 binomial_heap.py` prints sorted extraction and `ALL SELF-CHECKS PASSED`.
3. Merging two heaps yields the same pop order as one combined heap.

## 5. Tasks

1. Implement `decrease_key(handle, new_val)` (needs node handles from push).
2. Add `delete(handle)` via decrease-key + extract-min.
3. Verify O(log n) shape: assert tree orders are distinct after random inserts.
4. Benchmark push/pop vs `heapq` for n = 50k; record in a comment.
5. Implement `union` that reuses (moves) nodes instead of copying keys.
