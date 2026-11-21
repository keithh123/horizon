# Compatibility & architecture decisions

## Target: Minecraft 1.21.1 + NeoForge 21.1.267, Java 21

Measured on 2026-11-21 against the Modrinth API (release/beta builds tagged for each target):

| Mod | NeoForge 1.21.1 | Fabric 1.21.1 | Forge 1.20.1 | NeoForge 26.1.2 | NeoForge 26.3 |
|---|---|---|---|---|---|
| Voxy (native) | – (via Roxy) | – | – | – | – |
| Apotheosis | yes | – | yes | yes | – |
| Simply Swords | yes | yes | yes | – | – |
| Better Combat | yes | yes | yes | yes | yes |
| Create | yes | – | yes | – | – |
| AE2 | yes | – | yes | yes | yes |
| Modern Industrialization | yes | – | – | – | – |
| Mekanism | yes | – | yes | – | – |
| Ars Nouveau | yes | – | yes | – | – |
| Iron's Spells | yes | – | yes | – | – |
| Occultism | yes | – | yes | yes | yes |
| Terralith / Tectonic | yes | yes | yes | yes | yes |
| When Dungeons Arise | yes | yes | yes | – | – |
| L_Ender's Cataclysm | yes | – | yes | – | – |
| The Aether | yes | yes | yes | – | – |
| KubeJS | yes | – | yes | yes | – |

NeoForge 1.21.1 is the only target that has every pillar of the design. Forge 1.20.1 is missing
Modern Industrialization and has no Voxy path at all. 26.x is too early: Create, Mekanism and both
main magic mods have not been ported yet. Choosing it would have meant dropping half the pack for
a newer version number.

## Renderer stack (validated)

| Component | Version | Notes |
|---|---|---|
| Sodium | 0.8.13 (NeoForge) | Renderer base. |
| Iris | 1.8.14-beta.1 (NeoForge) | Upstream tags this build "release" on Modrinth. |
| Forgified Fabric API | 0.116.15+2.3.6 | Fabric API surface for Voxy. Fabric API itself is **not** installed (`skip_deps` in the roster). |
| Roxy | 0.4.2 (beta) | Translation layer that runs the original Voxy jar on NeoForge. |
| Voxy | 0.2.16-beta for MC **1.21.11** (Fabric jar) | The only Voxy build Roxy verifies. Loaded by Roxy's locator, not by FML. |
| Voxy World Gen V2 | 2.4.2 (NeoForge, beta) | Generates real chunks in the background and feeds them to Voxy. Because it runs the real generator, LODs match Terralith/Tectonic and the structure mods exactly. Seed-based LOD approximation is deliberately **not** used. |
| Complementary Reimagined | r5.9.3 | Default shader, Voxy-aware since r5.8.1. r5.10 was 3 days old and was not chosen. |

Observed in logs: `Voxy render system created … pipeline 'IrisVoxyRenderPipeline'` (shader integration
active), `voxy integration initialized (enabled: true …)` (worldgen addon connected). Distant Horizons is
excluded. It is mutually exclusive with Voxy.

Optional Roxy compat mixins for absent mods (BetterFog, Chunksmith) log `ClassNotFoundException`
warnings at startup. These are expected and harmless.

## Dependency issues found by launch testing (not visible in Modrinth metadata)

| Symptom | Cause | Fix |
|---|---|---|
| Crash: `relics requires octolib 0.6.0.1` | Relics 0.10.x does not declare the lib | Added `shatterbyte-lib` (provides mod id `octolib`). |
| Crash: `irons_spellbooks requires irons_lib [2,3)` | Undeclared dependency | Added `irons-lib` 1.21.1-2.4.0. |
| Prism import silently skipped 16 mods | Modrinth `client_side: unsupported` on worldgen/structure mods was copied into the pack's `env` | Pack builder now installs every mod on the client, because singleplayer runs an integrated server. |
| Prism import offered to untick core mods | Modrinth `optional` side flag copied into `env` | Only the alternate shader is optional now. |
| `Failed to load options` (all defaults lost) | Shipped `options.txt` had no `version:` line, so the LWJGL2 key fixer ran | `version:3955` added. |

## Mixing rules followed

- One biome foundation (Terralith + Tectonic, an officially paired set). BoP, Regions Unexplored and BWG are rejected so two biome placers never stack.
- One LOD renderer (Voxy). One shader loader (Iris). No OptiFine-style or alternative renderers.
- No Connector/Sinytra: the only Fabric jar is Voxy, loaded by Roxy.
- No experimental optimizers (C2ME is alpha, Noisium is stale for 1.21.1).
- Every jar comes from Modrinth with its sha512 pinned in `manifests/lock.json`. Nothing third-party is redistributed.

## CurseForge-only content (not in the .mrpack)

`.mrpack` files may only reference Modrinth/GitHub/GitLab downloads. These candidates exist only on CurseForge:

- **The Twilight Forest**: optional manual add-on (see INSTALLATION.md). The pack does not depend on it.
- **FTB Quests**: replaced by Odyssey Quests (Heracles), which is on Modrinth.
