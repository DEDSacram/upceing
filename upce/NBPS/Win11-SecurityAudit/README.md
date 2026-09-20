# Audit zabezpečení Windows 11 Pro

GUI aplikace v PowerShell (WPF) – výstupní tabulka **Kategorie | Kontrola | Stav | Komentář**.

## Struktura

- `Start-SecurityAudit.ps1` – hlavní GUI aplikace
- `checks/` – samostatné PowerShell skripty pro každou oblast:
  - `Check-Antivirus.ps1` – Defender / jiný AV, real-time ochrana, signatury
  - `Check-WindowsUpdate.ps1` – služba, poslední záplata, chybějící aktualizace
  - `Check-UAC.ps1` – UAC registry, administrátoři, Guest, účty bez hesla
  - `Check-Services.ps1` – SMBv1, Telnet, RDP, rizikové služby, PSv2
  - `Check-BitLocker.ps1` – BitLocker svazky, TPM
  - `Check-Network.ps1` – otevřené porty, firewall, VPN, proxy, Wi-Fi šifrování
- `export/` – CSV/HTML výstupy
- `Spustit-kontrolu.bat` – spouštěč

## Spuštění

1. Klikněte pravým na `Spustit-kontrolu.bat` → **Spustit jako správce**.
2. V okně klikněte **Spustit kontrolu**.
3. Filtrujte podle kategorie, hledejte textem, exportujte do CSV/HTML.

Přímo přes PowerShell:

```powershell
powershell -STA -ExecutionPolicy Bypass -File Start-SecurityAudit.ps1
```

Konzolový režim bez GUI (tabulka do terminálu):

```powershell
powershell -ExecutionPolicy Bypass -File Start-SecurityAudit.ps1 -Console
```

Samostatná kontrola:

```powershell
powershell -ExecutionPolicy Bypass -File checks\Check-Antivirus.ps1
```

## Stavy

- `OK` – zelená, vyhovuje
- `Varovani` – žlutá, doporučeno řešit
- `Riziko` – červená, řešit přednostně
- `Info` – šedá/modrá, nelze zjistit (typicky chybí práva)

## Poznámky

- Pro úplné výsledky (BitLocker, TPM, SecurityCenter) spusťte jako správce.
- Vyhledávání chybějících aktualizací používá `Microsoft.Update.Session` COM – může trvat desítky sekund.
- Testováno na Windows 11 Pro, PowerShell 5.1.
