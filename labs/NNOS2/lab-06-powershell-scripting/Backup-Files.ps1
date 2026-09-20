#Requires -Version 5.1
<#
.SYNOPSIS
    Back up a folder into a timestamped ZIP (params + error handling demo).
.DESCRIPTION
    Linux-verifiable twin: backup.py implements the same logic with zipfile.
    Run on Windows:  powershell -ExecutionPolicy Bypass -File Backup-Files.ps1 -Source C:\Data -Destination C:\Backup
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Source,

    [Parameter(Mandatory)]
    [string]$Destination
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path $Source)) { Write-Error "Source not found: $Source"; exit 1 }
try {
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
} catch {
    Write-Error "Cannot create destination '$Destination': $($_.Exception.Message)"
    exit 1
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$name = (Split-Path $Source -Leaf) + "-$stamp.zip"
$zip = Join-Path $Destination $name
try {
    Compress-Archive -Path (Join-Path $Source "*") -DestinationPath $zip -ErrorAction Stop
} catch {
    Write-Error "Backup failed: $($_.Exception.Message)"
    exit 1
}
$size = (Get-Item $zip).Length
Write-Host "Backup OK: $zip ($size bytes)"
