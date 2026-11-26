particle minecraft:end_rod ~ ~1.2 ~ 0.4 1.0 0.4 0.04 24 normal @a[distance=..48,tag=!horizon_fx_quiet]
execute as @a[distance=..48,tag=!horizon_fx_quiet] at @s run playsound horizon:cue.legend_slain player @s ~ ~ ~ 1 1
title @s[tag=!horizon_fx_quiet] actionbar {"text":"Foe vanquished - an Ancient Core and a trophy are yours","color":"aqua"}
