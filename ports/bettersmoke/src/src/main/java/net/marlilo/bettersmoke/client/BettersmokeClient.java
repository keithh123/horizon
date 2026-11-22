// SPDX-License-Identifier: MIT
// Better Smoke by Marlilo (MIT). NeoForge entry point by Project Horizon: replaces the Fabric client initializer,
// END_CLIENT_TICK registration and ModMenu screen factory; the Fabric datagen entry point is dropped (unused at runtime).
package net.marlilo.bettersmoke.client;

import net.minecraft.client.Minecraft;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.gui.IConfigScreenFactory;
import net.neoforged.neoforge.common.NeoForge;

@Mod(value = "bettersmoke", dist = Dist.CLIENT)
public class BettersmokeClient {
   public BettersmokeClient(ModContainer container) {
      BettersmokeConfig.INSTANCE.load();
      NeoForge.EVENT_BUS.addListener((ClientTickEvent.Post e) -> WindManager.tick(Minecraft.getInstance()));
      container.registerExtensionPoint(IConfigScreenFactory.class, (mc, parent) -> new BettersmokeConfigScreen(parent));
   }
}
