# Lab 05 — Networking & IIS

Windows network inspection/config (`Get-NetAdapter`, `netsh`, `New-NetIPAddress`), IIS setup notes, Linux `ip`/`ss` counterpart that runs here.

## 1. Theory

- **Windows network stack:** adapters (`Get-NetAdapter`), IP config (`Get-NetIPConfiguration`), routes (`Get-NetRoute`), firewall (`Get-NetFirewallRule`, `New-NetFirewallRule`), DNS (`Resolve-DnsName`). Legacy CLI `netsh interface ip …` still works; modern PowerShell cmdlets are `*-NetAdapter`, `New-NetIPAddress`, `Set-DnsClientServerAddress`.
- **Static IP recipe:** pick adapter alias → `New-NetIPAddress -InterfaceAlias Ethernet -IPAddress 192.168.10.50 -PrefixLength 24 -DefaultGateway 192.168.10.1` → set DNS → verify with `Test-Connection`. Needs an elevated prompt; `-ApplyStatic` in the script gates the mutating part.
- **IIS setup:** `Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole` (client) or `Install-WindowsFeature Web-Server` (Server); serve from `C:\inetpub\wwwroot`; test `http://localhost`; manage with `IIS Manager` / `appcmd`; open port 80 via firewall rule. For class demos `python3 -m http.server` is the zero-install analogue.
- **Linux analogue:** `ip addr`, `ip route`, `ss -tlnp`, `ping`; static IP via distro tooling (`ip addr add …`, Netplan/NetworkManager) — `net_info.sh` covers the read-only side.

## 2. Project layout

```
lab-05-network-iis/
  Network-Config.ps1  # inspection + gated -ApplyStatic config (run ELEVATED on Windows)
  net_info.sh         # Linux counterpart: ip/ss/ping (runs here)
  README.md
```

## 3. Run

```powershell
# On a student Windows machine (elevated for -ApplyStatic):
powershell -ExecutionPolicy Bypass -File Network-Config.ps1
powershell -ExecutionPolicy Bypass -File Network-Config.ps1 -ApplyStatic -WhatIf
```

```bash
# On Linux (verifiable here):
cd lab-05-network-iis
bash net_info.sh
```

## 4. Verify

1. On Windows: adapter/IP/route tables print; `Test-Connection 127.0.0.1` replies; without `-ApplyStatic` nothing is modified (script says so).
2. On Linux: `bash net_info.sh` prints addresses, routes, listening sockets, ping stats, ends with `Linux counterpart: OK`, exit code `0`.
3. (IIS, on Windows) `http://localhost` serves the default page after enabling the role; you can state the docroot path.

## 5. Tasks

1. On Windows: record your adapter's DHCP vs static state; convert to static + back, documenting each command.
2. Add a firewall rule allowing TCP 8080 (`New-NetFirewallRule`), test with a local listener, then remove it.
3. Install IIS (or IIS Express), deploy a one-line `index.html`, fetch it with `Invoke-WebRequest http://localhost`.
4. On Linux: serve the same page with `python3 -m http.server 8080` and compare the setup effort with IIS; note what IIS gives you on top (app pools, bindings, logging).
5. Compare `netsh` vs `Get-Net*` output for the same adapter; which would you parse in a script and why?
