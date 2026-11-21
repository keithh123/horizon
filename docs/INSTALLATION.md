# Installation (Prism Launcher)

1. Install [Prism Launcher](https://prismlauncher.org) and sign in with your Microsoft account.
2. **Add Instance → Import**, then choose `ProjectHorizon-0.1.0.mrpack` → OK.
   Prism downloads the 112 mods from Modrinth (verified by sha512) plus NeoForge 21.1.267.
   When asked about optional files, keep *Complementary Unbound* ticked if you want the Cinematic profile.
3. Java 21 is required. Prism picks it automatically.
4. Default memory is set by the Balanced profile: 10 GB max on a 16+ GB machine. On a 16 GB machine,
   apply the Performance profile instead (see PERFORMANCE.md).
5. Launch. The first start takes 30–60 s. In a new world the long-distance view fills in over the first hour.

## Optional: The Twilight Forest (CurseForge-only)

Not part of the pack and not integrated with quests or loot. If you want it: Instance → Edit → Mods →
Download mods → CurseForge → "The Twilight Forest", NeoForge 1.21.1 build. Back up worlds first.

## Dedicated server

1. Install the server: `java -jar neoforge-21.1.267-installer.jar --installServer <dir>` (from maven.neoforged.net).
2. From this repo: `python scripts/build.py server <dir>`. This copies the 97 server-side mods, configs, KubeJS
   scripts and datapacks, and sets memory from the Balanced profile.
   Add `--accept-eula` only if you, the operator, accept the [Minecraft EULA](https://aka.ms/MinecraftEULA).
3. Start it with `run.bat` / `run.sh`. Players join with the `.mrpack` client.

## Building from source

Requires Python 3.11+ and network access.

```
python scripts/resolve.py --frozen     # verify/refresh manifests/lock.json (drop --frozen to update)
python scripts/index_ids.py            # registry id index used for validation
python scripts/gen_datapack.py         # ores, structure tiers, relic loot
python scripts/gen_quests.py           # quest book
python scripts/patch_configs.py        # config overrides (needs a dev instance that has launched once)
python scripts/gen_docs.py             # docs/MODLIST.md
python scripts/build.py mrpack         # dist/ProjectHorizon-<version>.mrpack
python scripts/build.py instance       # dev instance in Prism (optional: --groups a,b)
bash scripts/smoke.sh                  # launch the dev instance and summarise errors
```

Jar downloads are cached in `~/.cache/project-horizon/jars` (override with `PH_CACHE`).
