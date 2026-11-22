# Ports and locally built jars (0.3.0)

Everything here is rebuilt by `python scripts/build_ports.py` from `ports/<name>/port.json` and recorded with exact
hashes in `manifests/ports_lock.json`. `scripts/build.py` refuses to package a jar whose hash differs from the lock.
These jars ship inside the `.mrpack` (`overrides/mods` or `client-overrides/mods`) because each license permits
redistribution; every jar keeps its upstream license text and credits.

| Port | Kind | License | Upstream | What changed | Side | Status |
|---|---|---|---|---|---|---|
| Grand Teleport | metadata repack | MIT | Modrinth `grandteleport-neoforge` neoforge-1.0.1 | `neoforge.mods.toml` version `neoforge-1.0.1` -> `1.0.1` (FML rejected the file). No code change. | client only (its constructor loads client classes; crashed a dedicated server, tested) | launch-tested |
| SnowyLeavesPlus | source port | MPL-2.0 | github.com/theRookieCoder/SnowyLeavesPlus @78d079e (Fabric 1.21.1) | Yarn -> Mojang names, Fabric colour registry -> `RegisterColorHandlersEvent.Block`. Adds a blockstate property to vanilla leaves. | client + server | compiled; **not yet tested in game** |
| Armour Sound Tweak Updated | back-port | Apache-2.0 | github.com/yourlocalfinancialadvisor/ArmourSoundTweakUpdated @5433562 (Fabric 1.21.2) | 1.21.2 components -> 1.21.1 armour material / elytra sounds; NeoForge client config instead of MidnightLib/ModMenu (NOTICE). | client | compiled; **not yet tested in game** |
| Eating Animation | source port | MIT | github.com/Theoness1/EatingAnimation @8dc8b78 (Fabric 1.21) | Item predicates via `ItemProperties` after registries freeze (modded food included), support pack via `AddPackFindersEvent`, GUI mixin retargeted. | client | compiled; **not yet tested in game** |
| Item Landing Sound | re-implementation from jar | CC0-1.0 (bundled LICENSE; metadata says MIT) | Modrinth `item-landing-sound` 1.0.2 (no public source) | Logic recovered with Vineflower; NeoForge tick; client command registered once (upstream re-registered it every tick). | client | compiled; **not yet tested in game** |
| Better Smoke | source port from jar | MIT | Modrinth `better-smoke` 0.1.2+1.21-1.21.8 (no public source) | Decompiled (Vineflower 1.10.1), remapped with `scripts/remap_intermediary.py`, Fabric entry points -> NeoForge. Mixin logic unchanged. | client | compiled; **not yet tested in game** |
| Weather Glass | verbatim | PolyForm Shield 1.0.0 | CurseForge file 9613334 (0.6.2 for 1.21.1 NeoForge) | None; shipped byte-for-byte (license file is inside the jar). | client | hash-verified; **not yet tested in game** |

## Building

Requirements: Java 21, network on first run (Gradle 8.10 via `ports/_gradle` wrapper, ModDevGradle 2.0.141, NeoForge
21.1.267). Source ports build in a short staging path (`~/.cache/project-horizon/portbuild`, override with
`PH_PORT_BUILD`) because NeoForm fails with Windows error 267 in deep folders. Jars are reproducible
(`preserveFileTimestamps=false`, `reproducibleFileOrder=true`); repacks are written with fixed timestamps.

```
python scripts/build_ports.py            # all ports
python scripts/build_ports.py bettersmoke
```

`scripts/remap_intermediary.py <mappings.tiny> <src> <out>` rewrites decompiled Fabric intermediary sources to
Mojang names (the tiny file is Loom's `mappings-base.tiny` for 1.21.1). It is a porting aid; the output still needs
the loader glue rewritten by hand.

## Not ported (see docs/EXPANSION_CHECKLIST.md for every reason)

Wet Sand (GPL, invasive vanilla re-registration; deferred), Enchantment Glint Outline (CC0, 26.2 render code;
deferred), Mob Dismemberment (LGPL, Forge 1.20.1 only; deferred), Soft Leaves / Tight Fire / Feur Dungeon Spawner /
Cube Animals (All Rights Reserved; permission needed), Cinematic Interactions (native build exists but CurseForge-only
and All Rights Reserved, so it cannot be embedded).
