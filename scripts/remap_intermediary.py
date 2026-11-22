"""Rewrite decompiled Fabric (intermediary) Java sources to Mojang names for a NeoForge source port.

  python scripts/remap_intermediary.py <mappings.tiny> <src_dir> <out_dir>

<mappings.tiny>: tiny v2 with namespaces 'intermediary named ...' where 'named' is Mojang mappings for 1.21.1
(e.g. Loom's mappings-base.tiny for 1.21.1, or Fabric intermediary + Mojang official joined on 'official').
Intermediary ids are globally unique, so class_N / method_N / field_N are replaced textually; imports become
Mojang package paths and inner classes use Outer.Inner. The output still needs a human pass (Fabric APIs,
mixin targets/descriptors) - it is a porting aid, not a converter. Used for ports/bettersmoke.
"""
import re, sys
from pathlib import Path


def load(tiny):
    classes, methods, fields = {}, {}, {}
    lines = Path(tiny).read_text(encoding="utf-8").splitlines()
    head = lines[0].split("\t")
    ns = head[3:]
    i_int, i_named = ns.index("intermediary"), ns.index("named")
    for line in lines[1:]:
        parts = line.split("\t")
        if parts[0] == "c":
            classes[parts[1 + i_int]] = parts[1 + i_named]
        elif len(parts) > 2 and parts[1] in ("m", "f"):
            names = parts[3:]
            (methods if parts[1] == "m" else fields)[names[i_int]] = names[i_named]
    return classes, methods, fields


def main():
    classes, methods, fields = load(sys.argv[1])
    simple = {}
    for k, v in classes.items():
        simple[k.rsplit("/", 1)[1].split("$")[-1]] = v.rsplit("/", 1)[1].split("$")[-1]
    src, out = Path(sys.argv[2]), Path(sys.argv[3])
    for f in src.rglob("*.java"):
        t = f.read_text(encoding="utf-8")
        # imports: net.minecraft.class_A[.class_B] -> mojang path with inner classes dotted
        def imp(m):
            parts = m.group(1).split(".")
            key = "net/minecraft/" + parts[0] + "".join("$" + p for p in parts[1:])
            named = classes.get(key)
            return "import " + named.replace("/", ".").replace("$", ".") + ";" if named else m.group(0)
        t = re.sub(r"import net\.minecraft\.((?:class_\d+)(?:\.class_\d+)*);", imp, t)
        t = re.sub(r"\bclass_\d+\b", lambda m: simple.get(m.group(0), m.group(0)), t)
        t = re.sub(r"\bmethod_\d+\b", lambda m: methods.get(m.group(0), m.group(0)), t)
        t = re.sub(r"\bfield_\d+\b", lambda m: fields.get(m.group(0), m.group(0)), t)
        dst = out / f.relative_to(src)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(t, encoding="utf-8")
        left = sorted(set(re.findall(r"\b(?:class|method|field)_\d+\b", t)))
        print(f"{f.relative_to(src)}: unmapped {left[:8]}")


if __name__ == "__main__":
    main()
