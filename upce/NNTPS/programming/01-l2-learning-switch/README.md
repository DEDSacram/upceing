# Programming 01 — Layer-Two Learning Switch (RYU)

**Objective:** Write a RYU app that learns MAC → port and forwards like a classic L2 switch.

## Run

```bash
pip install ryu
ryu-manager l2_learning_switch.py
# Terminal 2:
sudo mn --topo single,3 --mac --switch ovsk --controller remote,ip=127.0.0.1,port=6633
mininet> pingall
```

## How It Works (`l2_learning_switch.py`)

- `OFPSwitchFeatures` → install table-miss flow (priority 0 → `CONTROLLER`, `OFPCML_NO_BUFFER`).
- `PacketIn` → parse Ethernet, learn `mac_to_port[dpid][src] = in_port`.
- If `dst` known → `FlowMod` (match `in_port, eth_dst`, action `output:port`, `idle_timeout=10`) + `PacketOut`.
- Else → `PacketOut` with `FLOOD`.

This is the standard OpenFlow 1.3 learning-switch pattern. MAC table is per-DPID (per-switch).

## Exercises

1. Add `print`/logging of the learned table on every Packet-In. Ping and show learning order.
2. Add `hard_timeout=30`. What changes in `ovs-ofctl dump-flows s1` after 30s idle vs active?
3. **Loop test:** run with `--observe-links` topo containing a loop. Why does the network storm? (Leads into STP / spanning-tree module.)

## Expected Output

```
$ ryu-manager l2_learning_switch.py
loading app l2_learning_switch.py
...
dizzied h1 -> h2 learned 00:00:00:00:00:01 on s1 port 1
installed flow s1: in_port=1,dl_dst=00:00:00:00:00:02 -> output:2
mininet> pingall → 0% dropped
```
