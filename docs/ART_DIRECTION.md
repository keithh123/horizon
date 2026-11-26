# Art, effects and presentation ownership (0.6)

One owner per behaviour. When two mods can do the same thing, the table says which one does it in Horizon and what the
other is set to. Status words: **verified** (observed), **configured** (set in shipped files, not observed in a client),
**unverified** (no client was available to look).

## Visual language

- **Materials:** warm timber (spruce/dark oak), stone and deepslate brick, weathered copper and brass, restrained turquoise
  survey markings, parchment and ink for UI. Workshop and Foundry light is warm and practical (lanterns, copper); the
  Observatory earns the cool luminous accent (turquoise beacon, tinted glass, amethyst).
- **Palette (hex):** timber `5a3b22/7a5230/9c6b3e`, copper `8c4a2f/b86b3e`, verdigris `3f8f80/5fb8a4`, brass
  `a9822f/d9b24a/f2d27a`, survey turquoise `2aa9a0/6ee6d8`, parchment `d9c79e/efe2c0`, ink `2b1d12`.
- **Pixel art:** 16x16, outlined, light from top-left, same palette family as the 0.5 relic icons. Masters are editable text grids
  in `art/horizon/*.txt` (original, MIT); `gen_assets.py` renders them deterministically. No placeholder geometry is shipped.
- **Shapes and furniture:** FramedBlocks is the one shape system (no Copycats+). Handcrafted is the furniture set; plans and
  guide text name a small palette (spruce/dark oak, stone brick, copper) rather than the whole catalogue. Create Deco gives
  Workshop/Foundry their catwalks and lamps.

## Headquarters presentation

| Element | Asset / owner | Status |
|---|---|---|
| Charter (controller) | `horizon:survey_charter` - parchment map top with the turquoise survey chevron, timber sides with a brass plate | art verified as a contact sheet; in-world look unverified |
| Stage emblems I-VI | `horizon:emblem_<stage>` - parchment standards on a timber pedestal (same silhouette family as trophies) | contact sheet verified; in-world unverified |
| Discovery Case | glass case on brass rail with a shard inside (cutout) | contact sheet verified |
| Observatory Lens / Horizon Beacon | brass ring + turquoise lens / copper frame with a luminous core (light 15) | contact sheet verified |
| Items | Founding Kit (satchel with chevron), Survey Blank (dull disc), Survey Plate (engraved brass) | contact sheet verified |
| Physical change per stage | the emblem standard placed in the room it names; Observatory adds lens and beacon | configured |

## Sound and notification ownership

| Behaviour | Owner | Others |
|---|---|---|
| Stage commissioned | charter: title + subtitle (next stage) + `horizon:cue.commission` (beacon activate, low) + short end-rod burst at the charter | advancement toast **off**, chat announce **off**; Heracles quest popup stays (it is the quest book's own) |
| Region/route contribution | `horizon:cue.contribution` (cartography take) + action bar | - |
| Finale | `horizon:cue.finale` (challenge toast, lowered pitch) + title + totem/end-rod burst, members only | - |
| Relic/rare finds | existing `cue.item_found / rare_loot / mythic` (unchanged) | ordinary pickups silent |
| Boss first kill | existing `cue.trophy / legend_slain` | unchanged |
| Quiet mode | `/horizon fx quiet` silences every Horizon cue, particle and title for that player | - |

All cues map to vanilla sound events (subtitled; subtitles now also in the KubeJS lang). Volumes were chosen below vanilla UI
sounds; **comparison against rain, machinery and combat was not possible here (unverified).**

## Overlapping visual/audio behaviours (unchanged in 0.6 unless noted)

| Behaviour | Owner | Note |
|---|---|---|
| Attack arms / ordinary hand actions | Punchy! + Punchy! Moves | `isShowingArmsInFirstPerson=false` kept as the comparison point |
| Body in first person | none by default; optional First-person Model preset (ships disabled) | full matrix (weapons, shield, bow, trident, spells, mounts, elytra, Curios) **not run** |
| Camera by state, roll/shake | vanilla + Better Combat; no Camera Overhaul / Combat Roll | experiments only |
| Rain visuals/audio | Particle Rain (existing) | no second rain layer |
| Clouds | Better Clouds with shader clouds off in Complementary profiles (existing choice) | unchanged |
| Ambient particles | Subtle Effects (existing) | Particular rejected earlier |
| Handheld light | shader held-light only | no dynamic-light mod (Sodium Options API incompatibility recorded) |
| Reward notifications | see table above | one owner each |

## Shader presentation

Default: Complementary Reimagined r5.9.3 MEDIUM (Balanced); no-shader profile: Performance; cinematic: Complementary
Unbound HIGH. 0.6 did not retune shader options because no GPU client was available; the End limitation (Voxy shader
patch, distant End terrain unshaded) is **retained** as documented in KNOWN_ISSUES #1.
