#!/usr/bin/env bash
# Launch ONE Prism instance ($PH_INSTANCE, default ProjectHorizon-expansion) and wait for the title screen or a
# crash, then summarise errors.  Usage: scripts/smoke.sh [timeout_seconds]
# 0.1.0 closed and force-killed *every* javaw process first (other instances, IDEs, servers). This version only
# refuses to start if the target instance is already running, and never stops anything it did not launch.
NAME="${PH_INSTANCE:-ProjectHorizon-expansion}"
INST="$APPDATA/PrismLauncher/instances/$NAME/minecraft"
L="$INST/logs/latest.log"; T=${1:-420}
running() {  # is a java process running with this instance's game dir on its command line?
  powershell -NoProfile -Command "\$n='$NAME'; if (Get-CimInstance Win32_Process -Filter \"Name like 'java%'\" | Where-Object { \$_.CommandLine -like \"*instances\\\$n\\minecraft*\" -or \$_.CommandLine -like \"*instances/\$n/minecraft*\" }) { exit 0 } else { exit 1 }"
}
if running; then echo "RESULT: $NAME is already running - close it first (nothing was stopped)"; exit 2; fi
before=$(ls "$INST/crash-reports" 2>/dev/null | wc -l)
[ -f "$L" ] && mv -f "$L" "$INST/logs/previous-smoke.log"
# PH_EXTRA="--world HorizonTest" joins a world directly (Prism quick play)
ARGS="'--launch','$NAME'"; for a in $PH_EXTRA; do ARGS="$ARGS,'$a'"; done
powershell -NoProfile -Command "Start-Process \"\$env:LOCALAPPDATA\Programs\PrismLauncher\prismlauncher.exe\" -ArgumentList $ARGS"
for ((i=0;i<T;i+=5)); do
  sleep 5
  if [ -f "$L" ] && grep -qE "Game took|took .* seconds to start" "$L"; then echo "RESULT: TITLE SCREEN after ${i}s"; break; fi
  if [ "$(ls "$INST/crash-reports" 2>/dev/null | wc -l)" -gt "$before" ]; then echo "RESULT: CRASH"; ls -t "$INST/crash-reports" | head -1; break; fi
  if [ $i -gt 60 ] && ! running; then echo "RESULT: PROCESS EXITED"; break; fi
done
if [ -f "$L" ]; then
  echo "ERROR lines: $(grep -c '/ERROR\]' "$L")"
  grep -E "/ERROR\]|FATAL" "$L" | cut -c1-300 | sed 's/^\[[^]]*\] //' | sort | uniq -c | sort -rn | head -40
  grep -E "Game took|took .* seconds" "$L"
fi
