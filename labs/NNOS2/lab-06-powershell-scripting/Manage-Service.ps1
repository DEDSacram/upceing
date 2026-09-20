#Requires -Version 5.1
<#
.SYNOPSIS
    Start/stop/restart a Windows service safely.
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File Manage-Service.ps1 -Name wuauserv -Action Status
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)]
    [string]$Name,

    [ValidateSet("Status", "Start", "Stop", "Restart")]
    [string]$Action = "Status"
)

$ErrorActionPreference = "Stop"
try {
    $svc = Get-Service -Name $Name -ErrorAction Stop
} catch {
    Write-Error "Service '$Name' not found. Available match: $(Get-Service | Where-Object { $_.Name -like "*$Name*" } | Select-Object -ExpandProperty Name | Select-Object -First 5)"
    exit 1
}

switch ($Action) {
    "Status" {
        $svc | Select-Object Name, Status, StartType | Format-List | Out-String | Write-Host
    }
    "Start" {
        if ($svc.Status -eq "Running") { Write-Host "'$Name' already running."; break }
        if ($PSCmdlet.ShouldProcess($Name, "Start service")) {
            Start-Service -Name $Name -ErrorAction Stop
            Write-Host "'$Name' started."
        }
    }
    "Stop" {
        if ($svc.Status -eq "Stopped") { Write-Host "'$Name' already stopped."; break }
        if ($PSCmdlet.ShouldProcess($Name, "Stop service")) {
            Stop-Service -Name $Name -Force -ErrorAction Stop
            Write-Host "'$Name' stopped."
        }
    }
    "Restart" {
        if ($PSCmdlet.ShouldProcess($Name, "Restart service")) {
            Restart-Service -Name $Name -Force -ErrorAction Stop
            Write-Host "'$Name' restarted."
        }
    }
}
