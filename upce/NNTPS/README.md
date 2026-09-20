# SDN Coursework — Labs, Programming Assignments & Projects

Hands-on examples and documentation for Software-Defined Networking based on Mininet, OpenFlow, RYU, and Floodlight.

## Structure

```
labs/
  01-virtual-network-deployment/  — Mininet + remote controller
  02-topology-design/             — Tree / linear via MiniEdit + Python
  03-manual-traffic-engineering/  — dpctl / ofctl manual flows
  04-packet-analysis/             — Wireshark OpenFlow capture
  05-rest-api-interaction/        — cURL + Python vs Floodlight REST
programming/
  01-l2-learning-switch/          — RYU L2 learning switch (Python)
  02-ryu-module-customization/    — RYU routing + blocklist security
  03-floodlight-java-module/      — Floodlight Java custom module
projects/
  01-controller-comparison/       — RYU vs Floodlight vs ODL vs ONOS report
  02-end-to-end-deployment/       — Capstone: multi-switch + routing + failover
  03-openflow-deep-dive/          — Paper/presentation on control/data separation
```

## Prerequisites

- Ubuntu 20.04+ / Mininet VM
- Mininet 2.3+, Open vSwitch, Wireshark
- RYU: `pip install ryu`
- Floodlight v1.2 + Java 11 + Eclipse (optional)
- Python 3.8+, `pip install requests`

## Quick Start

```bash
# 1. Start controller (example: RYU)
ryu-manager programming/01-l2-learning-switch/l2_learning_switch.py

# 2. In another terminal, run a Mininet topo
sudo python3 labs/01-virtual-network-deployment/mininet_remote.py

# 3. Test
mininet> pingall
```

Each folder contains its own `README.md` (lab guide), example code, and expected output.
