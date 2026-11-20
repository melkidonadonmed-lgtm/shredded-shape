# CONTEXT.MD — Authoritative Project State (`shredded-shape`)
> **Last Updated:** 2026-11-20 | **Status:** `ACTIVE` | **Version:** `1.6.0`

## 1. Overview & Current Architecture
- **Purpose:** Dedicated UI/UX Architecture, Forensic DevTools Analyst, Brand & Style Planner, Clean Optical Worker, and WCAG 2.2 OKLCH Actor-Critic Judge suite packaged as the `shredded-shape` Antigravity plugin.
- **Stack & Runtime:** Python 3.12+ (`uv`, `pydantic`, `pyyaml`, `pytest`), Chrome DevTools Probe JS, Modern CSS (`OKLCH`, `light-dark()`, `@container`, `subgrid`, Tailwind v4 `@theme`, `color-mix(in oklab)`, `@starting-style`), Windows 11 (`pwsh`).
- **Active Modules:**
  - `"skills/"`: **7 canonical UI/UX skills** (`ui-frontend-analyst`, `ui-brand-ux-planner`, `ui-clean-worker`, `ui-quality-judge`, `clinical-minimalist-ui`, `complex-zero`, plus decoupled `stitch-canvas`) with lean L3 `references/*.md` (`<= 150` lines), `artifact_axis_judge.py` (3-Axis Judge), and 12-vector + Craft/AppSec Anti-Slop contracts.
  - `"agents/"`: **4 declarative Actor-Critic subagents** (`ui-analyst.md`, `ui-planner.md`, `ui-worker.md`, `ui-judge.md`) with `send_message`, `max_steps` (`10/8/16/8`), `<= 5` rules/node, and `P0..P3` causal discipline.
  - `"rules/"`: `frontend-9-axes-guidelines.md` (9-Axis SSOT + 5-Plane `OKLCH` + Tailwind v4 `@theme` shadows + `@container` cards + silent breadcrumbs + Mobile-First postures).
  - `"plans/"`: `ui_actor_critic_dag.json` (4-stage bounded DAG + unrolled `planner_directed` `max_discovery_hops: 1`, `<= 5` rules/node, `ui-worker max_steps: 16`, `max_self_refine_rounds: 3`).
  - `"assets/"`: `logo.svg` + modular 3-file Unified 7-Chapter Atlas (`ui_skills_architecture_atlas.html`, `atlas_styles.css`, `atlas_app.js` — `<= 600` lines each, zero external CDN, `file://`-compatible).
  - `"scripts/"` & `"tests/"`: `_ss_core.py`, `_ss_guards.py`, `_ss_craft_guards.py` (vendored to 6 skill `scripts/` dirs), `validate_shredded_shape.py`, `sync_shredded_shape.py`, and `28` unit/calibration/adversarial tests.

## 2. Critical Technical Decisions (Do Not Violate)
- **`[SSOT-UI-01]` Perceptual 5-Plane `OKLCH 60-30-10` & 12-Vector Anti-AI-Slop Gate:** Never use `#000000`, `C > 0.22` accents (`C <= 0.20` target; `C <= 0.24` semantic red `15°..40°` only), neon glows, blur blobs, confetti badges, dashed wireframes, reflow animations (`all`, `width`, `height`), or visual/tab desync. Use `color-mix(in oklab, ...)` for UI mixing.
- **`[SSOT-UI-02]` Polarity-Isolated Verification & Physical Depth:** Resolve `[data-theme="<name>"]`, `.dark`/`.light`, and `@media (prefers-color-scheme)` blocks isolated by polarity over `:root:light`/`:root:dark`, enforcing `well < canvas < card < card-lit` in Dark Mode and 3-layer/135° depth in Light Mode.
- **`[SSOT-UI-03]` Bounded Actor-Critic Isolation (`<= 5` rules/node) & Fail-Closed Scope:** Keep `ui-analyst`, `ui-planner`, and `ui-judge` strictly read-only (`sandbox`), return fail-closed `UNVERIFIED` when scans truncate or narrow to `styles/`, require SHA-256 `Read-After-Write` verification from `ui-worker` with fail-closed `--run-tsc`, and keep zero gatekeeper bypass flags.
- **`[SSOT-UI-04]` Technical English Internals + `pt-BR` Bridge (`[LOCK-04]`):** Author all code, skills, references, rules, and subagents in Technical English; deliver all user communication and Atlas UI copy in **Portuguese (`pt-BR`)**.

## 3. Recent Changes (Changelog)
- `[2026-11-20]` **Cross-Repo Alignment & Reference Pruning (`v1.6.0`):**
  - Deduplicated `max_refinement_rounds` -> canonical `max_self_refine_rounds: 3` in `plans/ui_actor_critic_dag.json`; decoupled L1 overlap between `ui-brand-ux-planner` and `stitch-canvas` and between `complex-zero` and `ui-frontend-analyst`; harmonized `44/48px targets (<40px blocker)` and `C <= 0.20 (hard cap 0.22, red <= 0.24)` across skills and subagents; consolidated 3 `complex-zero` micro-references into `references/cdp_ast_and_axes_guide.md` (`5 -> 3` refs); pruned completed audit dumps (`refined-finishing-gap-analysis-2026-11-17.md`, `skill-atlas-audit-2026-11-17.md`) from `.context/` and compacted `context.md`.
- `[2026-11-19]` **`v1.6.0` (`TASK-07`) — Intent-First Discovery, Craft/AppSec Guards, Canvas Layout & 3-Axis Severe Judge:** Added `scripts/_ss_craft_guards.py` (vendored to 6 skill dirs), `artifact_axis_judge.py` (`--axis ui_code|execution_plan|technical_audit`), unrolled `planner_directed` 5-node DAG (`max_discovery_hops: 1`), `XYFLOW_UNHOISTED_NODE_TYPES` / Windows `/` checks, new L3 guides, and `test_v160_intent_judge_and_craft_guards.py` (`28` total tests, `F1 = 1.0`, `ruff` clean).
- `[2026-11-18]` **`v1.5.1` (`TASK-06`) — Decoupled `stitch-canvas` 7th Skill & Scalar Metadata:** Added `skills/stitch-canvas/` (`stitch_asset_bridge.py` SSRF-safe `=w{width}` downloader), flattened `metadata:` scalars with top-level `allowed-tools` across all `7` skills for ADK Go v2 parity, removed 17 redundant `.agents/skills/` staging packages, and brought all `.py` modules to `<= 600`L / `<= 60`L (`100% APPROVED`).
- `[2026-11-18]` **`v1.5.0` (`TASK-05`) — Gatekeeper Calibration & Print/Test Isolation:** Added `scripts/_ss_guards.py`, scoped `collect_ui_files_scoped()` excluding tests/stories, isolated `.sus-grid`/`@media print`/standalone `.tsx`, fail-closed `UNVERIFIED` on truncation/`styles/` narrowing, balanced JSX `<div onClick>`, pseudo-icon and target-override detectors.
- `[2026-11-17]` **`v1.2.0–v1.4.0` — Actor-Critic Suite, 5-Plane Matte Optics & Unified 7-Chapter Atlas:** Standardized `max_steps` (`10/8/16/8`), `CoT -> ToT -> ReAct -> RAW`, 9-Axis `OKLCH` SSOT, Björn Ottosson OKLab contrast, interactive `:focus-visible`, collapsible sidebar rail, `base-select`, and 3-file standalone `assets/` Atlas (`ai_slop_score == 0`, `Readiness = 100.0`, `UI/UX = 100.0`).

## 4. Backlog & Next Steps (Execution Queue)
- [x] `TASK-01..03`, `TASK-05..07`: 4-stage Actor-Critic suite, Unified 7-Chapter Atlas, `v1.5.0` calibration, `stitch-canvas` (`7/7` skills), and `v1.6.0` Intent-First + 3-Axis Judge.
- [x] `TASK-04`: Connected `shredded-shape` remote GitHub repository (`origin/main`) and published `v1.6.0`.
