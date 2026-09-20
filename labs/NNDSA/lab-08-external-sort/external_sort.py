"""Lab 08 — External sort: chunk sort + k-way merge. Run: python3 external_sort.py [--total N --chunk C --seed S]"""
import argparse, heapq, os, random, sys, tempfile

def gen(n, seed=1):
    rng = random.Random(seed)
    return [rng.randint(0, 10 * n) for _ in range(n)]

def write_runs(data, chunk, tmp):
    runs = []
    for i in range(0, len(data), chunk):
        run = sorted(data[i:i + chunk])
        p = os.path.join(tmp, f"run_{len(runs):03d}.txt")
        with open(p, "w") as f:
            f.write("\n".join(map(str, run)) + "\n")
        runs.append(p)
    return runs

def k_way_merge(run_files, out_path):
    """TODO(2): buffer I/O in blocks of B lines and count block reads."""
    fps = [open(p) for p in run_files]
    heap = []
    for i, fp in enumerate(fps):
        line = fp.readline()
        if line: heapq.heappush(heap, (int(line), i))
    n = 0
    with open(out_path, "w") as out:
        while heap:
            v, i = heapq.heappop(heap)
            out.write(f"{v}\n"); n += 1
            line = fps[i].readline()
            if line: heapq.heappush(heap, (int(line), i))
    for fp in fps: fp.close()
    return n

def external_sort(data, chunk):
    with tempfile.TemporaryDirectory() as tmp:
        runs = write_runs(data, chunk, tmp)
        print(f"phase1: {len(data)} items -> {len(runs)} sorted runs (chunk={chunk})")
        out = os.path.join(tmp, "sorted.txt")
        k_way_merge(runs, out)
        with open(out) as f:
            return [int(x) for x in f.read().split()]

def _check(c, m):
    if not c: raise AssertionError(m)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--total", type=int, default=5000)
    ap.add_argument("--chunk", type=int, default=500)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    data = gen(a.total, a.seed)
    got = external_sort(data, a.chunk)
    _check(got == sorted(data), "external sort mismatch")
    _check(len(got) == a.total, "lost items")
    print(f"phase2: k-way merged {a.total} items OK; head={got[:5]}")
    # small deterministic edge cases
    _check(external_sort([], 10) == [], "empty")
    _check(external_sort([3, 1, 2, 1], 2) == [1, 1, 2, 3], "duplicates")
    print("ALL SELF-CHECKS PASSED")

if __name__ == "__main__":
    main()
