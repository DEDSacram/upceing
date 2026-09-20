#!/usr/bin/env python3
"""Lab 02b: Custom linear topology: s1-s2-...-sN, one host per switch."""
import argparse
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel


class LinearTopo(Topo):
    def build(self, n=3, bw=10):
        switches, hosts = [], []
        for i in range(1, n + 1):
            sw = self.addSwitch(f"s{i}", protocols="OpenFlow13")
            h = self.addHost(f"h{i}", ip=f"10.0.0.{i}/24")
            self.addLink(h, sw, bw=bw)
            switches.append(sw)
            hosts.append(h)
        for i in range(n - 1):
            # Bottleneck link students can experiment with: try loss=5, delay='10ms'
            self.addLink(switches[i], switches[i + 1], bw=bw)


if __name__ == "__main__":
    setLogLevel("info")
    ap = argparse.ArgumentParser()
    ap.add_argument("--switches", type=int, default=3)
    ap.add_argument("--ip", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=6633)
    a = ap.parse_args()
    net = Mininet(topo=LinearTopo(n=a.switches),
                  controller=RemoteController("c0", ip=a.ip, port=a.port))
    net.start()
    net.pingAll()
    CLI(net)
    net.stop()
