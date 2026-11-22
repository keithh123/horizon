// SPDX-License-Identifier: MIT
// Better Smoke by Marlilo (MIT, Modrinth better-smoke 0.1.2+1.21-1.21.8). No public source: recovered from the
// published jar (Vineflower 1.10.1), remapped intermediary->Mojang (scripts/remap_intermediary.py) and ported to
// NeoForge 1.21.1 by Project Horizon. Logic unchanged.
package net.marlilo.bettersmoke.client;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Path;

public class BettersmokeConfig {
   public static final BettersmokeConfig INSTANCE = new BettersmokeConfig();
   private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
   private static final Path CONFIG_PATH = net.neoforged.fml.loading.FMLPaths.CONFIGDIR.get().resolve("bettersmoke.json");
   public boolean enabled = true;
   public float windStrength = 1.0F;
   public float gustStrength = 1.0F;
   public float rainWindMultiplier = 1.6F;
   public float thunderWindMultiplier = 2.2F;
   public float particleLifetimeMultiplier = 1.0F;
   public float clusterScaleMultiplier = 1.0F;
   public float windDirection = -999.0F;
   public float turbulenceStrength = 1.0F;
   public float riseSpeed = 1.0F;
   public float smokeSpread = 1.0F;
   public float soulCampfireTint = 1.0F;

   public void load() {
      if (Files.exists(CONFIG_PATH)) {
         try (Reader reader = Files.newBufferedReader(CONFIG_PATH)) {
            BettersmokeConfig loaded = (BettersmokeConfig)GSON.fromJson(reader, BettersmokeConfig.class);
            if (loaded != null) {
               this.copyFrom(loaded);
            }
         } catch (IOException var6) {
            System.err.println("[bettersmoke] Failed to load config: " + var6.getMessage());
         }
      }
   }

   public void save() {
      try (Writer writer = Files.newBufferedWriter(CONFIG_PATH)) {
         GSON.toJson(this, writer);
      } catch (IOException var6) {
         System.err.println("[bettersmoke] Failed to save config: " + var6.getMessage());
      }
   }

   public void resetToDefaults() {
      this.copyFrom(new BettersmokeConfig());
   }

   private void copyFrom(BettersmokeConfig other) {
      this.enabled = other.enabled;
      this.windStrength = other.windStrength;
      this.gustStrength = other.gustStrength;
      this.rainWindMultiplier = other.rainWindMultiplier;
      this.thunderWindMultiplier = other.thunderWindMultiplier;
      this.particleLifetimeMultiplier = other.particleLifetimeMultiplier;
      this.clusterScaleMultiplier = other.clusterScaleMultiplier;
      this.windDirection = other.windDirection;
      this.turbulenceStrength = other.turbulenceStrength;
      this.riseSpeed = other.riseSpeed;
      this.smokeSpread = other.smokeSpread;
      this.soulCampfireTint = other.soulCampfireTint;
   }
}
