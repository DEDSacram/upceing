# Lab 08 — External Sort (k-Way Merge of Chunk Files)

Sort data bigger than RAM: sort chunks, then k-way merge with a heap.

## 1. Theory

- **External merge sort:** split input into memory-sized chunks, sort each in RAM (Timsort), spill runs to files, then **k-way merge** with a min-heap over run heads: O(N log N) comparisons, O(N/B) block I/Os.
- Heap holds one head element per run (k entries) → merge in O(N log k). Fewer, larger runs beat many tiny ones; a tournament tree / buffered I/O is the production refinement.
- Demo uses small chunk sizes on purpose so the multi-phase flow is visible; raise `--total/--chunk` for a real scale test.

## 2. Project layout

```
lab-08-external-sort/
  README.md
  external_sort.py   # chunk sort + k-way merge + end-to-end self-check (stdlib, tmp files)
```

## 3. Run

```bash
cd lab-08-external-sort
python3 external_sort.py
python3 external_sort.py --total 20000 --chunk 2000 --seed 7
```

## 4. Verify

1. `python3 -m py_compile external_sort.py` succeeds.
2. `python3 external_sort.py` prints phases (runs, merge) and `ALL SELF-CHECKS PASSED`.
3. Output equals `sorted(input)` on the generated data; temp chunk files are cleaned up.

## 5. Tasks

1. Add replacement selection for longer initial runs; measure run-count change.
2. Merge with bounded memory: read/write buffered in blocks of B lines (count I/Os).
3. Support duplicate-heavy data; verify stability requirement (or document instability).
4. Parallelize chunk sorting with `concurrent.futures` and time the speedup.
5. Sort a file larger than your RAM (e.g. 2× RAM with small `--chunk`) and record wall time.
