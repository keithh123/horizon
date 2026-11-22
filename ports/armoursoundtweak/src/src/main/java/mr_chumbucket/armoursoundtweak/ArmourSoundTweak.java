// SPDX-License-Identifier: Apache-2.0
// Port of Armour Sound Tweak Updated (yourlocalfinancialadvisor/ArmourSoundTweakUpdated, branch 1.21.2, commit 5433562;
// based on Mr_Chumbucket's Armour Sound Tweak). Changes for NeoForge 1.21.1, by Project Horizon:
//  - Fabric ClientTickEvents.START_CLIENT_TICK -> NeoForge ClientTickEvent.Pre (client dist only)
//  - 1.21.2 EQUIPPABLE/GLIDER components -> 1.21.1 ArmorItem material equip sound / ElytraItem
//  - MidnightLib + ModMenu config -> NeoForge client ModConfigSpec (same four switches, same defaults)
// Behaviour unchanged: while the inventory screen is open, changing an equipment slot plays the removed item's equip sound.
package mr_chumbucket.armoursoundtweak;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.inventory.CreativeModeInventoryScreen;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.ElytraItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.AbstractSkullBlock;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.common.ModConfigSpec;
import net.neoforged.neoforge.common.NeoForge;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

@Mod(value = ArmourSoundTweak.MOD_ID, dist = Dist.CLIENT)
public final class ArmourSoundTweak {
    public static final String MOD_ID = "armoursoundtweak";

    static final ModConfigSpec SPEC;
    static final ModConfigSpec.BooleanValue ARMOUR, ELYTRA, SKULLS, PUMPKINS;

    static {
        ModConfigSpec.Builder b = new ModConfigSpec.Builder();
        b.push("sounds");
        ARMOUR = b.define("armour", true);
        ELYTRA = b.define("elytra", true);
        SKULLS = b.define("skulls", true);
        PUMPKINS = b.define("pumpkins", true);
        b.pop();
        SPEC = b.build();
    }

    private List<ItemStack> oldEquipment = Collections.emptyList();

    public ArmourSoundTweak(IEventBus modBus, ModContainer container) {
        container.registerConfig(ModConfig.Type.CLIENT, SPEC);
        NeoForge.EVENT_BUS.addListener(this::onClientTick);
    }

    private static SoundEvent getEquipSound(ItemStack stack) {
        Item item = stack.getItem();
        if (ARMOUR.get() && item instanceof ArmorItem armor) return armor.getMaterial().value().equipSound().value();
        if (ELYTRA.get() && item instanceof ElytraItem) return SoundEvents.ARMOR_EQUIP_ELYTRA.value();
        if ((PUMPKINS.get() && item == Items.CARVED_PUMPKIN) || (SKULLS.get() && isSkull(item))) return SoundEvents.ARMOR_EQUIP_GENERIC.value();
        return null;
    }

    private static boolean isSkull(Item item) {
        return item instanceof BlockItem bi && bi.getBlock() instanceof AbstractSkullBlock;
    }

    private void onClientTick(ClientTickEvent.Pre event) {
        Minecraft mc = Minecraft.getInstance();
        LocalPlayer player = mc.player;
        if (player == null || !player.level().isClientSide) return;
        List<ItemStack> equipment = new ArrayList<>(4);
        for (ItemStack s : player.getArmorSlots()) equipment.add(s.copy());
        if (mc.screen instanceof InventoryScreen || mc.screen instanceof CreativeModeInventoryScreen) {
            Iterator<ItemStack> now = equipment.iterator(), before = oldEquipment.iterator();
            while (before.hasNext() && now.hasNext()) {
                ItemStack n = now.next(), o = before.next();
                if (!ItemStack.matches(n, o)) {
                    SoundEvent sound = getEquipSound(o);
                    if (sound != null) player.playSound(sound, 1.0F, 1.0F);
                }
            }
        }
        oldEquipment = equipment;
    }
}
