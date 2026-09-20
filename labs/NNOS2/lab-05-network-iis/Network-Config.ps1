#Requires -Version 5.1
#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Network inspection + static IP configuration on Windows (ADMIN required).
.DESCRIPTION
    Read-only part: adapter list, IP config, routing table, connectivity tests.
    Config part (commented by default): set a static IP with New-NetIPAddress.
    Run on Windows:  powershell -ExecutionPolicy Bypass -File Network-Config.ps1
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$AdapterAlias = "Ethernet",
    [string]$StaticIP = "192.168.10.50",
    [int]$PrefixLength = 24,
    [string]$Gateway = "192.168.10.1",
    [switch]$ApplyStatic
)

Write-Host "=== Adapters ==="
Get-NetAdapter | Select-Object Name, Status, LinkSpeed, MacAddress |
    Format-Table -AutoSize | Out-String | Write-Host

Write-Host "=== IP configuration ==="
Get-NetIPConfiguration | Select-Object InterfaceAlias, IPv4Address, IPv4DefaultGateway, DNSServer |
    Format-List | Out-String | Write-Host

Write-Host "=== Routing table (IPv4) ==="
Get-NetRoute -AddressFamily IPv4 | Sort-Object RouteMetric |
    Select-Object DestinationPrefix, NextHop, RouteMetric, InterfaceAlias |
    Format-Table -AutoSize | Out-String | Write-Host

Write-Host "=== Connectivity ==="
Test-Connection -ComputerName 127.0.0.1 -Count 2 | Select-Object Address, ResponseTime |
    Format-Table -AutoSize | Out-String | Write-Host

if ($ApplyStatic) {
    if ($PSCmdlet.ShouldProcess("$AdapterAlias", "set static IP $StaticIP/$PrefixLength")) {
        # Classic netsh equivalent:
        #   netsh interface ip set address "$AdapterAlias" static $StaticIP 255.255.255.0 $Gateway
        New-NetIPAddress -InterfaceAlias $AdapterAlias -IPAddress $StaticIP `
            -PrefixLength $PrefixLength -DefaultGateway $Gateway -ErrorAction Stop
        Write-Host "Static IP $StaticIP/$PrefixLength set on $AdapterAlias"
    }
} else {
    Write-Host "(Static-IP part skipped; re-run with -ApplyStatic to apply.)"
    Write-Host " Equivalent netsh: netsh interface ip set address `"$AdapterAlias`" static $StaticIP 255.255.255.0 $Gateway"
}
