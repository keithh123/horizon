# Project Horizon

An exploration-first RPG and technology modpack for **Minecraft 1.21.1 / NeoForge 21.1.267**, built for
Prism Launcher. 177 mods + 8 locally built/ported jars (docs/PORTS.md), Voxy long-distance terrain, Complementary shaders, a 143-quest guide, and
exploration relics that tie dungeons to factories.

- **Install:** import `dist/ProjectHorizon-0.3.1.mrpack` in Prism. See [docs/INSTALLATION.md](docs/INSTALLATION.md).
- **What's inside:** [docs/MODLIST.md](docs/MODLIST.md)
- **How it fits together:** [docs/PROGRESSION.md](docs/PROGRESSION.md)
- **Why these versions, renderer setup:** [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md)
- **Profiles and measurements:** [docs/PERFORMANCE.md](docs/PERFORMANCE.md)
- **What was tested, what failed, what wasn't tested:** [docs/VALIDATION_REPORT.md](docs/VALIDATION_REPORT.md)
- **0.3.0 expansion status (every requested entry):** [docs/EXPANSION_CHECKLIST.md](docs/EXPANSION_CHECKLIST.md) · ports: [docs/PORTS.md](docs/PORTS.md)
- Resource pack order and Fresh Animations curation: [docs/RESOURCE_PACKS.md](docs/RESOURCE_PACKS.md)
- [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) · [CHANGELOG.md](CHANGELOG.md)

## Layout

```
manifests/   roster.json (curated input) -> lock.json (exact versions + hashes), ids.json, loot_tiers.json
scripts/     resolve, index_ids, gen_datapack, gen_quests, patch_configs, gen_docs, build, smoke.sh
kubejs/      startup (relic items), server (recipe gates/sinks), client (tooltips), assets (lang)
datapacks/   generated: ore unification, structure tiers, relic loot modifiers, structure tag  -> kubejs/data
config/      generated config overrides + quest book (config/heracles)
options/     default options.txt (keybind layout)
profiles/    performance / balanced / cinematic + apply-profile.ps1   -> horizon-profiles/
dist/        built .mrpack
```

Integration is configs, datapacks and KubeJS. Since 0.3.0, `ports/` holds license-permitted NeoForge ports of
mods that had no NeoForge 1.21.1 build (reproducible, see docs/PORTS.md). Modrinth jars are never redistributed;
Modrinth downloads with pinned hashes.
