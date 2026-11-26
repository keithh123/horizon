"""Regression checks for data coverage, removed nodes and freshness detection."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PLAIN = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("horizon_graph", PLAIN / "scripts/horizon_graph.py")
graph = importlib.util.module_from_spec(spec)
spec.loader.exec_module(graph)


class HorizonGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = graph.read("graphify-out/graph.json")
        cls.nodes = {n["id"]: n for n in cls.data["nodes"]}
        cls.edges = cls.data.get("links", cls.data.get("edges", []))

    def test_exact_roster_and_quest_coverage(self):
        expected = {"horizon_mod:" + m["slug"] for m in graph.read("manifests/lock.json")["mods"]}
        actual = {k for k in self.nodes if k.startswith("horizon_mod:")}
        self.assertEqual(expected, actual)
        expected = {"horizon_quest:" + p.stem for p in (graph.ROOT / "config/heracles/quests").rglob("*.json")}
        self.assertEqual(expected, {k for k in self.nodes if k.startswith("horizon_quest:")})

    def test_required_dependency_edges_match_lock(self):
        mods = graph.read("manifests/lock.json")["mods"]
        projects = {m["project_id"]: "horizon_mod:" + m["slug"] for m in mods}
        expected = {(projects[m["project_id"]], projects[d["project_id"]]) for m in mods
                    for d in m.get("deps", []) if d.get("type") == "required" and d.get("project_id") in projects}
        actual = {(e["source"], e["target"]) for e in self.edges if e.get("horizon") and e["relation"] == "requires"}
        self.assertEqual(expected, actual)

    def test_quest_prerequisites_and_edit_sources(self):
        expected = set()
        for p in (graph.ROOT / "config/heracles/quests").rglob("*.json"):
            q = json.loads(p.read_text(encoding="utf-8"))
            expected.update(("horizon_quest:" + p.stem, "horizon_quest:" + d) for d in q.get("dependencies", []))
        actual = {(e["source"], e["target"]) for e in self.edges if e["relation"] == "requires_quest"}
        self.assertEqual(expected, actual)
        for node in self.nodes.values():
            if node.get("kind") == "quest":
                self.assertEqual("scripts/gen_quests.py", node["edit_source"])

    def test_no_dangling_edges_and_valid_json_pointers(self):
        for edge in self.edges:
            self.assertIn(edge["source"], self.nodes)
            self.assertIn(edge["target"], self.nodes)
            pointer = edge.get("source_pointer", "")
            if edge.get("horizon") and pointer:
                value = graph.read(edge["source_file"])
                for part in pointer.split("/")[1:]:
                    key = part.replace("~1", "/").replace("~0", "~")
                    value = value[int(key)] if isinstance(value, list) else value[key]

    def test_refresh_removes_deleted_domain_nodes(self):
        fixture = dict(nodes=[dict(id="code"), dict(id="deleted_quest", horizon=True)],
                       links=[dict(source="deleted_quest", target="code", horizon=True),
                              dict(source="code", target="deleted_quest")])
        cleaned = graph.strip_horizon(fixture)
        self.assertEqual([dict(id="code")], cleaned["nodes"])
        self.assertEqual([], cleaned["links"])

    def test_new_source_invalidates_fingerprint(self):
        before = graph.fingerprint()[0]
        with tempfile.NamedTemporaryFile(dir=graph.ROOT / "tests", prefix="graph-freshness-", suffix=".txt", delete=False) as f:
            probe = Path(f.name)
            f.write(b"freshness regression test")
        try:
            self.assertNotEqual(before, graph.fingerprint()[0])
            self.assertFalse(graph.is_current())
        finally:
            probe.unlink()
        self.assertEqual(before, graph.fingerprint()[0])

    def test_affected_includes_horizon_generator_relations(self):
        result = subprocess.run([sys.executable, str(PLAIN / "scripts/horizon_graph.py"),
                                 "affected", "manifests/legends.json", "--depth", "1"],
                                cwd=PLAIN, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("gen_datapack.py", result.stdout)
        self.assertIn("gen_assets.py", result.stdout)

    def test_headquarters_stages_options_and_mirrors(self):
        hq = graph.read("manifests/headquarters.json")
        stages = {"horizon_hq_stage:" + s["id"] for s in hq["stages"]}
        self.assertEqual(stages, {k for k in self.nodes if k.startswith("horizon_hq_stage:")})
        options = {f"horizon_hq_option:{s['id']}/{o['id']}" for s in hq["stages"] for o in (s.get("choices") or {}).get("options", [])}
        self.assertEqual(options, {k for k in self.nodes if k.startswith("horizon_hq_option:")})
        expected = {("horizon_hq_stage:" + s["id"], "horizon_hq_stage:" + r) for s in hq["stages"] for r in s["requires"]}
        actual = {(e["source"], e["target"]) for e in self.edges if e["relation"] == "requires_stage"}
        self.assertEqual(expected, actual)
        mirrored = {e["target"] for e in self.edges if e["relation"] == "mirrors"}
        self.assertEqual(stages | options, mirrored)   # every stage and option has a quest that mirrors it

    def test_headquarters_generator_ownership(self):
        reads = {(e["source"], e["target"]) for e in self.edges if e["relation"] == "reads"}
        src = "horizon_file:manifests/headquarters.json"
        for gen in ("gen_headquarters", "gen_assets", "gen_quests"):   # script files reuse the code-AST node ids
            self.assertIn(("scripts_" + gen, src), reads)
        made = {(e["source"], e["target"]) for e in self.edges if e["relation"] == "generated_by"}
        self.assertTrue(any(s.endswith("horizon_hq_data") and t == "scripts_gen_headquarters" for s, t in made), made)
        self.assertIn(("kubejs_server_scripts_horizon_headquarters", "kubejs_startup_scripts_horizon_hq_data"), reads)

if __name__ == "__main__":
    unittest.main()
