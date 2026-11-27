# Project Horizon

An exploration-first RPG and technology modpack for **Minecraft 1.21.1 / NeoForge 21.1.267**, built for
Prism Launcher. 253 locked Modrinth entries (3 optional first-person jars ship disabled, Clavis disabled) + locally built
ports (docs/PORTS.md), Voxy long-distance terrain, Complementary shaders, a 233-quest book, and exploration relics that tie
dungeons to factories.

**0.6: the headquarters campaign.** Plant a Meridian Survey Charter anywhere in the open world and relight the Lantern
Line: commission six stations in order - Outpost, Workshop, Expedition Hall, Arcane Conservatory, Foundry and Logistics,
Observatory and Horizon Beacon - each with choices inside it, each sending you farther out and bringing something home.
Your base, your architecture; the charter only checks what stands near it. See [docs/PROGRESSION.md](docs/PROGRESSION.md)
and the generated stage reference [docs/HEADQUARTERS.md](docs/HEADQUARTERS.md).

### First minutes

1. Unpack the **Founding Kit** in your inventory (right-click). Place the **Survey Charter** where your base will grow.
2. Right-click the charter and click **[Found a headquarters here]**. The panel lists Outpost's needs with ticks and crosses.
3. Sleep in a bed near it, place two chests and a cartography table, plant a crop, walk into the nearest ruin, then click
   **[Commission Outpost]** with 3 paper and 8 torches. You get a Construction Stick, a building kit and a chart to the next site.
4. Friends: click **[Invite]** and type their name; they click **Join**. Press **J** for the quest book: chapter
   `0 - Headquarters Campaign` follows the same stages.

- **Install:** import `dist/ProjectHorizon-0.6.0.mrpack` in Prism (built by `python scripts/build_all.py --mrpack`). The reference instance is the `ProjectHorizon-0.5` Prism instance; the roster tracks its mods (`instance_only` in `manifests/roster.json` lists the jars Modrinth cannot supply). See [docs/INSTALLATION.md](docs/INSTALLATION.md).
- **What's inside:** [docs/MODLIST.md](docs/MODLIST.md)
- **How it fits together:** [docs/PROGRESSION.md](docs/PROGRESSION.md)
- **Code, mod and quest graph / efficient Claude workflow:** [docs/GRAPHIFY.md](docs/GRAPHIFY.md) · open `graphify-out/graph.html` for the interactive map.
- **Why these versions, renderer setup:** [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md)
- **Profiles and measurements:** [docs/PERFORMANCE.md](docs/PERFORMANCE.md)
- **What was tested, what failed, what wasn't tested:** [docs/VALIDATION_REPORT.md](docs/VALIDATION_REPORT.md)
- **0.3.0 expansion status (every requested entry):** [docs/EXPANSION_CHECKLIST.md](docs/EXPANSION_CHECKLIST.md) · ports: [docs/PORTS.md](docs/PORTS.md)
- Resource pack order and Fresh Animations curation: [docs/RESOURCE_PACKS.md](docs/RESOURCE_PACKS.md)
- Headquarters: [docs/HEADQUARTERS.md](docs/HEADQUARTERS.md) (stages) · [docs/HQ_PLANS.md](docs/HQ_PLANS.md) (optional schematics) · [docs/HQ_GRAPH.md](docs/HQ_GRAPH.md) (alternatives) · [docs/ART_DIRECTION.md](docs/ART_DIRECTION.md) · [docs/HQ_BASELINE.md](docs/HQ_BASELINE.md) (baseline + mod decisions) · [docs/HQ_CHECKLIST.md](docs/HQ_CHECKLIST.md) (completion + evidence)
- [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) · [docs/MIGRATION.md](docs/MIGRATION.md) · [CHANGELOG.md](CHANGELOG.md)

## Layout

```
manifests/   roster.json (curated input) -> lock.json (exact versions + hashes), ids.json, headquarters.json (campaign source)
scripts/     resolve, index_ids, gen_datapack, gen_quests, patch_configs, gen_docs, build, smoke.sh
kubejs/      startup (relic + HQ items), server (recipe gates/sinks, headquarters ledger), client (tooltips), assets (lang)
art/         editable 16x16 pixel masters for Horizon textures (rendered by gen_assets.py)
schematics/  optional headquarters plans (Create schematics, generated)
tests/       hq_sim.js (ledger state tests, Node), server_hq.txt (dedicated-server smoke), calibration/density notes
datapacks/   generated: ore unification, structure tiers, relic loot modifiers, structure tag  -> kubejs/data
config/      generated config overrides + quest book (config/heracles)
options/     default options.txt (keybind layout)
profiles/    performance / balanced / cinematic + apply-profile.ps1   -> horizon-profiles/
dist/        built .mrpack
```

Integration is configs, datapacks and KubeJS. Since 0.3.0, `ports/` holds license-permitted NeoForge ports of
mods that had no NeoForge 1.21.1 build (reproducible, see docs/PORTS.md). Modrinth jars are never redistributed;
Modrinth downloads with pinned hashes.
