# Check-Network.ps1
#Requires -Version 5.1
function New-AuditResult {
    param([string]$Kategorie, [string]$Kontrola, [string]$Stav, [string]$Komentar)
    [pscustomobject]@{ Kategorie = $Kategorie; Kontrola = $Kontrola; Stav = $Stav; Komentar = $Komentar }
}
function Invoke-NetworkCheck {
    $vysledky = @(); $kat = 'Sit'
    # Otevrene TCP porty (LISTEN)
    try {
        $listen = Get-NetTCPConnection -State Listen -ErrorAction Stop
        $ports = $listen | Sort-Object LocalPort -Unique
        $rizikove = @{ 21='FTP'; 23='Telnet'; 445='SMB'; 3389='RDP'; 5900='VNC'; 1433='MSSQL'; 3306='MySQL' }
        $nalezeno = @()
        foreach ($r in $rizikove.Keys) { if ($ports.LocalPort -contains $r) { $nalezeno += "$r ($($rizikove[$r]))" } }
        $pocet = @($ports).Count
        $seznam = (($ports | Select-Object -First 20 | ForEach-Object { $_.LocalPort }) -join ', ')
        if ($nalezeno.Count -gt 0) { $vysledky += New-AuditResult $kat 'Otevrene porty (TCP Listen)' 'Varovani' "Celkem $pocet. Rizikove: $($nalezeno -join ', '). Prvnich 20: $seznam" }
        elseif ($pocet -gt 30) { $vysledky += New-AuditResult $kat 'Otevrene porty (TCP Listen)' 'Varovani' "Mnoho otevrenych portu ($pocet): $seznam" }
        else { $vysledky += New-AuditResult $kat 'Otevrene porty (TCP Listen)' 'OK' "Celkem $pocet. Porty: $seznam" }
    } catch { $vysledky += New-AuditResult $kat 'Otevrene porty (TCP Listen)' 'Info' $_.Exception.Message }
    # Firewall profily
    try {
        $fw = Get-NetFirewallProfile -ErrorAction Stop
        foreach ($p in $fw) {
            if ($p.Enabled) { $vysledky += New-AuditResult $kat "Firewall $($p.Name)" 'OK' "Zapnut, vychozi prichozi: $($p.DefaultInboundAction)." }
            else { $vysledky += New-AuditResult $kat "Firewall $($p.Name)" 'Riziko' 'Profil vypnut!' }
        }
    } catch { $vysledky += New-AuditResult $kat 'Windows Firewall' 'Info' $_.Exception.Message }
    # VPN
    try {
        $vpn = Get-VpnConnection -AllUserConnection -ErrorAction SilentlyContinue
        if (-not $vpn) { $vpn = Get-VpnConnection -ErrorAction SilentlyContinue }
        if ($vpn -and @($vpn).Count -gt 0) { $vysledky += New-AuditResult $kat 'VPN pripojeni' 'OK' "Nalezeno $(@($vpn).Count): $((@($vpn) | ForEach-Object { $_.Name }) -join ', ')" }
        else { $vysledky += New-AuditResult $kat 'VPN pripojeni' 'Info' 'Zadne VPN pripojeni nenalezeno.' }
    } catch { $vysledky += New-AuditResult $kat 'VPN pripojeni' 'Info' $_.Exception.Message }
    # Proxy
    try {
        $px = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -ErrorAction Stop
        if ($px.ProxyEnable -eq 1) { $vysledky += New-AuditResult $kat 'Proxy' 'Varovani' "Proxy zapnuto: $($px.ProxyServer). Overte duveryhodnost." }
        else { $vysledky += New-AuditResult $kat 'Proxy' 'OK' 'Systemovy proxy vypnut.' }
    } catch { $vysledky += New-AuditResult $kat 'Proxy' 'Info' $_.Exception.Message }
    # Wi-Fi sifrovani: zive rozhrani (vyzaduje admin), fallback pres profil pripojene SSID (funguje bez admin)
    try {
        $authLines = @(); $ciphers = @(); $zdroj = ''; $ssid = $null
        # SSID pripojene site (funguje bez admin)
        try {
            $cp = Get-NetConnectionProfile -ErrorAction SilentlyContinue | Where-Object { $_.InterfaceAlias -match 'Wi-?Fi|WLAN|Bezdr' }
            if (-not $cp) {
                $wlanUp = Get-NetAdapter -Physical -ErrorAction SilentlyContinue | Where-Object { $_.MediaType -match '802\.11' -and $_.Status -eq 'Up' }
                if ($wlanUp) { $cp = Get-NetConnectionProfile -InterfaceAlias (@($wlanUp)[0].Name) -ErrorAction SilentlyContinue }
            }
            if ($cp) { $ssid = @($cp)[0].Name }
        } catch { }
        # 1. pokus: zive rozhrani (presny vyjednany typ, ale vyzaduje administratora)
        $ifOut = netsh wlan show interfaces 2>$null
        if ($ifOut -and ($ifOut -match 'WPA3|WPA2|WEP|Open')) {
            $authLines = @($ifOut | Select-String 'Authentication' | ForEach-Object { $_.Line.Trim() })
            if ($authLines.Count -gt 0) { $zdroj = 'zive pripojeni' }
        }
        # 2. pokus: ulozeny profil pripojene SSID (funguje bez administratora)
        if ($authLines.Count -eq 0 -and $ssid) {
            $profOut = netsh wlan show profile name="$ssid" 2>$null
            if ($profOut) {
                $authLines = @($profOut | Select-String 'Authentication' | ForEach-Object { $_.Line.Trim() })
                $ciphers = @($profOut | Select-String 'Cipher' | ForEach-Object { $_.Line.Trim() })
                if ($authLines.Count -gt 0) { $zdroj = "profil site '$ssid'" }
            }
        }
        if ($authLines.Count -gt 0) {
            $auth = (($authLines | Sort-Object -Unique) -join ' | ')
            if ($ciphers.Count -gt 0) { $auth += ' [' + ((($ciphers | Sort-Object -Unique) -join ' | ')) + ']' }
            if ($auth -match 'Open|WEP|\bWPA\b') { $vysledky += New-AuditResult $kat 'Wi-Fi sifrovani' 'Riziko' "$zdroj`: $auth. Nezabezpecena sit!" }
            elseif ($auth -match 'WPA3|WPA2') { $vysledky += New-AuditResult $kat 'Wi-Fi sifrovani' 'OK' "$zdroj`: $auth." }
            else { $vysledky += New-AuditResult $kat 'Wi-Fi sifrovani' 'Info' "$zdroj`: $auth." }
        } elseif ($ssid) {
            $vysledky += New-AuditResult $kat 'Wi-Fi sifrovani' 'Info' "Pripojeno k '$ssid', typ sifrovani nelze zjistit (netsh vyzaduje administratora)."
        } else {
            $vysledky += New-AuditResult $kat 'Wi-Fi sifrovani' 'Info' 'Zadne aktivni Wi-Fi pripojeni.'
        }
    } catch { $vysledky += New-AuditResult $kat 'Wi-Fi sifrovani' 'Info' $_.Exception.Message }
    return $vysledky
}
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-NetworkCheck | Format-Table -AutoSize -Property @{n='Kontrola';e={$_.Kontrola}}, @{n='Stav';e={$_.Stav}}, @{n='Komentar';e={$_.Komentar}}
}
