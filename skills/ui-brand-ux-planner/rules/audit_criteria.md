# UI Brand & UX Planner — Audit Criteria (`ui-brand-ux-planner`)

1. **Architecture, 5-Plane Palette & Craft Contracts:**
   - `[PASS]` Complete **8-Section `DESIGN.md` Blueprint** with Light & Dark 5-Plane `oklch()` + `light-dark()` tokens (`--bg-well`..`--bg-key`, `#000000` absent, `C <= 0.20`, hard cap `C > 0.22`, `color-mix(in oklab, ...)`), Light 3-layer shadows, Dark `--light-zenith`, Mobile-First postures (`Compact`/`Medium`/`Expanded`), single-library `24x24` SVGs, variable Google Fonts (`font-optical-sizing: auto`, heading-only `optimizeLegibility`), and 5-state FSM.
   - `[FAIL]` Any blueprint permitting `#000000`, `C > 0.22`, blur blobs, confetti badges, dashed wireframes, reflow transitions, `DOM != Tab` order, amateur `<svg>` clouds, mixed icon packs, missing Light or Dark polarity, or body `optimizeLegibility`.

2. **Bounded DAG & Ownership Contracts:**
   - `[PASS]` `ui_dag_compiler.py` emits valid Pydantic v2 `UIExecutionDAG` (`greenfield` = 3 nodes: `ui-planner -> ui-worker -> ui-judge`; `refactor` = 4 nodes: `ui-analyst -> ui-planner -> ui-worker -> ui-judge`), `active_rules_count <= 5` per node, `owned_files == []` + non-empty `read_targets` on read-only nodes, zero overlapping `owned_files` across sibling workers, and `max_self_refine_rounds <= 3`.
   - `[FAIL]` Read-only nodes listing `owned_files`, colliding write targets across worker nodes, or rules exceeding 5 per node.
