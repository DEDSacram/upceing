# Check-UAC.ps1
#Requires -Version 5.1
function New-AuditResult {
    param([string]$Kategorie, [string]$Kontrola, [string]$Stav, [string]$Komentar)
    [pscustomobject]@{ Kategorie = $Kategorie; Kontrola = $Kontrola; Stav = $Stav; Komentar = $Komentar }
}
function Invoke-UacCheck {
    $vysledky = @(); $kat = 'Ucty a UAC'
    $reg = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
    try {
        $p = Get-ItemProperty $reg -ErrorAction Stop
        if ($p.EnableLUA -eq 1) { $vysledky += New-AuditResult $kat 'UAC zapnuto (EnableLUA)' 'OK' 'EnableLUA = 1.' }
        else { $vysledky += New-AuditResult $kat 'UAC zapnuto (EnableLUA)' 'Riziko' "EnableLUA = $($p.EnableLUA). UAC je vypnute!" }
        $cpa = $p.ConsentPromptBehaviorAdmin
        $msg = switch ($cpa) { 0 {'0 = nikdy neptat (nevhodne)'} 1 {'1 = heslo na bezpecne plose'} 2 {'2 = souhlas na bezpecne plose (vychozi)'} 3 {'3 = heslo bez bezpecne plochy'} 4 {'4 = souhlas bez bezpecne plochy'} 5 {'5 = souhlas pro ne-Windows binarky (vychozi Win11)'} default {"nezname ($cpa)"} }
        if ($cpa -in @(2,5)) { $vysledky += New-AuditResult $kat 'UAC uroven vyzvy' 'OK' $msg }
        elseif ($cpa -eq 0) { $vysledky += New-AuditResult $kat 'UAC uroven vyzvy' 'Riziko' $msg }
        else { $vysledky += New-AuditResult $kat 'UAC uroven vyzvy' 'Varovani' $msg }
        if ($p.PromptOnSecureDesktop -eq 1) { $vysledky += New-AuditResult $kat 'Bezpecna plocha' 'OK' 'PromptOnSecureDesktop = 1.' }
        else { $vysledky += New-AuditResult $kat 'Bezpecna plocha' 'Varovani' "PromptOnSecureDesktop = $($p.PromptOnSecureDesktop). Doporuceno 1." }
    } catch { $vysledky += New-AuditResult $kat 'Nastaveni UAC' 'Info' $_.Exception.Message }
    # Administratori
    try {
        $admins = Get-LocalGroupMember -Group 'Administrators' -ErrorAction Stop
        $names = ($admins | ForEach-Object { $_.Name }) -join '; '
        if (@($admins).Count -gt 3) { $vysledky += New-AuditResult $kat 'Clenove Administrators' 'Varovani' "Pocet: $(@($admins).Count). $names" }
        else { $vysledky += New-AuditResult $kat 'Clenove Administrators' 'OK' "Pocet: $(@($admins).Count). $names" }
    } catch { $vysledky += New-AuditResult $kat 'Clenove Administrators' 'Info' $_.Exception.Message }
    # Zastarele / docasne / rizikove ucty
    try {
        $users = Get-LocalUser -ErrorAction Stop
        $disabled = @($users | Where-Object { -not $_.Enabled }).Count
        $nopass = @($users | Where-Object { $_.PasswordRequired -eq $false -and $_.Enabled }).Count
        $guest = $users | Where-Object { $_.Name -eq 'Guest' }
        $vysledky += New-AuditResult $kat 'Prehled mistnich uctu' 'OK' "Celkem: $(@($users).Count), zakazanych: $disabled, bez pozadavku na heslo: $nopass."
        if ($guest -and $guest.Enabled) { $vysledky += New-AuditResult $kat 'Ucet Guest' 'Varovani' 'Built-in Guest je povolen. Doporuceno zakazat.' }
        else { $vysledky += New-AuditResult $kat 'Ucet Guest' 'OK' 'Guest je zakazan nebo neexistuje.' }
        if ($nopass -gt 0) {
            $jmena = (($users | Where-Object { $_.PasswordRequired -eq $false -and $_.Enabled }) | ForEach-Object { $_.Name }) -join ', '
            $vysledky += New-AuditResult $kat 'Ucty bez hesla' 'Riziko' "Povolene ucty bez hesla: $jmena"
        } else { $vysledky += New-AuditResult $kat 'Ucty bez hesla' 'OK' 'Zadne povolene ucty bez pozadavku na heslo.' }
        try {
            $old = @($users | Where-Object { $_.Enabled -and $_.LastLogon -and ((New-TimeSpan -Start $_.LastLogon -End (Get-Date)).Days -gt 90) })
            if ($old.Count -gt 0) { $vysledky += New-AuditResult $kat 'Neaktivni ucty (>90 dnu)' 'Varovani' (($old | ForEach-Object { $_.Name }) -join ', ') }
            else { $vysledky += New-AuditResult $kat 'Neaktivni ucty (>90 dnu)' 'OK' 'Zadne.' }
        } catch { }
    } catch { $vysledky += New-AuditResult $kat 'Mistni ucty' 'Info' $_.Exception.Message }
    return $vysledky
}
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-UacCheck | Format-Table -AutoSize -Property @{n='Kontrola';e={$_.Kontrola}}, @{n='Stav';e={$_.Stav}}, @{n='Komentar';e={$_.Komentar}}
}
