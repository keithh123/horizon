"""First-person body / held-item screenshots (client QA harness). Test instances only.

usage: python tests/client_qa/fp_matrix.py <instance> <tag>
For each item: hold it, look slightly down in first person (body + hands visible), screenshot; for melee weapons also a
mid-swing frame (attack key) and for use-items a mid-use frame (use key). Then one third-person shot. Uses the sky
platform at (-838, 150, 266) built by the charter test.
"""
import subprocess, sys
# Grand Teleport plays a ~80-tick satellite camera transition on every vanilla /tp (enableVanillaTp=true): every tp is
# followed by wait:150 + persp:0, otherwise a frame of the transition is captured instead of the first-person view.

inst, tag = sys.argv[1], sys.argv[2]
ITEMS = [("empty", "minecraft:air", None), ("pickaxe", "minecraft:diamond_pickaxe", "attack"),
         ("sword", "minecraft:diamond_sword", "attack"), ("claymore", "simplyswords:iron_claymore", "attack"),
         ("shield", "minecraft:shield", "use"), ("bow", "minecraft:bow", "use"), ("crossbow", "minecraft:crossbow", None),
         ("trident", "minecraft:trident", "use"), ("map", "minecraft:map", None), ("torch", "minecraft:torch", None),
         ("lantern", "minecraft:lantern", None), ("bread", "minecraft:bread", "use"), ("potion", "minecraft:potion", "use"),
         ("spellbook", "irons_spellbooks:copper_spell_book", None)]
A = ["cmd:/gamemode survival", "cmd:/effect give @s minecraft:hunger 2 255 true", "hud:on", "persp:0",
     "cmd:/tp @s -837.5 150 266.5 0 35", "cmd:/give @s minecraft:arrow 16", "wait:150", "persp:0", "wait:5"]
for name, item, act in ITEMS:
    A += [f"cmd:/item replace entity @s weapon.mainhand with {item}", "wait:15", f"shot:{tag}_{name}"]
    if act == "attack":
        A += ["attack", "wait:3", f"shot:{tag}_{name}_swing", "wait:20"]
    elif act == "use":
        A += ["hold:Use=on", "wait:12", f"shot:{tag}_{name}_use", "hold:Use=off", "wait:20"]
A += ["cmd:/tp @s -837.5 150 266.5 0 75", "cmd:/item replace entity @s weapon.mainhand with minecraft:air", "wait:150", "persp:0", "wait:5", f"shot:{tag}_body_down",
      "cmd:/item replace entity @s weapon.mainhand with simplyswords:iron_claymore", "wait:15", f"shot:{tag}_body_claymore",
      "hold:Shift=on", "wait:12", f"shot:{tag}_body_sneak", "hold:Shift=off", "wait:10",
      "cmd:/tp @s -837.5 150 266.5 0 20", "wait:150", "persp:0", "hold:Up=on", "hold:Sprint=on", "wait:8", f"shot:{tag}_sprint", "hold:Up=off", "hold:Sprint=off", "wait:10",
      "cmd:/item replace entity @s weapon.mainhand with simplyswords:iron_claymore", "persp:2", "wait:20", f"shot:{tag}_third_front",
      "persp:1", "wait:20", f"shot:{tag}_third_back", "persp:0", "cmd:/item replace entity @s weapon.mainhand with minecraft:air"]
sys.exit(subprocess.call([sys.executable, "tests/client_qa/qa.py", inst, *A, "--timeout", "900"]))
