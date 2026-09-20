# Lab 02 — Topology Design (MiniEdit + Python Scripts)

**Objective:** Build custom tree and linear topologies two ways: GUI (MiniEdit) and code.

## A. MiniEdit (GUI)

```bash
sudo python3 /usr/share/mininet/examples/miniedit.py &
# or: sudo miniedit &
```

Steps:
1. Drag 4 hosts + 2 switches, wire h1,h2→s1, h3,h4→s2, s1↔s2.
2. Edit Preferences → check `Start CLI`, set Controller `Remote`, IP `127.0.0.1`, Port `6633`.
3. File → Export Level 2 Script → save as `miniedit_export.py`.
4. Run: controller in term 1, then `sudo python3 miniedit_export.py`.

## B. Python Scripts (provided)

Tree (depth=2, fanout=2 → 3 switches, 4 hosts):

```bash
sudo python3 custom_tree.py
mininet> pingall
mininet> xterm h1 h4
# h1: iperf -s &   h4: iperf -c 10.0.0.4
```

Linear (3 switches in a chain, 1 host each):

```bash
sudo python3 custom_linear.py --switches 3
mininet> pingall
mininet> net
```

## Exercises

1. Change `custom_tree.py` depth to 3, fanout 2. How many hosts/switches? (`TreeTopo` formula).
2. Add `bw=5, loss=5` to one link in `custom_linear.py`. Measure `ping -c 20` impact.
3. Export your MiniEdit design and `diff` it against `custom_tree.py` — what boilerplate does MiniEdit add?

## Expected Output

```
*** Ping: testing ping reachability
h1 -> h2 h3 h4
...
*** Results: 0% dropped (12/12 received)
```
