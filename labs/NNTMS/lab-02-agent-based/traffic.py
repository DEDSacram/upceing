"""Agent-based ring-road traffic toy (stdlib only)."""
import argparse, random

def simulate(L=100, N=20, vmax=5, p=0.2, steps=300, seed=1, clustered=True):
    rng = random.Random(seed)
    pos = sorted(rng.sample(range(L), N)) if not clustered else list(range(N))
    vel = [0] * N
    order = sorted(range(N), key=lambda i: pos[i])
    flows = []
    for _ in range(steps):
        order = sorted(range(N), key=lambda i: pos[i])
        gaps = []
        for k, i in enumerate(order):
            nxt = order[(k + 1) % N]
            gaps.append((pos[nxt] - pos[i] - 1) % L)
        new_v = []
        for k, i in enumerate(order):
            v = min(vel[i] + 1, vmax)
            v = min(v, gaps[k])
            if v > 0 and rng.random() < p:
                v -= 1
            new_v.append((i, v))
        for i, v in new_v:
            vel[i] = v
            pos[i] = (pos[i] + v) % L
        flows.append(sum(vel) / L)
    mean_v = sum(vel) / N
    flow = sum(vel) / L
    return pos, vel, mean_v, flow, sum(flows) / len(flows)

def ascii_ring(pos, L=100, width=60):
    road = ["."] * width
    for x in pos:
        road[int(x / L * width) % width] = "#"
    return "".join(road)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cars", type=int, default=20)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--road", type=int, default=100)
    a = ap.parse_args()
    pos, vel, mv, flow, avgflow = simulate(L=a.road, N=a.cars, steps=a.steps, seed=a.seed)
    print(f"cars={a.cars} density={a.cars/a.road:.2f} mean_v={mv:.2f} flow={flow:.3f} avgflow={avgflow:.3f}")
    print("ring:", ascii_ring(pos, a.road))
    print("speeds:", vel[:20])

if __name__ == "__main__":
    main()
