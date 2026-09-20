# Project 01 — Controller Comparison Report (RYU vs Floodlight vs OpenDaylight vs ONOS)

**Deliverable:** 6–10 page report + 10-min presentation. Use the comparison matrix below as starting point — verify each claim by running at least RYU + Floodlight (this repo) and reading ODL/ONOS docs.

## 1. Suggested Outline

1. Introduction: why centralized control; OpenFlow / NETCONF / P4 southbound.
2. Architecture per controller: language, modularity, threading, clustering.
3. Northbound & intent: REST, OSGi services, ONOS intents.
4. Scalability & HA: single-instance vs distributed (ODL Akka clustering, ONOS Atomix/Raft).
5. Use-cases: campus/research (RYU), enterprise prototyping (Floodlight), carrier/DC (ODL/ONOS).
6. Hands-on evaluation: same Mininet topo on RYU + Floodlight — table with setup time, Packet-In latency, failover behavior.
7. Conclusion + recommendation matrix (which controller for which scenario).

## 2. Comparison Matrix (verify before submitting)

| Dimension | RYU | Floodlight | OpenDaylight | ONOS |
|---|---|---|---|---|
| Language | Python | Java | Java (OSGi/Karaf) | Java (OSGi) |
| OF versions | 1.0–1.5 (+Nicira ext) | 1.0–1.3 (+1.4 partial) | 1.0–1.3, NETCONF, P4 | 1.0–1.3, NETCONF, P4 |
| Architecture | Single-threaded eventlets, app-per-file | Static modules, listener chain | MD-SAL models (YANG), Karaf features | Distributed core, intents, Atomix store |
| Northbound | WSGI REST (per-app) | REST (`/wm/...`), Java API | RESTCONF, DLUX UI | REST, CLI, intent framework |
| Clustering / HA | None (research) | None (single) | Akka shards, 3-node cluster | RAFT-backed, active-active |
| Learning curve | Low (Python, quick proto) | Medium (Java, Eclipse/ant) | High (YANG/Maven/Karaf) | Medium-high (Bazel, distributed) |
| Community | Small, NTT legacy, mostly frozen | Small, Big Switch legacy | Large (Linux Foundation) | Large (ONF → LF) |
| Best for | Teaching, quick experiments | Teaching Java SDN, static flows | Carrier/DC, NETCONF, SFC | Scale-out fabric, research on availability |

## 3. Hands-On Rubric (20 pts)

- Both controllers run same `labs/02-topology-design/custom_linear.py --switches 3` (5 pts).
- `pingall` + `ovs-ofctl dump-flows` evidence for each (5 pts).
- REST evidence: Floodlight `/wm/...` vs RYU `/stats/flow/...` screenshots (5 pts).
- Latency note: first-ping vs steady ping (Packet-In cost) (5 pts).

## 4. Sources (start here, cite properly)

- Floodlight wiki, RYU docs, ODL docs (`docs.opendaylight.org`), ONOS docs (`wiki.onosproject.org`).
- ONF OpenFlow 1.3 spec; Kreutz et al. “Software-Defined Networking: A Comprehensive Survey”.
