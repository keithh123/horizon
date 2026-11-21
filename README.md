# Project Horizon

An exploration-first RPG and technology modpack for **Minecraft 1.21.1 / NeoForge 21.1.267**, built for
Prism Launcher. 112 mods, Voxy long-distance terrain, Complementary shaders, a 76-quest guide, and
exploration relics that tie dungeons to factories.

- **Install:** import `dist/ProjectHorizon-0.1.0.mrpack` in Prism. See [docs/INSTALLATION.md](docs/INSTALLATION.md).
- **What's inside:** [docs/MODLIST.md](docs/MODLIST.md)
- **How it fits together:** [docs/PROGRESSION.md](docs/PROGRESSION.md)
- **Why these versions, renderer setup:** [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md)
- **Profiles and measurements:** [docs/PERFORMANCE.md](docs/PERFORMANCE.md)
- **What was tested, what failed, what wasn't tested:** [docs/VALIDATION_REPORT.md](docs/VALIDATION_REPORT.md)
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

No custom Java mod was needed. Every integration is done with configs, datapacks and KubeJS, so there
is no compiled code to maintain. Third-party jars are never redistributed; the `.mrpack` references
Modrinth downloads with pinned hashes.
