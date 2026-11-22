// SPDX-License-Identifier: MIT
// Port of DrawContextMixin (Yarn DrawContext.drawItem -> Mojang GuiGraphics.renderItem). GUI icons of food keep the
// base model (no eating frames), exactly as upstream; items with custom_model_data are left alone.
package ru.tpsd.eatinganimationmod.mixin;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

@Mixin(GuiGraphics.class)
public abstract class GuiGraphicsMixin {
    @Shadow @Final private Minecraft minecraft;

    @ModifyVariable(
            method = "renderItem(Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/item/ItemStack;IIII)V",
            at = @At(value = "INVOKE_ASSIGN", target = "Lnet/minecraft/client/renderer/entity/ItemRenderer;getModel(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;I)Lnet/minecraft/client/resources/model/BakedModel;"))
    private BakedModel eatinganimation$baseModelInGui(BakedModel model, @Nullable LivingEntity entity, @Nullable Level level, ItemStack stack,
                                                       int x, int y, int seed, int guiOffset) {
        if (stack.has(DataComponents.FOOD) && stack.get(DataComponents.CUSTOM_MODEL_DATA) == null) {
            BakedModel base = minecraft.getItemRenderer().getItemModelShaper().getItemModel(stack);
            return base == null ? minecraft.getItemRenderer().getItemModelShaper().getModelManager().getMissingModel() : base;
        }
        return model;
    }
}
