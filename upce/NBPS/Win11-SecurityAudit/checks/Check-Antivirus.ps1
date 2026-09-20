# Check-Antivirus.ps1
# Samostatne spustitelna kontrola: Antivirovy software
# Vystup: objekty s vlastnostmi Kategorie, Kontrola, Stav, Komentar
# Stav: OK | Varovani | Riziko | Info
#Requires -Version 5.1

function New-AuditResult {
    param([string]$Kategorie, [string]$Kontrola, [string]$Stav, [string]$Komentar)
    [pscustomobject]@{
        Kategorie = $Kategorie
        Kontrola  = $Kontrola
        Stav      = $Stav
        Komentar  = $Komentar
    }
}

function Invoke-AntivirusCheck {
    $vysledky = @()
    $kat = 'Antivirus'

    # 1. Produkty registrovane ve Windows Security Center (Defender i treti strany)
    try {
        $produkty = Get-CimInstance -Namespace 'root/SecurityCenter2' -ClassName 'AntiVirusProduct' -ErrorAction Stop
        if (-not $produkty -or @($produkty).Count -eq 0) {
            $vysledky += New-AuditResult $kat 'Antivirovy produkt nainstalovan' 'Riziko' 'Security Center nehlasi zadny antivirus.'
        } else {
            foreach ($p in @($produkty)) {
                # productState (WSC): napr. 0x61100/0x61110 = zapnuto+aktualni, 0x60100 = zapnuto+zastarele, 0x40000 = vypnuto
                # 3. znak hex retezce = stav (1 = ON), 4. znak = aktualnost (0 = aktualni)
                $hex = '{0:X}' -f $p.productState
                $zapnuto = ($hex.Length -ge 3 -and $hex[2] -eq '1')
                $aktualni = ($hex.Length -ge 4 -and $hex[3] -eq '0')
                if ($zapnuto -and $aktualni) {
                    $vysledky += New-AuditResult $kat "AV produkt: $($p.displayName)" 'OK' "Zapnuto a aktualni (state=$hex, path=$($p.pathToSignedProductExe))."
                } elseif ($zapnuto) {
                    $vysledky += New-AuditResult $kat "AV produkt: $($p.displayName)" 'Varovani' "Zapnuto, ale zastarale signatury (state=$hex). Aktualizujte definice."
                } else {
                    $vysledky += New-AuditResult $kat "AV produkt: $($p.displayName)" 'Riziko' "Vypnuto nebo expirovano (state=$hex). Zapnete ochranu."
                }
            }
        }
    } catch {
        $vysledky += New-AuditResult $kat 'Antivirovy produkt nainstalovan' 'Info' "Nelze cist SecurityCenter2: $($_.Exception.Message)"
    }

    # 2. Windows Defender - detailni stav (Get-MpComputerStatus)
    try {
        $mp = Get-MpComputerStatus -ErrorAction Stop
        # Real-time ochrana
        if ($mp.RealTimeProtectionEnabled) {
            $vysledky += New-AuditResult $kat 'Real-time ochrana (Defender)' 'OK' 'RealTimeProtectionEnabled = True.'
        } else {
            $vysledky += New-AuditResult $kat 'Real-time ochrana (Defender)' 'Riziko' 'Real-time ochrana je vypnuta. Zapnete ji v Zabezpeceni Windows.'
        }
        # Behav. / cloud ochrana pokud dostupna
        if ($mp.PSObject.Properties.Name -contains 'BehaviorMonitorEnabled') {
            if ($mp.BehaviorMonitorEnabled) {
                $vysledky += New-AuditResult $kat 'Behavior Monitor' 'OK' 'Sledovani chovani zapnuto.'
            } else {
                $vysledky += New-AuditResult $kat 'Behavior Monitor' 'Varovani' 'Sledovani chovani vypnuto.'
            }
        }
        # Aktualnost signatur
        $sigAge = $null
        try { $sigAge = (New-TimeSpan -Start $mp.AntivirusSignatureLastUpdated -End (Get-Date)).Days } catch { $sigAge = $null }
        $sigVer = $mp.AntivirusSignatureVersion
        if ($sigAge -ne $null) {
            if ($sigAge -le 7) {
                $vysledky += New-AuditResult $kat 'Aktualnost signatur' 'OK' "Verze $sigVer, stari $sigAge dnu."
            } else {
                $vysledky += New-AuditResult $kat 'Aktualnost signatur' 'Varovani' "Verze $sigVer, stari $sigAge dnu (>7). Spustte Update-MpSignature."
            }
        } else {
            $vysledky += New-AuditResult $kat 'Aktualnost signatur' 'Info' "Verze $sigVer, stari nelze urcit."
        }
        # Quick scan stari
        try {
            $scanAge = (New-TimeSpan -Start $mp.QuickScanStartTime -End (Get-Date)).Days
            if ($scanAge -le 30) {
                $vysledky += New-AuditResult $kat 'Posledni rychly sken' 'OK' "Pred $scanAge dny ($($mp.QuickScanStartTime))."
            } else {
                $vysledky += New-AuditResult $kat 'Posledni rychly sken' 'Varovani' "Pred $scanAge dny. Doporucen sken."
            }
        } catch {
            $vysledky += New-AuditResult $kat 'Posledni rychly sken' 'Info' 'Datum skenu nelze urcit.'
        }
    } catch {
        $vysledky += New-AuditResult $kat 'Windows Defender stav' 'Info' "Get-MpComputerStatus selhal (moznost treti AV nebo nedostatecna prava): $($_.Exception.Message)"
    }

    return $vysledky
}

# Prime spusteni jako skript: vypis tabulku Kontrola/Stav/Komentar
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-AntivirusCheck | Format-Table -AutoSize -Property @{n='Kontrola';e={$_.Kontrola}}, @{n='Stav';e={$_.Stav}}, @{n='Komentar';e={$_.Komentar}}
}
