"""Matched rendering scenes for the shader/LOD/weather matrix (client QA harness).

usage: python tests/client_qa/render_matrix.py <instance> <tag> [--rd N] [--shaders on|off|keep] [--weather clear,rain,thunder]
       [--route] [--perf SECONDS]
Scenes (spectator mode, fixed time 6000): the reported x-ray spot (-838, 266) at eye level and from above, then
an 8-stop flight east through fresh and revisited chunks, all with the HUD hidden. Screenshots: qa_<tag>_<scene>.png.
"""
import subprocess, sys

args = sys.argv[1:]
inst, tag = args[0], args[1]
opt = lambda k, d=None: args[args.index(k) + 1] if k in args else d
rd, shaders, weather = opt("--rd"), opt("--shaders", "keep"), opt("--weather", "clear").split(",")
perf = opt("--perf")
A = ["cmd:/gamemode spectator", "cmd:/time set 6000", "hud:off", "persp:0"]
if rd:
    A += [f"rd:{rd}"]
if shaders != "keep":
    A += [f"shaders:{shaders}", "wait:200"]
VIEWS = {"eye": "/tp @s -838 68 266 0 8", "high": "/tp @s -838 112 266 300 32", "west": "/tp @s -838 70 266 90 6"}
for w in weather:
    A += [f"cmd:/weather {w}", "wait:60"]
    for name, tp in VIEWS.items():
        A += [f"cmd:{tp}", "wait:160", f"shot:{tag}_{w}_{name}"]
if "--route" in args:
    for i in range(8):
        x = -838 + i * 48
        A += [f"cmd:/tp @s {x} 104 266 270 28", "wait:50"] + ([f"shot:{tag}_route_{i}"] if i % 2 else [])
    A += ["cmd:/tp @s -838 104 266 90 28", "wait:80", f"shot:{tag}_route_back"]
if perf:
    A += ["cmd:/weather clear", "cmd:" + VIEWS["high"], "wait:100", f"perf:{tag}:{perf}"]
A += ["hud:on", "pos"]
sys.exit(subprocess.call([sys.executable, "tests/client_qa/qa.py", inst, *A, "--timeout", "1200"]))
