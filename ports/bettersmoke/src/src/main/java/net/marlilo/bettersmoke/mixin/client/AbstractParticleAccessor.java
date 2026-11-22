// SPDX-License-Identifier: MIT
// Better Smoke by Marlilo (MIT, Modrinth better-smoke 0.1.2+1.21-1.21.8). No public source: recovered from the
// published jar (Vineflower 1.10.1), remapped intermediary->Mojang (scripts/remap_intermediary.py) and ported to
// NeoForge 1.21.1 by Project Horizon. Logic unchanged.
package net.marlilo.bettersmoke.mixin.client;

import net.minecraft.client.particle.Particle;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;
import org.spongepowered.asm.mixin.gen.Invoker;

@Mixin({Particle.class})
public interface AbstractParticleAccessor {
   @Accessor("xd")
   double bettersmoke$getVelocityX();

   @Accessor("xd")
   void bettersmoke$setVelocityX(double var1);

   @Accessor("yd")
   double bettersmoke$getVelocityY();

   @Accessor("yd")
   void bettersmoke$setVelocityY(double var1);

   @Accessor("zd")
   double bettersmoke$getVelocityZ();

   @Accessor("zd")
   void bettersmoke$setVelocityZ(double var1);

   @Accessor("age")
   int bettersmoke$getAge();

   @Accessor("age")
   void bettersmoke$setAge(int var1);

   @Accessor("lifetime")
   int bettersmoke$getMaxAge();

   @Accessor("lifetime")
   void bettersmoke$setMaxAge(int var1);

   @Invoker("remove")
   void bettersmoke$markDead();

   @Accessor("x")
   double bettersmoke$getX();

   @Accessor("x")
   void bettersmoke$setX(double var1);

   @Accessor("y")
   double bettersmoke$getY();

   @Accessor("z")
   double bettersmoke$getZ();

   @Accessor("z")
   void bettersmoke$setZ(double var1);

   @Accessor("rCol")
   float bettersmoke$getRed();

   @Accessor("rCol")
   void bettersmoke$setRed(float var1);

   @Accessor("gCol")
   float bettersmoke$getGreen();

   @Accessor("gCol")
   void bettersmoke$setGreen(float var1);

   @Accessor("bCol")
   float bettersmoke$getBlue();

   @Accessor("bCol")
   void bettersmoke$setBlue(float var1);

   @Accessor("alpha")
   float bettersmoke$getAlpha();

   @Accessor("alpha")
   void bettersmoke$setAlpha(float var1);
}
