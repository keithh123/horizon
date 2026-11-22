<#
  Project Horizon - switch performance profile.
  Run with the game CLOSED, from the instance's horizon-profiles folder:
      powershell -ExecutionPolicy Bypass -File apply-profile.ps1 balanced
  Profiles: performance | balanced | cinematic
  Edits (only these keys; everything else in each file is left as you set it):
    options.txt                      render/simulation distance, max fps, graphics, particles, entity distance
    config/voxy-config.json          enabled, section_render_distance, service_threads
    config/voxyworldgenv2.json       enabled, generationRadius, maxActiveTasks, maxQueueSize  (background LOD generation)
    config/iris.properties           enableShaders, shaderPack
    shaderpacks/<pack>.txt           the shader preset's option values (Complementary MEDIUM / HIGH ...)
    effect configs                   from effects.json: ambient particle/sound mods per effect level
    ../instance.cfg (Prism)          memory and JVM arguments
  Optional -Shader photon|noble|bliss (balanced) or solas|noble (cinematic) swaps the shader pack and its preset.
  Gameplay, loot and rewards are identical in every profile; only visuals and background generation change.
#>
param([Parameter(Mandatory)][ValidateSet('performance','balanced','cinematic')][string]$Profile,
      [ValidateSet('','photon','noble','bliss','solas')][string]$Shader = '')
$ErrorActionPreference = 'Stop'
function Write-NoBom([string]$Path, $Lines) { [IO.File]::WriteAllText($Path, (($Lines | ForEach-Object { "$_".TrimStart([char]0xFEFF) }) -join "`n") + "`n", (New-Object Text.UTF8Encoding $false)) }
function Set-JsonKeys([string]$Path, $Pairs) {
  if (-not (Test-Path $Path)) { Write-Host "  skip (not generated yet): $Path"; return }
  $j = Get-Content $Path -Raw | ConvertFrom-Json
  foreach ($k in $Pairs.Keys) { if ($j.PSObject.Properties[$k]) { $j.$k = $Pairs[$k] } else { $j | Add-Member -NotePropertyName $k -NotePropertyValue $Pairs[$k] } }
  Write-NoBom $Path ($j | ConvertTo-Json -Depth 20)
}
function Set-LineKeys([string]$Path, $Pairs, [string]$Sep) {
  if (-not (Test-Path $Path)) { Write-Host "  skip (not generated yet): $Path"; return }
  $t = @(Get-Content $Path -Encoding UTF8)
  foreach ($k in $Pairs.Keys) {
    $rx = '^(\s*)' + [regex]::Escape($k) + '\s*' + [regex]::Escape($Sep.Trim()) + '.*$'
    if ($t -match $rx) { $t = $t -replace $rx, ('$1' + $k + $Sep + $Pairs[$k]) } else { Write-Host "  key not found in $(Split-Path -Leaf $Path): $k" }
  }
  Write-NoBom $Path $t
}

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

# Voxy + Voxy World Gen
Set-JsonKeys (Join-Path $mc 'config/voxy-config.json') @{ enabled = [bool]$p.voxy.enabled; section_render_distance = [double]$p.voxy.sectionRenderDistance; service_threads = [int]$p.voxy.serviceThreads }
$wg = $p.voxyWorldgen
Set-JsonKeys (Join-Path $mc 'config/voxyworldgenv2.json') @{ enabled = [bool]$wg.enabled; generationRadius = [int]$wg.generationRadius; maxActiveTasks = [int]$wg.maxActiveTasks; maxQueueSize = [int]$wg.maxQueueSize }

# Iris + shader preset options
$ir = Join-Path $mc 'config/iris.properties'
$soKey = if ($Shader) { "$Profile-$Shader" } else { $Profile }
$so = (Get-Content (Join-Path $here 'shader_options.json') -Raw | ConvertFrom-Json).$soKey
if ($Shader -and -not $so) { throw "No shader preset '$Shader' for profile '$Profile' (see shader_options.json)" }
if ($so.voxy_programs -eq $false) { Write-Warning "$($so.pack_file) has no Voxy programs: distant terrain will not be shaded. $($so.note)" }
if (Test-Path $ir) {
  $t = Get-Content $ir
  $pack = if ($so) { $so.pack_file } else { '' }
  $t = $t -replace '^enableShaders=.*', ("enableShaders=" + ($(if ($pack) { 'true' } else { 'false' })))
  if ($pack) { $t = $t -replace '^shaderPack=.*', "shaderPack=$pack" }
  Write-NoBom $ir $t
}
if ($so) {
  $txt = Join-Path $mc ("shaderpacks/" + $so.pack_file + ".txt")
  $cur = [ordered]@{}
  if (Test-Path $txt) { foreach ($l in Get-Content $txt) { if ($l -match '^([^#=]+)=(.*)$') { $cur[$Matches[1]] = $Matches[2] } } }
  foreach ($o in $so.options.PSObject.Properties) { $cur[$o.Name] = $o.Value }
  Write-NoBom $txt ($cur.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" })
  Write-Host "  shader: $($so.pack_file) preset $($so.preset) ($($so.options.PSObject.Properties.Count) options)"
}

# Ambient effects (Subtle Effects, Particle Rain, AmbientSounds ...) - see effects.json
$fxFile = Join-Path $here 'effects.json'
if (Test-Path $fxFile) {
  $fx = (Get-Content $fxFile -Raw | ConvertFrom-Json).levels.($p.effects)
  foreach ($f in $fx.PSObject.Properties) {
    $path = Join-Path $mc $f.Name; $pairs = @{}
    foreach ($kv in $f.Value.set.PSObject.Properties) { $pairs[$kv.Name] = $kv.Value }
    switch ($f.Value.format) { 'json' { Set-JsonKeys $path $pairs } 'toml' { Set-LineKeys $path $pairs ' = ' } default { Set-LineKeys $path $pairs '=' } }
  }
  Write-Host "  effects: $($p.effects)"
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
