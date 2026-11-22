package dev.horizon.questbook;

import net.neoforged.fml.common.Mod;

/**
 * Horizon Quest Book: client glue for Heracles (the pack's quest mod). It reuses Heracles' own right-clickable
 * heracles:quest_book item, adds an inventory-screen button, opens quest details in a popup on one click, centres every
 * chapter on its quest tree when opened and keeps the minimap off. See ClientBridge and the mixin package.
 */
@Mod(HorizonQuestBook.ID)
public final class HorizonQuestBook {
    public static final String ID = "horizon_questbook";

    public HorizonQuestBook() {}
}
