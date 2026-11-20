---
name: ui-brand-ux-planner
description: "Use when planning brand identity, 5-plane OKLCH 60-30-10 tokens, 7 style archetypes (Soft..Clinical), 6 Spatial Archetypes, Gestalt relational spacing, Figma MCP, Google Fonts, icon packs, 3D Unity assets, DESIGN.md blueprints, and <=5-rule DAGs. Do NOT use for live DevTools audits, writing code, or Stitch CLI/MCP capture (stitch-canvas)."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv) and Pydantic v2"
allowed-tools: "read_file run_command"
metadata:
  author: "shredded-shape"
  version: "1.6.0"
  updated_at: "2026-11-19"
  category: "frontend-planning"
  tags: "design-blueprint, oklch-palette, google-fonts, lucide-svg, stitch-figma, dag-compiler, ambiguity-triage, spacing-engineering"
---

# Brand Strategy, Optical Token & DAG Planner (`ui-brand-ux-planner`)

## Overview
Strictly **read-only** Stage 1 Architect. Execute order-dependent planning (`post-analysis`, `greenfield`, or 1-hop `planner_directed`), triage ambiguity by risk, answer 5 usage/intuitiveness questions, and compile an 8-section `DESIGN.md` blueprint + bounded DAG for `ui-worker`.

## Inputs
- Brand goals, domain constraints (`EHR/PEP`, `@xyflow/react`, SaaS, editorial), and Stage 0 CLAREZA diff (or raw user prompt).
- Target directory (`greenfield`, `refactor`, or `planner_directed`).

## Procedure
Execute under **Zero-Trust Read-Only Guardrails** (zero writes; load only needed L3 refs):

1. **Phase 1 (`[ToT]`) — Intent, Ambiguity Triage & Archetypes:** Apply [`references/context_engineering_and_ambiguity_protocol.md`](references/context_engineering_and_ambiguity_protocol.md) (`refactor`/`greenfield`/`planner_directed` max 1 discovery hop; auto-defaults on cosmetic gaps vs 1–3 HITL questions on clinical/auth/destructive gaps; Phase 0 Scope Lock). Answer the 5 Usage/Intuitiveness questions and lock 1 of 7 Styles + 1 of 6 Spatials via [`references/style_archetypes_tokens_and_menus.md`](references/style_archetypes_tokens_and_menus.md) and [`references/intuitive_ux_rsc_and_agentic_ui.md`](references/intuitive_ux_rsc_and_agentic_ui.md).
2. **Phase 2 — 5-Plane `OKLCH 60-30-10`, Palettes & Unslop Direction:** Apply [`references/curated_palettes_and_unslop_direction.md`](references/curated_palettes_and_unslop_direction.md) (5-line Direction Brief, 9-pass redline order, curated *Midnight Noir / Horizon Code / Moss River / Deep Oceanic / Horizon Warm SaaS* palettes, and `Graphite/Warm/Ink` ramps) with `light-dark()` surfaces (`--bg-well..--bg-key`, no `#000000`), `--brand-primary` (`C <= 0.20`, hard cap `0.22`, red `<= 0.24`), `@theme inline` shadows, and zero slop/blobs/neon/gradient-text.
3. **Phase 3 — Fonts, Spacing & `24x24` SVGs:** Lock variable Google Fonts (`font-optical-sizing: auto`, `text-wrap: balance/pretty`, body `text-rendering: auto`, heading `optimizeLegibility`), `flow-root`/Gestalt spacing per [`references/external_assets_stitch_figma_fonts_3d.md`](references/external_assets_stitch_figma_fonts_3d.md), silent CSS breadcrumbs + `.skip-link`, and ONE `24x24` `<symbol>` SVG set from [`references/design_md_and_plan_template.md`](references/design_md_and_plan_template.md).
4. **Phase 4 — Toolkits & Blueprint Gate:** Bind `Figma`, `modern-web-guidance`, `Unity`/`Three.js` budgets (or consume `stitch-canvas` OKLCH handoffs) and validate the 8-section blueprint against [`rules/audit_criteria.md`](rules/audit_criteria.md).
5. **Phase 5 — Bounded DAG & Phase 0 Gate:** Run `--json` stdout (`--out <dag.json>` optional), enforcing `owned_files == []` on read-only nodes, disjoint worker `owned_files`, `<= 5` rules/node, and `stop_condition`:
   - `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-brand-ux-planner/scripts/ui_dag_compiler.py" <target> --style <archetype> [--spatial <slug>] --hue <deg> --mode <auto|greenfield|refactor|planner_directed> --json` (repo fallback: `uv run python skills/ui-brand-ux-planner/scripts/ui_dag_compiler.py ...`)

## Gotchas
- **Zero-Write Isolation:** Emit `DESIGN.md` verbatim for `ui-worker`; use `--json` stdout in read-only sessions.
- **Canonical Style Slugs:** Pass `--style hi-tech` (normalizes `hitech`) and one of 6 `SpatialArchetype` CLI slugs.
- **Verified SVGs & 1-Hop Discovery:** Never chain unrolled `planner <-> analyst` past 1 discovery hop.

## Output
- Verifiable **8-Section `DESIGN.md` Blueprint** (or 1-hop `ScopedAuditRequest`) and compiled `UIExecutionDAG` JSON (`Read-After-Write` / `Self-Refine` bounded).

## User Communication
Present architectural choices, assumptions, HITL questions, and DAG phases in **Portuguese (`pt-BR`)**, keeping `DESIGN.md` tokens and DAG schemas in Technical English.
