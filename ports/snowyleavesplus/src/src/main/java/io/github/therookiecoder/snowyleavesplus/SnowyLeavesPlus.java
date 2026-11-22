// SPDX-License-Identifier: MPL-2.0
// Port of SnowyLeavesPlusClient: Fabric ColorProviderRegistry -> NeoForge RegisterColorHandlersEvent.Block.
package io.github.therookiecoder.snowyleavesplus;

import net.minecraft.client.renderer.BiomeColors;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockAndTintGetter;
import net.minecraft.world.level.FoliageColor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.loading.FMLEnvironment;
import net.neoforged.neoforge.client.event.RegisterColorHandlersEvent;

import static io.github.therookiecoder.snowyleavesplus.Snowiness.SNOWINESS;

@Mod("snowyleavesplus")
public class SnowyLeavesPlus {
    public SnowyLeavesPlus(IEventBus modBus) {
        if (FMLEnvironment.dist == Dist.CLIENT) Client.register(modBus);
    }

    static final class Client {
        static void register(IEventBus bus) {
            bus.addListener((RegisterColorHandlersEvent.Block event) -> event.register(
                    (state, level, pos, tintIndex) -> {
                        int colour = leafColour(state.getBlock(), level, pos);
                        if (!state.hasProperty(SNOWINESS)) return colour;
                        return whiten(colour, (double) state.getValue(SNOWINESS).ordinal() / Snowiness.values().length);
                    },
                    Blocks.OAK_LEAVES, Blocks.SPRUCE_LEAVES, Blocks.BIRCH_LEAVES, Blocks.JUNGLE_LEAVES, Blocks.ACACIA_LEAVES,
                    Blocks.DARK_OAK_LEAVES, Blocks.MANGROVE_LEAVES, Blocks.AZALEA_LEAVES, Blocks.FLOWERING_AZALEA_LEAVES));
        }

        // same per-leaf defaults as vanilla BlockColors
        private static int leafColour(Block block, BlockAndTintGetter level, BlockPos pos) {
            if (block == Blocks.BIRCH_LEAVES) return FoliageColor.getBirchColor();
            if (block == Blocks.SPRUCE_LEAVES) return FoliageColor.getEvergreenColor();
            if (block == Blocks.MANGROVE_LEAVES) return FoliageColor.getMangroveColor();
            return level != null && pos != null ? BiomeColors.getAverageFoliageColor(level, pos) : FoliageColor.getDefaultColor();
        }

        private static int whiten(int colour, double w) {
            int r = colour >> 16 & 0xff, g = colour >> 8 & 0xff, b = colour & 0xff;
            r += (int) ((0xff - r) * w);
            g += (int) ((0xff - g) * w);
            b += (int) ((0xff - b) * w);
            return r << 16 | g << 8 | b;
        }
    }
}
