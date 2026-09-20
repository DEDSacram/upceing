# Check-Services.ps1
#Requires -Version 5.1
function New-AuditResult {
    param([string]$Kategorie, [string]$Kontrola, [string]$Stav, [string]$Komentar)
    [pscustomobject]@{ Kategorie = $Kategorie; Kontrola = $Kontrola; Stav = $Stav; Komentar = $Komentar }
}
function Invoke-ServicesCheck {
    $vysledky = @(); $kat = 'Sluzby a protokoly'
    # SMBv1
    try {
        $feat = Get-WindowsOptionalFeature -Online -FeatureName 'SMB1Protocol' -ErrorAction SilentlyContinue
        if ($feat -and $feat.State -eq 'Enabled') { $vysledky += New-AuditResult $kat 'Protokol SMBv1' 'Riziko' 'SMB1Protocol je nainstalovan/povolen. Odinstalujte (zranitelnost typu WannaCry).' }
        else { $vysledky += New-AuditResult $kat 'Protokol SMBv1' 'OK' 'SMBv1 neni povolen.' }
    } catch { $vysledky += New-AuditResult $kat 'Protokol SMBv1' 'Info' "Nelze overit feature SMB1Protocol (vyzaduje administratora): $($_.Exception.Message)" }
    try {
        $cfg = Get-SmbServerConfiguration -ErrorAction SilentlyContinue
        if ($cfg -and $cfg.EnableSMB1Protocol) { $vysledky += New-AuditResult $kat 'SMB server: SMB1' 'Riziko' 'EnableSMB1Protocol = True. Vypnete: Set-SmbServerConfiguration -EnableSMB1Protocol $false.' }
        elseif ($cfg) { $vysledky += New-AuditResult $kat 'SMB server: SMB1' 'OK' 'EnableSMB1Protocol = False.' }
    } catch { }
    # Telnet klient
    try {
        $t = Get-WindowsOptionalFeature -Online -FeatureName 'TelnetClient' -ErrorAction SilentlyContinue
        if ($t -and $t.State -eq 'Enabled') { $vysledky += New-AuditResult $kat 'Telnet klient' 'Varovani' 'TelnetClient nainstalovan (nesifrovany protokol). Odinstalujte pokud nepotrebujete.' }
        else { $vysledky += New-AuditResult $kat 'Telnet klient' 'OK' 'Telnet klient neni nainstalovan.' }
    } catch { }
    # Nebezpecne sluzby
    $rizikove = @('TlntSvr','RemoteRegistry','SSDPSRV','upnphost','SNMP','Telnet')
    foreach ($s in $rizikove) {
        try {
            $svc = Get-Service -Name $s -ErrorAction SilentlyContinue
            if ($svc) {
                if ($svc.Status -eq 'Running') { $vysledky += New-AuditResult $kat "Sluzba $s" 'Varovani' "Bezi (StartType=$($svc.StartType)). Zvazte zakazani." }
                elseif ($svc.StartType -eq 'Automatic') { $vysledky += New-AuditResult $kat "Sluzba $s" 'Varovani' "Automaticky start, momentalne $($svc.Status)." }
                else { $vysledky += New-AuditResult $kat "Sluzba $s" 'OK' "$($svc.Status), StartType=$($svc.StartType)." }
            }
        } catch { }
    }
    # RDP
    try {
        $deny = (Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server' -Name 'fDenyTSConnections' -ErrorAction Stop).fDenyTSConnections
        $term = Get-Service -Name 'TermService' -ErrorAction SilentlyContinue
        if ($deny -eq 0) { $vysledky += New-AuditResult $kat 'Vzdalena plocha (RDP)' 'Varovani' "Povolena (fDenyTSConnections=0, TermService=$($term.Status)). Omezte firewall/NLA, pouzijte VPN." }
        else { $vysledky += New-AuditResult $kat 'Vzdalena plocha (RDP)' 'OK' 'RDP zakazano (fDenyTSConnections=1).' }
        $nla = (Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name 'UserAuthentication' -ErrorAction SilentlyContinue).UserAuthentication
        if ($deny -eq 0) {
            if ($nla -eq 1) { $vysledky += New-AuditResult $kat 'RDP NLA' 'OK' 'Network Level Authentication zapnuto.' }
            else { $vysledky += New-AuditResult $kat 'RDP NLA' 'Riziko' 'NLA vypnuto nebo nezjisteno. Zapnete.' }
        }
    } catch { $vysledky += New-AuditResult $kat 'Vzdalena plocha (RDP)' 'Info' $_.Exception.Message }
    # PowerShell v2 (zastaraly)
    try {
        $psv2 = Get-WindowsOptionalFeature -Online -FeatureName 'MicrosoftWindowsPowerShellV2Root' -ErrorAction SilentlyContinue
        if ($psv2 -and $psv2.State -eq 'Enabled') { $vysledky += New-AuditResult $kat 'PowerShell v2' 'Varovani' 'PSv2 povolen (zastaraly, zneuzivan utocniky). Odinstalujte.' }
        else { $vysledky += New-AuditResult $kat 'PowerShell v2' 'OK' 'PSv2 neni povolen.' }
    } catch { }
    return $vysledky
}
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-ServicesCheck | Format-Table -AutoSize -Property @{n='Kontrola';e={$_.Kontrola}}, @{n='Stav';e={$_.Stav}}, @{n='Komentar';e={$_.Komentar}}
}
