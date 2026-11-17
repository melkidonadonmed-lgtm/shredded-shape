# SPEC.MD — Implementation Contract: `shredded-shape` UI/UX Suite (v1.4.0)

## 1. Objective and Boundaries (Scope Lock)
- **What to build:**
  1. Standalone UI/UX repository & Antigravity plugin (`C:\Users\melki\dev\repos\shredded-shape` synced to `C:\Users\melki\.gemini\config\plugins\shredded-shape\`) with `1.4.0` / `MIT` parity.
  2. Modular 3-file 7-Chapter Atlas (`assets/ui_skills_architecture_atlas.html`, `assets/atlas_styles.css`, `assets/atlas_app.js` — `<= 600` lines each, zero external CDN, `file://`-compatible) uniting `To-Be`/`As-Is`, 7 real Style Archetypes, 12-Vector Anti-Slop + Stitch Radii, Mobile-First Adaptive Postures, 5-Plane `OKLCH` + Gradients, 4-Stage Shadows, Tactile Hardware + 5 Pseudoclasses, and Draggable `@container`/`subgrid`/`0fr` Menus.
  3. 6 canonical skills (`<= 150`L L3 refs) + 4 declarative subagents (`send_message`, `max_steps` `10/8/16/8`, `<= 5` rules/node) + unified positional/`--target` CLI scripts.
- **Non-Goals (Forbidden):**
  - Never mutate read-only `C:\Users\melki\.agents\skills\design-taste-frontend\`.
  - Never introduce gatekeeper bypass flags (`data-slop-demo`), AudioContext synthesizers, external CDN scripts, `#000000`, neon glows, blur blobs, confetti badges, or dashed wireframes.

## 2. Data Contracts and Interfaces (I/O)
- **Strict Schemas (`extra="forbid"`):** `UIExecutionDAG` (`normalize_style_archetype`, optional `--out`), `FrontendInventoryReport`, `RAWVerificationResult` (SHA-256 + wireframes/confetti/reflow/600L/fail-closed `--run-tsc`), and `UIJudgeReport` (polarity-isolated OKLab contrast + `.sus-grid` AAA).
- **Plugin Bundle (`plugin.json`):** Version `"1.4.0"`, License `"MIT"`, synced to `~/.gemini/config/plugins/shredded-shape/`.

## 3. Acceptance and Exit Criteria (Definition of Done)
- [x] `uv run python scripts/validate_shredded_shape.py --strict` passes `6/6` skills and `4/4` subagents with exit code `0`.
- [x] `uv run pytest -v` passes 100% including adversarial validation, polarity isolation, multi-file DOM evaluation, CLI smoke tests, and $F_1 = 1.0$ trigger evals.
- [x] Unified 3-file Atlas passes `frontend_inventory_and_slop_scanner.py` (`ai_slop_score == 0`), `verify_raw_frontend.py`, `ui_judge_gatekeeper.py --composite` (`PASSED`, Readiness `100.0`, 6-Dim `100.0`), and `complex_zero_ast_auditor.py` (`100/100`).
- [x] `sync_shredded_shape.py` deploys cleanly to `C:\Users\melki\.gemini\config\plugins\shredded-shape\`.
