# Gameplay overhaul report (0.5 pass, 2026-11-22)

Target: `ProjectHorizon-0.3.1` Prism instance (no new instance made) + the source repo on branch `expansion-0.3.0`.

## Implemented
- Campaign quest chapter (5 acts), bounty chapter, discovery chapter: +64 quests (see QUEST_AUDIT.md).
- 19 mini-bosses now give a repeat Wayfarer Shard (see LOOT_BALANCE_REPORT.md).
- Instance deploy: `config/heracles` (quests, groups.txt) and `kubejs/data` (all generated datapacks, including the earlier polish pass:
  75 fallback loot tables, landmark spacing 44/30) replaced from the repo. Backups: `_backup/pre-0.5-overhaul-*` in the instance folder.

## Files changed
`scripts/quest_campaign.py` (new), `scripts/gen_quests.py`, `manifests/legends.json`, `config/heracles/**`, `datapacks/**`, five report docs.

## Tested
Static: audit_quests (0 problems), id checks in the generator. Runtime: headless dedicated server boots with the new book and datapacks, no new errors.
## Not tested
Client rendering of the quest book, actually completing quests, repeat-drop behaviour in play, existing-save migration with the new landmark spacing.
## Not done
Dungeon loot identities, gear rebalance, mod-to-mod recipe links, kill-count bounties, a .mrpack build, world-visible lore.
Performance work was out of scope as instructed; trophies untouched.

## Second pass (same night)
- Instance: new Prism instance `ProjectHorizon-0.5` (cloned from 0.3.1 without saves, keeps the hand-added Immersive Portals mods). 0.3.1 received the same content.
  `dist/ProjectHorizon-0.5.0.mrpack` rebuilt. Backups of the old 0.3.1 config/data: `ProjectHorizon-0.3.1/_backup/pre-0.5-overhaul-*`.
- Added: 7 item contracts, chapter layouts, family loot extras, magic bridge recipes (see QUEST_AUDIT.md, LOOT_BALANCE_REPORT.md).
- Tested: full headless smoke (kubejs 0 failed recipes, 4 structure loot audits), and a real client launch of 0.5 auto-joining a copied world:
  quests loaded without per-quest errors. NOT tested: visuals, claiming rewards, repeat drops, family extras in real chests.
- Not done: kill-count bounties (format unverifiable), gear rebalance (no values changed), pushing to a git remote (the repo has none).
