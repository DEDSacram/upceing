# Lab 03 — Filesystems & ACLs (NTFS vs ReFS, `icacls`)

NTFS/ReFS comparison, NTFS ACL demo with `icacls` on Windows, Linux permission counterpart that runs here.

## 1. Theory

- **NTFS vs ReFS:** NTFS (journaling, compression, EFS encryption, quotas, per-file ACLs, max ~256 TB volumes) is the general-purpose default incl. boot. ReFS (integrity streams + checksums, copy-on-write-ish block cloning, auto-healing on Storage Spaces, huge scale) targets file servers/VHDs — *cannot boot Windows*, no EFS/compression/quotas. FAT32/exFAT remain for removable media (no ACLs at all).
- **NTFS ACL model:** each file has a DACL = list of ACEs (`Identity : Rights (Allow|Deny)`), e.g. `Everyone:(R)`, `Administrators:(F)`. Explicit **Deny beats Allow**; inheritance flows from parent unless blocked. `icacls file` shows, `/grant User:R` adds allow-read, `/deny User:W` adds deny-write, `/remove:g|:d User` cleans up, `/save`+`/restore` backs ACLs up.
- **Linux analogue:** classic `rwxrwxrwx` bits + ownership (`chmod`, `chown`), extended with POSIX ACLs (`setfacl -m u:nobody:r`, `getfacl`) — same allow-list idea, but **no deny ACEs** (a missing allow = denied) and no inheritance by default.
- Inspect from PowerShell too: `(Get-Acl file).Access | Format-Table`.

## 2. Project layout

```
lab-03-filesystem-acl/
  Get-AclDemo.ps1  # icacls grant/deny demo on .\AclDemo\secret.txt (run on Windows)
  perms_demo.sh    # Linux counterpart: chmod + stat + setfacl/getfacl (runs here)
  README.md
```

## 3. Run

```powershell
# On a student Windows machine:
powershell -ExecutionPolicy Bypass -File Get-AclDemo.ps1 -User Everyone
```

```bash
# On Linux (verifiable here):
cd lab-03-filesystem-acl
bash perms_demo.sh
```

## 4. Verify

1. On Windows: initial ACL prints, then the ACL with `Everyone:(DENY)(W)` present; `Get-Acl` table shows both Allow and Deny rows; final ACL after cleanup.
2. On Linux: `bash perms_demo.sh` prints `ls -l`/`stat` lines, `readable: OK`, ends with `Linux counterpart: OK`, exit code `0`.
3. You can explain why `Deny:W` still blocks writes even though `Allow:R` (and inherited rights) exist.

## 5. Tasks

1. On Windows: `icacls secret.txt /save acl.txt`, break the ACL, restore with `/restore`; show the file content.
2. Demonstrate inheritance: create a subfolder, block inheritance (`icacls dir /inheritance:r`), compare child ACLs before/after.
3. On Linux: replicate allow+deny with classic bits only — why is "deny write to one user, allow to group" impossible without ACLs? Show the `setfacl` version.
4. Compare effective-rights tools: Windows "Effective Access" tab vs `sudo -u nobody cat file` on Linux.
5. Table: NTFS vs ReFS vs ext4 vs FAT32 (journaling/checksums, ACLs, encryption, bootable, max file size).
