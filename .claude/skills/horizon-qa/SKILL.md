---
name: horizon-qa
description: Horizon QA runs - loot (headless server), trophies (Yeti/Sun Spirit in a disposable Prism world), shaders (fixed-seed Solas/Voxy route), observe (record a seen visual check).
disable-model-invocation: true
argument-hint: loot|trophies|shaders|observe <key> [--server DIR] [--shader solas] [--fresh]
allowed-tools: Bash(python scripts/horizon.py qa *)
---
Run `python scripts/horizon.py qa $ARGUMENTS` and relay the output. loot needs `--server <dedicated server dir>` or PH_SERVER; trophies/shaders launch the live game in the QA instance only.
Exit codes: 0 ok, 1 check failed, 2 prerequisite/usage, 3 crash, 4 timeout. On 3 run `/horizon-crash`.
Visual checks stay `pending-visual` until a person looks; record it with `qa observe <key>` only after they say they saw it.
