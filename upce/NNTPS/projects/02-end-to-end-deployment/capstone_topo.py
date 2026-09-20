#!/usr/bin/env python3
"""Capstone topo: 3 switches, 5 hosts, redundant s1-s2 links for failover demo.

    h1-s1-s2-s3-h2, h3 on s1, h4 on s2, h5 on s3. Two parallel links s1<->s2.
Run: sudo python3 capstone_topo.py  (with ryu-manager capstone_app.py running)
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel


class CapstoneTopo(Topo):
    def build(self):
        s1 = self.addSwitch("s1", protocols="OpenFlow13")
        s2 = self.addSwitch("s2", protocols="OpenFlow13")
        s3 = self.addSwitch("s3", protocols="OpenFlow13")
        hosts = {}
        for i, sw in [(1, s1), (2, s3), (3, s1), (4, s2), (5, s3)]:
            h = self.addHost(f"h{i}", ip=f"10.0.0.{i}/24")
            self.addLink(h, sw, bw=10)
            hosts[i] = h
        self.addLink(s1, s2, bw=20)   # primary
        self.addLink(s1, s2, bw=20)   # backup (parallel -> failover demo)
        self.addLink(s2, s3, bw=20)


if __name__ == "__main__":
    setLogLevel("info")
    net = Mininet(topo=CapstoneTopo(),
                  controller=RemoteController("c0", ip="127.0.0.1", port=6633))
    net.start()
    print("*** Try: pingall | link s1 s2 down | h1 ping -c 20 h2")
    CLI(net)
    net.stop()
