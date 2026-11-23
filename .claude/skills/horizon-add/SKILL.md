---
name: horizon-add
description: Preview, then apply, a new Horizon boss, expedition trial or loot family in the source manifests.
disable-model-invocation: true
argument-hint: boss|expedition|loot-family [--id ns:x --name N --tier mini|major --glyph g] [--spec file.json] [--apply]
allowed-tools: Bash(python scripts/horizon.py add *)
---
Run `python scripts/horizon.py add $ARGUMENTS` WITHOUT `--apply` first and show the preview. Add `--apply` only after the user confirms.
Apply validates ids, writes the manifest, runs the affected generators and audits, and reverts the manifest if they fail. Generators own all outputs.
expedition and loot-family take `--spec` (file or inline JSON): trial = {id,name,color,size,cost,waves,rewards}; family = {id,family:{title,stage,icon,identity,prep,signature,repeat,connects,budget[,token]},structures:[regex],tables:[regex]}.
