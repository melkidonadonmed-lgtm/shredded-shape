---
name: ui-brand-ux-planner
description: "Use when planning brand identity, 5-plane OKLCH 60-30-10 tokens, 7 style archetypes (Soft, Hi-Tech, Tactile, Elevated, Retro, Vintage, Clinical), 6 Spatial Archetypes, Google Stitch spacing, Figma MCP, Google Fonts, verified 24x24 SVGs, 3D Unity assets, DESIGN.md blueprints, and <=5-rule DAGs. Do NOT use for live DevTools audits or writing code."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv) and Pydantic v2"
allowed-tools: "read_file run_command"
metadata:
  author: "shredded-shape"
  version: "1.5.1"
  updated_at: "2026-11-18"
  category: "frontend-planning"
  tags: "design-blueprint, oklch-palette, google-fonts, lucide-svg, stitch-figma, dag-compiler"
---

# Brand Strategy, Optical Token & DAG Planner (`ui-brand-ux-planner`)

## Overview
Strictly **read-only** Stage 1 Architect. Convert brand goals, personas, and Stage 0 CLAREZA findings into an 8-section `DESIGN.md` blueprint, verified assets, and a `<= 5`-rule DAG for `ui-worker`.

## Inputs
- Brand goals, domain constraints (`EHR/PEP`, `@xyflow/react`, SaaS, editorial), and Stage 0 CLAREZA diff.
- Target directory (`greenfield` vs `refactor`).

## Procedure
Execute under **Zero-Trust Read-Only Guardrails** (zero writes; load only needed L3 refs):

1. **Phase 1 (`[ToT]`) — Archetypes & Ergonomics:** Prune `(StyleArchetype x SpatialArchetype x Dials)` branches and lock 1 of 7 Style + 1 of 6 Spatial Archetypes (`bento_12_col`, `workbench_split_view`, `command_center_grid`, `editorial_65ch`, `spatial_hud_dock`, `vector_a4_print`) in [`references/style_archetypes_tokens_and_menus.md`](references/style_archetypes_tokens_and_menus.md). See [`references/intuitive_ux_rsc_and_agentic_ui.md`](references/intuitive_ux_rsc_and_agentic_ui.md) for RSC, Next.js 15+ `await params`, Mobile-First postures, and `DOM == Tab Order`.
2. **Phase 2 — 5-Plane `OKLCH 60-30-10` Palette:** Lock `light-dark()` surfaces (`--bg-well`, 60% `--bg-canvas` without `#000000`, `--bg-card`, `--bg-card-lit`, `--bg-key`) and 10% `--brand-primary` (`C <= 0.20`, cap `0.22`, semantic red `15°..40° <= 0.24`, `color-mix(in oklab, ...)`), Light 3-layer shadows, and Dark `--light-zenith` + rim light. Ban blobs, confetti pills, dashed wireframes, and neon glows.
3. **Phase 3 — Fonts, Stitch Spacing & `24x24` SVGs:** Lock Google Fonts variable `@font-face` (`font-optical-sizing: auto`, body `text-rendering: auto`, heading `optimizeLegibility`) and Stitch spacing per [`references/external_assets_stitch_figma_fonts_3d.md`](references/external_assets_stitch_figma_fonts_3d.md). Pick ONE SVG set (`Lucide`/`Material`/`Phosphor`/`Fluent`) and copy `24x24` `<symbol>` paths from [`references/design_md_and_plan_template.md`](references/design_md_and_plan_template.md).
4. **Phase 4 — Toolkits & Blueprint Gate:** Bind `Google Stitch`, `Figma` MCP, `modern-web-guidance` (or L3 fallback), or `Unity`/`Three.js` budgets and check the 8-section blueprint via [`rules/audit_criteria.md`](rules/audit_criteria.md).
5. **Phase 5 — Bounded DAG & Self-Refine Checklist:** Run `--json` stdout in sandbox (`--out <dag.json>` optional), verifying `owned_files == []` on read-only nodes, disjoint worker `owned_files`, and `<= 5` rules/node:
   - Plugin (`pwsh`/POSIX): `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-brand-ux-planner/scripts/ui_dag_compiler.py" <target> --style <archetype> [--spatial <slug>] --hue <deg> --mode <auto|greenfield|refactor> --json`
   - Repo fallback: `uv run python skills/ui-brand-ux-planner/scripts/ui_dag_compiler.py <target> --style <archetype> --hue <deg> --json`

## Gotchas
- **Zero-Write Isolation:** Emit `DESIGN.md` verbatim for `ui-worker`; prefer `--json` stdout in read-only sessions.
- **Canonical Style Slugs:** Pass `--style hi-tech` (normalizes `hitech`) and one of 6 `SpatialArchetype` CLI slugs.
- **Verified SVGs:** Copy verified `24x24` paths or run explicit `npx svgo` optimization.

## Output
- Complete **8-Section `DESIGN.md` Blueprint** and compiled `UIExecutionDAG` JSON.

## User Communication
Present architectural choices, dials, icon plans, and DAG phases in **Portuguese (`pt-BR`)**, keeping `DESIGN.md` tokens and DAG schemas in Technical English.
