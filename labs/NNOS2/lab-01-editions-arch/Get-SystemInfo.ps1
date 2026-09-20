#Requires -Version 5.1
<#
.SYNOPSIS
    Collect basic Windows edition + hardware architecture info (student machine).
.DESCRIPTION
    Uses Get-ComputerInfo (Windows 10/11, Server 2016+) and falls back to
    WMI/CIM when Get-ComputerInfo is unavailable. Saves a summary to a text file.
    Run on Windows:  powershell -ExecutionPolicy Bypass -File Get-SystemInfo.ps1
#>
[CmdletBinding()]
param(
    [string]$OutFile = "systeminfo.txt"
)

$info = @{}
try {
    $ci = Get-ComputerInfo -ErrorAction Stop
    $info['WindowsProductName'] = $ci.WindowsProductName
    $info['WindowsEditionId']   = $ci.WindowsEditionId
    $info['WindowsVersion']     = $ci.WindowsVersion
    $info['OsArchitecture']     = $ci.OsArchitecture
    $info['CsProcessors']       = ($ci.CsProcessors | Select-Object -ExpandProperty Name) -join '; '
    $info['CsTotalPhysicalMemory'] = $ci.CsTotalPhysicalMemory
    $info['BiosFirmwareType']   = $ci.BiosFirmwareType
} catch {
    Write-Warning "Get-ComputerInfo failed ($($_.Exception.Message)); falling back to CIM."
    $os = Get-CimInstance Win32_OperatingSystem
    $cs = Get-CimInstance Win32_ComputerSystem
    $info['WindowsProductName'] = $os.Caption
    $info['WindowsEditionId']   = 'n/a (fallback)'
    $info['WindowsVersion']     = $os.Version
    $info['OsArchitecture']     = $os.OSArchitecture
    $info['CsProcessors']       = ($cs | Select-Object -ExpandProperty Model) -join '; '
    $info['CsTotalPhysicalMemory'] = $cs.TotalPhysicalMemory
    $info['BiosFirmwareType']   = 'n/a (fallback)'
}

$lines = foreach ($k in $info.Keys) { "{0,-24}: {1}" -f $k, $info[$k] }
$lines | Tee-Object -FilePath $OutFile
Write-Host "Saved to $OutFile"
