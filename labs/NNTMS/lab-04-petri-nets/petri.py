"""Petri net engine + reachability explorer (stdlib only)."""
import argparse
from collections import deque

# Order workflow with explicit fork/join: one token, parallel branch pay || pack.
PLACES = ["order", "to_pay", "to_pack", "paid", "packed", "ready", "shipped"]
TRANSITIONS = {
    "fork": (["order"], ["to_pay", "to_pack"]),
    "pay": (["to_pay"], ["paid"]),
    "pack": (["to_pack"], ["packed"]),
    "join": (["paid", "packed"], ["ready"]),
    "ship": (["ready"], ["shipped"]),
}
M0 = {"order": 1, "to_pay": 0, "to_pack": 0, "paid": 0, "packed": 0, "ready": 0, "shipped": 0}

def enabled(mark, t):
    ins, _ = TRANSITIONS[t]
    return all(mark.get(p, 0) >= 1 for p in ins)

def fire(mark, t):
    ins, outs = TRANSITIONS[t]
    nm = dict(mark)
    for p in ins:
        nm[p] -= 1
    for p in outs:
        nm[p] = nm.get(p, 0) + 1
    return nm

def key(mark):
    return tuple(mark.get(p, 0) for p in PLACES)

def explore(m0, max_states=100):
    seen = {key(m0): m0}
    dq = deque([m0])
    deadlocks = []
    while dq and len(seen) < max_states:
        m = dq.popleft()
        en = [t for t in TRANSITIONS if enabled(m, t)]
        if not en and m.get("shipped", 0) < 1:
            deadlocks.append(key(m))
        for t in en:
            nm = fire(m, t)
            k = key(nm)
            if k not in seen:
                seen[k] = nm
                dq.append(nm)
    return seen, deadlocks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-states", type=int, default=100)
    a = ap.parse_args()
    seen, deadlocks = explore(M0, a.max_states)
    print(f"places: {PLACES}")
    print(f"reachable markings: {len(seen)}")
    for k in sorted(seen):
        print(f"  {dict(zip(PLACES, k))}")
    final = any(m.get("shipped", 0) >= 1 for m in seen.values())
    print(f"final marking (shipped>=1) reachable: {final}")
    print(f"deadlocks (non-final, none-enabled): {len(deadlocks)} {deadlocks}")
    assert len(seen) == 7, f"expected 7 markings, got {len(seen)}"
    assert final and not deadlocks
    print("OK: finite, deadlock-free, final reachable.")

if __name__ == "__main__":
    main()
