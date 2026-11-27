package dev.horizon.enchtips;

import com.mojang.blaze3d.platform.InputConstants;
import it.unimi.dsi.fastutil.objects.Object2IntMap;
import java.util.ArrayList;
import java.util.List;
import java.util.TreeSet;
import net.minecraft.ChatFormatting;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.resources.language.I18n;
import net.minecraft.core.Holder;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.ItemEnchantments;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import net.neoforged.neoforge.client.settings.KeyConflictContext;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;
import org.lwjgl.glfw.GLFW;

/**
 * Horizon Enchantment Tooltips. Collapsed tooltip: one blank line and "Shift for more info" (yellow) after the enchantment
 * lines (and after a "Placeable" line when present). While the key is held (rebindable, Left Shift by default), each
 * enchantment line is followed by its description (gray, from the lang key enchantment.<ns>.<id>.desc) and the exact
 * enchantments it cannot be combined with (red, read live from the enchantment's exclusive set), then a blank line.
 */
@Mod(value = HorizonEnchTips.ID, dist = Dist.CLIENT)
public final class HorizonEnchTips {
    public static final String ID = "horizon_enchtips";
    static final KeyMapping SHOW = new KeyMapping("key.horizon_enchtips.show", KeyConflictContext.GUI,
            InputConstants.Type.KEYSYM, GLFW.GLFW_KEY_LEFT_SHIFT, "key.categories.inventory");
    private static final int WRAP = 44;

    public HorizonEnchTips(IEventBus modBus) {
        modBus.addListener(RegisterKeyMappingsEvent.class, e -> e.register(SHOW));
        NeoForge.EVENT_BUS.addListener(EventPriority.LOWEST, ItemTooltipEvent.class, HorizonEnchTips::onTooltip);
    }

    /** Key state read from GLFW: key mappings are not updated while a screen is open. */
    static boolean held() {
        InputConstants.Key k = SHOW.getKey();
        if (k.equals(InputConstants.UNKNOWN)) return false;
        long w = Minecraft.getInstance().getWindow().getWindow();
        if (k.getType() == InputConstants.Type.MOUSE) return GLFW.glfwGetMouseButton(w, k.getValue()) == GLFW.GLFW_PRESS;
        return InputConstants.isKeyDown(w, k.getValue());
    }

    /** "Left Shift" -> "Shift", "Right Control" -> "Control"; other key names unchanged. */
    static String keyName() {
        return SHOW.getTranslatedKeyMessage().getString().replaceFirst("^(Left|Right) ", "");
    }

    static void onTooltip(ItemTooltipEvent e) {
        ItemStack stack = e.getItemStack();
        List<Object2IntMap.Entry<Holder<Enchantment>>> all = new ArrayList<>();
        all.addAll(stack.getOrDefault(DataComponents.ENCHANTMENTS, ItemEnchantments.EMPTY).entrySet());
        all.addAll(stack.getOrDefault(DataComponents.STORED_ENCHANTMENTS, ItemEnchantments.EMPTY).entrySet());
        if (all.isEmpty()) return;
        List<Component> lines = e.getToolTip();
        // Another mod prints the raw .desc line on enchanted books (always on, unstyled): drop it, this mod owns descriptions.
        java.util.Set<String> descs = new java.util.HashSet<>();
        for (Object2IntMap.Entry<Holder<Enchantment>> en : all) {
            en.getKey().unwrapKey().ifPresent(k -> {
                String dk = "enchantment." + k.location().getNamespace() + "." + k.location().getPath() + ".desc";
                if (I18n.exists(dk)) descs.add(I18n.get(dk));
            });
        }
        lines.removeIf(c -> descs.contains(c.getString()));
        boolean expand = held();
        int last = -1;
        for (Object2IntMap.Entry<Holder<Enchantment>> en : all) {
            Holder<Enchantment> h = en.getKey();
            String name = Enchantment.getFullname(h, en.getIntValue()).getString();
            int idx = -1;
            for (int i = Math.max(0, last + 1); i < lines.size(); i++) {
                if (lines.get(i).getString().equals(name)) { idx = i; break; }
            }
            if (idx < 0) continue;
            int at = idx + 1;
            while (at < lines.size() && isIconRow(lines.get(at).getString())) at++;   // e.g. Apothic slot icons
            if (!expand) { last = at - 1; continue; }
            List<Component> add = new ArrayList<>();
            ResourceLocation id = h.unwrapKey().map(k -> k.location()).orElse(null);
            String key = id == null ? null : "enchantment." + id.getNamespace() + "." + id.getPath() + ".desc";
            if (key != null && I18n.exists(key)) {
                for (String l : wrap(I18n.get(key))) add.add(Component.literal(l).withStyle(ChatFormatting.GRAY));
            }
            TreeSet<String> ex = new TreeSet<>();
            h.value().exclusiveSet().forEach(o -> { if (!o.equals(h) && !o.value().equals(h.value())) ex.add(o.value().description().getString()); });
            if (!ex.isEmpty()) {
                for (String l : wrap(String.join(", ", ex))) add.add(Component.literal(l).withStyle(ChatFormatting.RED));
            }
            add.add(Component.empty());
            lines.addAll(at, add);
            last = at + add.size() - 1;
        }
        if (!expand && last >= 0) {
            int at = last + 1;   // directly under the enchantments; a following "Placeable" line moves below a blank line
            lines.add(at, Component.translatable("tooltip.horizon_enchtips.more", keyName()).withStyle(ChatFormatting.YELLOW));
            if (at + 1 < lines.size() && lines.get(at + 1).getString().trim().equalsIgnoreCase("Placeable")) lines.add(at + 1, Component.empty());
        }
    }

    /** A line with no letters or digits (icon glyph rows drawn under an enchantment by other mods). */
    static boolean isIconRow(String s) {
        if (s.isBlank()) return false;
        for (int i = 0; i < s.length(); i++) if (Character.isLetterOrDigit(s.charAt(i))) return false;
        return true;
    }

    static List<String> wrap(String text) {
        List<String> out = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        for (String w : text.split(" ")) {
            if (cur.length() > 0 && cur.length() + 1 + w.length() > WRAP) { out.add(cur.toString()); cur.setLength(0); }
            if (cur.length() > 0) cur.append(' ');
            cur.append(w);
        }
        if (cur.length() > 0) out.add(cur.toString());
        return out;
    }
}
