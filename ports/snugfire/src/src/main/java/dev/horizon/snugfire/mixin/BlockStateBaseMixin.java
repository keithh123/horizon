package dev.horizon.snugfire.mixin;

import dev.horizon.snugfire.SnugFire;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Uses the block render-offset hook, which both the vanilla and the Sodium block renderers apply. */
@Mixin(BlockBehaviour.BlockStateBase.class)
public abstract class BlockStateBaseMixin {
    private BlockState snugfire$self() {
        return (BlockState) (Object) this;
    }

    @Inject(method = "hasOffsetFunction", at = @At("HEAD"), cancellable = true)
    private void snugfire$hasOffset(CallbackInfoReturnable<Boolean> cir) {
        if (SnugFire.isFire(snugfire$self())) cir.setReturnValue(true);
    }

    @Inject(method = "getOffset", at = @At("HEAD"), cancellable = true)
    private void snugfire$offset(BlockGetter level, BlockPos pos, CallbackInfoReturnable<Vec3> cir) {
        if (SnugFire.isFire(snugfire$self())) cir.setReturnValue(SnugFire.offset(snugfire$self(), level, pos));
    }

    @Inject(method = "getShape(Lnet/minecraft/world/level/BlockGetter;Lnet/minecraft/core/BlockPos;Lnet/minecraft/world/phys/shapes/CollisionContext;)Lnet/minecraft/world/phys/shapes/VoxelShape;",
            at = @At("RETURN"), cancellable = true)
    private void snugfire$shape(BlockGetter level, BlockPos pos, CollisionContext ctx, CallbackInfoReturnable<VoxelShape> cir) {
        if (SnugFire.isFire(snugfire$self())) {
            cir.setReturnValue(SnugFire.shape(cir.getReturnValue(), SnugFire.drop(snugfire$self(), level, pos)));
        }
    }
}
