# Lab 01 — Windows Editions & Architecture

Compare Windows editions and CPU architectures; collect the data with `Get-ComputerInfo` on a student Windows machine. Linux counterpart script runs here.

## 1. Theory

- **Editions (same kernel, different feature locks):** `Home` (consumer, no BitLocker/Group Policy/Hyper-V host), `Pro` (adds BitLocker, Hyper-V, Remote Desktop host, Group Policy), `Pro for Workstations`/`Enterprise` (ReFS, persistent memory, AppLocker, DirectAccess), `Education` (≈ Enterprise for schools), `Server` (Standard vs Datacenter: Datacenter adds unlimited VMs + Storage Spaces Direct; both have Server Core / Desktop Experience installs). Edition is licensing + enabled components, not a different OS core.
- **Architectures:** `x64` (amd64, dominant desktop/server), `ARM64` (Surface Pro X, Copilot+ laptops; runs x64 apps via emulation Prism/x86-64 emulation), `x86` (32-bit, legacy; max ~4 GB RAM, WoW64 runs it on 64-bit Windows). `OsArchitecture` from `Get-ComputerInfo` reports the OS bitness; `(Get-CimInstance Win32_Processor).AddressWidth` reports CPU.
- **Useful commands (Windows):** `winver`, `systeminfo`, `Get-ComputerInfo | Select WindowsProductName, WindowsEditionId, WindowsVersion, OsArchitecture`, `slmgr /dli` (license).
- **Linux analogue:** `/etc/os-release` ≈ edition, `uname -m` ≈ architecture (`x86_64`, `aarch64`, `i686`).

## 2. Project layout

```
lab-01-editions-arch/
  Get-SystemInfo.ps1  # Get-ComputerInfo + CIM fallback, writes systeminfo.txt (run on Windows)
  sysinfo.sh          # Linux counterpart: os-release + uname + /proc/cpuinfo (runs here)
  README.md
```

## 3. Run

```powershell
# On a student Windows machine:
powershell -ExecutionPolicy Bypass -File Get-SystemInfo.ps1
```

```bash
# On Linux (verifiable here):
cd lab-01-editions-arch
bash sysinfo.sh
```

## 4. Verify

1. On Windows: `systeminfo.txt` contains `WindowsProductName`, `WindowsEditionId`, `WindowsVersion`, `OsArchitecture`.
2. On Linux: `bash sysinfo.sh` prints OS, kernel, architecture, CPU, RAM, firmware and exits `0`.
3. You can state which edition + architecture your own machine has and why it matters (e.g. ARM64 → check driver/app compatibility).

## 5. Tasks

1. Run `Get-SystemInfo.ps1` on a Windows machine, paste the output into this README's results section, and identify edition + arch.
2. Fill a comparison table: Home vs Pro vs Enterprise vs Server Datacenter (Hyper-V, BitLocker, RDP host, max RAM, ReFS boot support).
3. Explain WoW64: where do 32-bit binaries live (`SysWOW64` vs `System32`) and why are the names "swapped"?
4. On Linux, compare `uname -m` output on x86_64 vs an ARM board/VM (`aarch64`); note what breaks when moving binaries across them.
5. Server Core vs Desktop Experience: list two admin tasks that require a different toolset on Core (no Explorer) and how PowerShell remoting solves it.
