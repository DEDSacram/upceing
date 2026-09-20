# Check-WindowsUpdate.ps1
#Requires -Version 5.1
function New-AuditResult {
    param([string]$Kategorie, [string]$Kontrola, [string]$Stav, [string]$Komentar)
    [pscustomobject]@{ Kategorie = $Kategorie; Kontrola = $Kontrola; Stav = $Stav; Komentar = $Komentar }
}
function Invoke-WindowsUpdateCheck {
    $vysledky = @(); $kat = 'Windows Update'
    # Sluzba wuauserv
    try {
        $svc = Get-Service -Name 'wuauserv' -ErrorAction Stop
        if ($svc.Status -eq 'Running') { $vysledky += New-AuditResult $kat 'Sluzba Windows Update' 'OK' 'wuauserv bezi.' }
        else { $vysledky += New-AuditResult $kat 'Sluzba Windows Update' 'Varovani' "wuauserv = $($svc.Status) (StartType=$($svc.StartType))." }
    } catch { $vysledky += New-AuditResult $kat 'Sluzba Windows Update' 'Info' $_.Exception.Message }
    # Posledni uspesna instalace z registru
    try {
        $r = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\Results\Install' -ErrorAction Stop
        $last = $r.LastSuccessTime
        if ($last) {
            $age = (New-TimeSpan -Start ([datetime]$last) -End (Get-Date)).Days
            if ($age -le 35) { $vysledky += New-AuditResult $kat 'Posledni instalace aktualizaci' 'OK' "Posledni uspech: $last (pred $age dny)." }
            else { $vysledky += New-AuditResult $kat 'Posledni instalace aktualizaci' 'Varovani' "Posledni uspech: $last (pred $age dny > 35). Zkontrolujte aktualizace." }
        } else { $vysledky += New-AuditResult $kat 'Posledni instalace aktualizaci' 'Info' 'LastSuccessTime prazdne.' }
    } catch { $vysledky += New-AuditResult $kat 'Posledni instalace aktualizaci' 'Info' "Nelze cist registr: $($_.Exception.Message)" }
    # Posledni HotFix
    try {
        $hf = Get-HotFix | Where-Object { $_.InstalledOn -is [datetime] } | Sort-Object InstalledOn -Descending | Select-Object -First 1
        if ($hf -and $hf.InstalledOn) {
            $age = (New-TimeSpan -Start $hf.InstalledOn -End (Get-Date)).Days
            $msg = "$($hf.HotFixID) z $($hf.InstalledOn) (pred $age dny)."
            if ($age -le 45) { $vysledky += New-AuditResult $kat 'Posledni bezpecnostni zaplata (HotFix)' 'OK' $msg }
            else { $vysledky += New-AuditResult $kat 'Posledni bezpecnostni zaplata (HotFix)' 'Varovani' "$msg Aktualizace jsou pravdepodobne zastarale." }
        } else { $vysledky += New-AuditResult $kat 'Posledni bezpecnostni zaplata (HotFix)' 'Info' 'Zadne HotFix nenalezeny.' }
    } catch { $vysledky += New-AuditResult $kat 'Posledni bezpecnostni zaplata (HotFix)' 'Info' $_.Exception.Message }
    # Chybejici aktualizace pres COM (s timeout ochranou)
    try {
        $session = New-Object -ComObject Microsoft.Update.Session
        $searcher = $session.CreateUpdateSearcher()
        $res = $searcher.Search("Type='Software' and IsInstalled=0")
        $pending = @($res.Updates)
        $crit = @($pending | Where-Object { $_.MsrcSeverity -eq 'Critical' })
        if ($pending.Count -eq 0) { $vysledky += New-AuditResult $kat 'Chybejici aktualizace' 'OK' 'System hlasi 0 neinstalovanych softwarovych aktualizaci.' }
        elseif ($crit.Count -gt 0) { $vysledky += New-AuditResult $kat 'Chybejici aktualizace' 'Riziko' "Chybi $($pending.Count) aktualizaci, z toho $($crit.Count) kritickych. Nainstalujte je." }
        else { $vysledky += New-AuditResult $kat 'Chybejici aktualizace' 'Varovani' "Chybi $($pending.Count) aktualizaci (zadna kriticka)." }
    } catch { $vysledky += New-AuditResult $kat 'Chybejici aktualizace' 'Info' "COM vyhledavani selhalo: $($_.Exception.Message)" }
    return $vysledky
}
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-WindowsUpdateCheck | Format-Table -AutoSize -Property @{n='Kontrola';e={$_.Kontrola}}, @{n='Stav';e={$_.Stav}}, @{n='Komentar';e={$_.Komentar}}
}
