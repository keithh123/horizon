#!/usr/bin/env bash
# Launch the Prism dev instance and wait for the title screen or a crash, then
# summarise errors.  Usage: scripts/smoke.sh [timeout_seconds]
INST="$APPDATA/PrismLauncher/instances/${PH_INSTANCE:-ProjectHorizon-dev}/minecraft"
L="$INST/logs/latest.log"; T=${1:-420}
# close any previous client (graceful first so worlds save, then force)
powershell -NoProfile -Command "Get-Process javaw -EA 0 | % { \$_.CloseMainWindow() | Out-Null }; Start-Sleep 8; Get-Process javaw -EA 0 | Stop-Process -Force"
sleep 2; rm -f "$L"; before=$(ls "$INST/crash-reports" 2>/dev/null | wc -l)
# PH_EXTRA="--world HorizonTest" joins a world directly (Prism quick play)
ARGS="'--launch','${PH_INSTANCE:-ProjectHorizon-dev}'"; for a in $PH_EXTRA; do ARGS="$ARGS,'$a'"; done
powershell -NoProfile -Command "Start-Process \"\$env:LOCALAPPDATA\Programs\PrismLauncher\prismlauncher.exe\" -ArgumentList $ARGS"
for ((i=0;i<T;i+=5)); do
  sleep 5
  if [ -f "$L" ] && grep -qE "Game took|took .* seconds to start" "$L"; then echo "RESULT: TITLE SCREEN after ${i}s"; break; fi
  if [ "$(ls "$INST/crash-reports" 2>/dev/null | wc -l)" -gt "$before" ]; then echo "RESULT: CRASH"; ls -t "$INST/crash-reports" | head -1; break; fi
  if [ $i -gt 40 ] && ! powershell -NoProfile -Command "if(Get-Process javaw -EA 0){exit 0}else{exit 1}"; then echo "RESULT: PROCESS EXITED"; break; fi
done
if [ -f "$L" ]; then
  echo "ERROR lines: $(grep -c '/ERROR\]' "$L")"
  grep -E "/ERROR\]|FATAL" "$L" | cut -c1-300 | sed 's/^\[[^]]*\] //' | sort | uniq -c | sort -rn | head -40
  grep -E "Game took|took .* seconds" "$L"
fi
