"""Time Warp toy: speculative execution with rollback (stdlib only).

One LP owns a counter. Base events arrive in order; straggler events arrive
late with past timestamps. On a straggler the LP rolls back to the newest
checkpoint <= straggler ts, sends one anti-message per undone event, then
re-executes (straggler + undone events in timestamp order). Final state is
verified against a sequential timestamp-sorted reference.
"""
import argparse, random

def run(n=50, stragglers=4, seed=1):
    rng = random.Random(seed)
    base = [(float(i), 1) for i in range(1, n + 1)]
    strag = []
    for _ in range(stragglers):
        strag.append((round(rng.uniform(1, n - 1), 2), 10))
    arrival = list(base) + strag  # optimistic order: future first, past trickles in

    known = []          # all events seen so far: (ts, delta, seq)
    executed_until = -1.0
    counter = 0
    clock = 0.0
    rollbacks, anti, reexec = 0, 0, 0
    seq = 0

    def checkpoint_state(ts):
        # counter after applying all known events with ts' <= ts, in order
        c = 0
        for t2, d2, _ in sorted(known, key=lambda e: (e[0], e[2])):
            if t2 <= ts:
                c += d2
        return c

    for ts, d in arrival:
        seq += 1
        known.append((ts, d, seq))
        if ts < clock:
            rollbacks += 1
            undone = [e for e in known if e[0] > ts and e[2] < seq]
            anti += len(undone)
            reexec += len(undone)
            counter = checkpoint_state(ts)  # includes the straggler itself
            clock = ts
            # re-execute undone future events in timestamp order
            for t2, d2, _ in sorted(undone, key=lambda e: (e[0], e[2])):
                counter += d2
                clock = max(clock, t2)
        else:
            counter += d
            clock = max(clock, ts)

    ref = sum(d for _, d in sorted(base + [(t, dd) for t, dd in strag]))
    print(f"base={n} stragglers={stragglers} rollbacks={rollbacks} "
          f"anti-messages={anti} re-executed={reexec}")
    print(f"optimistic counter={counter} reference counter={ref}")
    assert counter == ref, f"DIVERGED: {counter} != {ref}"
    print("OK: final state matches sequential reference.")
    return rollbacks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stragglers", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--events", type=int, default=50)
    a = ap.parse_args()
    run(a.events, a.stragglers, a.seed)

if __name__ == "__main__":
    main()
