#Requires -Version 5.1
<#
.SYNOPSIS
    Registry read/write demo under HKCU:\Software\NNOS2Lab (no admin needed).
.DESCRIPTION
    Creates the key, writes String/DWord values, reads them back, increments
    the counter, then optionally removes the key.
    Run on Windows:  powershell -ExecutionPolicy Bypass -File Registry-Demo.ps1 [-Cleanup]
#>
[CmdletBinding()]
param(
    [switch]$Cleanup
)

$ErrorActionPreference = "Stop"
$key = "HKCU:\Software\NNOS2Lab"

if ($Cleanup) {
    Remove-Item -Path $key -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Removed $key"
    return
}

New-Item -Path $key -Force | Out-Null
New-ItemProperty -Path $key -Name "Greeting" -Value "Hello from NNOS2 lab-04" `
    -PropertyType String -Force | Out-Null
New-ItemProperty -Path $key -Name "Counter" -Value 42 `
    -PropertyType DWord -Force | Out-Null

Write-Host "=== Values after write ==="
Get-ItemProperty -Path $key | Select-Object Greeting, Counter | Format-List |
    Out-String | Write-Host

$c = (Get-ItemProperty -Path $key).Counter + 1
Set-ItemProperty -Path $key -Name "Counter" -Value $c
Write-Host "Counter incremented to $c"

Write-Host "=== reg.exe view ==="
reg query HKCU\Software\NNOS2Lab

Write-Host "Done. Re-run with -Cleanup to remove the key."
