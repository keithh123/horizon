"""Local Graphify + deterministic Horizon data links. No LLM or API key required.

  python scripts/horizon_graph.py setup
  python scripts/horizon_graph.py build
  python scripts/horizon_graph.py query "quest rewards" --budget 1200
  python scripts/horizon_graph.py affected "manifests/legends.json"
  python scripts/horizon_graph.py status

The isolated environment lives outside the checkout to avoid Windows path limits.
All remaining arguments are forwarded to the pinned Graphify CLI.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import venv

PLAIN = Path(__file__).resolve().parent.parent
ROOT = Path("\\\\?\\" + str(PLAIN)) if os.name == "nt" and not str(PLAIN).startswith("\\\\?\\") else PLAIN
OUT = ROOT / "graphify-out"
VERSION = "0.9.121"
ENV = Path.home() / ".cache/horizon-graphify/venv"
PYTHON = ENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
RESOURCE = re.compile(r"[a-z][a-z0-9_.-]*:[a-z0-9_/.-]+\Z")


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def inputs():
    result = subprocess.check_output(
        ["git", "-C", str(PLAIN), "ls-files", "--cached", "--others", "--exclude-standard", "-z"]
    ).decode().split("\0")
    return sorted({p for p in result if p and not p.startswith(
        ("graphify-out/", "dist/", "ports/dist/", ".horizon/", ".claude/skills/graphify/")
    ) and (ROOT / p).is_file()})


def fingerprint():
    digest = hashlib.sha256()
    paths = inputs()
    for p in paths:
        digest.update(p.encode() + b"\0" + hashlib.sha256((ROOT / p).read_bytes()).digest())
    return digest.hexdigest(), len(paths)


def graphify(*args):
    env = dict(os.environ, GRAPHIFY_BACKEND="none", PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    return subprocess.run([str(PYTHON), "-m", "graphify", *map(str, args)], cwd=PLAIN, env=env).returncode


def setup():
    if not PYTHON.exists():
        venv.create(ENV, with_pip=True)
    subprocess.run([str(PYTHON), "-m", "pip", "install", "--disable-pip-version-check",
                    f"graphifyy=={VERSION}"], check=True)
    print("Ready. Run: python scripts/horizon_graph.py build")


class HorizonLinks:
    def __init__(self, data):
        self.data = data
        self.nodes = {n["id"]: n for n in data["nodes"]}
        self.edges = data["edges"]
        self.files = {n["source_file"]: n["id"] for n in data["nodes"]
                      if n.get("label") == Path(n.get("source_file", "")).name}
        self.counts = {}

    def node(self, key, label, source, pointer="", **extra):
        if key not in self.nodes:
            self.nodes[key] = dict(id=key, label=label, file_type="concept", source_file=source,
                                   source_location="L1", source_pointer=pointer, horizon=True, **extra)
        return key

    def file(self, path):
        if path not in self.files:
            self.files[path] = self.node("horizon_file:" + path, path, path)
        return self.files[path]

    def edge(self, source, target, relation, file, pointer="", **extra):
        self.edges.append(dict(source=source, target=target, relation=relation, confidence="EXTRACTED",
                               context=relation, weight=1.0, source_file=file, source_location="L1",
                               source_pointer=pointer, horizon=True, **extra))

    def resource(self, value, source, pointer=""):
        return self.node("horizon_id:" + value, value, source, pointer)

    def refs(self, owner, value, source, pointer="", relation="references_id"):
        if isinstance(value, dict):
            for k, v in value.items():
                part = str(k).replace("~", "~0").replace("/", "~1")
                self.refs(owner, v, source, pointer + "/" + part, relation)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                self.refs(owner, v, source, pointer + "/" + str(i), relation)
        elif isinstance(value, str) and RESOURCE.fullmatch(value):
            self.edge(owner, self.resource(value, source, pointer), relation, source, pointer)

    def mods(self):
        lockfile = "manifests/lock.json"
        locked = read(lockfile)["mods"]
        by_project = {m["project_id"]: "horizon_mod:" + m["slug"] for m in locked}
        for i, mod in enumerate(locked):
            key = by_project[mod["project_id"]]
            pointer = f"/mods/{i}"
            self.node(key, f"{mod['title']} [{mod['slug']}]", lockfile, pointer,
                      version=mod["version"], kind="mod")
            self.edge(key, self.file(lockfile), "resolved_in", lockfile, pointer)
        for i, mod in enumerate(locked):
            for j, dep in enumerate(mod.get("deps", [])):
                if dep.get("type") == "required" and dep.get("project_id") in by_project:
                    self.edge(by_project[mod["project_id"]], by_project[dep["project_id"]],
                              "requires", lockfile, f"/mods/{i}/deps/{j}")
        rosterfile = "manifests/roster.json"
        for group, mods in read(rosterfile)["groups"].items():
            for i, mod in enumerate(mods):
                key = "horizon_mod:" + mod["slug"]
                if key in self.nodes:
                    pointer = f"/groups/{group}/{i}"
                    self.nodes[key]["edit_source"] = rosterfile
                    self.nodes[key]["reason"] = mod.get("why", "")
                    self.edge(key, self.file(rosterfile), "configured_in", rosterfile, pointer)
        self.counts["mods"] = len(locked)

    def gameplay(self):
        source = "manifests/legends.json"
        bosses = read(source)["bosses"]
        for i, boss in enumerate(bosses):
            key = self.resource(boss["id"], source, f"/bosses/{i}")
            self.nodes[key].update(label=f"{boss['name']} ({boss['id']})", kind="boss", edit_source=source)
            self.edge(key, self.file(source), "declared_in", source, f"/bosses/{i}")
        source = "manifests/loot_families.json"
        families = read(source)["families"]
        for name, family in families.items():
            key = self.node("horizon_family:" + name, f"{family['title']} loot family [{name}]",
                            source, f"/families/{name}", edit_source=source, kind="loot_family")
            self.edge(key, self.file(source), "declared_in", source, f"/families/{name}")
            self.refs(key, family, source, f"/families/{name}")
        source = "manifests/expeditions.json"
        trials = read(source)["trials"]
        for i, trial in enumerate(trials):
            key = self.node("horizon_trial:" + trial["id"], trial["name"], source,
                            f"/trials/{i}", edit_source=source, kind="trial")
            self.edge(key, self.file(source), "declared_in", source, f"/trials/{i}")
            for item in trial["cost"]:
                self.edge(key, self.resource(item, source), "consumes", source, f"/trials/{i}/cost")
            self.refs(key, trial["waves"], source, f"/trials/{i}/waves", "wave_entity_reference")
            self.refs(key, trial["rewards"], source, f"/trials/{i}/rewards", "reward_reference")
        self.counts.update(bosses=len(bosses), loot_families=len(families), trials=len(trials))

    def headquarters(self):
        # 0.6 campaign: stages, choice options and services from manifests/headquarters.json, their prerequisites and the
        # quests that mirror them. The ledger itself is runtime state (kubejs_persistent_data.nbt) and is not in the graph.
        source = "manifests/headquarters.json"
        hq = read(source)
        stages = hq["stages"]
        for i, st in enumerate(stages):
            key = self.node("horizon_hq_stage:" + st["id"], f"{st['numeral']}. {st['title']} (headquarters stage)", source,
                            f"/stages/{i}", edit_source=source, kind="hq_stage")
            self.edge(key, self.file(source), "declared_in", source, f"/stages/{i}")
            for j, req in enumerate(st["requires"]):
                self.edge(key, "horizon_hq_stage:" + req, "requires_stage", source, f"/stages/{i}/requires/{j}")
            self.refs(key, st["requirements"], source, f"/stages/{i}/requirements", "requirement_reference")
            for j, c in enumerate(st["cost"]):
                self.edge(key, self.resource(c[0], source), "consumes", source, f"/stages/{i}/cost/{j}")
            self.refs(key, st["rewards"], source, f"/stages/{i}/rewards", "reward_reference")
            for j, sv in enumerate(st["services"]):
                self.edge(key, "horizon_hq_service:" + sv, "unlocks_service", source, f"/stages/{i}/services/{j}")
            for j, o in enumerate((st.get("choices") or {}).get("options", [])):
                ok = self.node(f"horizon_hq_option:{st['id']}/{o['id']}", f"{o['title']} ({st['title']} option)", source,
                               f"/stages/{i}/choices/options/{j}", edit_source=source, kind="hq_option")
                self.edge(ok, key, "option_of", source, f"/stages/{i}/choices/options/{j}")
                self.refs(ok, o["requirements"], source, f"/stages/{i}/choices/options/{j}/requirements", "requirement_reference")
                for k, c in enumerate(o["cost"]):
                    self.edge(ok, self.resource(c[0], source), "consumes", source, f"/stages/{i}/choices/options/{j}/cost/{k}")
                for k, sv in enumerate(o["services"]):
                    self.edge(ok, "horizon_hq_service:" + sv, "unlocks_service", source, f"/stages/{i}/choices/options/{j}/services/{k}")
        for name in hq["services"]:
            key = self.node("horizon_hq_service:" + name, hq["services"][name]["title"] + " (charter service)", source,
                            f"/services/{name}", edit_source=source, kind="hq_service")
            self.edge(key, self.file(source), "declared_in", source, f"/services/{name}")
        server = self.file("kubejs/server_scripts/horizon_headquarters.js")
        self.edge(server, self.file("kubejs/startup_scripts/horizon_hq_data.js"), "reads", "docs/BUILDING.md")
        self.counts.update(hq_stages=len(stages), hq_services=len(hq["services"]))

    def quests(self):
        paths = sorted((ROOT / "config/heracles/quests").rglob("*.json"))
        quests = {}
        for path in paths:
            source = path.relative_to(ROOT).as_posix()
            quest = read(source)
            title = quest.get("display", {}).get("title", path.stem)
            try:
                title = json.loads(title).get("text", title)
            except (ValueError, AttributeError):
                pass
            key = self.node("horizon_quest:" + path.stem, title + " [" + path.stem + "]",
                            source, edit_source="scripts/gen_quests.py", kind="quest")
            quests[path.stem] = (key, quest, source)
            self.edge(key, self.file("scripts/gen_quests.py"), "generated_by", source)
            self.refs(key, quest.get("tasks", {}), source, "/tasks", "task_reference")
            self.refs(key, quest.get("rewards", {}), source, "/rewards", "reward_reference")
            for i, t in enumerate(quest.get("tasks", {}).values()):   # headquarters quests mirror ledger stages/options
                for adv in t.get("advancements", []):
                    if adv.startswith("horizon:hq/") and adv != "horizon:hq/root":
                        rest = adv[len("horizon:hq/"):]
                        target = ("horizon_hq_option:" if "/" in rest else "horizon_hq_stage:") + rest
                        if target in self.nodes:
                            self.edge(key, target, "mirrors", source, "/tasks")
        for key, quest, source in quests.values():
            for i, dependency in enumerate(quest.get("dependencies", [])):
                if dependency not in quests:
                    raise ValueError(f"Missing quest dependency {dependency!r} in {source}")
                self.edge(key, quests[dependency][0], "requires_quest", source, f"/dependencies/{i}")
        self.counts["quests"] = len(quests)

    def ownership(self):
        # The ownership and input contracts are documented in docs/BUILDING.md.
        contracts = {
            "resolve": (["manifests/roster.json"], ["manifests/lock.json"]),
            "check_deps": (["manifests/lock.json"], ["manifests/deps_report.json"]),
            "gen_assets": (["manifests/legends.json", "manifests/headquarters.json"], ["kubejs/.generated-assets.json"]),
            "gen_headquarters": (["manifests/headquarters.json", "manifests/legends.json", "manifests/loot_families.json",
                                  "manifests/expeditions.json", "manifests/ids.json"],
                                 ["datapacks/.generated-hq.json", "kubejs/.generated-hq.json", "kubejs/startup_scripts/horizon_hq_data.js",
                                  "docs/HEADQUARTERS.md", "docs/HQ_PLANS.md", "docs/HQ_GRAPH.md"]),
            "gen_datapack": (["manifests/loot_families.json", "manifests/legends.json",
                              "manifests/expeditions.json", "manifests/loot_calibration.json",
                              "manifests/loot_audit.json", "manifests/ids.json"],
                             ["datapacks/.generated.json", "docs/LOOT_BUDGET.md"]),
            "gen_quests": (["manifests/loot_families.json", "manifests/legends.json", "manifests/headquarters.json",
                            "manifests/expeditions.json", "manifests/ids.json"], ["config/heracles/groups.txt"]),
            "gen_docs": (["manifests/lock.json", "manifests/roster.json"], ["docs/MODLIST.md"]),
        }
        for script, (sources, outputs) in contracts.items():
            generator = self.file(f"scripts/{script}.py")
            for source in sources:
                self.edge(generator, self.file(source), "reads", "docs/BUILDING.md")
            for output in outputs:
                self.edge(self.file(output), generator, "generated_by", "docs/BUILDING.md")
        # Link documentation to actual, explicitly named source paths; no inferred prose facts.
        for path in sorted((ROOT / "docs").glob("*.md")):
            source = path.relative_to(ROOT).as_posix()
            doc = self.file(source)
            text = path.read_text(encoding="utf-8")
            for match in re.finditer(r"(?:scripts|manifests|kubejs|profiles)/[\w./-]+\.(?:py|json|js|ps1)", text):
                target = match.group()
                if (ROOT / target).is_file():
                    self.edge(doc, self.file(target), "documents", source)

    def finish(self):
        self.mods()
        self.gameplay()
        self.headquarters()
        self.quests()
        self.ownership()
        self.data["nodes"] = list(self.nodes.values())
        self.data["directed"] = True
        from graphify.validate import assert_valid
        assert_valid(self.data)
        return self.data


def build():
    before, count = fingerprint()
    if (OUT / "graph.json").exists():
        # Code-only refreshes preserve semantic nodes. Remove our old data layer
        # explicitly so deleted mods/quests cannot linger.
        write(OUT / "graph.json", strip_horizon(read("graphify-out/graph.json")))
    # Fresh raw AST removes stale domain links and deleted symbols on every build.
    rc = graphify("extract", ROOT, "--code-only", "--no-cluster", "--force", "--max-workers", "2")
    if rc:
        return rc
    data = read("graphify-out/graph.json")
    links = HorizonLinks(data)
    write(OUT / "graph.json", links.finish())
    rc = graphify("cluster-only", ROOT)
    if rc:
        return rc
    after, _ = fingerprint()
    if after != before:
        print("Source changed during build; rebuild before trusting this graph.", file=sys.stderr)
        return 1
    final = read("graphify-out/graph.json")
    report = OUT / "GRAPH_REPORT.md"
    text = report.read_text(encoding="utf-8").replace("graphify update .", "python scripts/horizon_graph.py build")
    text = text.replace("Run `git rev-parse HEAD` and compare to check if the graph is stale.",
                        "Check the source-content fingerprint with `python scripts/horizon_graph.py status`; the commit above is provenance, not the freshness check.")
    report.write_text(text + "\n## Horizon coverage\n\nLocal code AST plus explicit mod requirements, quest prerequisites, resource IDs, boss/trial declarations and generator ownership. No LLM semantic pass. JSON provenance uses file + source_pointer; L1 is the file anchor. Dynamic KubeJS registrations and prose reasoning can be incomplete: inspect the actual source before edits.\n", encoding="utf-8")
    stats = dict(links.counts, nodes=len(final["nodes"]), edges=len(final.get("links", final.get("edges", []))))
    write(OUT / "horizon-index.json", dict(graphify_version=VERSION, source_sha256=after,
          source_files=count, graph_sha256=hashlib.sha256((OUT / "graph.json").read_bytes()).hexdigest(),
          coverage="Local code AST + explicit Horizon JSON relationships; no LLM semantic extraction.",
          stats=stats))
    print("Horizon graph ready: " + ", ".join(f"{v} {k}" for k, v in stats.items()))
    return 0


def strip_horizon(data):
    data["nodes"] = [n for n in data["nodes"] if not n.get("horizon")]
    ids = {n["id"] for n in data["nodes"]}
    for key in ("edges", "links"):
        if key in data:
            data[key] = [e for e in data[key] if not e.get("horizon") and
                         e["source"] in ids and e["target"] in ids]
    return data


def is_current():
    if not (OUT / "horizon-index.json").exists() or not (OUT / "graph.json").exists():
        return False
    index = read("graphify-out/horizon-index.json")
    return (index["source_sha256"] == fingerprint()[0] and
            index["graph_sha256"] == hashlib.sha256((OUT / "graph.json").read_bytes()).hexdigest())


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 0
    if args[0] == "setup":
        setup()
        return 0
    if args[0] == "status":
        current = is_current()
        print("Graph is current." if current else "Graph is missing or stale. Run: python scripts/horizon_graph.py build")
        return 0 if current else 1
    if not PYTHON.exists():
        if args[0] == "hook-guard":
            return 0  # Advisory hooks fail open until setup is installed.
        print("Run: python scripts/horizon_graph.py setup", file=sys.stderr)
        return 2
    if Path(sys.executable).resolve() != PYTHON.resolve():
        env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
        return subprocess.run([str(PYTHON), str(ROOT / "scripts/horizon_graph.py"), *args], env=env, cwd=PLAIN).returncode
    if args[0] in ("build", "update"):
        return build()
    if args[0] != "hook-guard" and not is_current():
        print("Graph is stale; refresh with: python scripts/horizon_graph.py build", file=sys.stderr)
    if args[0] == "affected" and "--relation" not in args:
        for relation in ("reads", "generated_by", "configured_in", "declared_in", "resolved_in", "requires",
                         "requires_quest", "task_reference", "reward_reference", "consumes", "references_id",
                         "requires_stage", "requirement_reference", "unlocks_service", "option_of", "mirrors",
                         "wave_entity_reference", "calls", "imports", "uses", "references", "inherits"):
            args.extend(["--relation", relation])
    return graphify(*args)


if __name__ == "__main__":
    raise SystemExit(main())
