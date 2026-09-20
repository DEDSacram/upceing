#!/usr/bin/env python3
"""Lab 02a: Custom tree topology. depth=2, fanout=2 => 3 switches, 4 hosts."""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel


class TreeTopo(Topo):
    def build(self, depth=2, fanout=2):
        # TreeTopo from mininet.topolib could be used directly; written out for teaching.
        from mininet.topolib import TreeTopo as LibTree
        lib = LibTree(depth=depth, fanout=fanout)
        # Copy nodes/links from library topo into this topo
        for n, attrs in lib.g.nodes(data=True):
            self.addNode(n, **attrs)
        for u, v, attrs in lib.g.edges(data=True):
            self.addLink(u, v, **attrs)


if __name__ == "__main__":
    setLogLevel("info")
    topo = TreeTopo(depth=2, fanout=2)
    net = Mininet(topo=topo, controller=RemoteController("c0", ip="127.0.0.1", port=6633))
    net.start()
    print("*** Hosts:", [h.name for h in net.hosts])
    net.pingAll()
    CLI(net)
    net.stop()
