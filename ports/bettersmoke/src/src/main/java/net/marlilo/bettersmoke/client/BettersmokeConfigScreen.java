// SPDX-License-Identifier: MIT
// Better Smoke by Marlilo (MIT, Modrinth better-smoke 0.1.2+1.21-1.21.8). No public source: recovered from the
// published jar (Vineflower 1.10.1), remapped intermediary->Mojang (scripts/remap_intermediary.py) and ported to
// NeoForge 1.21.1 by Project Horizon. Logic unchanged.
package net.marlilo.bettersmoke.client;

import java.util.function.Consumer;
import net.minecraft.network.chat.Component;
import net.minecraft.client.gui.components.AbstractSliderButton;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;

public class BettersmokeConfigScreen extends Screen {
   private final Screen parent;
   private final BettersmokeConfig cfg = BettersmokeConfig.INSTANCE;
   private static final float DEF_WIND_STRENGTH = 1.0F;
   private static final float DEF_GUST_STRENGTH = 1.0F;
   private static final float DEF_RAIN_WIND_MULTIPLIER = 1.6F;
   private static final float DEF_THUNDER_WIND_MULTIPLIER = 2.2F;
   private static final float DEF_PARTICLE_LIFETIME = 1.0F;
   private static final float DEF_CLUSTER_SCALE = 1.0F;
   private static final float DEF_WIND_DIRECTION = -999.0F;
   private static final float DEF_TURBULENCE_STRENGTH = 1.0F;
   private static final float DEF_RISE_SPEED = 1.0F;
   private static final float DEF_SMOKE_SPREAD = 1.0F;
   private static final float DEF_SOUL_CAMPFIRE_TINT = 1.0F;
   private static boolean advancedExpanded = false;

   public BettersmokeConfigScreen(Screen parent) {
      super(Component.literal("Better Smoke Settings"));
      this.parent = parent;
   }

   protected void init() {
      int centreX = this.width / 2;
      int y = 40;
      int sliderW = 200;
      int resetW = 40;
      int gap = 4;
      int h = 20;
      int rowGap = 26;
      int rowX = centreX - (sliderW + gap + resetW) / 2;
      this.addRenderableWidget(Button.builder(Component.literal("Enabled: " + (this.cfg.enabled ? "ON" : "OFF")), btn -> {
         this.cfg.enabled = !this.cfg.enabled;
         btn.setMessage(Component.literal("Enabled: " + (this.cfg.enabled ? "ON" : "OFF")));
      }).bounds(rowX, y, sliderW + gap + resetW, h).build());
      y += rowGap;
      this.addRenderableWidget(new BettersmokeConfigScreen.WindDirectionSlider(rowX, y, sliderW, h, this.cfg.windDirection, v -> this.cfg.windDirection = v));
      this.addRenderableWidget(Button.builder(Component.literal("Reset"), btn -> {
         this.cfg.windDirection = -999.0F;
         this.rebuildWidgets();
      }).bounds(rowX + sliderW + gap, y, resetW, h).build());
      y += rowGap;
      y = this.addSliderRow(
         rowX,
         y,
         sliderW,
         resetW,
         gap,
         h,
         "Particle Lifetime",
         this.cfg.particleLifetimeMultiplier,
         0.5F,
         2.0F,
         1.0F,
         v -> this.cfg.particleLifetimeMultiplier = v
      );
      this.addRenderableWidget(Button.builder(Component.literal("Advanced " + (advancedExpanded ? "▲" : "▼")), btn -> {
         advancedExpanded = !advancedExpanded;
         this.rebuildWidgets();
      }).bounds(rowX, y, sliderW + gap + resetW, h).build());
      y += rowGap;
      if (advancedExpanded) {
         y = this.addSliderRow(rowX, y, sliderW, resetW, gap, h, "Wind Strength", this.cfg.windStrength, 0.0F, 3.0F, 1.0F, v -> this.cfg.windStrength = v);
         y = this.addSliderRow(rowX, y, sliderW, resetW, gap, h, "Gust Strength", this.cfg.gustStrength, 0.0F, 3.0F, 1.0F, v -> this.cfg.gustStrength = v);
         y = this.addSliderRow(
            rowX, y, sliderW, resetW, gap, h, "Turbulence Strength", this.cfg.turbulenceStrength, 0.0F, 3.0F, 1.0F, v -> this.cfg.turbulenceStrength = v
         );
         y = this.addSliderRow(rowX, y, sliderW, resetW, gap, h, "Rise Speed", this.cfg.riseSpeed, 0.2F, 3.0F, 1.0F, v -> this.cfg.riseSpeed = v);
         y = this.addSliderRow(
            rowX, y, sliderW, resetW, gap, h, "Rain Wind Multiplier", this.cfg.rainWindMultiplier, 1.0F, 4.0F, 1.6F, v -> this.cfg.rainWindMultiplier = v
         );
         y = this.addSliderRow(
            rowX,
            y,
            sliderW,
            resetW,
            gap,
            h,
            "Thunder Wind Multiplier",
            this.cfg.thunderWindMultiplier,
            1.0F,
            5.0F,
            2.2F,
            v -> this.cfg.thunderWindMultiplier = v
         );
         y = this.addSliderRow(
            rowX, y, sliderW, resetW, gap, h, "Cluster Scale", this.cfg.clusterScaleMultiplier, 0.5F, 2.0F, 1.0F, v -> this.cfg.clusterScaleMultiplier = v
         );
         y = this.addSliderRow(rowX, y, sliderW, resetW, gap, h, "Smoke Spread", this.cfg.smokeSpread, 0.2F, 3.0F, 1.0F, v -> this.cfg.smokeSpread = v);
         y = this.addSliderRow(
            rowX, y, sliderW, resetW, gap, h, "Soul Campfire Tint", this.cfg.soulCampfireTint, 0.0F, 1.0F, 1.0F, v -> this.cfg.soulCampfireTint = v
         );
      }

      y += 10;
      int btnW = 96;
      int btnGap = 8;
      int totalW = btnW * 2 + btnGap;
      int leftX = centreX - totalW / 2;
      this.addRenderableWidget(Button.builder(Component.literal("Reset All"), btn -> {
         this.cfg.resetToDefaults();
         this.rebuildWidgets();
      }).bounds(leftX, y, btnW, h).build());
      this.addRenderableWidget(
         Button.builder(Component.literal("Done"), btn -> this.onClose()).bounds(leftX + btnW + btnGap, y, btnW, h).build()
      );
   }

   private int addSliderRow(
      int x, int y, int sliderW, int resetW, int gap, int h, String label, float current, float min, float max, float defaultVal, Consumer<Float> setter
   ) {
      this.addRenderableWidget(new BettersmokeConfigScreen.ConfigSlider(x, y, sliderW, h, label, current, min, max, setter));
      this.addRenderableWidget(Button.builder(Component.literal("Reset"), btn -> {
         setter.accept(defaultVal);
         this.rebuildWidgets();
      }).bounds(x + sliderW + gap, y, resetW, h).build());
      return y + 26;
   }

   public void onClose() {
      this.cfg.save();
      if (this.minecraft != null) {
         this.minecraft.setScreen(this.parent);
      }
   }

   private static class ConfigSlider extends AbstractSliderButton {
      private final String label;
      private final float min;
      private final float max;
      private final Consumer<Float> setter;

      ConfigSlider(int x, int y, int w, int h, String label, float current, float min, float max, Consumer<Float> setter) {
         super(x, y, w, h, Component.literal(label + ": " + String.format("%.2f", current)), (double)((current - min) / (max - min)));
         this.label = label;
         this.min = min;
         this.max = max;
         this.setter = setter;
      }

      private float mapped() {
         return this.min + (float)this.value * (this.max - this.min);
      }

      protected void updateMessage() {
         this.setMessage(Component.literal(this.label + ": " + String.format("%.2f", this.mapped())));
      }

      protected void applyValue() {
         this.setter.accept(this.mapped());
      }
   }

   private static class WindDirectionSlider extends AbstractSliderButton {
      private static final int STEPS = 361;
      private final Consumer<Float> setter;

      WindDirectionSlider(int x, int y, int w, int h, float currentDegrees, Consumer<Float> setter) {
         super(x, y, w, h, Component.empty(), toSliderValue(currentDegrees));
         this.setter = setter;
         this.updateMessage();
      }

      private static double toSliderValue(float degrees) {
         if (degrees == -999.0F) {
            return 0.0;
         } else {
            int step = Math.round(degrees) + 181;
            step = Math.max(1, Math.min(361, step));
            return (double)step / 361.0;
         }
      }

      private float toDegrees() {
         int step = (int)Math.round(this.value * 361.0);
         return step <= 0 ? -999.0F : (float)(step - 181);
      }

      private static String yawToCompass(float yaw) {
         float y = (yaw % 360.0F + 360.0F) % 360.0F;
         if (y < 22.5F) {
            return "S";
         } else if (y < 67.5F) {
            return "SW";
         } else if (y < 112.5F) {
            return "W";
         } else if (y < 157.5F) {
            return "NW";
         } else if (y < 202.5F) {
            return "N";
         } else if (y < 247.5F) {
            return "NE";
         } else if (y < 292.5F) {
            return "E";
         } else {
            return y < 337.5F ? "SE" : "S";
         }
      }

      protected void updateMessage() {
         float deg = this.toDegrees();
         if (deg == -999.0F) {
            this.setMessage(Component.literal("Wind Direction: Dynamic"));
         } else {
            this.setMessage(Component.literal("Wind Direction: " + (int)deg + "° (" + yawToCompass(deg) + ")"));
         }
      }

      protected void applyValue() {
         this.setter.accept(this.toDegrees());
      }
   }
}
