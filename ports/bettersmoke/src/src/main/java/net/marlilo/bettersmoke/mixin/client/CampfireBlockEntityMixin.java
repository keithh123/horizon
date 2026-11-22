// SPDX-License-Identifier: MIT
// Better Smoke by Marlilo (MIT, Modrinth better-smoke 0.1.2+1.21-1.21.8). No public source: recovered from the
// published jar (Vineflower 1.10.1), remapped intermediary->Mojang (scripts/remap_intermediary.py) and ported to
// NeoForge 1.21.1 by Project Horizon. Logic unchanged.
package net.marlilo.bettersmoke.mixin.client;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import net.marlilo.bettersmoke.client.BettersmokeConfig;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.world.level.block.CampfireBlock;
import net.minecraft.world.level.block.entity.CampfireBlockEntity;
import net.minecraft.util.RandomSource;
import net.minecraft.core.Direction.Plane;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin({CampfireBlockEntity.class})
public class CampfireBlockEntityMixin {
   @Inject(
      method = {"particleTick"},
      at = {@At("HEAD")},
      cancellable = true
   )
   private static void bettersmoke$replaceSmoke(Level world, BlockPos pos, BlockState state, CampfireBlockEntity blockEntity, CallbackInfo ci) {
      if (BettersmokeConfig.INSTANCE.enabled) {
         if (world.isClientSide()) {
            if ((Boolean)state.getValue(CampfireBlock.LIT)) {
               Minecraft mc = Minecraft.getInstance();
               if (mc != null && mc.particleEngine != null) {
                  if (!hasBeehiveAbove(world, pos) && world.canSeeSky(pos.above())) {
                     boolean haybale = world.getBlockState(pos.below()).is(Blocks.HAY_BLOCK);
                     ci.cancel();
                     RandomSource random = world.getRandom();
                     List<BlockPos> cluster = new ArrayList<>();
                     Set<BlockPos> visited = new HashSet<>();
                     Deque<BlockPos> queue = new ArrayDeque<>();
                     BlockPos start = pos.immutable();
                     queue.add(start);
                     visited.add(start);

                     while (!queue.isEmpty() && cluster.size() < 64) {
                        BlockPos cur = queue.poll();
                        cluster.add(cur);

                        for (Direction dir : Plane.HORIZONTAL) {
                           BlockPos nb = cur.relative(dir).immutable();
                           if (!visited.contains(nb) && isLitCampfire(world, nb) && !hasBeehiveAbove(world, nb) && world.canSeeSky(nb.above())) {
                              visited.add(nb);
                              queue.add(nb);
                           }
                        }
                     }

                     if (cluster.size() == 1) {
                        BettersmokeConfig cfg = BettersmokeConfig.INSTANCE;
                        double velY = (haybale ? 0.1 : 0.07) * (double)cfg.riseSpeed;
                        double spread = 0.6 * (double)cfg.smokeSpread;
                        SimpleParticleType smokeType = haybale ? ParticleTypes.CAMPFIRE_SIGNAL_SMOKE : ParticleTypes.CAMPFIRE_COSY_SMOKE;
                        int attempts = haybale ? 5 : 3;

                        for (int i = 0; i < attempts; i++) {
                           if (random.nextInt(10) == 0) {
                              double x = (double)pos.getX() + 0.5 + (random.nextDouble() - 0.5) * spread;
                              double y = (double)pos.getY() + 0.8 + random.nextDouble() * 0.2;
                              double z = (double)pos.getZ() + 0.5 + (random.nextDouble() - 0.5) * spread;
                              double vx = (random.nextDouble() - 0.5) * 0.012;
                              double vz = (random.nextDouble() - 0.5) * 0.012;
                              mc.particleEngine.createParticle(smokeType, x, y, z, vx, velY, vz);
                           }
                        }
                     } else {
                        BlockPos leader = cluster.stream()
                           .min(Comparator.<BlockPos, Integer>comparing(bp -> bp.getX()).thenComparing(bp -> bp.getZ()))
                           .orElse(start);
                        if (!start.equals(leader)) {
                           return;
                        }

                        int clusterSize = cluster.size();
                        double centroidX = 0.0;
                        double centroidZ = 0.0;
                        boolean clusterHaybale = false;

                        for (BlockPos cp : cluster) {
                           centroidX += (double)cp.getX() + 0.5;
                           centroidZ += (double)cp.getZ() + 0.5;
                           if (world.getBlockState(cp.below()).is(Blocks.HAY_BLOCK)) {
                              clusterHaybale = true;
                           }
                        }

                        centroidX /= (double)clusterSize;
                        centroidZ /= (double)clusterSize;
                        double spread = Math.min(clusterHaybale ? 0.6 + (double)(clusterSize - 1) * 0.35 : 0.5 + (double)(clusterSize - 1) * 0.3, 4.0);
                        double clusterVelY = clusterHaybale ? 0.12 : 0.08;
                        int attempts = Math.min(clusterHaybale ? 12 * clusterSize : 8 * clusterSize, 80);

                        for (int ix = 0; ix < attempts; ix++) {
                           if (random.nextInt(10) == 0) {
                              double x = centroidX + (random.nextDouble() - 0.5) * spread;
                              double y = (double)start.getY() + 0.8 + random.nextDouble() * 0.1;
                              double z = centroidZ + (random.nextDouble() - 0.5) * spread;
                              double vx = (random.nextDouble() - 0.5) * 0.02;
                              double vz = (random.nextDouble() - 0.5) * 0.02;
                              mc.particleEngine.createParticle(ParticleTypes.CAMPFIRE_SIGNAL_SMOKE, x, y, z, vx, clusterVelY, vz);
                           }
                        }
                     }
                  }
               }
            }
         }
      }
   }

   private static boolean isLitCampfire(Level world, BlockPos pos) {
      BlockState s = world.getBlockState(pos);
      return s.getBlock() instanceof CampfireBlock && (Boolean)s.getValue(CampfireBlock.LIT);
   }

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
