---
name: horizon-crash
description: Summarize the newest QA log or crash report - root error, implicated mods, one excerpt, full path.
disable-model-invocation: true
argument-hint: [path]
allowed-tools: Bash(python scripts/horizon.py crash *)
---
Run `python scripts/horizon.py crash $ARGUMENTS` and relay the output. Mod versions marked "(heuristic)" come from lock.json name matching, not the report.
