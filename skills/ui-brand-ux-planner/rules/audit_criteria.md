# UI Brand & UX Planner — Audit Criteria (`ui-brand-ux-planner`)

1. **Architecture, Context Engineering & Craft Contracts:**
   - `[PASS]` Complete **8-Section `DESIGN.md` Blueprint** with Phase 0 Scope Lock, risk-triaged ambiguity defaults/HITL questions, 5 answered Usage/Intuitiveness questions, 5-Plane `oklch()` + `light-dark()` + Tailwind v4 `@theme inline` `--shadow-elevation-*`, variable Google Fonts (`font-optical-sizing: auto`, `text-wrap: balance/pretty`, heading-only `optimizeLegibility`), silent CSS breadcrumbs (`::before`), GPU `.skip-link`, `flow-root`, single-library `24x24` SVGs, and 5-state FSM.
   - `[FAIL]` Any blueprint permitting `#000000`, `C > 0.22`, blur blobs, confetti badges, dashed wireframes, gradient text, side-stripes, `grid-auto-flow: dense`, reflow transitions, `DOM != Tab` order, amateur `<svg>` clouds, mixed icon packs, unresolved TODO/TBD placeholders, or body `optimizeLegibility`.

2. **Bounded Acyclic DAG & Ownership Contracts:**
   - `[PASS]` `ui_dag_compiler.py` emits valid Pydantic v2 `UIExecutionDAG` (`greenfield` = 3 nodes, `refactor` = 4 nodes, `planner_directed` = 5 acyclic nodes with `max_discovery_hops: 1`), `active_rules_count <= 5` per node, `owned_files == []` + non-empty `read_targets` on read-only nodes, zero overlapping `owned_files` across sibling workers, explicit `stop_condition`, and `max_self_refine_rounds <= 3`.
   - `[FAIL]` Read-only nodes listing `owned_files`, colliding write targets across worker nodes, cyclic discovery loops (`> 1` hop), or rules exceeding 5 per node.
