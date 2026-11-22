package dev.horizon.questbook;

import earth.terrarium.heracles.client.HeraclesClient;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ScreenEvent;

/** Client-only glue: opens Heracles' quest screen exactly as its keybind does, and adds the inventory button. */
@EventBusSubscriber(modid = HorizonQuestBook.ID, value = Dist.CLIENT)
public final class ClientBridge {
    private ClientBridge() {}

    public static void openQuests() {
        HeraclesClient.openQuestScreen();   // same call the J keybind makes
    }

    @SubscribeEvent
    public static void onInit(ScreenEvent.Init.Post e) {
        if (e.getScreen() instanceof InventoryScreen inv) {
            e.addListener(new BookButton(inv));
        }
    }

    /** 20x20 button under the bottom-left corner of the inventory panel; follows the panel when the recipe book shifts it. */
    private static final class BookButton extends Button {
        private final InventoryScreen screen;
        private final ItemStack icon = new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.parse("heracles:quest_book")));

        BookButton(InventoryScreen screen) {
            super(screen.getGuiLeft(), screen.getGuiTop() + screen.getYSize() + 2, 20, 20, Component.empty(),
                    b -> openQuests(), DEFAULT_NARRATION);
            this.screen = screen;
            setTooltip(Tooltip.create(Component.translatable("gui.horizon_questbook.button")));
        }

        @Override
        protected void renderWidget(GuiGraphics g, int mx, int my, float pt) {
            setX(screen.getGuiLeft());
            setY(screen.getGuiTop() + screen.getYSize() + 2);
            super.renderWidget(g, mx, my, pt);
            g.renderItem(icon, getX() + 2, getY() + 2);
        }
    }
}
