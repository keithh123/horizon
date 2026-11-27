# Changelog

## 0.6.1 - visual, interaction and rendering repair (2026-11-26)

Installed in place into the existing `ProjectHorizon-0.6.0` Prism instance (same name/UUID); the artifact is 0.6.1.

**Fixed (each reproduced first in a real client on a copy of the affected world; docs/VALIDATION_REPORT.md 0.6.1).**
- Survey Charter right-click did nothing: KubeJS 2101 `event.cancel()` throws `EventExit`; it was the handler's first
  statement. `cancel()` is now last; the off-hand pass is consumed (an off-hand torch used to be placed against the charter);
  new `tests/kubejs_lint.js` guards every KubeJS exit call.
- Attributes and Accessories inventory buttons overlapped: Apothic's button moves to the preview's top-left corner (28,10).
- Shaders OFF + rain/thunder hid the whole landscape: caused by Weather Glass 0.6.2 (client bisection); it moves to the lab
  variant. Rain, splashes and ripples stay with Particle Rain.
- Render distance 2 (Voxy warns about LOD culling below 3): existing instances are raised to at least 8 on update.
- Updater (`build.py instance`): keeps instance.cfg identity/Java/memory, options.txt and the shader choice; UTF-8 pack names
  (0.6.0 duplicated "Vocal Villagers" as mojibake); keeps the player's accepted-incompatible packs; removes stale
  `.jar.disabled` twins; idempotent.

**First person and animation.** First-person Model + Not Enough Animations + FPM x Compat now ship ON. FA Player Extension owns
player movement, blended with Better Combat and Iron's casting by Entity Player Compat 2.2.3; Punchy! keeps first-person hands.
Punchy! Moves and Fluid & Foolish are removed (Punchy Moves flags every FA Player pack as conflicting).

**Visual stack.** Mandala's GUI Dark Mode + mod compatibility packs; Fresh Animations Objects, Player, V&V patch, Fresh Compats
enabled; Fancy Crops, 3D Default, Remodeled Doors, 3D Rails, Better Leaves, Fresh Flower Pots (+compats), Just 3D Potions.
Modefite added so a player-enabled Fresh Food works. Every one of the 73 researched projects has a recorded disposition:
`manifests/visual_catalogue.json` (docs/RESOURCE_PACKS.md).

## 0.6.0 - the headquarters campaign (2026-11-26)

**Campaign.** A Meridian Survey Charter, placed anywhere in the open world, anchors six stations commissioned in order:
I. Outpost, II. Workshop, III. Expedition Hall (2 of 3 regions), IV. Arcane Conservatory (1 of Ars / Iron's / Occultism),
V. Foundry and Logistics (1 of Mekanism / MI / Powah), VI. Observatory and Horizon Beacon (3 of 7 realms, 2 of 13 great
legends, 1 of 3 trials). Source of truth: `manifests/headquarters.json`; generator `scripts/gen_headquarters.py`; server
ledger `kubejs/server_scripts/horizon_headquarters.js` (authoritative, idempotent, party-aware, migration-versioned).
- Charter panel (chat-based screen with clickable, server-revalidated buttons): status, ticks/crosses per requirement,
  alternatives, contribution counts, next unlock, [Commission], [Contribute], services, members, invite/leave.
- Proof without borrowed machines: bounded room scan around the charter, builtin "machine ran" advancements, and receipts that
  exist only as machine output (Survey Plate = Create pressing; enriched iron; energized steel).
- Services: Supply Crate (daily, per headquarters; Foundry upgrades it), Tide/Archive/Landmark/Lair/Horizon charts (per
  player, cost a map + Wayfarer Shards), Ward of Passage (resistance + fire resistance, daily). No service mints relics.
- New items/blocks (original art, `art/horizon/*.txt`): Founding Kit (given once per player, old saves too), Survey Charter,
  Survey Blank/Plate, Discovery Case, Observatory Lens (one Starforged Heart), Horizon Beacon, six Station Emblems.
- Quests: new main spine `0 - Headquarters Campaign` (19 quests, mirrors of the ledger, XP-only rewards). The 0.5 acts chapter
  is now `0b - The Expedition Road (branch)` with the same folder and ids; all 214 old ids preserved. Atlas quests gain a
  "Brings home" line per structure family. Quest audit now rejects overlapping icons and non-mirror stage quests.
- Optional plans: 7 Create schematics (`schematics/`, incl. a ruined-outpost restoration) with material bills (docs/HQ_PLANS.md).
- Progression graph with alternatives per requirement; the build fails on a luck-only bottleneck (docs/HQ_GRAPH.md).
- Cues: `cue.commission`, `cue.contribution`, `cue.finale` (vanilla events, subtitled; subtitles now also in KubeJS lang).

**Mods.** Added Construction Sticks 1.5.0, FramedBlocks 10.6.3, Handcrafted 4.0.3, Create Deco 2.1.3, Comforts 9.0.5;
First-person Model 2.7.3 + Not Enough Animations 1.12.7 + FPM Compat 1.2.1 as a disabled optional preset; Fresh Compats v1.6
shipped but not enabled. Deferred with reasons: AStages, Open Parties and Claims, Exposure and the other conditional
candidates (docs/HQ_BASELINE.md). No mod upgraded or removed.

**Server fixes (the dedicated server did not boot in 0.5).** Controlify marked client-only; Terra Curio replaced by
`ports/terracurio` (LGPL repack moving its embedded ParticleStorm's GeckoLib mixins to the client list). `build.py server`
and `server_test.py` run on Linux. `build_ports.py` gains `nested_edits`.

**Build.** `gen_headquarters.py` and the Node ledger tests (`tests/hq_sim.js`) are in `build_all.py` and in the
quick-check routing; generated outputs regenerated from the real lock (the committed ones came from a partial jar index);
`.gitattributes` keeps generated files LF on every platform; new `scripts/mrpack_install.py` (headless .mrpack install + verify).


## 0.5 quest-book fixes and accessory/zoom mods (2026-11-23, not yet built or launched)

- **Trophy icons (chapters 0, 12):** the `ProjectHorizon-0.5` instance still had the pre-0.3.1 `horizon_items.js`
  (`.parentModel().textures()`), so every `horizon:trophy_*` rendered as a missing texture. The repo and the 0.5 .mrpack were
  already correct; the instance copy was replaced (old copy in `.horizon/backup-0.5-instance-*`).
- **Hall of Legends (chapter 12)** is now branched: one small tree per realm, following each mod's own progression
  (Slider > Valkyrie Queen > Sun Spirit, Warden > Stalker, Netherite Monstrosity > Ignis > Maledictus, Ender Guardian > Harbinger /
  Ender Golem, Leviathan > Scylla / Clawdian, ...), laid out as a shallow arch under the Hall. Great legends never wait on a
  lesser one except in the Aether. The Curator now links to the 7 realm-final great legends, which still require all 13 through
  their chains. Quest ids are unchanged; kill credit is retroactive, so out-of-order kills complete when the node unlocks.
- **Bulwark (chapter 13):** icon `minecraft:shield` rendered blank in Heracles; now `minecraft:iron_chestplate`.
- **Mods added to the roster (pinned to the jars added to the 0.5 instance):** Accessories, Accessories Compat Layer,
  Accessories Compat Vanilla, Accessorify, Dream Relics, Terra Curio, Immersive Lanterns (+ TxniLib), Sodium Dynamic Lights
  (+ Sodium Options API), Cinematic Zoom, Resourcify, More Mouse Tweaks, Mouse Tweaks x Accessories Fix. Lock 177 -> 191, no
  existing version changed, no declared incompatibilities. Not yet: `index_ids`, docs, .mrpack build, any launch.
  Dream Relics and Terra Curio items are outside the loot budget until audited.
- **`ProjectHorizon-0.5` is now the reference instance.** Every jar in it that Modrinth can supply is pinned in the roster
  (lock 191 -> 248, incl. auto dependency Hybrid API); the 8 that Modrinth cannot supply are listed under `instance_only`
  in `manifests/roster.json`. Regions Unexplored, YUNG's Cave Biomes and IDAS were removed from `rejected`; Sinytra Connector
  is now in the pack. The instance has a second Terralith jar (`Terralith_1.21.x_v2.6.2.jar`) that is not in the roster,
  and is missing Hybrid API (required by Hybrid Aquatic). Not launched, not built.
  Instance fixed after that: the extra Terralith jar is `.disabled`, Hybrid API 1.1.3 installed (sha512 checked against the lock).
- **Removed again: Immersive Lanterns, Sodium Dynamic Lights, Sodium Options API, TxniLib** (lock 248 -> 244). First launch stopped
  on "reeses_sodium_options is incompatible with sodiumoptionsapi". Options API (last build 2025-01) requires Reese's, and
  every Reese's build for Sodium 0.8 declares Options API incompatible, so neither order loads; Sodium Dynamic Lights needs
  Options API and Immersive Lanterns 1.0.6 hard-requires Sodium Dynamic Lights. Reese's stays. The jars are `.disabled` in
  the instance; reasons are in the roster's `rejected`. A static scan of every enabled jar's mods.toml found no other active
  incompatibility (the nine other declarations are version ranges the installed versions are past).
- **World-load crash fixed: Curios 9.6.0 -> 9.5.1.** Opening or creating a world crashed with
  `CuriosEntityManagerMixin ... failed injection check` (Accessories Compat Layer 0.1.13). Curios 9.6.0 (2026-11-19) moved
  entity-slot building from `apply()` into `rebuildEntitySlots(Registry)`, so the compat layer's mixin has no target; no newer
  compat layer exists yet. Every Curios dependent accepts 9.5.1. Roster pins `yohfFbgD`; in the instance the 9.6.0 jar is in
  `minecraft/mods-disabled/` and 9.5.1 is installed (sha512 checked). `resolve.py`: a roster `pin` now beats `--frozen`.
  `check_deps.py`: new `KNOWN_BAD` pair rule, standalone jars beat jar-in-jar copies (Aether's nested Accessories beta.48 was
  masking beta.54), malformed dependency tables (modelfix) are skipped. **TerraBlender 4.1.0.8** added to the roster
  (lock 244 -> 245): YUNG's Cave Biomes and Regions Unexplored require it but Modrinth metadata omits it. Checker: 0 failures.

## 0.3.1 hand-added Immersive Portals instance: crash fixes (2026-11-22)

Immersive Portals, Immersive Infinity, immptl-compat and Make it Compatible: Immersive Portals are **not** in the pack
roster or the .mrpack; they were added by hand to the `ProjectHorizon-0.3.1` Prism instance. Two crashes there:

- Create New World crashed: Immersive Infinity's `custom_portal_generation` datapack registry had 42 of 70 definitions
  referencing blocks/items of mods that are not installed (DivineRPG, Blue Skies, OrePortal, ...). Fixed by
  `scripts/gen_portal_guards.py`, which re-emits those 42 under `datapacks/immersive_infinity/` with a `neoforge:conditions`
  `mod_loaded` guard (portal returns by itself if the mod is added). The 28 working definitions (Aether, Deeper and Darker,
  Undergarden x4, Twilight Forest x2, and the ones with no registry references) are untouched. Shipped in the .mrpack
  as `kubejs/data`; inert without Immersive Infinity.
- World join crashed: Make it Compatible: Immersive Portals 1.0.0 targets an older Voxy; with Voxy 0.2.16-beta / Roxy
  0.4.2.1 / Sodium 0.8.13 two of its mixins fail (`voxy$clearBoundOnSectionRemoved` handler and the
  `ChunkBoundRenderer.delayQueueIndex` @Shadow field do not exist). No newer build found, so
  `scripts/patch_micimmptl.py` empties the add-on's Voxy mixin config. Voxy is unmodified and renders the main view; Voxy
  LODs are not drawn inside portal views.

## 0.3.1 (2026-11-22): quest book, hats, resource pack

Built and statically checked, headless-server tested, then played in a fresh Prism import (see the client pass below and
docs/VALIDATION_REPORT.md for what was and was not exercised).

## 0.3.1 client pass (2026-11-22, same day)

Played in a fresh Prism import of the .mrpack with a new world. Bugs found and fixed:

- Quest titles were all "New Quest" in game: Heracles reads `title` with `ComponentSerialization.FLAT_CODEC`, a string that
  holds component JSON, and silently falls back to "New Quest" for anything else. gen_quests now writes
  `"title": "{\"text\": ...}"`; audit_quests checks it. This was the real source of the placeholder names.
- J did nothing: Punchy Moves binds its Hello B emote to J (and H, K, L collide with other binds). Its four emote keys ship
  unbound in options.txt.
- First quest: an advancement task (tick or story/root) never completed it in game. It is a Check task again (same boolean
  storage, so older progress reads the same) and the popup now has a Check button for manual tasks.
- Chapter centring pushed the tree to the bottom-right (Heracles centre formula); fixed by a mixin. The tutorial screen no
  longer interrupts (heracles_options.json ships showTutorial false, minimap off).
- Popup: drawn under its own dim layer and under item icons; status label lagged behind progress. Fixed.
- Simple Hats random mob/chest drops are off (curated rewards only).

- Quests: 143 quests kept (ids unchanged). "Timber!" was unreachable on a fresh world: the first quest waited on
  `minecraft:story/root` ("craft a crafting table"), which needs the wood Timber! asks for. It is now a
  Check task you click in the popup (boolean storage like the old advancement task, so 0.3.0 progress reads the same). Fixed: Hearty Meals
  (cooking pot) now follows Iron Will, not Sleep; Flawless Ambition pointed at the Pinnacle advancement (a duplicate of
  another quest) and is now Gem Cutter's Bench (craft the table); five titles that duplicated Hall of Legends entries
  renamed. Every quest now ends with an "Objective" and a "Why it matters" line. `scripts/audit_quests.py` checks
  placeholders, duplicate titles, prerequisites, cycles and the early-chain deadlock (part of build_all).
- Quest book UI (new local mod `horizon_questbook`, original code): inventory button below the player inventory;
  Heracles' own `heracles:quest_book` is now craftable (book + compass), rewarded by the first quest and given once to
  every player on login; one click opens quest details in a popup (description, requirements with state, unmet
  prerequisites, rewards, claim, X and Esc); every open centres the chapter on its tree; the minimap is forced off.
- Cosmetics: Simple Hats 0.4.1. Eight curated hats are quest rewards (Frostmaw, Wrought, Sun Spirit, Dragon, Dead King,
  Cataclysm Conqueror, Curator of Legends, first roadside ruin).
- Effects: rain ripples (Particle Rain owns them; Subtle Effects off), rain/snow audio (Cool Rain owns it; Particle Rain
  volume 0), footsteps/impacts (Effectual run dust and block-place effect off; Footprint Particle splash off); Better
  Combat debug hit boxes off. Reward cues are now Horizon sound events (docs/RESOURCE_PACKS.md).
- Resource packs: new original `Horizon-16x.zip`; the Fresh Animations All-Extensions bundle is replaced by Details,
  Emissive and Quivers (Objects, Spiders, Creepers, Classic Horses held back, reasons in docs/RESOURCE_PACKS.md).
- Shaders: Photon v1.4, Solas 3.9, Noble 1.9.9 and Bliss 2.1.2 added with presets (`apply-profile.ps1 -Profile balanced
  -Shader photon`). Performance stays shader-free. Bliss has no Voxy programs; the switcher warns.
- Clavis ships **disabled by default** (`Clavis-*.jar.disabled`): the lockpicking cursor bug could not be tested.
- Immersive Portals (NeoForge 6.0.7) not enabled: server side loads and ticks like the baseline, client rendering is untested.
- Build: `build.py instance` now removes only jars Horizon itself shipped, so manually added mods survive an update.

## 0.3.0 (2026-11-21): expansion candidate

- 176 locked mods (+60: 51 requested native NeoForge 1.21.1 builds pinned by version id, 9 dependencies), 6 resource packs
  (Fresh Animations + official Extensions bundle, Fluid & Foolish, Vocal Villagers, Fire Rekindled, Animated Hearts) and
  7 local jars (docs/PORTS.md): Grand Teleport metadata repack, 5 source ports, Weather Glass (verbatim).
- Every audit entry has a status in docs/EXPANSION_CHECKLIST.md (62 implemented, 3 already present, 8 blocked,
  3 not ported yet, 12 FA add-ons not installed with reasons, 1 excluded by user).
- Blocked with concrete reasons: Infinity Cave and Blooming Biosphere (both replace the overworld dimension/noise
  settings owned by Terralith/Tectonic), Actually 3D Stuff (1.21.9+ model features), Cinematic Interactions and Cube
  Animals (CurseForge-only, All Rights Reserved), Soft Leaves, Tight Fire, Feur (All Rights Reserved).
- Fresh Animations: base + Extensions only. FA Player Extension/Player Compats removed after Punchy Moves reported them
  incompatible in game; F.M.R.P, Fresh Compats, Fresh Illager Mod Compats target mods Horizon does not have.
- Loot: new boss arenas join boss_lair (no Starforged Heart), homesteads/settlement, Moog's mineshafts/underground.
  Expansion structures only constrain their own loot tables, so all 0.2.0 calibrated budgets are byte-identical.
  10 new mini-tier Legends (Ancient Core + trophy); dense sets re-spaced (spider nests 8/6 -> 28/12, 3 MMR sets -> 40/20).
- Ownership configs: Cave Dust (cave dust), Footprint Particle (footprints), Swinging Lanterns (lanterns), Auto Third
  Person (elytra camera). Profiles control Better Clouds, Cozy Critters, Windy, Cave Dust, Interactive Foliage waving,
  Effectual trails and Streams Reflowing particles.
- Fixes found by testing: Visual Overhaul first-launch NPE (seed config), Grand Teleport invalid version string and
  server crash, checker quirks (Clavis/Lootr Maven ordering, More Sounds optional `forge`), patch_configs syntax/idempotency.
- Bug fix (0.2.0): Incendium function/component tables (armour-stand heads, artifacts, castle/base) were in the nether
  family; Incendium rolls them via /loot every second and Apotheosis' gem modifier threw. Excluded; only the Incendium
  castle group moves (core 0.68 -> 0.64, still under budget). Verified in game after /reload.
- Tooling: probe_expansion.py, build_ports.py, remap_intermediary.py, gen_checklist.py; server_test.py LOCATEAUDIT.
- Not changed: 0.2.0 mods' versions, calibrated loot, existing quests (10 legend quests appended by the generator), saves.


## 0.2.0 (2026-11-21)

- 116 mods (added Lootr, Corpse, Subtle Effects, Gateways to Adventure and dependencies).
- Curated reward families with per-structure relic budgets; loot budgets now use **measured** container counts from real placed structures (25 of 26 calibration structures; `minecraft:end_city` could not be measured and uses template counts).
- 133 quests in 13 chapters; 26 boss trophies and relic/token textures generated.
- Dependency checker evaluates Maven version ranges (`check_deps.py`). Subtle Effects vs Fzzy Config `0.7.7+fix1` was a false alarm in the checker's version ordering; FML accepts it (client launched). Recorded as a launch-verified exemption.
- New `profiles/effects.json` (Subtle Effects density/distance per profile); profile switching re-verified on a 0.2.0 instance (BOM-free).
- `gen_profiles.py` ignores `effects.json`; calibration is run in chunks (a single 26-structure run stalled after 10).
- Not changed: saves, mods' versions.

## 0.1.0 (2026-11-21): first playable build

- 112 mods on NeoForge 21.1.267, all resolved from Modrinth with pinned sha512.
- Voxy via Roxy + Voxy World Gen V2 + Iris + Complementary Reimagined r5.9.3.
- Terralith + Tectonic terrain; Incendium and Nullscape for the Nether and End; 18 structure mods with tier-based spacing changes.
- Exploration relics (Wayfarer Shard / Ancient Core / Starforged Heart) injected into 627 loot tables and 22 boss tables; they gate the ME controller, both fusion reactors and MEGA 256M, and feed back into Apotheosis and Iron's.
- Ore unification across Mekanism, Modern Industrialization and Powah.
- Balance changes: Simply Swords damage and loot, Apotheosis charms and boss cooldown.
- 76-quest Odyssey Quests book in 10 chapters.
- Conflict-free default keybinds; Performance/Balanced/Cinematic profiles with a switcher script.
- Dedicated server target (`build.py server`), validated headless at 20 TPS across all 9 dimensions.
- Fixes found by testing: undeclared deps (OctoLib, Iron's Lib), `.mrpack` env flags dropping 16 mods, options.txt data version.
