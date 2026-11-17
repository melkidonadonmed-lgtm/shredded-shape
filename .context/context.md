# CONTEXT.MD — Authoritative Project State (`shredded-shape`)
> **Last Updated:** 2026-11-17 | **Status:** `ACTIVE` | **Version:** `1.4.0`

## 1. Overview & Current Architecture
- **Purpose:** Dedicated UI/UX Architecture, Forensic DevTools Analyst, Brand & Style Planner, Clean Optical Worker, and WCAG 2.2 OKLCH Actor-Critic Judge suite packaged as the `shredded-shape` Antigravity plugin.
- **Stack & Runtime:** Python 3.12+ (`uv`, `pydantic`, `pyyaml`, `pytest`), Chrome DevTools Probe JS, Modern CSS (`OKLCH`, `light-dark()`, `@container`, `subgrid`, Tailwind v4 `@theme`, `color-mix(in oklab)`, `@starting-style`), Windows 11 (`pwsh`).
- **Active Modules:**
  - `"skills/"`: 6 canonical UI/UX skills (`ui-frontend-analyst`, `ui-brand-ux-planner`, `ui-clean-worker`, `ui-quality-judge`, `clinical-minimalist-ui`, `complex-zero`) with 2-tier L3 `references/*.md` (`<= 150` lines) and 12-vector Anti-Slop contracts.
  - `"agents/"`: 4 declarative Actor-Critic subagents (`ui-analyst.md`, `ui-planner.md`, `ui-worker.md`, `ui-judge.md`) with `send_message`, `max_steps` (`10/8/16/8`), and `<= 5` rules/node.
  - `"rules/"`: `frontend-9-axes-guidelines.md` (9-Axis SSOT + 5-Plane `OKLCH` + Mobile-First postures + `color-mix(in oklab)`).
  - `"plans/"`: `ui_actor_critic_dag.json` (4-stage bounded DAG with `<= 5` rules/node, `ui-worker max_steps: 16`, and closed-loop Self-Refine edge).
  - `"assets/"`: `logo.svg` + modular 3-file Unified 7-Chapter Atlas (`ui_skills_architecture_atlas.html`, `atlas_styles.css`, `atlas_app.js` — `<= 520` lines each, zero external CDN, `file://`-compatible).
  - `"scripts/"` & `"tests/"`: `_ss_core.py`, `validate_shredded_shape.py`, `sync_shredded_shape.py`, and `test_shredded_shape_suite.py`.

## 2. Critical Technical Decisions (Do Not Violate)
- **`[SSOT-UI-01]` Perceptual 5-Plane `OKLCH 60-30-10` & 12-Vector Anti-AI-Slop Gate:** Never use `#000000`, `C > 0.22` accents (`C <= 0.24` semantic red `15°..40°` only), neon glows, blur blobs, confetti badges, dashed wireframes, reflow animations (`all`, `width`, `height`), or visual/tab desync. Use `color-mix(in oklab, ...)` for UI mixing.
- **`[SSOT-UI-02]` Polarity-Isolated Verification & Physical Depth:** Resolve `[data-theme="<name>"]`, `.dark`/`.light`, and `@media (prefers-color-scheme)` blocks isolated by polarity over `:root:light`/`:root:dark`, enforcing `well < canvas < card < card-lit` in Dark Mode and 3-layer/135° depth in Light Mode.
- **`[SSOT-UI-03]` Bounded Actor-Critic Isolation (`<= 5` rules/node):** Keep `ui-analyst`, `ui-planner`, and `ui-judge` strictly read-only (`sandbox`), require SHA-256 `Read-After-Write` verification from `ui-worker` with fail-closed `--run-tsc`, and zero gatekeeper bypass flags.
- **`[SSOT-UI-04]` Technical English Internals + `pt-BR` Bridge (`[LOCK-04]`):** Author all code, skills, references, rules, and subagents in Technical English; deliver all user communication and Atlas UI copy in **Portuguese (`pt-BR`)**.

## 3. Recent Changes (Changelog)
- `[2026-11-17]` **`v1.4.0` — Interactive `:focus-visible` Scoping & Skill/Rule Propagation (`assets/*`, `rules/*`, `skills/*`)**:
  - Scoped `:focus-visible` in `assets/atlas_styles.css` strictly to interactive controls (`:where(a, button, input, select, textarea, summary, [tabindex="0"], [role="button"], [role="tab"]):focus-visible`), suppressed focus outlines on structural landmarks (`main[tabindex="-1"]`, `:where(h1, h2, h3)[tabindex="-1"]`), and updated `setChapter(1, { focus: false })` + `#live-status` announcements in `assets/atlas_app.js`.
  - Propagated interactive `:focus-visible` scoping, `>= 44x44px` compact `::before`/`::after` swatch/slider hit-boxes, `>= 0.5rem` nav gaps (`>= 13px` tab labels), and SVG `<link rel="icon">` rules across `rules/frontend-9-axes-guidelines.md`, `ui-clean-worker` (`SKILL.md` + `clean_components_cards_motion_and_fsm.md`), `ui-brand-ux-planner` (`intuitive_ux_rsc_and_agentic_ui.md`), `ui-frontend-analyst` (`devtools_webdev_and_modernweb_probe.md`), `ui-quality-judge` (`wcag22_oklch_actor_critic_rubric.md`), and `complex-zero/SKILL.md`.
- `[2026-11-17]` **`v1.4.0` — Live Probe Fitts & Network Console Cleanups (`assets/*` & `README.md`)**:
  - Expanded `.swatch-btn` interactive hit-boxes to `44x44px` (`48x48px` on coarse pointers) and `input[type="range"]` `min-block-size: 44px`, raised `.chapter-nav` / `.mobile-bottom-bar` gaps to `0.5rem` (`8px`) and `.mobile-tab-btn` to `0.8125rem` (`13px`) for `0` `crampedMenus` and `0` `smallTouchTargets`, added `<link rel="icon" href="logo.svg" type="image/svg+xml" />` to eliminate `/favicon.ico` `404`, and linked `assets/atlas_styles.css`, `assets/atlas_app.js`, and `assets/logo.svg` in `README.md`.
- `[2026-11-17]` **`v1.4.0` — Collapsible Sidebar Rail, `base-select` Picker, Natural Motion & Interactive Lists (`assets/*` & L3)**:
  - Upgraded the Unified Atlas sidebar (`264px <-> 72px` desktop rail with `::before` active bar, icon badges, `]`/`[` shortcut, collapsed tooltips, mobile `inert` scrim), implemented `appearance: base-select` + `::picker(select)` animated theme dropdown, refined swatch/segmented selection indicators with `:active` `scale` motion, and wired reactive operational lists in Chapter 3 and 3-item `0fr -> 1fr` disclosures in Chapter 7.
  - Documented collapsible rail, `base-select`, and `.row-action-hint` patterns in `clean_components_cards_motion_and_fsm.md`, and guarded `TS_GENERIC_CALL_RE` (`<(?!/)`) + `.ts/.tsx/.jsx` suffix isolation in `ui_ux_frontend_auditor.py` so closing HTML tags before parentheses (`</code> (`) never inflate DOM depth.
- `[2026-11-17]` **`v1.4.0` — Optical/Typography/Box Hardening + Gatekeeper Contrast & Stacking Audits**:
  - Added `--brand-fill` + `--ink-on-brand` polarity separation, translucent `--light-key` sheen, neutral high-contrast `nexus-slate` / `moss-calm` raised keycaps, `z-index: -1` grain stacking inside `isolation: isolate`, ClearType-ordered font stacks, `:not(pre) > code` token chips, `@layer utilities` cascade isolation (`.flex-row`), unclipped `.chapter-view` shadows + `24px` spacing, and consistent `.card-head`/`.card-foot` rhythm in `assets/*` and Stage-2 L3 references.
  - Hardened `_ss_core.py`, `ui_judge_gatekeeper.py`, and `frontend_inventory_and_slop_scanner.py` with `OPTICS-GRAIN-ABOVE-TEXT`, `WCAG-1.4.3-BRAND-FILL`, `OPTICS-OPAQUE-KEY-SHEEN`, `TYP-DEAD-FONT-FALLBACK`, var-hue `--brand-hue` resolution, and SVG `<use>` filtering from navigation route counts.
- `[2026-11-17]` **`v1.4.0` — EGM Audit Remediation, Unified CLI/Polarity Kernel, L3 Craft Guides & 7-Chapter Unified Atlas**:
  - Upgraded `scripts/_ss_core.py` and all 7 skill scripts (`resolve_cli_target()` positional + `--target`/`--scope`, `--out` on `ui_dag_compiler.py`, `STYLE_ALIASES` `hitech -> hi-tech`, comment-safe `collect_ui_files()`, polarity-isolated `extract_theme_oklch_maps()`, hyphen-safe `REFLOW_TRANSITION_RE`, `evaluate_target()` markup isolation, fail-closed `--run-tsc`, `.sus-grid` auto-AAA, and `audit_tactile_ui.py --self-test`).
  - Hardened `validate_shredded_shape.py` (`1.4.0`/`MIT` parity across `pyproject.toml`/`plugin.json`/6 `SKILL.md`s, `send_message` + `pt-BR` subagent checks, `ui-worker` `max_steps` sync, `.js` cap in `skills/*/scripts/`) and added `--local-only` to `sync_shredded_shape.py`.
  - Upgraded 6 `SKILL.md`s, 6 `audit_criteria.md`, 4 `agents/*.md` (`send_message`, `max_steps: 10/8/16/8`), and all 16 `references/*.md` (12-Vector Anti-Slop, Stitch spacing, Flexbox `min-inline-size: 0`, `@container` isolated from `subgrid`, Mobile-First postures, `0fr -> 1fr`/`@starting-style` menus, `:user-invalid`, Tailwind v4 `@theme`).
  - Integrated the `Atlas de Engenharia Frontend & UI Tátil` into a 3-file standalone `assets/` bundle (`<= 520`L each, 7 interactive chapters, zero external CDN, classic IIFE `defer` for `file://`, `ai_slop_score == 0`, `Readiness = 100.0`, `UI/UX = 100.0`, `Complex-Zero = 100`).
- `[2026-11-17]` **`v1.3.0` — 5-Plane Tactile Matte + Nexus `135°` Elevation & Anti-Confetti/Wireframe Gates**.
- `[2026-11-17]` **`v1.2.0` — Anti-AI-Slop Craft, Björn Ottosson `OKLab`, 2026 Web Docs & `<= 600`L Modularity Upgrade**.

## 4. Backlog & Next Steps (Execution Queue)
- [x] `TASK-01..03`: Bootstrap repository, 4-stage Actor-Critic suite, and `v1.4.0` EGM remediation + Unified 7-Chapter Atlas.
- [ ] `TASK-04`: Connect `shredded-shape` remote GitHub repository when requested by user.
