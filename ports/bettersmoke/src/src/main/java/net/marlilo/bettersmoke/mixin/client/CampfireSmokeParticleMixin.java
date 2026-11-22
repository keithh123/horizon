// SPDX-License-Identifier: MIT
// Better Smoke by Marlilo (MIT, Modrinth better-smoke 0.1.2+1.21-1.21.8). No public source: recovered from the
// published jar (Vineflower 1.10.1), remapped intermediary->Mojang (scripts/remap_intermediary.py) and ported to
// NeoForge 1.21.1 by Project Horizon. Logic unchanged.
package net.marlilo.bettersmoke.mixin.client;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;
import net.marlilo.bettersmoke.client.BettersmokeConfig;
import net.marlilo.bettersmoke.client.WindManager;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.block.HayBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.client.Minecraft;
import net.minecraft.world.level.block.CampfireBlock;
import net.minecraft.client.particle.CampfireSmokeParticle;
import net.minecraft.core.Direction.Plane;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin({CampfireSmokeParticle.class})
public abstract class CampfireSmokeParticleMixin {
   @Unique
   private int bettersmoke$adjacentCount = -1;
   @Unique
   private float bettersmoke$initScale;
   @Unique
   private float bettersmoke$initAlpha;
   @Unique
   private float bettersmoke$initRed;
   @Unique
   private boolean bettersmoke$hasHaybale;
   @Unique
   private float bettersmoke$seedX;
   @Unique
   private float bettersmoke$seedZ;
   @Unique
   private float bettersmoke$seedPhase;
   @Unique
   private boolean bettersmoke$isBeehive;
   @Unique
   private boolean bettersmoke$isSoulCampfire;

   @Inject(
      method = {"<init>"},
      at = {@At("TAIL")}
   )
   private void bettersmoke$onInit(CallbackInfo ci) {
      if (BettersmokeConfig.INSTANCE.enabled) {
         AbstractParticleAccessor self = (AbstractParticleAccessor)this;
         BillboardParticleAccessor sqp = (BillboardParticleAccessor)this;
         this.bettersmoke$initAlpha = self.bettersmoke$getAlpha();
         this.bettersmoke$initScale = sqp.bettersmoke$getScale();
         this.bettersmoke$initRed = self.bettersmoke$getRed();
         int maxAge = self.bettersmoke$getMaxAge();
         double px = self.bettersmoke$getX();
         double py = self.bettersmoke$getY();
         double pz = self.bettersmoke$getZ();
         Level world = Minecraft.getInstance().level;
         boolean isBeehiveSmoke = false;
         if (world != null) {
            label58:
            for (int dy = 0; dy <= 4; dy++) {
               int baseY = (int)Math.floor(py) - dy;

               for (int dx = -1; dx <= 1; dx++) {
                  for (int dz = -1; dz <= 1; dz++) {
                     BlockPos check = new BlockPos((int)Math.floor(px) + dx, baseY, (int)Math.floor(pz) + dz);
                     BlockState st = world.getBlockState(check);
                     if (st.getBlock() instanceof CampfireBlock && st.hasProperty(BlockStateProperties.LIT) && (Boolean)st.getValue(BlockStateProperties.LIT)
                        )
                      {
                        if (!hasBeehiveAbove(world, check) && world.canSeeSky(check.above())) {
                           this.bettersmoke$isSoulCampfire = st.is(Blocks.SOUL_CAMPFIRE);
                        } else {
                           isBeehiveSmoke = true;
                        }
                        break label58;
                     }
                  }
               }
            }
         }

         if (!isBeehiveSmoke && (maxAge >= 200 || this.bettersmoke$isSoulCampfire)) {
            self.bettersmoke$setAlpha(0.0F);
            sqp.bettersmoke$setScale(0.0F);
         }
      }
   }

   @Inject(
      method = {"tick"},
      at = {@At("HEAD")}
   )
   private void bettersmoke$onTickHead(CallbackInfo ci) {
      if (BettersmokeConfig.INSTANCE.enabled && !this.bettersmoke$isBeehive) {
         AbstractParticleAccessor self = (AbstractParticleAccessor)this;
         if (this.bettersmoke$adjacentCount == -1) {
            Random rng = new Random();
            this.bettersmoke$seedX = rng.nextFloat() * (float) (Math.PI * 2);
            this.bettersmoke$seedZ = rng.nextFloat() * (float) (Math.PI * 2);
            this.bettersmoke$seedPhase = rng.nextFloat() * (float) (Math.PI * 2);
            double px = self.bettersmoke$getX();
            double py = self.bettersmoke$getY();
            double pz = self.bettersmoke$getZ();
            Level world = Minecraft.getInstance().level;
            int count = 0;
            boolean haybale = false;
            if (world != null) {
               BlockPos campfirePos = null;

               label125:
               for (int dy = 0; dy <= 4; dy++) {
                  int baseY = (int)Math.floor(py) - dy;

                  for (int dx = -1; dx <= 1; dx++) {
                     for (int dz = -1; dz <= 1; dz++) {
                        BlockPos check = new BlockPos((int)Math.floor(px) + dx, baseY, (int)Math.floor(pz) + dz);
                        BlockState st = world.getBlockState(check);
                        if (st.getBlock() instanceof CampfireBlock
                           && st.hasProperty(BlockStateProperties.LIT)
                           && (Boolean)st.getValue(BlockStateProperties.LIT)) {
                           campfirePos = check;
                           break label125;
                        }
                     }
                  }
               }

               if (campfirePos != null && (hasBeehiveAbove(world, campfirePos) || !world.canSeeSky(campfirePos.above()))) {
                  this.bettersmoke$isBeehive = true;
                  this.bettersmoke$adjacentCount = 0;
                  return;
               }

               if (campfirePos != null) {
                  this.bettersmoke$isSoulCampfire = world.getBlockState(campfirePos).is(Blocks.SOUL_CAMPFIRE);
                  List<BlockPos> cluster = new ArrayList<>();
                  Set<BlockPos> visitedBFS = new HashSet<>();
                  Deque<BlockPos> bfsQueue = new ArrayDeque<>();
                  bfsQueue.add(campfirePos);
                  visitedBFS.add(campfirePos);

                  while (!bfsQueue.isEmpty() && cluster.size() < 64) {
                     BlockPos cur = bfsQueue.poll();
                     cluster.add(cur);
                     if (world.getBlockState(cur.below()).getBlock() instanceof HayBlock) {
                        haybale = true;
                     }

                     for (Direction dir : Plane.HORIZONTAL) {
                        BlockPos nb = cur.relative(dir);
                        if (!visitedBFS.contains(nb)) {
                           BlockState st = world.getBlockState(nb);
                           if (st.getBlock() instanceof CampfireBlock
                              && st.hasProperty(BlockStateProperties.LIT)
                              && (Boolean)st.getValue(BlockStateProperties.LIT)
                              && !hasBeehiveAbove(world, nb)
                              && world.canSeeSky(nb.above())) {
                              visitedBFS.add(nb);
                              bfsQueue.add(nb);
                           }
                        }
                     }
                  }

                  count = cluster.size() - 1;
                  if (count > 0) {
                     int maxAge = self.bettersmoke$getMaxAge();
                     if (maxAge >= 200) {
                        float mult = haybale ? 1.8F : 1.3F;
                        mult *= BettersmokeConfig.INSTANCE.particleLifetimeMultiplier;
                        self.bettersmoke$setMaxAge((int)((float)maxAge * mult));
                     }
                  }
               }
            }

            int maxAgeFinal = self.bettersmoke$getMaxAge();
            if (maxAgeFinal < 200) {
               count = 0;
            }

            this.bettersmoke$adjacentCount = count;
            this.bettersmoke$hasHaybale = haybale;
            if (count > 0) {
               float yVar = this.bettersmoke$seedPhase / (float) (Math.PI * 2);
               self.bettersmoke$setVelocityY(self.bettersmoke$getVelocityY() + (double)(-0.015F + yVar * 0.03F));
            }
         }

         int age = self.bettersmoke$getAge();
         int maxAge = self.bettersmoke$getMaxAge();
         float ageFactor = (float)age / (float)Math.max(maxAge, 1);
         if (this.bettersmoke$adjacentCount > 0) {
            double windScale = this.bettersmoke$hasHaybale ? 1.6 : 1.0;
            double windInfluence = 0.0012 * (0.1 + (double)ageFactor * 2.0) * windScale;
            self.bettersmoke$setVelocityX(self.bettersmoke$getVelocityX() + WindManager.getWindX() * windInfluence);
            self.bettersmoke$setVelocityZ(self.bettersmoke$getVelocityZ() + WindManager.getWindZ() * windInfluence);
            if (ageFactor > 0.05F) {
               float turbRamp = (ageFactor - 0.05F) / 0.95F;
               float turbStrength = (float)(0.0015 * (double)Math.min(1.0F, turbRamp * 2.0F));
               float t = ageFactor * 18.0F;
               double turbX = Math.sin((double)(t + this.bettersmoke$seedX)) * (double)turbStrength
                  + Math.sin((double)(t * 1.7F + this.bettersmoke$seedPhase)) * (double)turbStrength * 0.5;
               double turbZ = Math.cos((double)(t + this.bettersmoke$seedZ)) * (double)turbStrength
                  + Math.cos((double)(t * 2.1F + this.bettersmoke$seedPhase * 1.3F)) * (double)turbStrength * 0.5;
               self.bettersmoke$setVelocityX(self.bettersmoke$getVelocityX() + turbX);
               self.bettersmoke$setVelocityZ(self.bettersmoke$getVelocityZ() + turbZ);
            }

            double gustInfluence = windScale * 0.001 * (0.3 + (double)ageFactor);
            self.bettersmoke$setVelocityX(self.bettersmoke$getVelocityX() + WindManager.getGustX() * gustInfluence);
            self.bettersmoke$setVelocityZ(self.bettersmoke$getVelocityZ() + WindManager.getGustZ() * gustInfluence);
         } else {
            double pxx = self.bettersmoke$getX();
            double pyx = self.bettersmoke$getY();
            double pzx = self.bettersmoke$getZ();
            float turbPhaseX = (float)(pxx * 127.3 + pyx * 311.7);
            float turbPhaseZ = (float)(pzx * 191.1 + pyx * 59.3 + pxx * 17.7);
            float turbPhaseY = (float)(pzx * 89.7 + pxx * 233.1);
            float turbMult = BettersmokeConfig.INSTANCE.turbulenceStrength;
            float turbRamp = Math.max(0.0F, ageFactor - 0.2F) / 0.8F;
            float turbStrength = turbRamp * turbRamp * 0.005F * turbMult;
            float turbT = ageFactor * 20.0F;
            double turbX = Math.sin((double)(turbT + turbPhaseX)) * (double)turbStrength
               + Math.sin((double)(turbT * 2.3F + turbPhaseX * 1.5F)) * (double)turbStrength * 0.4;
            double turbZ = Math.cos((double)(turbT + turbPhaseZ)) * (double)turbStrength
               + Math.cos((double)(turbT * 2.7F + turbPhaseZ * 1.7F)) * (double)turbStrength * 0.4;
            float turbRampY = Math.max(0.0F, ageFactor - 0.1F) / 0.9F;
            float turbStrengthY = turbRampY * 0.011F * turbMult;
            double turbY = Math.sin((double)(turbT * 1.0F + turbPhaseY)) * (double)turbStrengthY * 0.42
               + Math.sin((double)(turbT * 2.8F + turbPhaseY * 1.3F)) * (double)turbStrengthY * 0.38
               + Math.sin((double)(turbT * 7.1F + turbPhaseY * 0.6F)) * (double)turbStrengthY * 0.14
               + Math.sin((double)(turbT * 14.3F + turbPhaseY * 0.9F)) * (double)turbStrengthY * 0.06;
            double windInfluence = 0.001 * (0.3 + (double)ageFactor * 1.5);
            double gustInfluence = 8.0E-4 * (0.2 + (double)ageFactor);
            double gustMag = Math.abs(WindManager.getGustX()) + Math.abs(WindManager.getGustZ());
            self.bettersmoke$setVelocityX(
               self.bettersmoke$getVelocityX() + WindManager.getWindX() * windInfluence + WindManager.getGustX() * gustInfluence + turbX
            );
            self.bettersmoke$setVelocityZ(
               self.bettersmoke$getVelocityZ() + WindManager.getWindZ() * windInfluence + WindManager.getGustZ() * gustInfluence + turbZ
            );
            self.bettersmoke$setVelocityY(self.bettersmoke$getVelocityY() + turbY - gustMag * 3.0E-4 * (0.2 + (double)ageFactor));
         }
      }
   }

   @Inject(
      method = {"tick"},
      at = {@At("TAIL")}
   )
   private void bettersmoke$onTickTail(CallbackInfo ci) {
      if (BettersmokeConfig.INSTANCE.enabled && !this.bettersmoke$isBeehive) {
         AbstractParticleAccessor self = (AbstractParticleAccessor)this;
         BillboardParticleAccessor sqp = (BillboardParticleAccessor)this;
         int age = self.bettersmoke$getAge();
         int maxAge = self.bettersmoke$getMaxAge();
         float ageFactor = (float)age / (float)Math.max(maxAge, 1);
         if (this.bettersmoke$adjacentCount > 0) {
            float scaleCfg = BettersmokeConfig.INSTANCE.clusterScaleMultiplier;
            float endMult = Math.min(
                  this.bettersmoke$hasHaybale ? 9.0F + (float)this.bettersmoke$adjacentCount * 0.5F : 7.0F + (float)this.bettersmoke$adjacentCount * 0.5F,
                  this.bettersmoke$hasHaybale ? 14.0F : 11.0F
               )
               * scaleCfg;
            float tSize = this.bettersmoke$seedX / (float) (Math.PI * 2);
            float sizeVar = 0.6F + (float)Math.sqrt((double)tSize) * 0.8F;
            float minScale = this.bettersmoke$initScale;
            float maxScale = this.bettersmoke$initScale * (this.bettersmoke$hasHaybale ? 12.0F : 8.0F);
            float endScale = Math.min(this.bettersmoke$initScale * endMult * sizeVar, maxScale);
            float scaleFactor = ageFactor * (float)Math.sqrt((double)ageFactor);
            float rawScale = minScale + (endScale - minScale) * scaleFactor;
            sqp.bettersmoke$setScale(Math.max(minScale, Math.min(maxScale, rawScale)));
            float alphaFade;
            if (ageFactor < 0.6F) {
               alphaFade = 1.0F;
            } else {
               float t = (ageFactor - 0.6F) / 0.4F;
               alphaFade = 1.0F - t * t;
            }

            self.bettersmoke$setAlpha(this.bettersmoke$initAlpha * Math.max(0.0F, alphaFade));
            if (this.bettersmoke$isSoulCampfire) {
               float tint = BettersmokeConfig.INSTANCE.soulCampfireTint;
               float ageLerp = Math.min(1.0F, ageFactor / 0.4F);
               float darkBase = this.bettersmoke$initRed * 0.45F;
               float tintedRG = darkBase + (this.bettersmoke$initRed * 0.7F - darkBase) * ageLerp;
               float tintedB = darkBase + (this.bettersmoke$initRed * 0.9F - darkBase) * ageLerp;
               self.bettersmoke$setRed(this.bettersmoke$initRed + (tintedRG - this.bettersmoke$initRed) * tint);
               self.bettersmoke$setGreen(this.bettersmoke$initRed + (tintedRG - this.bettersmoke$initRed) * tint);
               self.bettersmoke$setBlue(this.bettersmoke$initRed + (tintedB - this.bettersmoke$initRed) * tint);
            } else {
               float targetC = Math.min(this.bettersmoke$initRed * 1.1F, 1.0F);
               float c = this.bettersmoke$initRed * 0.65F + (targetC - this.bettersmoke$initRed * 0.65F) * Math.min(1.0F, ageFactor / 0.3F);
               self.bettersmoke$setRed(c);
               self.bettersmoke$setGreen(c);
               self.bettersmoke$setBlue(c);
            }
         } else {
            float holdUntil = 0.65F;
            float alphaFadex = ageFactor < holdUntil ? 1.0F : 1.0F - (ageFactor - holdUntil) / (1.0F - holdUntil);
            self.bettersmoke$setAlpha(this.bettersmoke$initAlpha * Math.max(0.0F, alphaFadex));
            float endScalex = this.bettersmoke$initScale * (this.bettersmoke$hasHaybale ? 4.0F : 2.0F);
            sqp.bettersmoke$setScale(this.bettersmoke$initScale + (endScalex - this.bettersmoke$initScale) * ageFactor);
            if (this.bettersmoke$isSoulCampfire) {
               float tint = BettersmokeConfig.INSTANCE.soulCampfireTint;
               float ageLerp = Math.min(1.0F, ageFactor / 0.4F);
               float darkBase = this.bettersmoke$initRed * 0.45F;
               float tintedRG = darkBase + (this.bettersmoke$initRed * 0.7F - darkBase) * ageLerp;
               float tintedB = darkBase + (this.bettersmoke$initRed * 0.9F - darkBase) * ageLerp;
               self.bettersmoke$setRed(this.bettersmoke$initRed + (tintedRG - this.bettersmoke$initRed) * tint);
               self.bettersmoke$setGreen(this.bettersmoke$initRed + (tintedRG - this.bettersmoke$initRed) * tint);
               self.bettersmoke$setBlue(this.bettersmoke$initRed + (tintedB - this.bettersmoke$initRed) * tint);
            }
         }
      }
   }

   @Unique
   private static boolean hasBeehiveAbove(Level world, BlockPos pos) {
      for (int dy = 1; dy <= 5; dy++) {
         BlockState above = world.getBlockState(pos.above(dy));
         if (above.is(Blocks.BEEHIVE) || above.is(Blocks.BEE_NEST)) {
            return true;
         }
      }

      return false;
   }
}
