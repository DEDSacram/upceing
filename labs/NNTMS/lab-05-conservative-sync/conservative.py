"""Two-LP conservative (CMB-style) sync demo with lookahead (stdlib only).

Setup: LP0 and LP1 each own a local arrival stream. 15% of LP0 completions
are cross-messages to LP1. LP1 may process its head event at time t only if
t <= safe_time, where safe_time = LP0's promised clock (last null message +
lookahead). Deliveries/nulls arrive in batches every BATCH LP0 completions.
--skew shifts LP1's busy period late so the conservative gate visibly blocks;
bigger lookahead -> further promise -> fewer blocked rounds.
"""
import argparse, heapq, random

BATCH = 10

def run(n_events=200, lookahead=0.5, seed=1, skew=150.0):
    rng = random.Random(seed)
    l0 = []
    t = 0.0
    for _ in range(n_events):
        t += rng.expovariate(1.0)
        l0.append(t)
    l1 = []
    t = skew
    for _ in range(n_events):
        t += rng.expovariate(1.2)
        l1.append(t)
    free, comp, cross = 0.0, [], []
    for i, a in enumerate(l0):
        free = max(a, free) + 0.5 + rng.expovariate(1.0)
        comp.append(free)
        if i % 7 == 0:
            cross.append((free, free + lookahead))  # (send_time, arrival)
    cross.sort()
    delivered_ptr = 0
    li = 0
    heap = [(x, "local") for x in l1]
    heapq.heapify(heap)
    done, blocked, violations, rounds = [], 0, 0, 0
    last = -1.0
    clock = 0.0
    while heap or delivered_ptr < len(cross):
        rounds += 1
        if li < len(comp):
            li = min(len(comp), li + BATCH)
            clock = comp[li - 1] if li else 0.0
        else:
            clock += max(lookahead, 0.05)  # idle LP0 null-message leap
        while delivered_ptr < len(cross) and cross[delivered_ptr][0] <= clock:
            heapq.heappush(heap, (cross[delivered_ptr][1], "cross"))
            delivered_ptr += 1
        safe = clock + lookahead
        progressed = False
        while heap and heap[0][0] <= safe + 1e-9:
            ts, kind = heapq.heappop(heap)
            if ts < last - 1e-9:
                violations += 1
            last = ts
            done.append((ts, kind))
            progressed = True
        if not progressed:
            blocked += 1  # LP1 idles waiting for LP0's next batch/null
        if rounds > 100000:
            raise RuntimeError("deadlock")
    print(f"events={n_events} lookahead={lookahead} skew={skew} processed={len(done)} "
          f"(local={sum(1 for _, k in done if k == 'local')} cross={sum(1 for _, k in done if k == 'cross')})")
    print(f"rounds={rounds} blocked_rounds={blocked} causality_violations={violations}")
    assert violations == 0 and len(done) == n_events + len(cross)
    print("OK: conservative run complete, no causality violations.")
    return blocked

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lookahead", type=float, default=0.5)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--events", type=int, default=200)
    ap.add_argument("--skew", type=float, default=150.0)
    a = ap.parse_args()
    run(a.events, a.lookahead, a.seed, a.skew)

if __name__ == "__main__":
    main()
