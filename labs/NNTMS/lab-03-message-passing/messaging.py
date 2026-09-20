"""Hierarchical agent messaging demo (stdlib only)."""
import argparse
from collections import defaultdict, deque

class Bus:
    def __init__(self, latency=1):
        self.latency = latency
        self.q = defaultdict(deque)  # tick -> [(dst, msg)]
        self.sent = 0
    def send(self, now, dst, msg):
        self.q[now + self.latency].append((dst, msg))
        self.sent += 1
    def deliver(self, now, agents):
        for dst, msg in self.q.pop(now, []):
            agents[dst].inbox.append(msg)

class Agent:
    def __init__(self, aid, kind):
        self.id, self.kind, self.inbox = aid, kind, deque()
        self.received = 0
        self.temp = 20.0

def run(latency=1, ticks=25, spike_at=10):
    bus = Bus(latency)
    agents = {}
    leaves = ["leaf0", "leaf1", "leaf2", "leaf3"]
    coords = {"leaf0": "coA", "leaf1": "coA", "leaf2": "coB", "leaf3": "coB"}
    for lid in leaves:
        agents[lid] = Agent(lid, "leaf")
    for c in ("coA", "coB"):
        agents[c] = Agent(c, "coord")
    agents["root"] = Agent("root", "root")
    alarms = []
    agg = defaultdict(list)
    for t in range(ticks):
        bus.deliver(t, agents)
        # leaves sense + report
        for lid in leaves:
            a = agents[lid]
            a.temp = 20.0 + (t * 0.1)
            if lid == "leaf2" and t >= spike_at:
                a.temp = 95.0
            # handle downlink (none in base demo)
            bus.send(t, coords[lid], ("reading", lid, round(a.temp, 1)))
        # coords aggregate
        for c in ("coA", "coB"):
            a = agents[c]
            while a.inbox:
                m = a.inbox.popleft()
                a.received += 1
                if m[0] == "reading":
                    agg[(c, t)].append(m[2])
            if agg[(c, t)]:
                vals = agg[(c, t)]
                bus.send(t, "root", ("summary", c, round(sum(vals) / len(vals), 1), max(vals)))
        # root decides
        r = agents["root"]
        while r.inbox:
            m = r.inbox.popleft()
            r.received += 1
            if m[0] == "summary" and m[3] > 80 and not alarms:
                alarms.append((t, m[1], m[3]))
                print(f"tick {t}: ROOT alarm OVERHEAT via {m[1]} peak={m[3]}")
    print(f"done: sent={bus.sent} root_inbox_total={agents['root'].received} alarms={len(alarms)}")
    assert len(alarms) == 1, f"expected exactly 1 alarm, got {alarms}"
    return alarms

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--latency", type=int, default=1)
    ap.add_argument("--ticks", type=int, default=25)
    a = ap.parse_args()
    run(a.latency, a.ticks)

if __name__ == "__main__":
    main()
