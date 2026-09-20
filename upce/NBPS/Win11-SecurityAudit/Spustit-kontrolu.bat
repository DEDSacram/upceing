@echo off
REM Spoustec auditu – pozada o admin prava pres PowerShell
powershell -NoProfile -Command "Start-Process powershell -ArgumentList '-STA -ExecutionPolicy Bypass -File \"%~dp0Start-SecurityAudit.ps1\"' -Verb RunAs"
