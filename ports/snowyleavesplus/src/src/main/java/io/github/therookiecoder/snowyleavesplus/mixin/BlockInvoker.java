// SPDX-License-Identifier: MPL-2.0
package io.github.therookiecoder.snowyleavesplus.mixin;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Invoker;

@Mixin(Block.class)
public interface BlockInvoker {
    @Invoker("registerDefaultState")
    void snowyleavesplus$registerDefaultState(BlockState state);
}
