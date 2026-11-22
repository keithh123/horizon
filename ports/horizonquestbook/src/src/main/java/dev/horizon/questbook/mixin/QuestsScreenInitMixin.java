package dev.horizon.questbook.mixin;

import earth.terrarium.heracles.client.HeraclesClient;
import earth.terrarium.heracles.client.handlers.DisplayConfig;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Runs when a quests screen object is created (a fresh open, not a return from a popup).
 * - Heracles centres a chapter on its quest tree only when the chapter differs from the last one shown; clearing
 *   lastGroup makes every open centre. lastGroup is rewritten by the widget right after, so "reopen last chapter" still works.
 * - The minimap is forced off (the in-memory flags only; the player's saved options file is not touched).
 */
@Mixin(targets = "earth.terrarium.heracles.client.ui.quests.AbstractQuestsScreen", remap = false)
public abstract class QuestsScreenInitMixin {
    @Inject(method = "<init>", at = @At("RETURN"))
    private void horizon$centreAndNoMinimap(CallbackInfo ci) {
        HeraclesClient.lastGroup = "";
        DisplayConfig.showMinimap = false;
        DisplayConfig.dockMinimap = false;
    }
}
