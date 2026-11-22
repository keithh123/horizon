package dev.horizon.questbook.mixin;

import org.joml.Vector2i;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Heracles' OffsetBounds.center sets the pan offset to (max - min) / 2, which pushes a chapter's tree toward the
 * bottom-right of the view (seen in game: the first quest sat at the right edge). The view origin is the view centre, so
 * centring on the tree needs offset = -(min + max) / 2.
 */
@Mixin(targets = "earth.terrarium.heracles.client.components.quests.OffsetBounds", remap = false)
public abstract class OffsetBoundsMixin {
    @Shadow private Vector2i offset;

    @Inject(method = "center", at = @At("HEAD"), cancellable = true)
    private void horizon$center(int minX, int minY, int maxX, int maxY, CallbackInfo ci) {
        offset.x = -(minX + maxX) / 2;
        offset.y = -(minY + maxY) / 2;
        ci.cancel();
    }
}
