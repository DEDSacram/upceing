#Requires -Version 5.1
<#
.SYNOPSIS
    Inspect processes and their threads on Windows (student machine).
.DESCRIPTION
    Lists top processes by CPU / working set and shows thread details
    (Id, StartTime, ThreadState, PriorityLevel) for one process.
    Run on Windows:  powershell -ExecutionPolicy Bypass -File Get-ProcessesThreads.ps1 -Top 10 -Name svchost
#>
[CmdletBinding()]
param(
    [int]$Top = 10,
    [string]$Name = "svchost"
)

Write-Host "=== Top $Top processes by CPU ==="
Get-Process | Sort-Object CPU -Descending | Select-Object -First $Top `
    Name, Id, CPU, WorkingSet64, HandleCount, PriorityClass |
    Format-Table -AutoSize | Out-String | Write-Host

Write-Host "=== Top $Top processes by working set ==="
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First $Top `
    Name, Id, WorkingSet64, PagedMemorySize64 |
    Format-Table -AutoSize | Out-String | Write-Host

Write-Host "=== Threads of process '$Name' (first instance) ==="
$proc = Get-Process -Name $Name -ErrorAction SilentlyContinue | Select-Object -First 1
if ($null -eq $proc) {
    Write-Warning "No running process named '$Name'."
} else {
    $proc.Threads | Select-Object Id, StartTime, ThreadState, WaitReason, PriorityLevel |
        Format-Table -AutoSize | Out-String | Write-Host
}

Write-Host "=== Current process affinity / priority ==="
$me = Get-Process -Id $PID
$me | Select-Object Name, Id, PriorityClass, ProcessorAffinity | Format-List | Out-String | Write-Host
