# SPEC.MD — Implementation Contract: `shredded-shape` UI/UX Suite (v1.0.0)

## 1. Objective and Boundaries (Scope Lock)
- **What to build:**
  1. Standalone UI/UX repository & Antigravity plugin (`C:\Users\melki\dev\repos\shredded-shape` synced to `C:\Users\melki\.gemini\config\plugins\shredded-shape\`) decoupled from `franklin-quebragalho`.
  2. Interactive HTML Architecture Atlas (`assets/ui_skills_architecture_atlas.html`) showcasing the legacy `franklin-quebragalho` UI topology (`As-Is`), the separated 4-stage Actor-Critic suite (`To-Be`), and a live interactive 7-style laboratory (`Soft`, `Hi-Tech`, `Tactile`, `Elevated`, `Retro`, `Vintage`, `Clinical`) in dual Light/Dark modes.
  3. 6 canonical skills (`ui-frontend-analyst`, `ui-brand-ux-planner`, `ui-clean-worker`, `ui-quality-judge`, `clinical-minimalist-ui`, `complex-zero`) + 4 declarative subagents (`ui-analyst.md`, `ui-planner.md`, `ui-worker.md`, `ui-judge.md`) + `plans/ui_actor_critic_dag.json` + deterministic scripts and tests.
- **Non-Goals (Forbidden):**
  - Never mutate third-party read-only skill `C:\Users\melki\.agents\skills\design-taste-frontend\`.
  - Never duplicate global plugin skill folders inside per-repo `.agents/skills.json`.
  - Never allow `../` relative link escapes in `SKILL.md`, UI emojis, `#000000` dark canvases, neon colors, or explanatory prose clutter in interfaces.

## 2. Data Contracts and Interfaces (I/O)
- **Strict Schemas (`extra="forbid"`):** `UIExecutionDAG` (`ui_dag_compiler.py`, `max_rules_per_node <= 5`, zero parallel file collisions), `FrontendInventoryReport` (`frontend_inventory_and_slop_scanner.py`), `RAWVerificationResult` (`verify_raw_frontend.py` with SHA-256), and `UIJudgeReport` (`ui_judge_gatekeeper.py` with WCAG 2.2 OKLCH contrast $FNR < 0.001$).
- **Plugin Bundle (`plugin.json`):** Only official keys (`$schema`, `name`, `displayName`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `logo`, `suggestedPrompts`).

## 3. Acceptance and Exit Criteria (Definition of Done)
- [ ] `uv run python scripts/validate_shredded_shape.py --strict` passes `6/6` skills and `4/4` subagents with exit code `0`.
- [ ] `uv run pytest -q` passes 100% including adversarial validation, WCAG 2.2 OKLCH math, RAW SHA-256, and $F_1 = 1.0$ trigger evals.
- [ ] `ui_skills_architecture_atlas.html` scores `PASSED` and `ai_slop_score == 0` under both `ui-frontend-analyst` and `ui-quality-judge`.
- [ ] `sync_shredded_shape.py` deploys the plugin cleanly to `C:\Users\melki\.gemini\config\plugins\shredded-shape\`.
