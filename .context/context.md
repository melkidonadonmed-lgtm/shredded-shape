# CONTEXT.MD — Authoritative Project State (`shredded-shape`)
> **Last Updated:** 2026-11-16 | **Status:** `ACTIVE`

## 1. Overview & Current Architecture
- **Purpose:** Dedicated UI/UX Architecture, Forensic DevTools Analyst, Brand & Style Planner, Clean Optical Worker, and WCAG 2.2 OKLCH Actor-Critic Judge suite decoupled from `franklin-quebragalho` and packaged as the `shredded-shape` Antigravity plugin.
- **Stack & Runtime:** Python 3.12+ (`uv`, `pydantic`, `pyyaml`, `pytest`), Node.js / Chrome DevTools Probe JS, CSS Modern (`OKLCH`, `light-dark()`, `@container`, `subgrid`, Tailwind v4 `@theme`), Windows 11 (`pwsh`).
- **Active Modules:**
  - `"skills/"`: 6 canonical UI/UX skills (`ui-frontend-analyst`, `ui-brand-ux-planner`, `ui-clean-worker`, `ui-quality-judge`, plus migrated domain packs `clinical-minimalist-ui` and `complex-zero`).
  - `"agents/"`: 4 declarative Actor-Critic subagents (`ui-analyst.md`, `ui-planner.md`, `ui-worker.md`, `ui-judge.md`).
  - `"rules/"`: `frontend-9-axes-guidelines.md` (9-Axis SSOT + Dynamic Dark Illumination + Superior Matte Finish + 7 Style Archetypes).
  - `"plans/"`: `ui_actor_critic_dag.json` (4-stage bounded DAG with `<= 5` rules/node and closed-loop Self-Refine edge).
  - `"assets/"`: `logo.svg` + interactive standalone `ui_skills_architecture_atlas.html` (`As-Is` vs. `To-Be` + live 7-style lab).
  - `"scripts/"` & `"tests/"`: `validate_shredded_shape.py`, `sync_shredded_shape.py`, and `test_shredded_shape_suite.py`.

## 2. Critical Technical Decisions (Do Not Violate)
- **`[SSOT-UI-01]` Perceptual `OKLCH 60-30-10` & Zero Neon:** Never use `#000000` OLED smearing or high-chroma neon accents (`C > 0.22`). Calibrate all palettes in `oklch()` + `light-dark()`.
- **`[SSOT-UI-02]` Polarity-Aware Optics (3-Layer Light Shadows + Dynamic Dark Rim Illumination + Superior Matte Finish):** Light mode uses 3-layer shadows (Contact Umbra + negative-spread Penumbra + Catch-Light `inset 0 1px 0 0`). Dark mode replaces ineffective dark shadows with progressive lightness (`L = 0.16 -> 0.22 -> 0.27`) + subtle specular rim light + non-neon ambient surface halo.
- **`[SSOT-UI-03]` Bounded Actor-Critic Isolation (`<= 5` rules/node):** Keep `ui-analyst`, `ui-planner`, and `ui-judge` strictly read-only (`sandbox`), require physical SHA-256 `Read-After-Write` verification from `ui-worker`, and support `workspace: "share"` vertical route ownership.
- **`[SSOT-UI-04]` Technical English Internals + `pt-BR` Bridge:** All internal skills, subagents, rules, and code run in Technical English; all user-facing conversation and UI diagram deliverables communicate in **Portuguese (`pt-BR`)**.

## 3. Recent Changes (Changelog)
- `[2026-11-16]` Bootstrapped `shredded-shape`, installed read-only `design-taste-frontend` (`taste-skill`) reference in `~/.agents/skills/`, authored `ui_skills_architecture_atlas.html`, implemented the 4-stage Actor-Critic skill/subagent suite (`+ 2` domain packs), and decoupled UI artifacts from `franklin-quebragalho`.

## 4. Backlog & Next Steps (Execution Queue)
- [x] `TASK-01`: Bootstrap repository, plugin manifest, and interactive `As-Is` vs. `To-Be` HTML Architecture Atlas.
- [x] `TASK-02`: Implement the 4 core UI Actor-Critic skills/subagents (`ui-frontend-analyst`, `ui-brand-ux-planner`, `ui-clean-worker`, `ui-quality-judge`) and migrate `clinical-minimalist-ui` & `complex-zero`.
- [x] `TASK-03`: Validate strict contracts, deterministic scripts, WCAG 2.2 OKLCH math, $F_1 = 1.0$ trigger evals, and decouple `franklin-quebragalho`.
- [ ] `TASK-04`: Connect `shredded-shape` remote GitHub repository when requested by user.
