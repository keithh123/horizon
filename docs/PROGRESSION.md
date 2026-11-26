# Progression design

## 0.6: the headquarters campaign (main spine)

The core loop: **improve headquarters -> prepare an expedition -> recover knowledge or relics -> bring discoveries home ->
commission a new capability -> venture farther.** Six stations are commissioned in a fixed order at a player-placed
**Meridian Survey Charter**, anywhere in the normal overworld. Nothing is placed or overwritten for you; the optional plans
(docs/HQ_PLANS.md) are Create schematics you print or copy only if you want them.

| Stage | Commissioned by (summary; full reference: docs/HEADQUARTERS.md) | Unlocks |
|---|---|---|
| I. Outpost | bed spawn near the charter, 2 storage blocks, cartography table, crops/animals, first ruin or settlement | copper Construction Stick, building kit, Surveyor's Chart |
| II. Workshop | a Create press that has actually made sheets, at the station, plus four pressed Survey Plates and a local dungeon/temple/ocean/arcane discovery | iron stick, schematic tools, millstone + fan, daily Supply Crate |
| III. Expedition Hall | equipment bench, archive, Discovery Case or trophy; **two of three** regions (Drowned Coast, Hollow Roads, High Landmarks) | regional chart services (permanent per region), warp scrolls, backpack |
| IV. Arcane Conservatory | **one of** Ars Nouveau apparatus, Iron's anvil + inscription table, or an Occultism ritual + bowl; an Ancient Core | Ward of Passage (resistance + fire resistance, daily), lair charts |
| V. Foundry and Logistics | precision mechanisms, a storage controller (AE2 / Sophisticated / Occultism), **one of** Mekanism, MI or Powah with a processing receipt | diamond stick + replacement template, mechanical crafters, larger crate |
| VI. Observatory and Horizon Beacon | Observatory Lens (one Starforged Heart) at the station, 3 of 7 realms, 2 of 13 great legends, 1 of 3 Horizon Trials | Horizon Beacon, explorer's hat, Horizon Charts; post-campaign Gauntlet |

Roles: **Create** is the mechanical foundation (stages II and V). The primary electrical route is a free choice between
**Mekanism** (processing/ore multiplication), **Modern Industrialization** (multiblock heavy industry) and **Powah**
(simple generation); the three checklists are equivalent, so nobody builds a duplicate factory. **AE2** (or Sophisticated
Storage / Occultism storage) is logistics. Relics gate milestones only (Conservatory: 1 Ancient Core; Lens: 1 Starforged
Heart; Hall's High Landmarks route: 1 Core); components and decorative blocks stay ordinary recipes.

### What each check proves (no borrowed machines)

- **Rooms** are checked by a bounded scan around the bound charter (21 x 13 x 21 blocks, loaded chunks only, on click only).
  A machine in your inventory never counts; it must stand at the station.
- **Processing** is proven by builtin advancements that fire only when the machine works (Create's `mechanical_press` fires
  when a press makes sheets) and by **receipts** that exist only as a machine's output (Survey Plate = Create pressing of a
  Survey Blank; enriched iron = Mekanism enrichment; energized steel = Powah orb). Receipts are consumed once.
- **Expeditions** are location advancements for a structure family (`horizon:atlas/*`), dimension entry, first-kill legend
  advancements and Gateways trial completion. They are retroactive: anything a member has already done counts.
- Exact proofs per requirement: docs/HEADQUARTERS.md; alternatives and luck: docs/HQ_GRAPH.md.

### Authority and state

- The **ledger** in the world's `kubejs_persistent_data.nbt` (`horizon_hq`) is the only source of truth. Quests in
  `0 - Headquarters Campaign` and the `horizon:hq/*` advancements are **mirrors**: their only criterion is
  `minecraft:impossible`, granted by the server after it wrote the ledger. A Check click or a client can never grant a stage.
- Every button is a chat command the server re-validates: membership, distance to the bound charter (8 blocks), prerequisite
  stages, requirements, contribution. Contributions are counted first and consumed all-or-nothing; the stage is written
  before rewards are paid; a second click (or a replayed command) finds the stage recorded and does nothing.
- Stage rewards are paid **once per headquarters** to the member who commissions. Quest rewards on the spine are XP only.
- **Unlock vs service:** commissioned stages are permanent (remodel freely). Services (Supply Crate, charts, Ward) need a bound,
  intact charter; a dormant station keeps every stage but pauses services.

### Parties

- A headquarters is founded by one player at a charter. Members **invite** by name (`[Invite]`), the invitee clicks **Join**.
  One headquarters per player; distinct headquarters are fully independent (no server-wide stage exists).
- Evidence is pooled: an advancement any member has been seen holding is recorded as a fact for the station, so an offline
  member's earlier expedition still counts. Facts are recorded at login and whenever a member uses the charter.
- Late joiners receive the mirrors (quest progress) of stages already commissioned but **no stage rewards**. Leavers keep
  their mirrors and everything personal; the station keeps its progress. If the founder leaves, ownership passes to the next
  member; a station with no members releases its charter and its record stays for admin recovery.
- Boss relics are untouched: `horizon:legend/*` still pays one relic + trophy per player on their first kill (party credit by
  distance as in 0.5). Headquarters requirements read those advancements but never pay relics.
- Services: Supply Crates are per headquarters (a party does not multiply them); charts and the Ward are per player.

### Recovery and administration (op level 2, `/horizon hqadmin ...`)

`list`, `info <hq>`, `resync` (re-grant mirrors to online members), `unbind <hq>`, `addmember <hq> <player>`,
`fixture <hq> <stage>` (marks a stage for testing; flagged `fixture`, never pays rewards), `selftest` (disposable worlds only).
Breaking a charter: members may (station goes dormant, progress kept); non-members cannot. A charter destroyed by
explosion is detected the next time someone near it uses the station. Place a new charter and click **Bind/Move
headquarters here** to relocate; stages stay commissioned and room checks use the new location.


## Pillars and roles

| Pillar | Mods | Role |
|---|---|---|
| Exploration | Terralith, Tectonic, Incendium, Nullscape, YUNG's, WDA, Repurposed Structures, T&T, CTOV, Explorify, Dungeons & Taverns, Structory | The world is the main source of rare value. |
| Dimensions | Aether, Deeper and Darker, Bumblezone, Undergarden | Self-contained adventures with their own bosses and gear lines. |
| RPG | Apotheosis (+ Attributes, Enchanting, Spawners), Simply Swords, Better Combat, Curios, Artifacts, Relics | Loot chase, affixes, sockets, world tiers. |
| Bosses | Cataclysm, Mowzie's Mobs, Aether/Undergarden/Iron's bosses, Apotheosis bosses, Warden, Wither, Dragon | Progression-defining encounters. |
| Magic | Iron's Spells (combat), Ars Nouveau (utility/automation), Occultism (spirits, storage, rituals) | Three separate roles, so no single magic mod covers everything. |
| Technology | Create → Create Crafts & Additions → Mekanism / MI / Powah → AE2 + MEGA + Applied Mekanistics, CC: Tweaked | Mechanical → electrical → multiblock → digital. |

## Exploration relics: the link between systems

Three KubeJS items (`horizon:*`) cannot be crafted. They come only from loot, injected by NeoForge
global loot modifiers in `datapacks/horizon/loot_modifiers` (generated by `scripts/gen_datapack.py`):

| Relic | Source (tables) | Chance | Used for |
|---|---|---|---|
| Wayfarer Shard | 309 common chest tables (villages, ruins, camps, small dungeons) | 35%, 1–2 | Warp stones, gem dust, omega stack upgrade |
| Ancient Core | 249 rare chest tables + 9 mini-boss/dimension-boss tables | 30% chests, 100% bosses | **ME Controller**, Sigils of Socketing, epic ink |
| Starforged Heart | 69 legendary chest tables + 13 major-boss tables | 45% chests, 100% bosses (1–2) | **Both fusion reactors**, **MEGA 256M component**, Sigil of Enhancement, legendary ink |

Gates are one relic per *milestone block*, never per component, so they ask for an expedition, not a grind.
In the other direction, relics feed Apotheosis sockets/enhancement and Iron's inks, so exploring stays
rewarding after the factory is built. Verified in game: `/loot` from Ignis's table gave 3 hearts across 2 rolls.

## Structure tiers

| Tier | Examples | Spacing changes |
|---|---|---|
| Common | Explorify, Structory, YUNG's Extras, villages | Authors' defaults (already well spread). |
| Uncommon | YUNG's dungeons, Apotheosis boss towers, Mowzie wrought chambers | Apotheosis towers 26/18 → 32/20; wrought chambers 15/5 → 24/10. |
| Rare | Mowzie Frostmaw/monasteries/groves, Aether dungeons, Iron's catacombs | Mowzie 25/8 → 36–40/14–16. |
| Legendary | WDA major structures, Cataclysm structures | WDA major 50/45 → 60/44. Cataclysm keeps its own (already rare) placement. |

Measured: nearest WDA structure from spawn was 610 blocks away.

## Ore unification

Mekanism owns tin, lead, uranium and osmium. Modern Industrialization's tin/lead/uranium generators and
Powah's uraninite generators are disabled (`neoforge:none` biome modifiers). Powah uraninite is
smelted from Mekanism raw uranium. MI keeps its unique ores (antimony, bauxite, monazite, nickel, salt,
tungsten, lignite).

## Balance changes

See `manifests/config_changes.md` (generated). Highlights:

- **Simply Swords**: material damage bonus +3 → +1. These weapons are now sidegrades with different movesets, not straight replacements for Apotheosis-affixed vanilla weapons. Loot weights are lowered (runic 0.7 → 0.35) and unique hard pity is raised (75 → 100).
- **Apotheosis**: potion charms work only from Curios slots, so 20 charms in a backpack can't stack buffs. Boss spawn cooldown is 3600 → 6000 ticks.
- **Apotheosis world tiers** (Haven → Frontier → Ascent → Summit → Pinnacle) are the progression-aware loot curve. Quests track them.
- Apothic Attributes' damage formulas (armor/protection caps, 85% max protection) stay at defaults. They already apply diminishing returns.

## Quest book (Odyssey Quests, key `J`)

76 quests in 10 chapters. The chapters are optional and parallel, not one checklist:

1. The First Steps
2. The Wild Frontier
3. Forged in Adventure
4. Forgotten Realms
5. Arcane Studies
6. Mechanical Revolution
7. Industrial Expansion
8. The Digital Age
9. Legends and Conquests
10. Beyond the Horizon

Tasks prefer advancements (boss kills, dimension entry, machines built) over item-count busywork.
Every id in every quest is checked against the jar index at build time. Rewards are modest: food,
XP, gem dust, and relics where a milestone deserves one.

## Keybinds

248 bindings were audited. In-world conflicts were removed (`options/options.txt`):

- Quests → `J`. Ars spell HUD → `` ` ``.
- Mekanism armour modes → `;` `.` `'`. MI jetpack → `,`. Cataclysm ability → Home. Otherside transmitter → End.
- Developer and rarely used toggles are unbound. Bind them in Options → Controls; Controlling makes the list searchable.
