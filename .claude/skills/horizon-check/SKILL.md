---
name: horizon-check
description: Run Horizon generators and audits for the current diff (quick) or the full .mrpack build plus a fresh Prism QA import (release).
disable-model-invocation: true
argument-hint: quick|release [--dry] [--files a,b]
allowed-tools: Bash(python scripts/horizon.py check *)
---
Run `python scripts/horizon.py check $ARGUMENTS` from the repo root and relay its output (it is already capped at 15 lines).
`quick` runs only generators/audits affected by changed files, in build order. `release` is long and launches Prism: only run it when asked.
Do not read the raw log unless the run failed; its path is the last output line.
