# Lab 05 — REST API Interaction (Floodlight)

**Objective:** Query network state and push static flows via Floodlight's REST API using cURL and Python.

> Floodlight REST default: `http://<controller-ip>:8080`. RYU has a similar WSGI API on `:8080` — concepts transfer.

## 1. Start Floodlight + Mininet

```bash
cd ~/floodlight && java -jar target/floodlight.jar &
sudo mn --topo single,3 --mac --switch ovsk --controller remote,ip=127.0.0.1,port=6653
```

## 2. cURL — query state

```bash
CTRL=127.0.0.1:8080
curl -s http://$CTRL/wm/core/controller/switches/json | python3 -m json.tool
curl -s http://$CTRL/wm/core/switch/all/flow/json | python3 -m json.tool
curl -s http://$CTRL/wm/device/ | python3 -m json.tool
curl -s http://$CTRL/wm/topology/links/json | python3 -m json.tool
```

## 3. cURL — push a static flow (StaticFlowPusher)

Block h3 (10.0.0.3) → h1, then allow h1 → h2:

```bash
# DROP h3 -> anywhere
curl -s -X POST -d '{"switch":"all","name":"block-h3","priority":"32768","eth_type":"0x0800","ipv4_src":"10.0.0.3","active":"true","actions":""}' \
  http://$CTRL/wm/staticflowpusher/json

# Verify + test
curl -s http://$CTRL/wm/staticflowpusher/list/all/json | python3 -m json.tool
mininet> h3 ping -c2 h1   # should FAIL
mininet> h1 ping -c2 h2   # should SUCCEED

# Delete
curl -s -X DELETE -d '{"name":"block-h3"}' http://$CTRL/wm/staticflowpusher/json
```

`actions:""` with a match = drop. Missing rule + default forwarding = flood/learn.

## 4. Python (provided `floodlight_rest.py`)

```bash
pip install requests
python3 floodlight_rest.py --controller 127.0.0.1:8080 list
python3 floodlight_rest.py --controller 127.0.0.1:8080 block --src 10.0.0.3 --name block-h3
python3 floodlight_rest.py --controller 127.0.0.1:8080 allow --src 10.0.0.1 --dst 10.0.0.2 --out-port 2 --name allow-h1-h2
python3 floodlight_rest.py --controller 127.0.0.1:8080 delete --name block-h3
```

## Exercises

1. Push a flow matching TCP `dst-port 80` from h1 and redirect to h3 (action `output=3`). Verify with `iperf`.
2. Compare `dump-flows` (OVS view) vs `/wm/core/switch/all/flow/json` (controller view). Why can they differ?
3. Script a loop polling `/wm/device/` every 2s while hosts ping — plot attach/detach timing.
