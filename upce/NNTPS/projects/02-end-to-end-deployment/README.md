# Project 02 — End-to-End SDN Deployment (Capstone)

**Objective:** Build a multi-switch network, connect the controller of your choice, and program custom routing, failover, and security policies.

## Topology (`capstone_topo.py`)

```
h1 -- s1 -- s2 -- s3 -- h2
       |     |     |
       h3    h4    h5     (2-redundant links s1-s2 for failover demo)
```

- 3 switches in a diamond/partial mesh, 5 hosts.
- Run: `sudo python3 capstone_topo.py` with controller from `capstone_app.py` (RYU) or Floodlight static pusher.

## Requirements

| # | Requirement | How (RYU example) | Verify |
|---|---|---|---|
| 1 | Custom routing | `capstone_app.py`: shortest-path via NetworkX on discovered links, proactive FlowMods | `h1 ping h2`, `dump-flows` shows path ports |
| 2 | Failover | `EventLinkDown`: delete affected flows, re-route over backup link < 1s | `link s1 s2 down`, ping continues after brief loss |
| 3 | Security | Blocklist (`BLOCKED_IPS`) + TCP port filter (drop `:22` except admin host) | Blocked ping 100% loss; `ssh` blocked, `http` allowed |
| 4 | Observability | REST/counters: poll flow stats, log Packet-In rate | Screenshot of counters before/after failover |

## Run (RYU path)

```bash
ryu-manager capstone_app.py &
sudo python3 capstone_topo.py
mininet> pingall
mininet> link s1 s2 down
mininet> h1 ping -c 20 h2   # expect <5 lost during reconvergence
mininet> link s1 s2 up
```

## Grading

- Topology code + diagram (20%), routing correctness (30%), failover demo with loss numbers (25%), security policy tests (15%), README evidence + cleanup (`mn -c`) (10%).

## Stretch

- QoS queue on s2→s3 (HTB), ECMP across both s1–s2 links, controller HA (2 RYUs — explain why state sharing fails).
