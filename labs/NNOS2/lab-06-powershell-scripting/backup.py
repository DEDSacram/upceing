#!/usr/bin/env python3
"""Linux-verifiable twin of Backup-Files.ps1: timestamped ZIP backup."""
import datetime
import pathlib
import sys
import zipfile

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <source> <destination>", file=sys.stderr)
    sys.exit(2)
src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
if not src.is_dir():
    print(f"Source not found: {src}", file=sys.stderr)
    sys.exit(1)
try:
    dst.mkdir(parents=True, exist_ok=True)
except OSError as e:
    print(f"Cannot create destination '{dst}': {e}", file=sys.stderr)
    sys.exit(1)

stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
zip_path = dst / f"{src.name}-{stamp}.zip"
try:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(src))
except OSError as e:
    print(f"Backup failed: {e}", file=sys.stderr)
    sys.exit(1)
print(f"Backup OK: {zip_path} ({zip_path.stat().st_size} bytes)")
