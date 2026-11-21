<#
  Project Horizon - switch performance profile.
  Run with the game CLOSED, from the instance's horizon-profiles folder:
      powershell -ExecutionPolicy Bypass -File apply-profile.ps1 balanced
  Profiles: performance | balanced | cinematic
  Edits: options.txt, config/voxy-config.json, config/iris.properties and, when the
  folder is inside a Prism instance, the instance memory/JVM settings (instance.cfg).
#>
param([Parameter(Mandatory)][ValidateSet('performance','balanced','cinematic')][string]$Profile)
$ErrorActionPreference = 'Stop'
function Write-NoBom([string]$Path, $Lines) { [IO.File]::WriteAllText($Path, (($Lines | ForEach-Object { "$_".TrimStart([char]0xFEFF) }) -join "`n") + "`n", (New-Object Text.UTF8Encoding $false)) }
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$mc = Split-Path -Parent $here
$p = Get-Content (Join-Path $here "$Profile.json") -Raw | ConvertFrom-Json

# options.txt
$opt = Join-Path $mc 'options.txt'
$lines = if (Test-Path $opt) { @(Get-Content $opt -Encoding UTF8 | ForEach-Object { $_.TrimStart([char]0xFEFF) }) } else { @() }
foreach ($prop in $p.vanilla.PSObject.Properties) {
  $k = $prop.Name; $v = "$($prop.Value)".ToLower()
  if ($lines -match "^${k}:") { $lines = $lines -replace "^${k}:.*", "${k}:$v" } else { $lines += "${k}:$v" }
}
Write-NoBom $opt $lines

# Voxy
$vx = Join-Path $mc 'config/voxy-config.json'
if (Test-Path $vx) {
  $j = Get-Content $vx -Raw | ConvertFrom-Json
  $j.enabled = [bool]$p.voxy.enabled
  $j.section_render_distance = [double]$p.voxy.sectionRenderDistance
  $j.service_threads = [int]$p.voxy.serviceThreads
  Write-NoBom $vx ($j | ConvertTo-Json)
}

# Iris / shader
$ir = Join-Path $mc 'config/iris.properties'
if (Test-Path $ir) {
  $t = Get-Content $ir
  $pack = switch -Wildcard ($p.shader) { 'none' { '' } 'ComplementaryUnbound*' { (Get-ChildItem (Join-Path $mc 'shaderpacks') -Filter 'ComplementaryUnbound*' | Select-Object -First 1).Name }
                                         default { (Get-ChildItem (Join-Path $mc 'shaderpacks') -Filter 'ComplementaryReimagined*' | Select-Object -First 1).Name } }
  $t = $t -replace '^enableShaders=.*', ("enableShaders=" + ($(if ($pack) { 'true' } else { 'false' })))
  if ($pack) { $t = $t -replace '^shaderPack=.*', "shaderPack=$pack" }
  Write-NoBom $ir $t
}

# Prism instance memory (instance.cfg sits next to the minecraft folder)
$cfg = Join-Path (Split-Path -Parent $mc) 'instance.cfg'
if (Test-Path $cfg) {
  $c = Get-Content $cfg
  $set = @{ OverrideMemory = 'true'; MinMemAlloc = $p.jvm.min_mb; MaxMemAlloc = $p.jvm.max_mb; OverrideJavaArgs = 'true'; JvmArgs = $p.jvm.args }
  foreach ($k in $set.Keys) {
    if ($c -match "^$k=") { $c = $c -replace "^$k=.*", "$k=$($set[$k])" } else { $c += "$k=$($set[$k])" }
  }
  Write-NoBom $cfg $c
}
Write-Host "Applied profile '$($p.name)'. Restart the instance for memory changes."
