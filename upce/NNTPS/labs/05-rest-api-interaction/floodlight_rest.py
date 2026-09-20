#!/usr/bin/env python3
"""Lab 05: Floodlight REST client — query state, push/delete static flows.

Usage:
    python3 floodlight_rest.py --controller 127.0.0.1:8080 list
    python3 floodlight_rest.py block --src 10.0.0.3 --name block-h3
    python3 floodlight_rest.py allow --src 10.0.0.1 --dst 10.0.0.2 --out-port 2
    python3 floodlight_rest.py delete --name block-h3
"""
import argparse
import json
import sys

try:
    import requests
except ImportError:
    sys.exit("pip install requests")


def url(ctrl, path):
    return f"http://{ctrl}{path}"


def cmd_list(ctrl):
    for p in ["/wm/core/controller/switches/json",
              "/wm/device/",
              "/wm/staticflowpusher/list/all/json"]:
        r = requests.get(url(ctrl, p), timeout=5)
        print(f"### GET {p} -> {r.status_code}")
        print(json.dumps(r.json(), indent=2)[:2000])


def cmd_block(ctrl, src, name):
    flow = {"switch": "all", "name": name, "priority": "32768",
            "eth_type": "0x0800", "ipv4_src": src,
            "active": "true", "actions": ""}  # empty actions = drop
    r = requests.post(url(ctrl, "/wm/staticflowpusher/json"), json=flow, timeout=5)
    print(r.status_code, r.text)


def cmd_allow(ctrl, src, dst, out_port, name):
    flow = {"switch": "all", "name": name, "priority": "32768",
            "eth_type": "0x0800", "ipv4_src": src, "ipv4_dst": dst,
            "active": "true", "actions": f"output={out_port}"}
    r = requests.post(url(ctrl, "/wm/staticflowpusher/json"), json=flow, timeout=5)
    print(r.status_code, r.text)


def cmd_delete(ctrl, name):
    r = requests.delete(url(ctrl, "/wm/staticflowpusher/json"),
                        json={"name": name}, timeout=5)
    print(r.status_code, r.text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--controller", default="127.0.0.1:8080")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    b = sub.add_parser("block"); b.add_argument("--src", required=True); b.add_argument("--name", required=True)
    al = sub.add_parser("allow"); al.add_argument("--src", required=True); al.add_argument("--dst", required=True)
    al.add_argument("--out-port", required=True); al.add_argument("--name", required=True)
    d = sub.add_parser("delete"); d.add_argument("--name", required=True)
    a = ap.parse_args()
    {"list": lambda: cmd_list(a.controller),
     "block": lambda: cmd_block(a.controller, a.src, a.name),
     "allow": lambda: cmd_allow(a.controller, a.src, a.dst, a.out_port, a.name),
     "delete": lambda: cmd_delete(a.controller, a.name)}[a.cmd]()
