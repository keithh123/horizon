package dev.horizon.questbook.mixin;

import dev.horizon.questbook.QuestPopupScreen;
import earth.terrarium.heracles.client.ui.QuestTab;
import earth.terrarium.heracles.common.menus.quest.QuestContent;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Replace Heracles' full-screen quest tabs with the popup (editors keep the original screens). */
@Mixin(targets = "earth.terrarium.heracles.client.ModScreens", remap = false)
public abstract class ModScreensMixin {
    @Inject(method = "openQuest", at = @At("HEAD"), cancellable = true)
    private static void horizon$popup(QuestContent content, CallbackInfo ci) {
        if (QuestTab.isEditing()) return;
        Minecraft mc = Minecraft.getInstance();
        Screen parent = mc.screen instanceof QuestPopupScreen p ? p.parent() : mc.screen;
        mc.setScreen(new QuestPopupScreen(parent, content));
        ci.cancel();
    }
}
