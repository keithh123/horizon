// SPDX-License-Identifier: MPL-2.0
// Port of LeavesBlockMixin from theRookieCoder/SnowyLeavesPlus (Yarn appendProperties/hasRandomTicks/randomTick ->
// Mojang createBlockStateDefinition/isRandomlyTicking/randomTick). Logic unchanged; setBlock only when the value changes.
package io.github.therookiecoder.snowyleavesplus.mixin;

import io.github.therookiecoder.snowyleavesplus.Snowiness;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.LightLayer;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.LeavesBlock;
import net.minecraft.world.level.block.MangroveLeavesBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import static io.github.therookiecoder.snowyleavesplus.Snowiness.SNOWINESS;

@Mixin(LeavesBlock.class)
public abstract class LeavesBlockMixin {
    @Unique
    private boolean snowyleavesplus$shouldModify() {
        // exact vanilla classes only; modded leaves subclasses keep their own state definitions
        return this.getClass().equals(LeavesBlock.class) || this.getClass().equals(MangroveLeavesBlock.class);
    }

    @Inject(method = "createBlockStateDefinition", at = @At("TAIL"))
    private void snowyleavesplus$addProperty(StateDefinition.Builder<Block, BlockState> builder, CallbackInfo ci) {
        if (snowyleavesplus$shouldModify()) builder.add(SNOWINESS);
    }

    @Inject(method = "<init>", at = @At("TAIL"))
    private void snowyleavesplus$defaultState(BlockBehaviour.Properties properties, CallbackInfo ci) {
        if (!snowyleavesplus$shouldModify()) return;
        Block self = (Block) (Object) this;
        ((BlockInvoker) this).snowyleavesplus$registerDefaultState(self.defaultBlockState().setValue(SNOWINESS, Snowiness.none));
    }

    @Inject(method = "isRandomlyTicking", at = @At("RETURN"), cancellable = true)
    private void snowyleavesplus$alwaysTick(BlockState state, CallbackInfoReturnable<Boolean> cir) {
        if (snowyleavesplus$shouldModify()) cir.setReturnValue(true);
    }

    @Inject(method = "randomTick", at = @At("HEAD"))
    private void snowyleavesplus$randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random, CallbackInfo ci) {
        if (!snowyleavesplus$shouldModify() || !state.hasProperty(SNOWINESS)) return;
        Snowiness current = state.getValue(SNOWINESS);
        Snowiness next = level.isRaining()
                && level.getBiome(pos).value().getPrecipitationAt(pos) == Biome.Precipitation.SNOW
                && level.getBrightness(LightLayer.SKY, pos) > 10
                ? current.increaseSnowiness() : current.decreaseSnowiness();
        if (next != current) level.setBlockAndUpdate(pos, state.setValue(SNOWINESS, next));
    }
}
