package dev.horizon.snugfire;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.BaseFireBlock;
import net.minecraft.world.level.block.FireBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.fml.common.Mod;

/**
 * Horizon Snug Fire - an independent equivalent of the idea behind Tight Fire (not a port; no Tight Fire code or
 * assets). Floor fire standing on a block lower than a full block (slab, carpet, snow layer, daylight sensor...) is
 * drawn on that block's real top surface instead of floating, and its outline reaches down to match. Client-side.
 */
@Mod(value = "horizon_snugfire", dist = Dist.CLIENT)
public final class SnugFire {
    private static final double MIN_DROP = 1.0 / 64.0;

    public SnugFire() {}

    public static boolean isFire(BlockState state) {
        return state.getBlock() instanceof BaseFireBlock;
    }

    /** Vertical drop (&lt;= 0) for floor fire whose supporting block is lower than a full block. */
    public static double drop(BlockState fire, BlockGetter level, BlockPos pos) {
        if (level == null || pos == null) return 0;
        if (fire.getBlock() instanceof FireBlock && (fire.getValue(FireBlock.NORTH) || fire.getValue(FireBlock.EAST)
                || fire.getValue(FireBlock.SOUTH) || fire.getValue(FireBlock.WEST) || fire.getValue(FireBlock.UP))) {
            return 0;   // wall / ceiling fire hangs on its neighbours: unchanged
        }
        BlockPos below = pos.below();
        BlockState support = level.getBlockState(below);
        if (support.isAir() || isFire(support)) return 0;
        VoxelShape shape = support.getShape(level, below);
        if (shape.isEmpty()) return 0;
        double top = shape.max(Direction.Axis.Y);
        if (top <= 0 || top >= 1.0 - MIN_DROP) return 0;
        return top - 1.0;
    }

    public static Vec3 offset(BlockState fire, BlockGetter level, BlockPos pos) {
        double d = drop(fire, level, pos);
        return d == 0 ? Vec3.ZERO : new Vec3(0, d, 0);
    }

    /** The fire outline stretched from the support's top surface up to its normal top. */
    public static VoxelShape shape(VoxelShape original, double drop) {
        if (drop == 0 || original.isEmpty()) return original;
        double top = Math.max(original.max(Direction.Axis.Y), 1.0 / 16.0);
        return Shapes.or(original, Shapes.box(0, drop, 0, 1, top, 1));
    }
}
