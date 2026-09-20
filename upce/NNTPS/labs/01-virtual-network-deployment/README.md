# Lab 01 — Virtual Network Deployment (Mininet + Remote Controller)

**Objective:** Install Mininet, start a virtual network, and connect it to a remote SDN controller.

## 1. Install

```bash
sudo apt update
sudo apt install -y mininet openvswitch-switch iperf
# RYU controller
pip install ryu
# Verify
mn --version
ovs-vsctl --version
```

## 2. Start Controller (Terminal 1)

```bash
# RYU simple switch
ryu-manager ../../programming/01-l2-learning-switch/l2_learning_switch.py
# Listens on 127.0.0.1:6633 by default
```

Or Floodlight:

```bash
cd ~/floodlight && java -jar target/floodlight.jar
# Listens on 127.0.0.1:6653 (check floodlightdefault.properties)
```

## 3. Start Mininet with Remote Controller (Terminal 2)

```bash
sudo python3 mininet_remote.py
```

See `mininet_remote.py` — creates 1 switch + 3 hosts, points to `127.0.0.1:6633` with OpenFlow13.

## 4. Verify

```
mininet> nodes
mininet> net
mininet> pingall
mininet> dpctl dump-flows
```

Expected: `pingall` 0% loss after controller learns MACs. `ovs-vsctl show` shows `is_connected: true`.

## 5. Cleanup

```
mininet> exit
sudo mn -c
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Unable to contact remote controller` | Controller not running, wrong IP/port, check `6633` vs `6653` |
| `RTNETLINK permission denied` | Forgot `sudo` |
| Stale bridges | `sudo mn -c`, `sudo ovs-vsctl del-br s1` |
