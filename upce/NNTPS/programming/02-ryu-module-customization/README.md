# Programming 02 — RYU Module Customization (Routing + Security Blocklist)

**Objective:** Extend a routing module with a security feature: drop traffic from blocked hosts.

## Run

```bash
ryu-manager firewall_block.py
sudo mn --topo single,3 --mac --switch ovsk --controller remote,ip=127.0.0.1,port=6633
mininet> pingall
```

Edit `BLOCKED_MACS` / `BLOCKED_IPS` at top of `firewall_block.py`, restart controller, re-test.

## What Was Added vs Prog 01

| Feature | Implementation |
|---|---|
| MAC blocklist | `if eth.src in BLOCKED_MACS: drop` — install high-priority drop flow so switch blocks without bothering controller again |
| IP blocklist | Parse `ipv4` header; match `ipv4_src` in drop flow (`priority=100`) |
| Drop flow | `OFPFlowMod` with **empty** `APPLY_ACTIONS` instructions = drop; `idle_timeout=0, hard_timeout=0` = permanent until restart |
| Logging | `self.logger.warning("BLOCKED ...")` for audit trail |

## Code Sketch

```python
BLOCKED_MACS = {"00:00:00:00:00:03"}
BLOCKED_IPS  = {"10.0.0.3"}

# in packet_in_handler, before learning:
if eth.src in BLOCKED_MACS: return self._install_drop(dp, parser, in_port, eth.src)
```

See full `firewall_block.py`.

## Exercises

1. Block by **destination TCP port** (e.g., drop port 80). Hint: parse `tcp` protocol, match `tcp_dst`.
2. Add a REST hook / CLI to add/remove blocked IPs at runtime (no restart). Compare with Floodlight static pusher.
3. Measure controller load: `h1 ping -f h2` with and without drop-flow installed. Why does the permanent drop flow reduce Packet-Ins?
