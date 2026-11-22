// SPDX-License-Identifier: MPL-2.0
// Original: theRookieCoder/SnowyLeavesPlus (Fabric, Yarn StringIdentifiable). Port: Mojang StringRepresentable.
package io.github.therookiecoder.snowyleavesplus;

import net.minecraft.util.StringRepresentable;
import net.minecraft.world.level.block.state.properties.EnumProperty;

public enum Snowiness implements StringRepresentable {
    none, low, medium, high, full;

    public static final EnumProperty<Snowiness> SNOWINESS = EnumProperty.create("snowiness", Snowiness.class);

    @Override
    public String getSerializedName() {
        return this.name();
    }

    public Snowiness increaseSnowiness() {
        return this.ordinal() + 1 < values().length ? values()[this.ordinal() + 1] : this;
    }

    public Snowiness decreaseSnowiness() {
        return this.ordinal() > 0 ? values()[this.ordinal() - 1] : this;
    }
}
