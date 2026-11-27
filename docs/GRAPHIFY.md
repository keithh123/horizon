# Graphify for Horizon and Claude

Horizon uses Graphify 0.9.121, pinned in `scripts/horizon_graph.py`. The graph combines local code parsing with explicit links from Horizon's JSON. It covers mod requirements, the quest prerequisite chain, task/reward resource references, bosses, trials, loot families, the 0.6 headquarters stages/options/services (`horizon_hq_stage:*`, `requires_stage`, `mirrors` from quests), and source-to-generator ownership. It does not change the modpack.

## Start here

Open the project root in Claude's coding session. `CLAUDE.md` teaches it to ask a small graph question before browsing files. The `/graphify` skill is installed in this repository; restart the Claude coding session to discover new skills/settings. The CLI wrapper works without restarting.

On this computer setup is already installed. On a fresh checkout with Python 3.11.5–3.14:

```sh
python scripts/horizon_graph.py setup
python scripts/horizon_graph.py status
```

`setup` installs the official `graphifyy` package in `~/.cache/horizon-graphify/venv`, outside the deeply nested Windows checkout. No API key or paid model call is needed for this workflow. Rebuild after source edits or pulling changed source:

```sh
python scripts/horizon_graph.py build
```

The committed `graphify-out/graph.html` is the clickable map: open it in a browser, search for a node and inspect its connections. `graph.json` is for queries; do not paste it into Claude. `GRAPH_REPORT.md` is an overview. Extraction caches stay local.

## Ask narrow questions

```sh
# Locate the code and inputs for quest generation.
python scripts/horizon_graph.py query "quest generation inputs" --seed "scripts/gen_quests.py" --context reads --depth 1 --budget 1200

# Find direct consumers before changing boss rewards.
python scripts/horizon_graph.py affected "manifests/legends.json" --depth 1

# Trace one connection through declared dependencies.
python scripts/horizon_graph.py path "horizon_mod:iris" "horizon_mod:sodium" --undirected

# Inspect one trial's resource costs and waves.
python scripts/horizon_graph.py explain "horizon_trial:tides"
```

Questions use lexical matching plus graph traversal, not a reasoning model. If results drift into similarly named Java classes, use a file seed or exact node ID. If a result is truncated, narrow it first. Raise `--budget` only for a remaining question. `affected` includes the wrapper's Horizon relations; a bare upstream CLI defaults to code relations and may miss generator/data links.

For exact items, drops and editable sources, use the existing `python scripts/horizon.py find <id-or-name>` as the second step. The graph does not replace source inspection, dependency checks or actual Minecraft testing.

## Prompt to paste into Claude

> Work on [one concrete task] in Horizon. Follow CLAUDE.md. Check graph freshness, then query the relevant subsystem with a 1200-token budget and an explicit file seed where possible. Read only the sources needed to verify the result, edit the owning manifests/generators, and fall back to a targeted search if coverage is missing. Run the affected checks, refresh the graph once after the final edits, and report changed files plus what was actually tested.

Good tasks are concrete: "fix this quest's prerequisites", "check the impact of changing Ancient Core costs", or "trace the Curios dependency". Do not ask Claude to understand the entire repo again at the start of every session.

## What is verified and what is incomplete

- Code parsing is local. Horizon data edges come directly from JSON values, with a source file and JSON Pointer; their `L1` anchor points to the file, not the precise value's line. Generator ownership links follow `docs/BUILDING.md`.
- Only `required` Modrinth dependencies with both endpoints in the lock are included. This is not a full NeoForge dependency/incompatibility analysis. Instance-only jars and disabled/rejected mods are outside this dependency graph.
- The graph links generated quests to their generator, and mods to their editable roster. Those outputs should not be edited directly.
- Dynamic KubeJS registrations, full recipe semantics, loot probability math, runtime mixins, and prose-only design decisions may need the original source or existing Horizon tools. One upstream Groovy parser warning for `ports/horizonquestbook/src/build.gradle` is known; it does not prove a Gradle build failure.
- `status` checks a content fingerprint and graph integrity, so edits and deleted files invalidate the index even without a new commit. The report's build commit is provenance, not the freshness test.
- This setup reduces repeated browsing by making focused context reusable. No Claude token-saving or speed percentage has been measured for Horizon.

The project includes advisory Claude hooks for graph reminders. They do not block reads. They use the current exec-form `args` hook configuration; `onFailure: continue` requires Claude Code 2.1.295+. A fresh session may ask you to review the newly added hook settings. The explicit CLI instructions work even when hooks are unavailable. Setup of the MCP server or Graphify Cloud is optional and has not been performed.

Upstream: https://github.com/Graphify-Labs/graphify (default branch `v8`; `main` contains an older release). Claude hooks: https://code.claude.com/docs/en/hooks.
