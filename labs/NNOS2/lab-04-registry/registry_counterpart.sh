#!/usr/bin/env bash
# Linux counterpart of Registry-Demo.ps1: HKCU-like per-user config store.
# Uses an INI-style file instead of the Registry (same key/value idea).
set -euo pipefail
STORE="${1:-nnos2lab.conf}"

kv_set() { # kv_set file key value
  local f="$1" k="$2" v="$3" tmp
  tmp="$(mktemp)"
  grep -v -E "^${k}=" "$f" 2>/dev/null > "$tmp" || true
  echo "${k}=${v}" >> "$tmp"
  mv "$tmp" "$f"
}
kv_get() { # kv_get file key
  grep -E "^$2=" "$1" | tail -1 | cut -d= -f2-
}

rm -f "$STORE"
kv_set "$STORE" "Greeting" "Hello from NNOS2 lab-04"
kv_set "$STORE" "Counter" "42"
echo "=== Store after write ==="
cat "$STORE"
c="$(kv_get "$STORE" "Counter")"
c=$((c + 1))
kv_set "$STORE" "Counter" "$c"
echo "Counter incremented to $c"
echo "=== Final store ==="
cat "$STORE"
[ "$(kv_get "$STORE" "Counter")" = "$c" ] && echo "Linux counterpart: OK"
