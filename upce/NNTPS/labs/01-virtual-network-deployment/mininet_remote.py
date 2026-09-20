#!/usr/bin/env python3
"""Lab 01: Mininet virtual network with remote controller.

Topology: 3 hosts (h1-h3) <-> single OVS switch (s1) <-> remote controller.
Usage:
    Terminal 1: ryu-manager ../../programming/01-l2-learning-switch/l2_learning_switch.py
    Terminal 2: sudo python3 mininet_remote.py [--ip 127.0.0.1] [--port 6633]
"""
import argparse
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info


def build(controller_ip="127.0.0.1", controller_port=6633):
    net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, autoSetMacs=True)

    info(f"*** Adding remote controller {controller_ip}:{controller_port}\n")
    net.addController("c0", controller=RemoteController,
                      ip=controller_ip, port=controller_port, protocols="OpenFlow13")

    info("*** Adding switch and hosts\n")
    s1 = net.addSwitch("s1", protocols="OpenFlow13")
    h1 = net.addHost("h1", ip="10.0.0.1/24")
    h2 = net.addHost("h2", ip="10.0.0.2/24")
    h3 = net.addHost("h3", ip="10.0.0.3/24")

    info("*** Linking\n")
    net.addLink(h1, s1, bw=10, delay="1ms")
    net.addLink(h2, s1, bw=10, delay="1ms")
    net.addLink(h3, s1, bw=10, delay="1ms")

    info("*** Starting\n")
    net.start()
    info("*** Testing connectivity (expect success once controller programs flows)\n")
    net.pingAll()
    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    p = argparse.ArgumentParser()
    p.add_argument("--ip", default="127.0.0.1")
    p.add_argument("--port", type=int, default=6633)
    args = p.parse_args()
    build(args.ip, args.port)
