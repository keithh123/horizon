// SPDX-License-Identifier: CC0-1.0
// NeoForge 1.21.1 port of Item Landing Sound by ExiledLizard635 (Modrinth: item-landing-sound, v1.0.2 for 1.21.4;
// bundled LICENSE is CC0 1.0, fabric.mod.json says MIT - both permit this port). No public source: logic recovered
// from the published jar (Vineflower 1.10.1) and rewritten with Mojang names. Changes by Project Horizon:
//  - Fabric END_CLIENT_TICK -> NeoForge ClientTickEvent.Post
//  - the /itemlandingsound:volume client command is registered once (RegisterClientCommandsEvent); upstream
//    re-registered it inside the tick callback on every tick
// Behaviour unchanged: dropped items within 32 blocks play the block's step sound the tick they land.
package com.example;

import com.mojang.brigadier.arguments.FloatArgumentType;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.commands.Commands;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.item.ItemEntity;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterClientCommandsEvent;
import net.neoforged.neoforge.common.NeoForge;

@Mod(value = "item_landing_sound", dist = Dist.CLIENT)
public final class ItemLandingSound {
    private float volume = 0.5F;

    public ItemLandingSound() {
        NeoForge.EVENT_BUS.addListener(this::onTick);
        NeoForge.EVENT_BUS.addListener(this::onCommands);
    }

    private void onCommands(RegisterClientCommandsEvent event) {
        event.getDispatcher().register(Commands.literal("itemlandingsound:volume")
                .then(Commands.argument("landingVolume", FloatArgumentType.floatArg(0.0F, 2.0F)).executes(ctx -> {
                    volume = FloatArgumentType.getFloat(ctx, "landingVolume");
                    Minecraft mc = Minecraft.getInstance();
                    if (mc.player != null) {
                        mc.player.displayClientMessage(Component.literal("[Item Landing Sound] volume set to " + volume), false);
                        if (volume > 0) mc.player.playSound(SoundEvents.ITEM_PICKUP, volume, 1.0F);
                    }
                    return 1;
                })));
    }

    private void onTick(ClientTickEvent.Post event) {
        Minecraft mc = Minecraft.getInstance();
        ClientLevel level = mc.level;
        if (level == null || mc.player == null || volume <= 0) return;
        for (ItemEntity item : level.getEntitiesOfClass(ItemEntity.class, mc.player.getBoundingBox().inflate(32.0), e -> true)) {
            if (!item.onGround() || item.yo == item.getY()) continue;
            BlockPos at = item.blockPosition();
            BlockPos target = level.getBlockState(at).isAir() ? at.below() : at;
            level.playLocalSound(target.getX() + 0.5, target.getY() - 1, target.getZ() + 0.5,
                    level.getBlockState(target).getSoundType().getStepSound(), SoundSource.BLOCKS, volume, 2.0F, false);
        }
    }
}
