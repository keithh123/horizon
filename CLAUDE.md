# Horizon: find context efficiently

- Before exploring an unfamiliar subsystem, run `python scripts/horizon_graph.py status`, then a focused `python scripts/horizon_graph.py query "<question>" --budget 1200`. On a missing/stale graph, run `python scripts/horizon_graph.py build`. If the environment is missing, run `python scripts/horizon_graph.py setup` once.
- Prefer `--seed "scripts/gen_quests.py" --context reads --depth 1` for generator inputs, or `--seed "manifests/legends.json"` when the source is known. A broad question may match unrelated Java UI classes. Narrow the seed or context before increasing the budget.
- Use `python scripts/horizon_graph.py affected "manifests/legends.json" --depth 1` for direct consumers, `path A B --undirected` for a connection, or `explain X` for neighbors. The wrapper includes Horizon relations in affected queries.
- Read the source files/lines returned by the query before editing. The graph is a navigation index, not runtime evidence; inferred AST edges and dynamic KubeJS callbacks can be incomplete. Fall back to a targeted text search when the graph misses something.
- Do not load the entire graph JSON or report into context. Use the report only for a requested broad architecture review.
- Edit curated manifests and generator scripts. Quests under `config/heracles/`, assets listed in `kubejs/.generated-assets.json`, and datapacks listed in `datapacks/.generated.json` are generated. Follow `docs/BUILDING.md` ownership; never patch generated output to fix the source problem.
- For item/boss/structure specifics use the existing `python scripts/horizon.py find <id-or-name>` (`/horizon-find`) after graph orientation. Run the existing relevant checks, including `/horizon-check quick` for source changes; report unperformed client/gameplay checks honestly.
- Refresh with `python scripts/horizon_graph.py build` after the task's final source edits, before committing. Generic `graphify update .` omits Horizon's JSON extension. Avoid rebuilding after every individual read or edit.
- If delegating exploration, give the agent the task's known source paths and this same scoped-query rule.

Examples and setup details: `docs/GRAPHIFY.md`.
