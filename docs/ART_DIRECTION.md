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
| Ordinary player movement (idle, walk/run/sprint, sneak, crawl, climb, swim, fall/land, ride, elytra) | **FA Player Extension 1.1** (EMF) | 0.6.1; replaces Punchy! Moves, whose own code flags every FA Player pack as conflicting |
| Combat actions (weapon swings, two-handed stances) | Better Combat 2.4 (PlayerAnimator) | per-body-part blending with FA Player by **Entity Player Compat 2.2.3** (one bridge; EMF Compat Core not added) |
| Spellcasting poses | Iron's Spells (PlayerAnimator) | blended by Entity Player Compat |
| Body in first person | **First-person Model 2.7.3, ON by default** (+ FPM x Compat for Better Combat and Accessories) | toggle in First-person Model's config / keybind; body pose comes from the third-person model above |
| First-person hands and arms | Punchy! 3.2b | EPC's author recommends Punchy over FA Player's first-person hands with Better Combat |
| Equipment/held poses (maps, lanterns, ladders) | Not Enough Animations 1.12.7 (EPC-compatible) | FA Player's torch/lantern poses are early-access only, not in the public 1.1 |
| Eating/drinking | Eating Animation port (item frames) + Punchy (hand motion); Just 3D Potions bottle animation via Punchy | Fresh Food stays optional |
| Camera by state | vanilla + Better Combat; Auto Third Person for vehicles/elytra | Punchy Moves' over-the-shoulder camera is gone with the mod; reduced bob in the Balanced/Performance profiles |
| Rain visuals/audio | Particle Rain (existing) | no second rain layer |
| Clouds | Better Clouds with shader clouds off in Complementary profiles (existing choice) | unchanged |
| Ambient particles | Subtle Effects (existing) | Particular rejected earlier |
| Handheld light | shader held-light; Ars Nouveau's built-in dynamic lights (off until `/ars-light on`) | Horizon ships no dynamic-light mod. A player-added LambDynamicLights 4.8.11 (found in the 0.6.0 instance) is kept by the updater and works shaderless; it is not part of the pack |
| Reward notifications | see table above | one owner each |

## Shader presentation

Default: Complementary Reimagined r5.9.3 MEDIUM (Balanced); no-shader profile: Performance; cinematic: Complementary
Unbound HIGH. 0.6 did not retune shader options because no GPU client was available; the End limitation (Voxy shader
patch, distant End terrain unshaded) is **retained** as documented in KNOWN_ISSUES #1.
