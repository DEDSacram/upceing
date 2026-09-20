# Lab 03 — Hierarchical Agent Messaging

Agents organized in a tree (leaves → coordinators → root) pass messages up/down with latency.

## 1. Theory

- **Hierarchical MAS:** leaf agents sense/act; coordinators aggregate (e.g. mean temperature) and forward; root decides (e.g. alarm).
- **Message passing:** async sends with delivery tick = `now + latency`; inbox queues decoupled from processing — the core of actor models and HLA-style federations.
- **Aggregation:** coordinators reduce N messages into 1 summary — bandwidth vs freshness trade-off.

## 2. Project layout

```
lab-03-message-passing/
  README.md
  messaging.py   # 4 leaves + 2 coordinators + root; latency sim; alarm demo
```

## 3. Run

```bash
cd labs/NNTMS/lab-03-message-passing
python3 messaging.py
python3 messaging.py --latency 3 --ticks 30
```

## 4. Verify

1. Default run prints message counts per level and the root raising exactly one `OVERHEAT` alarm when a leaf spikes.
2. Higher `--latency` delays (but does not lose) the alarm — delivery tick shifts.
3. `python3 -m py_compile messaging.py` passes.

## 5. Tasks

1. Add a downlink command: root broadcasts `SHED_LOAD`; leaves confirm.
2. Drop 10% of messages; add ACK/retry and measure duplicate rate.
3. Replace mean-aggregation with max-aggregation; compare alarm latency.
4. Draw the message sequence chart for the alarm episode.
