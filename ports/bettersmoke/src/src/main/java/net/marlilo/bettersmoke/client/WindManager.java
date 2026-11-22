// SPDX-License-Identifier: MIT
// Better Smoke by Marlilo (MIT, Modrinth better-smoke 0.1.2+1.21-1.21.8). No public source: recovered from the
// published jar (Vineflower 1.10.1), remapped intermediary->Mojang (scripts/remap_intermediary.py) and ported to
// NeoForge 1.21.1 by Project Horizon. Logic unchanged.
package net.marlilo.bettersmoke.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;

public class WindManager {
   private static long tickCount = 0L;
   private static double windX = 0.0;
   private static double windZ = 0.0;
   private static double gustX = 0.0;
   private static double gustZ = 0.0;
   private static double weatherMultiplier = 1.0;

   public static void tick(Minecraft client) {
      tickCount++;
      double t = (double)tickCount / 20.0;
      BettersmokeConfig cfg = BettersmokeConfig.INSTANCE;
      double target = 1.0;
      ClientLevel world = client.level;
      if (world != null) {
         if (world.isThundering()) {
            target = (double)cfg.thunderWindMultiplier;
         } else if (world.isRaining()) {
            target = (double)cfg.rainWindMultiplier;
         }
      }

      weatherMultiplier = weatherMultiplier + (target - weatherMultiplier) * 0.005;
      double configWind = (double)cfg.windStrength;
      double configGust = (double)cfg.gustStrength;
      windX = (Math.sin(t * 0.03) * 0.55 + Math.sin(t * 0.073) * 0.28 + Math.sin(t * 0.189) * 0.17) * weatherMultiplier * configWind;
      windZ = (Math.cos(t * 0.033) * 0.55 + Math.cos(t * 0.079) * 0.28 + Math.cos(t * 0.197) * 0.17) * weatherMultiplier * configWind;
      double baseGustX = Math.sin(t * 0.31 + 1.1) * 0.22 + Math.sin(t * 0.63 + 2.7) * 0.11;
      double baseGustZ = Math.cos(t * 0.28 + 0.5) * 0.22 + Math.cos(t * 0.57 + 1.9) * 0.11;
      double stormExtra = Math.max(0.0, weatherMultiplier - 1.0);
      double stormGustX = Math.sin(t * 1.1 + 3.3) * 0.18 + Math.sin(t * 2.3 + 0.7) * 0.09;
      double stormGustZ = Math.cos(t * 0.9 + 4.1) * 0.18 + Math.cos(t * 2.1 + 1.5) * 0.09;
      gustX = (baseGustX + stormGustX * stormExtra) * weatherMultiplier * configGust;
      gustZ = (baseGustZ + stormGustZ * stormExtra) * weatherMultiplier * configGust;
      float lockedDir = cfg.windDirection;
      if (lockedDir != -999.0F) {
         double angle = Math.toRadians((double)lockedDir);
         double dx = -Math.sin(angle);
         double dz = Math.cos(angle);
         double wMag = Math.sqrt(windX * windX + windZ * windZ);
         double gMag = Math.sqrt(gustX * gustX + gustZ * gustZ);
         windX = dx * wMag;
         windZ = dz * wMag;
         gustX = dx * gMag;
         gustZ = dz * gMag;
      }
   }

   public static double getWindX() {
      return windX;
   }

   public static double getWindZ() {
      return windZ;
   }

   public static double getGustX() {
      return gustX;
   }

   public static double getGustZ() {
      return gustZ;
   }

   public static double getWeatherMultiplier() {
      return weatherMultiplier;
   }
}
