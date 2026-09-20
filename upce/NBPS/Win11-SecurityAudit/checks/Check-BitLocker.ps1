# Check-BitLocker.ps1
#Requires -Version 5.1
function New-AuditResult {
    param([string]$Kategorie, [string]$Kontrola, [string]$Stav, [string]$Komentar)
    [pscustomobject]@{ Kategorie = $Kategorie; Kontrola = $Kontrola; Stav = $Stav; Komentar = $Komentar }
}
function Invoke-BitLockerCheck {
    $vysledky = @(); $kat = 'Sifrovani a BitLocker'
    try {
        $vols = Get-BitLockerVolume -ErrorAction Stop
        $sys = @($vols | Where-Object { $_.VolumeType -eq 'OperatingSystem' })
        if ($sys.Count -eq 0) { $vysledky += New-AuditResult $kat 'BitLocker systemovy disk' 'Info' 'Systemovy svazek nenalezen.' }
        foreach ($v in $sys) {
            if ($v.ProtectionStatus -eq 'On') { $vysledky += New-AuditResult $kat "BitLocker $($v.MountPoint)" 'OK' "Zapnuto, zasifrovano $($v.EncryptionPercentage)%." }
            else { $vysledky += New-AuditResult $kat "BitLocker $($v.MountPoint)" 'Riziko' "ProtectionStatus=$($v.ProtectionStatus), $($v.EncryptionPercentage)%. Zapnete BitLocker." }
            $tpmProt = @($v.KeyProtector | Where-Object { $_.KeyProtectorType -eq 'Tpm' })
            if (@($v.KeyProtector).Count -eq 0) { $vysledky += New-AuditResult $kat "Klic $(${v}.MountPoint)" 'Varovani' 'Zadny key protector.' }
            elseif ($tpmProt.Count -gt 0) { $vysledky += New-AuditResult $kat "Klic $($v.MountPoint) TPM" 'OK' 'TPM protector pritomen.' }
            else { $typy = (($v.KeyProtector | ForEach-Object { $_.KeyProtectorType }) -join ', '); $vysledky += New-AuditResult $kat "Klic $($v.MountPoint)" 'Varovani' "Bez TPM ($typy). Doporuceno TPM+PIN." }
        }
        $data = @($vols | Where-Object { $_.VolumeType -eq 'FixedData' })
        foreach ($v in $data) {
            if ($v.ProtectionStatus -eq 'On') { $vysledky += New-AuditResult $kat "BitLocker $($v.MountPoint)" 'OK' "Datovy disk sifrovan ($($v.EncryptionPercentage)%)." }
            else { $vysledky += New-AuditResult $kat "BitLocker $($v.MountPoint)" 'Varovani' "Datovy disk nesifrovan." }
        }
    } catch { $vysledky += New-AuditResult $kat 'BitLocker' 'Info' "Get-BitLockerVolume selhal (pravdepodobne edice bez BitLockeru nebo bez admin prav): $($_.Exception.Message)" }
    try {
        $tpm = Get-Tpm -ErrorAction Stop
        if ($tpm.TpmPresent) {
            if ($tpm.TpmReady -and $tpm.TpmEnabled) { $vysledky += New-AuditResult $kat 'TPM' 'OK' 'TPM pritomen, povolen a pripraven.' }
            else { $vysledky += New-AuditResult $kat 'TPM' 'Varovani' "Present=True, Enabled=$($tpm.TpmEnabled), Ready=$($tpm.TpmReady). Dokoncete inicializaci v BIOS/tpm.msc." }
        } else { $vysledky += New-AuditResult $kat 'TPM' 'Riziko' 'TPM nenalezen. Sifrovani a Secure Boot omezeny.' }
    } catch { $vysledky += New-AuditResult $kat 'TPM' 'Info' "Get-Tpm selhal: $($_.Exception.Message)" }
    return $vysledky
}
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-BitLockerCheck | Format-Table -AutoSize -Property @{n='Kontrola';e={$_.Kontrola}}, @{n='Stav';e={$_.Stav}}, @{n='Komentar';e={$_.Komentar}}
}
