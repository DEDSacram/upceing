#Requires -Version 5.1
<#
.SYNOPSIS
    NTFS ACL demo with icacls (student machine, Windows).
.DESCRIPTION
    Creates .\AclDemo\secret.txt, shows its ACL, grants/denies a user,
    then restores. Run on Windows in an elevated or normal prompt:
      powershell -ExecutionPolicy Bypass -File Get-AclDemo.ps1 -User Everyone
#>
[CmdletBinding()]
param(
    [string]$User = "Everyone",
    [string]$Dir = "AclDemo"
)

$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $Dir | Out-Null
$file = Join-Path $Dir "secret.txt"
"top secret" | Set-Content $file

Write-Host "=== Initial ACL ==="
icacls $file

Write-Host "=== Grant ${User}:R (read) ==="
icacls $file /grant "${User}:R"

Write-Host "=== Deny ${User}:W (write) ==="
icacls $file /deny "${User}:W"

Write-Host "=== Resulting ACL ==="
icacls $file

Write-Host "=== PowerShell view (Get-Acl) ==="
(Get-Acl $file).Access | Format-Table IdentityReference, FileSystemRights, AccessControlType -AutoSize |
    Out-String | Write-Host

Write-Host "=== Cleanup: remove explicit rules, show ACL ==="
icacls $file /remove:d $User
icacls $file /remove:g $User
icacls $file
Write-Host "Demo files left in .\$Dir (delete manually if desired)."
