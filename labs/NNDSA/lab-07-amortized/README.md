# Lab 07 — Amortized Analysis (Dynamic Array Timing)

Doubling a full array costs O(1) *amortized* per append — measure it.

## 1. Theory

- **Aggregate method:** n appends with doubling trigger resizes of size 1,2,4,...,n; total copy cost ≤ 2n, so amortized O(1) per op even though one append costs O(n).
- Contrast: growing by a constant (+k) copies O(n²/k) total → O(n) amortized. The growth *factor* is what matters.
- Experiment: instrument a `DynArray` (copies counter) and time `append` for n = 200k under growth factors 1.25×, 2×, +1000. Copies/op and wall time both tell the story.

## 2. Project layout

```
lab-07-amortized/
  README.md
  amortized.py   # DynArray with pluggable growth + timing table (stdlib only)
```

## 3. Run

```bash
cd lab-07-amortized
python3 amortized.py
```

## 4. Verify

1. `python3 -m py_compile amortized.py` succeeds.
2. `python3 amortized.py` prints copies/append ≈ small constant for doubling and `ALL SELF-CHECKS PASSED`.
3. Doubling beats +1000 growth clearly in the copies/append column.

## 5. Tasks

1. Add shrink-on-remove (halve at 1/4 full) and show hysteresis prevents thrash.
2. Plot copies/append vs n as ASCII bars.
3. Prove the 2n total-copy bound in a comment (geometric series).
4. Try factor 1.5× (CPython-like over-allocate) vs 2×; record time/memory trade-off.
5. Show the +1-growth quadratic blowup for n = 20k (copies/append ≈ n/2).
