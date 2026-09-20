# Project 03 — OpenFlow Deep Dive (Control/Data Plane Separation)

**Deliverable:** 8–12 slide presentation or 4–6 page paper + live Wireshark demo (reuse Lab 04 capture).

## 1. Required Outline

1. **Problem:** distributed control in legacy networks (per-device CLI, slow convergence, vendor lock-in) → SDN answer: centralize control, standardize southbound.
2. **Separation:** control plane (controller: topology, routing decisions) vs data plane (switch: match-action forwarding). Diagram: app → northbound → controller → OpenFlow (TLS/TCP 6633/6653) → flow tables.
3. **Switch anatomy:** flow table pipeline — `Match Fields → Priority → Counters → Instructions → Actions → Timeouts`. Table-miss: drop vs controller vs next-table.
4. **Protocol:** Hello → Features → Multipart → Packet-In/Out → Flow-Mod → Echo. Show real capture from Lab 04 with XIDs.
5. **Action sets:** forward (`output`, `group`), modify (`push_vlan`, `set_field`), drop (empty actions). Example: L2-learn Flow-Mod from Prog 01.
6. **Evolution & limits:** OF 1.0→1.5 (groups, meters, table sync), why P4/NETCONF emerged; single-point-of-failure → ODL/ONOS clustering (link to Project 01).

## 2. Figures to Include (draw or screenshot)

- [ ] Control/data plane split diagram (before/after SDN).
- [ ] Flow-entry structure diagram (match/priority/counters/instructions/timeouts).
- [ ] Pipeline across multiple tables (e.g., Table 0 ACL → Table 1 routing).
- [ ] Annotated Wireshark: Hello + Features + one Packet-In/Flow-Mod pair.
- [ ] `ovs-ofctl dump-flows` output mapped field-by-field to the diagram.

## 3. Demo Script (5 min)

1. Fresh `mn --controller none` → ping fails (empty table = data plane alone is dumb).
2. Push one manual flow (`manual_flows.sh`) → ping works (control decision compiled to data-plane entry).
3. Start controller → show Packet-In/Flow-Mod in Wireshark (control loop closed).

## 4. Grading Checklist

- Correct flow-table vocabulary (match/priority/instructions/timeouts) (25%).
- Real evidence: pcap + dump-flows mapped to theory (25%).
- Clear separation argument with failure-mode discussion (25%).
- Sources: OF 1.3.5 spec + one survey paper, cited (10%) + delivery quality (15%).
