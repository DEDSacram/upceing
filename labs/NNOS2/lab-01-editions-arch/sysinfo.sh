#!/usr/bin/env bash
# Linux counterpart of Get-SystemInfo.ps1: OS edition + architecture overview.
set -euo pipefail
OUT="${1:-systeminfo.txt}"
{
  echo "OS              : $(source /etc/os-release 2>/dev/null && echo "$PRETTY_NAME")"
  echo "Kernel          : $(uname -srm)"
  echo "Architecture    : $(uname -m)"
  echo "CPU             : $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | xargs)"
  echo "CPUs            : $(nproc)"
  echo "Total RAM (kB)  : $(awk '/MemTotal/{print $2}' /proc/meminfo)"
  echo "Firmware        : $([ -d /sys/firmware/efi ] && echo UEFI || echo BIOS/Legacy)"
} | tee "$OUT"
