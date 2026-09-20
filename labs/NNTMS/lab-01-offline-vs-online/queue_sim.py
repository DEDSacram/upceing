"""M/M/1 analytic vs discrete-event simulation (stdlib only)."""
import argparse, heapq, math, random

def analytic(lam, mu):
    rho = lam / mu
    wq = rho / (mu - lam)
    lq = rho * rho / (1 - rho)
    return rho, wq, lq

def simulate(lam, mu, T, seed=1):
    rng = random.Random(seed)
    t, server_free, q = 0.0, 0.0, []
    wait_sum, served = 0.0, 0
    events = [(rng.expovariate(lam), "arr")]
    waits = []
    while events:
        t, kind = heapq.heappop(events)
        if t > T:
            break
        if kind == "arr":
            heapq.heappush(events, (t + rng.expovariate(lam), "arr"))
            if t >= server_free:
                server_free = t + rng.expovariate(mu)
                heapq.heappush(events, (server_free, "dep"))
                waits.append(0.0)
                served += 1
            else:
                q.append(t)
        else:
            if q:
                at = q.pop(0)
                w = t - at
                waits.append(w)
                wait_sum += w
                served += 1
                server_free = t + rng.expovariate(mu)
                heapq.heappush(events, (server_free, "dep"))
    sim_wq = (wait_sum + 0.0) / served if served else 0.0
    # include zero-waits: wait_sum only counts queued; add zeros implicitly
    sim_wq = sum(waits) / len(waits) if waits else 0.0
    return sim_wq, served

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lam", type=float, default=0.6)
    ap.add_argument("--mu", type=float, default=1.0)
    ap.add_argument("--t", type=float, default=5000)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    rho, wq, lq = analytic(a.lam, a.mu)
    sim_wq, served = simulate(a.lam, a.mu, a.t, a.seed)
    err = abs(sim_wq - wq) / wq * 100 if wq else 0
    print(f"analytic: rho={rho:.3f} Wq={wq:.4f} Lq={lq:.4f}")
    print(f"sim:      Wq={sim_wq:.4f} served={served} (T={a.t}, seed={a.seed})")
    print(f"error: {err:.1f}% {'OK (<20%)' if err < 20 else 'TOO HIGH'}")

if __name__ == "__main__":
    main()
