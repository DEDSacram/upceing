# Lab 03 — Manual Traffic Engineering (dpctl / ofctl)

**Objective:** Manually insert, inspect, and delete OpenFlow rules to route ping traffic — no controller learning logic.

## Setup: run switch with NO controller (fail-secure)

```bash
sudo mn --topo single,3 --mac --switch ovsk --controller none
```

Switch starts with empty flow table → all pings fail. Good baseline:

```
mininet> h1 ping -c2 h2
# 100% packet loss
```

## 1. Inspect flows

```bash
# Inside mininet CLI:
mininet> dpctl dump-flows
# or from another terminal:
sudo ovs-ofctl -O OpenFlow13 dump-flows s1
```

OpenFlow10 `dpctl` vs OpenFlow13 `ovs-ofctl -O OpenFlow13` — note version flag.

## 2. Add manual flows (see `manual_flows.sh`)

```bash
# Allow ARP both ways + ICMP h1<->h2, drop h1<->h3
sudo ovs-ofctl -O OpenFlow13 add-flow s1 "priority=10,arp,in_port=1,actions=output:2,output:3"
# ... full script:
sudo bash manual_flows.sh s1
sudo ovs-ofctl -O OpenFlow13 dump-flows s1
```

## 3. Test policy

```
mininet> h1 ping -c2 h2   # should SUCCEED
mininet> h1 ping -c2 h3   # should FAIL (no flow / drop)
mininet> dpctl show
```

## 4. Delete / modify

```bash
sudo ovs-ofctl -O OpenFlow13 del-flows s1
sudo ovs-ofctl -O OpenFlow13 dump-flows s1   # empty again
mininet> h1 ping -c1 h2  # fails again — proves forwarding was from YOUR flows
```

## Questions

1. Why do you need explicit ARP flows? What happens with only IP flows?
2. What does `priority=` do when two flows overlap?
3. Rewrite one flow with `actions=drop` vs no-flow (table-miss). Difference in counters?
