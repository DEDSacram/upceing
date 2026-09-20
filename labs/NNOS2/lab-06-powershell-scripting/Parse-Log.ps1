#Requires -Version 5.1
<#
.SYNOPSIS
    Parse a log file and count lines by severity (INFO/WARN/ERROR).
.DESCRIPTION
    Linux-verifiable twin: parse_log.py implements the same logic.
    Run on Windows:  powershell -ExecutionPolicy Bypass -File Parse-Log.ps1 -Path .\sample.log
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Path,

    [string]$Pattern = '\b(INFO|WARN|ERROR)\b'
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path $Path)) { Write-Error "File not found: $Path"; exit 1 }

$counts = @{ INFO = 0; WARN = 0; ERROR = 0 }
$errors = @()
foreach ($line in Get-Content $Path) {
    if ($line -match $Pattern) {
        $level = $Matches[1]
        $counts[$level]++
        if ($level -eq "ERROR") { $errors += $line }
    }
}
Write-Host "=== Summary for $Path ==="
$counts.GetEnumerator() | Sort-Object Name | Format-Table -AutoSize Name, Value |
    Out-String | Write-Host
if ($errors.Count -gt 0) {
    Write-Host "=== ERROR lines ==="
    $errors | Write-Host
}
