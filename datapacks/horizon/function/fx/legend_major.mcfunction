particle minecraft:totem_of_undying ~ ~1.2 ~ 0.7 1.0 0.7 0.35 70 normal @a[distance=..48,tag=!horizon_fx_quiet]
particle minecraft:end_rod ~ ~1.2 ~ 0.4 1.4 0.4 0.05 30 normal @a[distance=..48,tag=!horizon_fx_quiet]
execute as @a[distance=..48,tag=!horizon_fx_quiet] at @s run playsound horizon:cue.trophy player @s ~ ~ ~ 1 1
title @s[tag=!horizon_fx_quiet] actionbar {"text":"Legend defeated - a Starforged Heart and a trophy are yours","color":"light_purple"}
