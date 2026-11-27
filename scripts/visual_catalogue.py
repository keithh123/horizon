"""Write manifests/visual_catalogue.json: the 0.6.1 disposition of every entry in the 73-project visual research catalogue.

Source of the entry list: the research canvas exported to tests/evidence/visual_catalogue_source.json (title/slug/url/category/
priority). Dispositions: default (shipped and enabled), optional (shipped or allowed, not enabled by Horizon), superseded
(a named choice replaces it), rejected (reason given), blocked (no compatible 1.21.1 path). Deterministic output.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = {
    'fresh-animations': ('default', 'Kept 1.11.2 (base).'),
    'fresh-animations-details': ('default', 'Kept 2.4.'),
    'fresh-animations-emissive': ('default', 'Kept 1.7.'),
    'fresh-animations-quivers': ('default', 'Kept 2.3.'),
    'fresh-animations-objects': ('default', '2.1.2 as the individual Objects extension; above 3D Default so EMF chest/boat models win. Lootr/Sophisticated/Create chests keep their own renderers.'),
    'fa-player-extension': ('default', "1.1.0: player-movement owner. Punchy Moves removed (its ConflictingAnimationsState flags any FA Player pack); Entity Player Compat blends Better Combat and Iron's casting per body part."),
    'fresh-variants-and-ventures': ('default', '1.0: matches the installed Variants & Ventures mod.'),
    'fresh-compats': ('default', 'v1.6 now enabled (Quark variants, Supplementaries entities only).'),
    'fresh-animations-extensions': ('superseded', 'All Extensions duplicates Details/Emissive/Quivers/Objects; individual extensions chosen. The updater drops it from the enabled list (file kept).'),
    'fresh-animations-spiders': ('optional', 'Not a Horizon default: Spider Overhaul adds 14 spider types with their own models; FA Spiders only re-animates vanilla spiders. Kept enabled where the player enabled it.'),
    'fresh-animations-creepers': ('rejected', 'Creeper Overhaul supplies biome creepers with their own models; FA Creepers would add a third creeper style.'),
    'fresh-animations-classic-horses': ('rejected', 'Art preference only; base FA horses kept for consistency.'),
    'just-expressions': ('optional', "Not default: animated eyes need the skin's eye pixels in the pack's layout; most skins do not match."),
    'fa-player-extension-plusjust-expressions': ('optional', 'Bridge for Just Expressions + FA Player; same skin-layout condition.'),
    'tras-fresh-player': ('superseded', 'Alternative primary player animation set; FA Player Extension chosen.'),
    'freshmoves': ('superseded', 'Alternative primary player animation set; FA Player Extension chosen.'),
    'freshly-modded': ('rejected', 'Covers none of the installed mods (checked against lock.json).'),
    'semos-animations-lib': ('rejected', 'Only needed by Freshly Modded.'),
    'fresh-food': ('optional', 'Format 46+ items/ definitions. Modefite (native NeoForge 1.21.1 item-definition backport) now ships, so a player-enabled copy can work; not a Horizon default (the Eating Animation port owns eating frames).'),
    'fresh-xp-orbs': ('rejected', 'Format 55+, no 1.21.1 file for this project; not shipped. A player-enabled copy is left as the player\'s choice.'),
    'just-3d-potions': ('default', '1.2 (explicit 1.21.1 release), Punchy bottle animation.'),
    'als-3d-potions': ('superseded', 'One potion-model pack: Just 3D Potions.'),
    'animated-items': ('rejected', 'Overrides many vanilla item sprites also changed by Fancy Crops/3D Default/Cataclysm icons; low value next to Horizon icons.'),
    'fresh-flowers-and-plants': ('blocked', '1.5 needs format 46+ item definitions plus Polytone and Interactive Stuff (Fabric) through Connector; no native 1.21.1 path verified.'),
    'simply-swords-reforged': ('rejected', 'v0.1 work in progress (format 16) built for older Simply Swords models; not matched to Simply Swords 1.70.2.'),
    'consistently-2d': ('rejected', "1.0.0 also replaces Create/FD/Iron's held models with flat ones; Horizon keeps detailed held/world models and native icons."),
    'cataclysm-reimagined': ('rejected', 'v1.3.5 NeoForge: its inventory models reference cataclysm:item/*_gui textures absent from both the pack and Cataclysm 3.33 (22 missing-texture models in a client log, 0 without it). Native icons kept.'),
    'xalis-enchanted-books': ('blocked', 'Needs OptiFine-style CIT; no CIT implementation exists in this NeoForge 1.21.1 stack (EMF/ETF are entity-only).'),
    'xalis-enchanted-books-create-addon': ('blocked', 'Same CIT requirement.'),
    'visual-enchantments': ('blocked', 'Same CIT requirement.'),
    'better-leaves': ('default', '9.6 now shipped by Horizon (Dynamic Trees, Regions Unexplored, Quark, Ars Nouveau leaves).'),
    'fancy-crops': ('default', '1.3 (formats 15-1024); primary crop treatment, Farmer\'s Delight aware.'),
    '3d-crops': ('superseded', 'One crop treatment: Fancy Crops.'),
    'fresh-flower-pots': ('default', '1.5.4.'),
    'fresh-flower-pots-compats': ('default', '8.0: Regions Unexplored, Deeper and Darker, Supplementaries, Creeper Overhaul pots.'),
    '3d-default': ('default', '1.16.0 (1_21 overlay); lowest-priority model pack.'),
    '3d-default-compat': ('rejected', 'Among installed mods it only covers Deeper and Darker tools.'),
    'remodeled-doors': ('default', '2.0, above 3D Default.'),
    'rails-3d': ('default', '1.0, vanilla rails only (Create tracks unaffected).'),
    'better-lanterns': ('rejected', 'Swinging Lanterns renders lanterns itself (static-lantern suppression hooks); the model pack would be ignored or doubled.'),
    'mandalas-gui-dark-mode': ('default', '1.21.5 build: its description covers 1.20.5-1.21.5 but pack_format is 55, so Minecraft labels it newer; v2.1 is a 1.21.6 layout. Metadata not edited.'),
    'unofficial-mandalas-gui-dark-mode-mod-compatibility': ('default', '0.3: Accessories, Apothic Attributes, Curios, EMI, Aether, Farmer\'s Delight, Sophisticated Core.'),
    'mandalas-gui-compats-fixes': ('default', '1.3.5: wider mod coverage, above the unofficial pack.'),
    'colourful-containers-dark-mode-gui': ('superseded', 'Competing base GUI theme; Mandala chosen.'),
    'colourful-containers-modded-dark-mode-gui-compat': ('superseded', 'Companion of a theme not chosen.'),
    'colourful-containers-gui': ('superseded', 'Competing base GUI theme.'),
    'unique-dark': ('superseded', 'Competing theme; full features need OptiGUI (not available).'),
    'fancys-gui-overhaul': ('superseded', 'Competing base GUI theme.'),
    'gui-revision': ('superseded', 'Competing base GUI theme.'),
    'updated-gui': ('superseded', 'Competing theme; overlaps Animated Hearts.'),
    'dark-smooth-gui': ('superseded', 'Competing base GUI theme.'),
    'icons': ('rejected', 'Replaces glyphs in the default font that Horizon/Heracles and mod screens print; readability risk for no gameplay gain.'),
    'enhanced-boss-bars': ('rejected', 'Author documents conflicts with Cataclysm/Aether/Mowzie bars and needs a companion mod; native bars kept.'),
    'applied-energistics-style-mekanism': ('rejected', 'Light AE2-style Mekanism art against the chosen dark theme.'),
    'reimagined': ('rejected', 'Needs Polytone, Continuity, Respackopts and pre-1.21.4 item support; reskins vanilla while modded content stays default.'),
    'reimagined-fresh-animations-patch': ('rejected', 'Only with Reimagined.'),
    'excal': ('rejected', 'Medieval 16x vanilla reskin; installed tech/magic mods stay default (mismatch).'),
    'excalibur-fresh-animations': ('rejected', 'Only with Excalibur.'),
    'excalibur-lootr-support': ('rejected', 'Only with Excalibur.'),
    'alacrity': ('rejected', '32x: clashes with 16x modded content.'),
    'patrix-32x': ('rejected', '32x labPBR showcase; same mismatch.'),
    'faithful-32x': ('rejected', '32x needs matching add-ons for every mod.'),
    'nature-x': ('rejected', 'Needs Polytone and API mods; Dynamic Trees/RU coverage unverified.'),
    'bettervanillabuilding': ('rejected', 'Relies on OptiFine-style features without verified NeoForge replacements.'),
    'vanilla-ultra-pbr': ('rejected', 'labPBR materials change every shader profile; not measured in 0.6.1.'),
    'avpbr-retextured': ('superseded', 'One PBR set per profile; none shipped in 0.6.1.'),
    'dramatic-skys': ('rejected', 'Shader skies replace it; shaderless sky stays vanilla.'),
    'create-energistics': ('blocked', 'No 1.21.1 file.'),
    'animated-armor-trims': ('blocked', 'No 1.21.1 file.'),
    'creeper-overhaul-x-fresh-animations': ('blocked', 'No 1.21.1 file; targets a resource pack, not the mod.'),
    'fresh-mowzies-mobs-textures': ('blocked', "No 1.21.1 file; Mowzie's animates natively."),
    'better-dogs': ('blocked', 'No 1.21.1 file.'),
    'better-cats-x-fresh-animations': ('rejected', 'Needs the separate Better Cats base pack; cats stay Fresh Animations.'),
}


def main():
    src = json.loads((ROOT / "tests/evidence/visual_catalogue_source.json").read_text(encoding="utf-8"))
    slugs = [p["slug"] for p in src]
    missing = set(slugs) ^ set(D)
    if missing:
        raise SystemExit(f"catalogue/disposition mismatch: {sorted(missing)}")
    out = [dict(slug=p["slug"], title=p["title"], url=p["url"], category=p["category"], research_priority=p["priority"],
                disposition=D[p["slug"]][0], reason=D[p["slug"]][1]) for p in src]
    (ROOT / "manifests/visual_catalogue.json").write_text(json.dumps(
        {"_comment": "Generated by scripts/visual_catalogue.py. 0.6.1 disposition of the visual research catalogue.", "entries": out},
        indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = {}
    for v in D.values():
        counts[v[0]] = counts.get(v[0], 0) + 1
    print(f"visual_catalogue: {len(out)} entries {counts}")


if __name__ == "__main__":
    main()
