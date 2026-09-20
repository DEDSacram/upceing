#!/usr/bin/env bash
# Linux counterpart of Network-Config.ps1 (read-only; runs anywhere).
set -euo pipefail
echo "=== Addresses (ip addr) ==="
ip -brief addr 2>/dev/null || ifconfig 2>/dev/null || echo "(no ip/ifconfig)"
echo "=== Routes (ip route) ==="
ip route 2>/dev/null || route -n 2>/dev/null || echo "(no route info)"
echo "=== Listening sockets (ss) ==="
(ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null) | head -20 || true
echo "=== Connectivity ==="
ping -c 2 -W 2 127.0.0.1 | tail -3
echo "Linux counterpart: OK"
