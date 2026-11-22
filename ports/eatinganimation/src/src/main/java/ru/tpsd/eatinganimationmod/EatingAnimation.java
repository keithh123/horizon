// SPDX-License-Identifier: MIT
// NeoForge 1.21.1 port of Eating Animation by theone_ss, spusik_, PinkGoosik, DoctorNight1
// (https://github.com/Theoness1/EatingAnimation, branch 1.21, commit 8dc8b78). Port by Project Horizon:
//  - Fabric ModelPredicateProviderRegistry -> NeoForge ItemProperties.register in FMLClientSetupEvent
//  - Fabric built-in resource pack -> AddPackFindersEvent (always active, like DEFAULT_ENABLED)
//  - The food list is built after registries freeze (the Fabric static initialiser ran before modded items existed)
// Predicate maths unchanged.
package ru.tpsd.eatinganimationmod;

import net.minecraft.client.player.RemotePlayer;
import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.PackType;
import net.minecraft.server.packs.repository.Pack;
import net.minecraft.server.packs.repository.PackSource;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.event.AddPackFindersEvent;

import java.util.ArrayList;
import java.util.List;

@Mod(value = EatingAnimation.MOD_ID, dist = Dist.CLIENT)
public final class EatingAnimation {
    public static final String MOD_ID = "eatinganimationid";

    public EatingAnimation(IEventBus modBus) {
        modBus.addListener(this::clientSetup);
        modBus.addListener(this::addPacks);
    }

    private void clientSetup(FMLClientSetupEvent event) {
        event.enqueueWork(() -> {
            List<Item> food = new ArrayList<>();
            for (Item item : BuiltInRegistries.ITEM) {
                if (item.components().has(DataComponents.FOOD)) food.add(item);
            }
            food.add(Items.MILK_BUCKET);
            for (Item item : food) {
                ItemProperties.register(item, ResourceLocation.withDefaultNamespace("eat"), (stack, level, entity, seed) -> {
                    if (entity == null || entity.getUseItem() != stack) return 0.0F;
                    if (entity instanceof RemotePlayer) {
                        int max = stack.getUseDuration(entity);
                        return max > 16 ? ((float) entity.getTicksUsingItem() / (float) max) % 1
                                        : ((float) entity.getTicksUsingItem() / 32.0F) % 0.5F;
                    }
                    return (stack.getUseDuration(entity) - entity.getUseItemRemainingTicks()) / 30.0F;
                });
                ItemProperties.register(item, ResourceLocation.withDefaultNamespace("eating"), (stack, level, entity, seed) ->
                        entity != null && entity.isUsingItem() && entity.getUseItem() == stack ? 1.0F : 0.0F);
            }
            // DrinkingAnimationClientMod: vanilla potion
            ItemProperties.register(Items.POTION, ResourceLocation.withDefaultNamespace("drink"), (stack, level, entity, seed) ->
                    entity == null || entity.getUseItem() != stack ? 0.0F : (stack.getUseDuration(entity) - entity.getUseItemRemainingTicks()) / 30.0F);
            ItemProperties.register(Items.POTION, ResourceLocation.withDefaultNamespace("drinking"), (stack, level, entity, seed) ->
                    entity != null && entity.isUsingItem() && entity.getUseItem() == stack ? 1.0F : 0.0F);
        });
    }

    private void addPacks(AddPackFindersEvent event) {
        event.addPackFinders(ResourceLocation.fromNamespaceAndPath(MOD_ID, "resourcepacks/supporteatinganimation"),
                PackType.CLIENT_RESOURCES, Component.literal("Eating Animation: mod support"), PackSource.BUILT_IN,
                true, Pack.Position.TOP);
    }
}
