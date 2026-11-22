package dev.horizon.questbook;

import earth.terrarium.heracles.api.quests.Quest;
import earth.terrarium.heracles.api.rewards.QuestReward;
import earth.terrarium.heracles.api.rewards.defaults.ItemReward;
import earth.terrarium.heracles.api.rewards.defaults.LootTableReward;
import earth.terrarium.heracles.api.rewards.defaults.XpQuestReward;
import earth.terrarium.heracles.api.tasks.QuestTask;
import earth.terrarium.heracles.api.tasks.defaults.CheckTask;
import earth.terrarium.heracles.common.network.packets.tasks.CheckTaskPacket;
import earth.terrarium.heracles.api.tasks.client.display.TaskTitleFormatter;
import earth.terrarium.heracles.client.handlers.ClientQuests;
import earth.terrarium.heracles.client.ui.quests.AbstractQuestsScreen;
import earth.terrarium.heracles.common.handlers.progress.QuestProgress;
import earth.terrarium.heracles.common.menus.quest.QuestContent;
import earth.terrarium.heracles.common.network.NetworkHandler;
import earth.terrarium.heracles.common.network.packets.rewards.ClaimRewardsPacket;
import earth.terrarium.heracles.common.utils.ModUtils.QuestStatus;
import net.minecraft.ChatFormatting;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.world.item.ItemStack;

import java.util.ArrayList;
import java.util.List;

/**
 * FTB-Quests-style popup for one quest: description, requirements with per-task state, unmet prerequisites,
 * rewards and a claim button. Closes with the X button or Esc and returns to the chapter view underneath.
 * All data is read live from Heracles' client caches, so a claim shows up as soon as the server confirms it.
 */
public final class QuestPopupScreen extends Screen {
    private static final int W = 340, PAD = 10, LINE = 11;
    private static final int C_BORDER = 0xFF6B4E1F, C_PANEL = 0xFF1B1713, C_HEAD = 0xFF2C2218, C_GOLD = 0xFFE8C872,
            C_TEXT = 0xFFD8D2C4, C_DIM = 0xFF8C8577, C_GOOD = 0xFF7FD36B, C_BAD = 0xFFE0705A;

    private final Screen parent;
    private final QuestContent content;
    private Button close, claim;
    private int left, top, ph, bodyTop, bodyBottom;
    private double scroll;
    private int contentHeight;
    private final List<Object[]> checkHits = new ArrayList<>();   // {x0, y0, x1, y1, taskId}

    public QuestPopupScreen(Screen parent, QuestContent content) {
        super(Component.empty());
        this.parent = parent;
        this.content = content;
    }

    public Screen parent() { return parent; }

    private Quest quest() { return ClientQuests.getQuest(content.id()).orElse(null); }

    /** The furthest state among the open-time snapshot, Heracles' lazily updated cache and the live progress object. */
    private QuestStatus status() {
        QuestStatus best = QuestStatus.LOCKED;
        QuestStatus snap = content.quests().get(content.id());
        QuestStatus cached = ClientQuests.getStatus(content.id()).orElse(null);
        for (QuestStatus s : new QuestStatus[]{snap, cached}) if (s != null && s.ordinal() > best.ordinal()) best = s;
        Quest q = quest();
        QuestProgress p = ClientQuests.getProgress(content.id());
        if (q != null && p != null && p.isComplete()) {
            QuestStatus d = p.isClaimed(q) ? QuestStatus.COMPLETED_CLAIMED : QuestStatus.COMPLETED;
            if (d.ordinal() > best.ordinal()) best = d;
        }
        return best;
    }

    @Override
    protected void init() {
        ph = Math.min(280, this.height - 24);
        left = (this.width - W) / 2;
        top = (this.height - ph) / 2;
        bodyTop = top + 30;
        bodyBottom = top + ph - 34;
        close = addRenderableWidget(Button.builder(Component.literal("X"), b -> onClose())
                .bounds(left + W - 22, top + 5, 18, 18)
                .tooltip(Tooltip.create(Component.translatable("gui.horizon_questbook.close"))).build());
        claim = addRenderableWidget(Button.builder(Component.translatable("gui.horizon_questbook.claim"), b -> {
                    NetworkHandler.CHANNEL.sendToServer(new ClaimRewardsPacket(content.id()));
                    // Horizon reward cue (kubejs/assets/horizon/sounds.json; re-skinnable by the Horizon-16x pack)
                    this.minecraft.getSoundManager().play(SimpleSoundInstance.forUI(
                            SoundEvent.createVariableRangeEvent(ResourceLocation.parse("horizon:cue.quest_claim")), 1.0F, 1.0F));
                })
                .bounds(left + PAD, top + ph - 28, W - 2 * PAD, 20).build());
    }

    @Override
    public void onClose() {
        if (parent instanceof AbstractQuestsScreen q) q.updateProgress();
        this.minecraft.setScreen(parent);
    }

    @Override
    public boolean isPauseScreen() { return false; }

    @Override
    public void renderBackground(GuiGraphics g, int mx, int my, float pt) {
        // intentionally empty: Screen.render() calls this *after* our panel is drawn, so the dimmed chapter view
        // is drawn once at the start of render() instead (otherwise it covers the popup)
    }

    @Override
    public void render(GuiGraphics g, int mx, int my, float pt) {
        if (parent != null) parent.render(g, -1, -1, pt);   // the chapter view stays visible, dimmed, behind the popup
        g.fill(0, 0, this.width, this.height, 0xB0000000);
        g.pose().pushPose();
        g.pose().translate(0, 0, 400);   // above the chapter view's item icons
        try { renderPanel(g, mx, my, pt); } finally { g.pose().popPose(); }
    }

    private void renderPanel(GuiGraphics g, int mx, int my, float pt) {
        Quest quest = quest();
        if (quest == null) { onClose(); return; }
        checkHits.clear();
        QuestStatus st = status();
        QuestProgress progress = ClientQuests.getProgress(content.id());

        g.fill(left - 2, top - 2, left + W + 2, top + ph + 2, C_BORDER);
        g.fill(left, top, left + W, top + ph, C_PANEL);
        g.fill(left, top, left + W, top + 28, C_HEAD);
        quest.display().icon().render(g, left + PAD, top + 6, 16, 16);
        g.drawString(font, quest.display().title(), left + PAD + 22, top + 5, C_GOLD, false);
        g.drawString(font, statusLabel(st), left + PAD + 22, top + 16, st == QuestStatus.LOCKED ? C_BAD : C_DIM, false);

        // scrollable body
        g.enableScissor(left, bodyTop, left + W, bodyBottom);
        int y = bodyTop + 4 - (int) scroll;
        y = section(g, "gui.horizon_questbook.description", y);
        for (String raw : quest.display().description()) {
            for (FormattedCharSequence line : font.split(Component.literal(raw.replace('&', '§')), W - 2 * PAD)) {
                g.drawString(font, line, left + PAD, y, C_TEXT, false);
                y += LINE;
            }
            if (raw.isEmpty()) y += 4;
        }
        y = section(g, "gui.horizon_questbook.requirements", y + 6);
        for (QuestTask<?, ?, ?> task : quest.tasks().values()) {
            boolean done = isDone(progress, task);
            Component title;
            try { title = TaskTitleFormatter.create(task); } catch (RuntimeException e) { title = Component.literal(task.id()); }
            g.drawString(font, (done ? "✔ " : "○ ") + "", left + PAD, y, done ? C_GOOD : C_DIM, false);
            if (task instanceof CheckTask && !done && st != QuestStatus.LOCKED) {
                // Heracles' own quest screens show a Check button for manual tasks; the popup must too
                int bx = left + W - PAD - 52, by = y - 2;
                boolean hot = mx >= bx && mx < bx + 48 && my >= by && my < by + 12 && my >= bodyTop && my < bodyBottom;
                g.fill(bx, by, bx + 48, by + 12, hot ? 0xFF6B4E1F : 0xFF3B2A14);
                g.drawCenteredString(font, "Check", bx + 24, by + 2, C_GOLD);
                checkHits.add(new Object[]{bx, by, bx + 48, by + 12, task.id()});
            }
            for (FormattedCharSequence line : font.split(title, W - 2 * PAD - 14)) {
                g.drawString(font, line, left + PAD + 12, y, done ? C_GOOD : C_TEXT, false);
                y += LINE;
            }
        }
        y = section(g, "gui.horizon_questbook.prerequisites", y + 6);
        List<Component> unmet = new ArrayList<>();
        for (String dep : quest.dependencies()) {
            QuestStatus ds = ClientQuests.getStatus(dep).orElse(QuestStatus.LOCKED);
            if (!ds.isComplete()) {
                unmet.add(ClientQuests.getQuest(dep).map(q -> q.display().title()).orElse(Component.literal(dep)));
            }
        }
        if (unmet.isEmpty()) {
            g.drawString(font, Component.translatable("gui.horizon_questbook.prereq_met"), left + PAD, y, C_GOOD, false);
            y += LINE;
        } else {
            g.drawString(font, Component.translatable("gui.horizon_questbook.prereq_missing"), left + PAD, y, C_BAD, false);
            y += LINE;
            for (Component c : unmet) {
                g.drawString(font, Component.literal("• ").append(c), left + PAD + 6, y, C_BAD, false);
                y += LINE;
            }
        }
        y = section(g, "gui.horizon_questbook.rewards", y + 6);
        boolean claimed = progress != null && progress.isClaimed(quest);
        for (QuestReward<?> r : quest.rewards().values()) {
            y = reward(g, r, y, claimed);
        }
        contentHeight = y + (int) scroll - bodyTop;
        g.disableScissor();

        int maxScroll = Math.max(0, contentHeight - (bodyBottom - bodyTop) + 8);
        scroll = Math.max(0, Math.min(scroll, maxScroll));
        if (maxScroll > 0) {   // scrollbar
            int bh = bodyBottom - bodyTop, th = Math.max(16, bh * bh / (contentHeight + 8));
            int ty = bodyTop + (int) ((bh - th) * (scroll / maxScroll));
            g.fill(left + W - 4, bodyTop, left + W - 2, bodyBottom, 0x40FFFFFF);
            g.fill(left + W - 4, ty, left + W - 2, ty + th, C_GOLD);
        }

        claim.active = st == QuestStatus.COMPLETED;
        claim.setMessage(Component.translatable(st == QuestStatus.COMPLETED_CLAIMED ? "gui.horizon_questbook.claimed"
                : "gui.horizon_questbook.claim"));
        super.render(g, mx, my, pt);
    }

    private int section(GuiGraphics g, String key, int y) {
        g.drawString(font, Component.translatable(key).withStyle(ChatFormatting.BOLD), left + PAD, y, C_GOLD, false);
        g.fill(left + PAD, y + 10, left + W - PAD, y + 11, 0x55E8C872);
        return y + 15;
    }

    private int reward(GuiGraphics g, QuestReward<?> r, int y, boolean claimed) {
        int color = claimed ? C_DIM : C_TEXT;
        if (r instanceof ItemReward ir) {
            ItemStack s = ir.stack();
            g.renderItem(s, left + PAD, y - 3);
            g.renderItemDecorations(font, s, left + PAD, y - 3);
            g.drawString(font, s.getHoverName(), left + PAD + 22, y + 1, color, false);
            return y + 18;
        }
        String text;
        if (r instanceof XpQuestReward xr) text = xr.amount() + (xr.xpType().name().startsWith("L") ? " experience levels" : " experience points");
        else if (r instanceof LootTableReward lr) text = "Loot: " + lr.lootTable();
        else text = r.id();
        g.drawString(font, text, left + PAD + 4, y, color, false);
        return y + LINE + 2;
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static boolean isDone(QuestProgress progress, QuestTask task) {
        try { return progress != null && progress.getTask(task).isComplete(); } catch (RuntimeException e) { return false; }
    }

    private Component statusLabel(QuestStatus s) {
        return Component.translatable(switch (s) {
            case LOCKED -> "gui.horizon_questbook.locked";
            case IN_PROGRESS -> "gui.horizon_questbook.in_progress";
            case COMPLETED -> "gui.horizon_questbook.complete";
            case COMPLETED_CLAIMED -> "gui.horizon_questbook.done";
        });
    }

    @Override
    public boolean mouseClicked(double mx, double my, int button) {
        if (button == 0 && my >= bodyTop && my < bodyBottom) {
            for (Object[] h : checkHits) {
                if (mx >= (int) h[0] && mx < (int) h[2] && my >= (int) h[1] && my < (int) h[3]) {
                    NetworkHandler.CHANNEL.sendToServer(new CheckTaskPacket(content.id(), (String) h[4]));
                    return true;
                }
            }
        }
        return super.mouseClicked(mx, my, button);
    }

    @Override
    public boolean mouseScrolled(double mx, double my, double dx, double dy) {
        scroll -= dy * 14;
        return true;
    }
}
