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
