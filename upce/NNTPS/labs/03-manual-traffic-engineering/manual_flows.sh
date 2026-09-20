#!/usr/bin/env bash
# Lab 03: manually program s1 (ports: h1=1, h2=2, h3=3 in `single,3` topo).
# Usage: sudo bash manual_flows.sh [bridge]  (default s1)
# Requires OVS with OpenFlow13.
set -e
BR=${1:-s1}
OF="ovs-ofctl -O OpenFlow13"

echo "*** Flushing $BR"
$OF del-flows "$BR"

echo "*** ARP: flood ARP on all host ports"
$OF add-flow "$BR" "priority=10,arp,in_port=1,actions=output:2,output:3"
$OF add-flow "$BR" "priority=10,arp,in_port=2,actions=output:1,output:3"
$OF add-flow "$BR" "priority=10,arp,in_port=3,actions=output:1,output:2"

echo "*** ICMP h1 <-> h2 ALLOW"
$OF add-flow "$BR" "priority=20,ip,nw_src=10.0.0.1,nw_dst=10.0.0.2,actions=output:2"
$OF add-flow "$BR" "priority=20,ip,nw_src=10.0.0.2,nw_dst=10.0.0.1,actions=output:1"

echo "*** h3 ISOLATED: explicit drop (counter proves hits)"
$OF add-flow "$BR" "priority=20,ip,nw_src=10.0.0.3,actions=drop"
$OF add-flow "$BR" "priority=20,ip,nw_dst=10.0.0.3,actions=drop"

echo "*** Table-miss drop (fail-secure, no controller)"
$OF add-flow "$BR" "priority=0,actions=drop"

echo "*** Current flows:"
$OF dump-flows "$BR"
