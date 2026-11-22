package dev.horizon.questbook.mixin;

import earth.terrarium.heracles.client.components.quests.QuestWidget;
import earth.terrarium.heracles.client.handlers.ClientQuests;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Heracles opens quest details on a double-click (second click within 500 ms). Open them on the first click. */
@Mixin(targets = "earth.terrarium.heracles.client.ui.quests.QuestsScreen$1", remap = false)
public abstract class QuestClickMixin {
    @Shadow private ClientQuests.QuestEntry selected;

    @Shadow private void open() { throw new AssertionError(); }

    @Inject(method = "onLeftClick", at = @At("HEAD"), cancellable = true)
    private void horizon$singleClick(double x, double y, QuestWidget widget, CallbackInfoReturnable<Boolean> cir) {
        if (widget == null) return;   // empty-space click keeps Heracles' own deselect handling
        this.selected = widget.entry();
        this.open();
        cir.setReturnValue(true);
    }
}
