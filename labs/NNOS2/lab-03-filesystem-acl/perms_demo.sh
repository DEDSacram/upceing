#!/usr/bin/env bash
# Linux permission counterpart of Get-AclDemo.ps1 (runs anywhere).
# Demonstrates owner/group/other bits + setfacl/getfacl when available.
set -euo pipefail
D="${1:-AclDemo}"
mkdir -p "$D"
F="$D/secret.txt"
echo "top secret" > "$F"
chmod 640 "$F"

echo "=== ls -l ==="
ls -l "$F"
echo "=== stat ==="
stat -c 'owner=%U group=%G mode=%a' "$F"

echo "=== Read check ==="
if [ -r "$F" ]; then echo "readable: OK"; else echo "readable: FAIL"; fi

if command -v setfacl >/dev/null 2>&1; then
  echo "=== ACL: grant + deny via setfacl ==="
  setfacl -m u:nobody:r "$F" || echo "(cannot setfacl for nobody, skipped)"
  getfacl "$F" || true
  setfacl -b "$F" 2>/dev/null || true
else
  echo "(setfacl not installed; classic rwx bits shown above)"
fi

echo "=== umask default for new files ==="
umask
echo "Linux counterpart: OK"
