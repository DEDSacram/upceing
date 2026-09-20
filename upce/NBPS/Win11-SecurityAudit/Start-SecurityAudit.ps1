# Start-SecurityAudit.ps1
# GUI audit zabezpečení Windows 11 Pro
# Sloupce vystupni tabulky: Kategorie | Kontrola | Stav | Komentar
# Spusteni: pravy klik -> Spustit s PowerShell, nebo: powershell -STA -ExecutionPolicy Bypass -File Start-SecurityAudit.ps1
#Requires -Version 5.1
Add-Type -AssemblyName PresentationFramework, PresentationCore, WindowsBase, System.Xaml

$script:Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$script:ChecksDir = Join-Path $script:Root 'checks'
$script:ExportDir = Join-Path $script:Root 'export'
if (-not (Test-Path $script:ExportDir)) { New-Item -ItemType Directory -Path $script:ExportDir | Out-Null }

# Nacti modularni kontroly, pokud existuji (jinak pouzij vestavene fallbacky)
foreach ($f in @('Check-Antivirus.ps1','Check-WindowsUpdate.ps1','Check-UAC.ps1','Check-Services.ps1','Check-BitLocker.ps1','Check-Network.ps1')) {
    $p = Join-Path $script:ChecksDir $f
    if (Test-Path $p) { . $p }
}

function New-AuditResult {
    param([string]$Kategorie, [string]$Kontrola, [string]$Stav, [string]$Komentar)
    [pscustomobject]@{ Kategorie=$Kategorie; Kontrola=$Kontrola; Stav=$Stav; Komentar=$Komentar }
}
function Test-IsAdmin {
    try { ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator) }
    catch { $false }
}
function Invoke-AllChecks {
    $all = @()
    $map = @(
        @{ Name='Invoke-AntivirusCheck'; Kat='Antivirus' },
        @{ Name='Invoke-WindowsUpdateCheck'; Kat='Windows Update' },
        @{ Name='Invoke-UacCheck'; Kat='Ucty a UAC' },
        @{ Name='Invoke-ServicesCheck'; Kat='Sluzby a protokoly' },
        @{ Name='Invoke-BitLockerCheck'; Kat='Sifrovani a BitLocker' },
        @{ Name='Invoke-NetworkCheck'; Kat='Sit' }
    )
    foreach ($m in $map) {
        try {
            if (Get-Command $m.Name -ErrorAction SilentlyContinue) { $all += & $m.Name }
            else { $all += New-AuditResult $m.Kat 'Kontrola nedostupna' 'Info' "Funkce $($m.Name) nenalezena." }
        } catch { $all += New-AuditResult $m.Kat 'Chyba kontroly' 'Info' $_.Exception.Message }
    }
    return $all
}

[xml]$xaml = @'
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Audit zabezpečení – Windows 11 Pro" Height="700" Width="1080" MinHeight="500" MinWidth="800">
  <DockPanel>
    <StackPanel DockPanel.Dock="Top" Orientation="Vertical" Margin="10,10,10,0">
      <TextBlock Text="Audit zabezpečení – Windows 11 Pro" FontSize="18" FontWeight="Bold"/>
      <TextBlock x:Name="txtAdmin" Text="" FontSize="12" Margin="0,2,0,6"/>
      <StackPanel Orientation="Horizontal">
        <Button x:Name="btnRun" Content="Spustit kontrolu" Width="130" Height="30" Margin="0,0,8,0"/>
        <Button x:Name="btnCsv" Content="Export CSV" Width="110" Height="30" Margin="0,0,8,0"/>
        <Button x:Name="btnHtml" Content="Export HTML" Width="110" Height="30" Margin="0,0,8,0"/>
        <ComboBox x:Name="cmbFilter" Width="190" Height="30" Margin="0,0,8,0"/>
        <TextBlock Text="  Hledat:" VerticalAlignment="Center"/>
        <TextBox x:Name="txtSearch" Width="200" Height="30" Margin="6,0,0,0"/>
      </StackPanel>
      <TextBlock x:Name="txtSummary" Text="Zatím nespustěno." FontSize="13" FontWeight="SemiBold" Margin="0,8,0,4"/>
      <ProgressBar x:Name="bar" Height="10" Minimum="0" Maximum="6" Value="0" Margin="0,0,0,6"/>
    </StackPanel>
    <StatusBar DockPanel.Dock="Bottom">
      <StatusBarItem><TextBlock x:Name="txtStatus" Text="Připraveno."/></StatusBarItem>
    </StatusBar>
    <DataGrid x:Name="grid" Margin="10,0,10,10" AutoGenerateColumns="False" IsReadOnly="True" CanUserSortColumns="True">
      <DataGrid.Columns>
        <DataGridTextColumn Header="Kategorie" Binding="{Binding Kategorie}" Width="150"/>
        <DataGridTextColumn Header="Kontrola" Binding="{Binding Kontrola}" Width="280"/>
        <DataGridTextColumn Header="Stav" Binding="{Binding Stav}" Width="100"/>
        <DataGridTextColumn Header="Komentář" Binding="{Binding Komentar}" Width="*"/>
      </DataGrid.Columns>
    </DataGrid>
  </DockPanel>
</Window>
'@

$reader = New-Object System.Xml.XmlNodeReader $xaml
$win = [Windows.Markup.XamlReader]::Load($reader)
$grid = $win.FindName('grid'); $btnRun = $win.FindName('btnRun')
$btnCsv = $win.FindName('btnCsv'); $btnHtml = $win.FindName('btnHtml')
$cmb = $win.FindName('cmbFilter'); $txtSearch = $win.FindName('txtSearch')
$txtSummary = $win.FindName('txtSummary'); $txtStatus = $win.FindName('txtStatus')
$txtAdmin = $win.FindName('txtAdmin'); $bar = $win.FindName('bar')

$script:Data = New-Object System.Collections.ObjectModel.ObservableCollection[object]
$grid.ItemsSource = $script:Data

if (Test-IsAdmin) { $txtAdmin.Text = 'Běží s právy administrátora – všechny kontroly dostupné.' }
else { $txtAdmin.Text = 'POZOR: bez práv administrátora – BitLocker/TPM a některé kontroly budou neúplné. Spusťte jako správce.' }

# Barveni radku podle Stav
$grid.Add_LoadingRow({
    param($s,$e)
    $r = $e.Row.Item
    if (-not $r) { return }
    switch ($r.Stav) {
        'OK' { $e.Row.Background = [System.Windows.Media.Brushes]::Honeydew }
        'Varovani' { $e.Row.Background = [System.Windows.Media.Brushes]::LightYellow }
        'Riziko' { $e.Row.Background = [System.Windows.Media.Brushes]::MistyRose }
        default { $e.Row.Background = [System.Windows.Media.Brushes]::AliceBlue }
    }
})

function Update-Summary {
    $ok = @($script:Data | Where-Object { $_.Stav -eq 'OK' }).Count
    $w = @($script:Data | Where-Object { $_.Stav -eq 'Varovani' }).Count
    $r = @($script:Data | Where-Object { $_.Stav -eq 'Riziko' }).Count
    $i = @($script:Data | Where-Object { $_.Stav -eq 'Info' }).Count
    $txtSummary.Text = "OK: $ok   |   Varování: $w   |   Riziko: $r   |   Info: $i   |   Celkem: $($script:Data.Count)"
}
function Refresh-Filter {
    $f = $cmb.SelectedItem
    $q = $txtSearch.Text
    $view = [System.Windows.Data.CollectionViewSource]::GetDefaultView($grid.ItemsSource)
    $view.Filter = {
        param($item)
        $ok = $true
        if ($f -and $f -ne 'Vše') { $ok = $ok -and ($item.Kategorie -eq $f) }
        if ($q -and $q.Trim() -ne '') { $ok = $ok -and (($item.Kontrola + ' ' + $item.Komentar) -like "*$q*") }
        return $ok
    }
}
function Set-FilterOptions {
    $cmb.Items.Clear(); [void]$cmb.Items.Add('Vše')
    foreach ($c in ($script:Data | Select-Object -ExpandProperty Kategorie -Unique | Sort-Object)) { [void]$cmb.Items.Add($c) }
    $cmb.SelectedIndex = 0
}

$btnRun.Add_Click({
    $btnRun.IsEnabled = $false; $bar.Value = 0
    $txtStatus.Text = 'Probíhá kontrola...'
    $script:Data.Clear()
    $steps = @('Invoke-AntivirusCheck','Invoke-WindowsUpdateCheck','Invoke-UacCheck','Invoke-ServicesCheck','Invoke-BitLockerCheck','Invoke-NetworkCheck')
    $n = 0
    foreach ($fn in $steps) {
        $n++; $bar.Value = $n
        $txtStatus.Text = "Krok $n/6: $fn"
        $win.Dispatcher.Invoke([action]{}, 'Background') | Out-Null
        try {
            if (Get-Command $fn -ErrorAction SilentlyContinue) {
                foreach ($r in (& $fn)) { $script:Data.Add($r) }
            }
        } catch { $script:Data.Add((New-AuditResult 'Obecne' $fn 'Info' $_.Exception.Message)) }
    }
    Update-Summary; Set-FilterOptions; Refresh-Filter
    $txtStatus.Text = "Hotovo: $($script:Data.Count) kontrol. Export do složky export/."
    $btnRun.IsEnabled = $true
})
$btnCsv.Add_Click({
    if ($script:Data.Count -eq 0) { [System.Windows.MessageBox]::Show('Nejdřív spusťte kontrolu.') | Out-Null; return }
    $f = Join-Path $script:ExportDir ("audit-{0:yyyyMMdd-HHmmss}.csv" -f (Get-Date))
    $script:Data | Select-Object Kategorie, Kontrola, Stav, Komentar | Export-Csv -Path $f -NoTypeInformation -Encoding UTF8
    $txtStatus.Text = "CSV uloženo: $f"
})
$btnHtml.Add_Click({
    if ($script:Data.Count -eq 0) { [System.Windows.MessageBox]::Show('Nejdřív spusťte kontrolu.') | Out-Null; return }
    $f = Join-Path $script:ExportDir ("audit-{0:yyyyMMdd-HHmmss}.html" -f (Get-Date))
    $css = '<style>body{font-family:Segoe UI}table{border-collapse:collapse;width:100%}th,td{border:1px solid #999;padding:6px}th{background:#222;color:#fff}.OK{background:#dff0d8}.Varovani{background:#fcf8e3}.Riziko{background:#f2dede}</style>'
    $rows = foreach ($r in $script:Data) { "<tr class='$($r.Stav)'><td>$($r.Kategorie)</td><td>$($r.Kontrola)</td><td>$($r.Stav)</td><td>$($r.Komentar)</td></tr>" }
    "<html><head><meta charset='utf-8'><title>Audit zabezpečení Win11 Pro</title>$css</head><body><h1>Audit zabezpečení – Windows 11 Pro ($((Get-Date).ToString('g')))</h1><table><tr><th>Kategorie</th><th>Kontrola</th><th>Stav</th><th>Komentář</th></tr>$($rows -join '')</table></body></html>" | Out-File -FilePath $f -Encoding utf8
    $txtStatus.Text = "HTML uloženo: $f"
})
$cmb.Add_SelectionChanged({ Refresh-Filter })
$txtSearch.Add_TextChanged({ Refresh-Filter })

# Konzolovy rezim: -Console vypise tabulku bez GUI (hodi se pro skriptovani)
if ($args -contains '-Console') {
    Invoke-AllChecks | Format-Table -AutoSize -Property @{n='Kategorie';e={$_.Kategorie}},@{n='Kontrola';e={$_.Kontrola}},@{n='Stav';e={$_.Stav}},@{n='Komentar';e={$_.Komentar}}
    return
}
[void]$win.ShowDialog()
