package dev.horizon.modelangles.mixin;

import com.google.gson.JsonObject;
import net.minecraft.util.GsonHelper;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * 1.21.1 rejects element rotations other than -45/-22.5/0/22.5/45 ("Invalid rotation ... found"), although
 * FaceBakery's rotation math handles any angle. Newer versions accept any angle; this accepts the same range
 * (-180..180) so models written for them load unchanged. Models that were valid before are unaffected.
 */
@Mixin(targets = "net.minecraft.client.renderer.block.model.BlockElement$Deserializer")
public abstract class BlockElementDeserializerMixin {
    @Inject(method = "getAngle", at = @At("HEAD"), cancellable = true)
    private void modelangles$anyAngle(JsonObject json, CallbackInfoReturnable<Float> cir) {
        float angle = GsonHelper.getAsFloat(json, "angle");
        if (angle >= -180.0F && angle <= 180.0F) cir.setReturnValue(angle);
    }
}
