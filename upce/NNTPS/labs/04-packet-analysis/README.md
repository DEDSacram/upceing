# Lab 04 — Packet Analysis (Wireshark + OpenFlow)

**Objective:** Capture the OpenFlow handshake and Packet-In / Flow-Mod exchange between OVS and controller.

## 1. Setup

- Topo: `sudo python3 ../01-virtual-network-deployment/mininet_remote.py` (keep it running but controller STOPPED first is instructive).
- Capture interface: `any` or `lo` (controller on 127.0.0.1) + the OVS bridge. Filter:

```
openflow_v4
# or version-agnostic:
tcp.port == 6633 || tcp.port == 6653 || openflow
```

> Wireshark dissectors: `openflow_v1`, `openflow_v4` (OF 1.3). If filter fails, use `tcp.port==6633`.

## 2. Capture Sequence

1. Start Wireshark capture → start RYU controller → start Mininet.
2. Observe in order:
   1. `HELLO` (version negotiation: switch bitmask → `v4` selected)
   2. `FEATURES_REQUEST` / `FEATURES_REPLY` (datapath-id, ports)
   3. `MULTIPART_REQUEST` (port-desc) — OF1.3 replaces stats
   4. `PACKET_IN` (first ping → table-miss → to controller, with `buffer_id` + `in_port`)
   5. `PACKET_OUT` + `FLOW_MOD` (controller installs forward rule)
3. Run `h1 ping h2`, stop after ~10 packets.

## 3. Analysis Tasks

| # | Question | Where to look |
|---|---|---|
| 1 | What OF version was negotiated? | `Hello.Xid`, `version` field |
| 2 | What is the switch DPID? | `Features Reply.datapath_id` |
| 3 | Why does only the FIRST ping generate Packet-In? | Subsequent match installed flow; check `Flow-Mod.match.in_port + eth_dst` |
| 4 | What `output` action + `idle_timeout` did controller set? | `Flow-Mod` → `actions`, `idle_timeout` |
| 5 | ECHO_REQUEST interval? | Filter `openflow_v4.type == 2` — keepalive every ~5s |

## 4. Save Evidence

- File → Save as `openflow_handshake.pcapng` (submit with report).
- Screenshot annotated handshake + one Packet-In/Flow-Mod pair.
- `tshark` alternative (headless):

```bash
sudo tshark -i lo -f "tcp port 6633" -Y openflow -T fields \
  -e openflow_v4.type -e openflow.xid -c 50 > capture.txt
```

## Deliverable

Short report: message sequence diagram (switch ↔ controller), table of 5 messages with type/XID/purpose, answers to Q1–Q5.
