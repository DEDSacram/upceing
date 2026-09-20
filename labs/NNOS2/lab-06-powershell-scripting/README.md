# Lab 06 — PowerShell Scripting (service manager, log parser, backup)

Three small scripts with `param()` + error handling; Python twins verify the logic on Linux. (No Windows host here, so `.ps1` files are authored carefully but **not executed** — see §4.)

## 1. Theory

- **Script anatomy:** `param()` block (types, `[Parameter(Mandatory)]`, `[ValidateSet()]`), `$ErrorActionPreference = "Stop"` (turn non-terminating errors into catchable ones), `try/catch`, `Write-Host` vs `Write-Error` + `exit 1`. Advanced functions add `[CmdletBinding()]` → free `-Verbose`, `-WhatIf` (via `SupportsShouldProcess`).
- **Piping objects, not text:** `Get-Service | Where-Object {…} | Select-Object Name,Status` passes .NET objects; `Format-Table` is for display only (never pipe after it).
- **The three scripts:** `Manage-Service.ps1` (Status/Start/Stop/Restart with `ShouldProcess` + friendly "not found" error), `Parse-Log.ps1` (regex `-match` over lines, counts per severity, collects ERROR lines), `Backup-Files.ps1` (`Compress-Archive` to timestamped ZIP, validates source/destination, `exit 1` on failure).
- **Linux twins:** `parse_log.py` and `backup.py` implement identical logic (same CLI shape, same summary format) so the algorithms are testable here. `Manage-Service.ps1` has no Linux twin (Windows SCM-specific); its review is by reading.

## 2. Project layout

```
lab-06-powershell-scripting/
  Manage-Service.ps1  # service Start/Stop/Restart/Status (Windows only)
  Parse-Log.ps1       # severity counter over a log file (Windows)
  Backup-Files.ps1    # timestamped ZIP backup (Windows)
  sample.log          # shared fixture for both Parse-Log.ps1 and parse_log.py
  parse_log.py        # Linux twin of Parse-Log.ps1 (runs here)
  backup.py           # Linux twin of Backup-Files.ps1 (runs here)
  README.md
```

## 3. Run

```powershell
# On a student Windows machine:
powershell -ExecutionPolicy Bypass -File Manage-Service.ps1 -Name wuauserv -Action Status
powershell -ExecutionPolicy Bypass -File Parse-Log.ps1 -Path .\sample.log
powershell -ExecutionPolicy Bypass -File Backup-Files.ps1 -Source C:\Data -Destination C:\Backup
```

```bash
# On Linux (verifiable here):
cd lab-06-powershell-scripting
python3 parse_log.py sample.log
mkdir -p demodata && echo hello > demodata/a.txt
python3 backup.py demodata /tmp/nnos2backup
```

## 4. Verify

1. ⚠️ `.ps1` scripts were **not executed** — no PowerShell/`pwsh` exists on this Linux host (`which pwsh` → not found). They were authored against PowerShell 5.1 conventions (`#Requires`, `CmdletBinding`, `ShouldProcess`) and cross-checked with the Python twins; students must run them on Windows.
2. `python3 parse_log.py sample.log` prints `INFO: 4, WARN: 2, ERROR: 2` plus the two ERROR lines, exit code `0`.
3. `python3 backup.py demodata <dest>` prints `Backup OK: <dest>/demodata-<stamp>.zip (<N> bytes)`, and the ZIP extracts to the original files.
4. `python3 backup.py /nonexistent <dest>` exits `1` with `Source not found` (error path works).

## 5. Tasks

1. On Windows: run all three `.ps1` scripts; paste outputs and note any syntax fixes needed (report back — the Linux host couldn't check!).
2. Extend `Parse-Log.ps1` with a `-Level` filter (`ERROR` only) and a `-Tail N` option; mirror it in `parse_log.py` and test here.
3. Add `-WhatIf` support to `Backup-Files.ps1` (`SupportsShouldProcess`) so dry runs print the ZIP name without creating it.
4. Make `Manage-Service.ps1` accept pipeline input (`ValueFromPipelineByPropertyName`) so `Get-Service w* | .\Manage-Service.ps1 -Action Status` works.
5. Schedule `Backup-Files.ps1` with Task Scheduler (`New-ScheduledTaskAction` + `Register-ScheduledTask`) for a daily run; export the task XML.
