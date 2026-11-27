# Restart the disposable QA clone (ProjectHorizon-0.6.0-vtest) with a pristine copy of the test save.
# Safety: only acts when exactly one javaw.exe exists AND its working directory is the vtest instance
# (Prism starts the game with cwd = <instance>/minecraft); never touches any other instance or Java process.
param([string]$World = 'New World', [switch]$NoRestore, [switch]$NoLaunch)
$inst = 'C:\Users\Starl\AppData\Roaming\PrismLauncher\instances\ProjectHorizon-0.6.0-vtest'
$backup = 'C:\Users\Starl\HorizonBackups\ProjectHorizon-0.6.0_2026-11-26_pre-visual-repair\minecraft\saves'
$procs = @(Get-Process javaw -ErrorAction SilentlyContinue)
if ($procs.Count -gt 1) { throw "more than one javaw.exe is running; refusing to stop anything" }
if ($procs.Count -eq 1) {
  $p = $procs[0]
  $logOpen = $false
  try { $fs = [IO.File]::Open("$inst\minecraft\logs\latest.log", 'Open', 'ReadWrite', 'None'); $fs.Close() } catch { $logOpen = $true }
  if (-not $logOpen) { throw "the running javaw.exe does not hold the vtest log open; refusing to stop it" }
  Stop-Process -Id $p.Id -Force
  $p.WaitForExit(30000) | Out-Null
  Start-Sleep 2
}
if (-not $NoRestore) {
  robocopy "$backup\$World" "$inst\minecraft\saves\$World" /MIR /NFL /NDL /NJH /NJS /NP /R:2 /W:2 | Out-Null
  if ($LASTEXITCODE -ge 8) { throw "robocopy failed ($LASTEXITCODE)" }
}
Copy-Item "$PSScriptRoot\zz_horizon_qa.js" "$inst\minecraft\kubejs\client_scripts\" -Force
Remove-Item "$inst\minecraft\horizon_qa\*.json" -ErrorAction SilentlyContinue
if (-not $NoLaunch) {
  Start-Process 'C:\Users\Starl\AppData\Local\Programs\PrismLauncher\prismlauncher.exe' -ArgumentList '--launch', 'ProjectHorizon-0.6.0-vtest', '--world', "`"$World`""
}
"restarted vtest (restore=$(-not $NoRestore))"
