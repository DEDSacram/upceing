# Lab 04 — Windows Registry

Hive/key/value model, `.reg` import file, PowerShell read/write demo, Linux INI-file counterpart that runs here.

## 1. Theory

- **Model:** configuration database of *hives* → *keys* (paths) → *values* (name + type + data). Root hives: `HKLM` (machine-wide, admin), `HKCU` (per-user, no admin), `HKCR` (file associations = merged view), `HKU`, `HKCC`. Common types: `REG_SZ` (string), `REG_DWORD` (32-bit int), `REG_QWORD`, `REG_BINARY`, `REG_MULTI_SZ`, `REG_EXPAND_SZ` (`%SystemRoot%`-style expansion).
- **Tools:** `regedit.exe` (GUI), `reg query/add/delete` (CLI), PowerShell provider (`HKCU:\…`, `Get/Set/New-ItemProperty`), `.reg` files (`Windows Registry Editor Version 5.00` header; `dword:0000002a` = hex 42; `-` prefix deletes).
- **Safety:** `HKCU\Software\…` is per-user and safe for experiments; `HKLM\SYSTEM` can brick boot — always export (`reg export`) before editing. 32/64-bit views redirect (`Wow6432Node`).
- **Linux analogue:** no central registry — per-app config files (`~/.config/`, `/etc/`). `registry_counterpart.sh` mimics `HKCU\Software\NNOS2Lab` with an INI-style file and `key=value` get/set helpers.

## 2. Project layout

```
lab-04-registry/
  registry-demo.reg       # imports HKCU\Software\NNOS2Lab (Greeting + Counter=42) on Windows
  Registry-Demo.ps1       # New/Get/Set-ItemProperty + reg.exe view + -Cleanup (run on Windows)
  registry_counterpart.sh # Linux counterpart: INI store with kv_set/kv_get (runs here)
  README.md
```

## 3. Run

```powershell
# On a student Windows machine (no admin needed, HKCU):
reg import registry-demo.reg
powershell -ExecutionPolicy Bypass -File Registry-Demo.ps1
powershell -ExecutionPolicy Bypass -File Registry-Demo.ps1 -Cleanup
```

```bash
# On Linux (verifiable here):
cd lab-04-registry
bash registry_counterpart.sh
```

## 4. Verify

1. On Windows: `.reg` import succeeds; script prints `Greeting` + `Counter`, increments the counter, `reg query` shows both values; `-Cleanup` removes the key.
2. On Linux: `bash registry_counterpart.sh` prints the store, `Counter incremented to 43`, ends with `Linux counterpart: OK`, exit code `0`.
3. You can name the type of each value (`REG_SZ` vs `REG_DWORD`) and where the `.reg` hex `2a` maps to decimal 42.

## 5. Tasks

1. Add a `REG_QWORD` and a `REG_MULTI_SZ` value via PowerShell; read them back and show their types.
2. Export your key (`reg export HKCU\Software\NNOS2Lab backup.reg`), delete it, re-import — confirm round-trip.
3. Run `Get-ItemProperty` on a `Wow6432Node` path from 32-bit vs 64-bit PowerShell; explain redirection.
4. Extend the Linux counterpart with a `kv_del` (delete key) matching `Remove-ItemProperty`; test it.
5. Find where a real app stores a setting (e.g. PuTTY sessions under `HKCU\Software\SimonTatham`) and document the key path + types.
