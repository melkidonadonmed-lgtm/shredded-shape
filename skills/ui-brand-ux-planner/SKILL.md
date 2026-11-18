---
name: ui-brand-ux-planner
description: "Use when planning brand identity, 5-plane OKLCH 60-30-10 tokens, 7 style archetypes (Soft, Hi-Tech, Tactile, Elevated, Retro, Vintage, Clinical), 6 Spatial Archetypes, Google Stitch spacing, Figma MCP, Google Fonts, verified 24x24 SVGs, 3D Unity assets, DESIGN.md blueprints, and <=5-rule DAGs. Do NOT use for live DevTools audits or writing code."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv) and Pydantic v2"
metadata:
  author: shredded-shape
  version: "1.5.0"
  updated_at: "2026-11-18"
  category: frontend-planning
  tags:
    - design-md
    - oklch-palette
    - google-fonts
    - lucide-svg
    - stitch-figma
    - dag-compiler
---

# Brand Strategy, Optical Token & DAG Planner (`ui-brand-ux-planner`)

## Overview
Serve as the **strictly read-only** Stage 1 Architect. Translate business goals, target personas, and Stage 0 `ui-frontend-analyst` CLAREZA findings into an unambiguous 8-section `DESIGN.md` blueprint, verified asset specs, and a bounded `<= 5`-rule DAG ready for `ui-worker`.

## Inputs
- Project goal, brand positioning, domain constraints (`EHR/PEP` clinical, `@xyflow/react` cockpit, SaaS, editorial, etc.), and optional Stage 0 CLAREZA diff.
- Target files/directories (`greenfield` vs `refactor`).

## Procedure
Execute in causal order without modifying target source files (load only the `references/*.md` files needed):

1. **Phase 1 (`[ToT]`) — Tree-of-Thoughts Brand, Archetype & Ergonomic Dials Selection:**
   - Evaluate candidate `(StyleArchetype x SpatialArchetype x Dials)` branches against domain constraints and Stage 0 CLAREZA findings, prune incompatible branches, and lock 1 of the 7 Style Archetypes + 1 of the 6 Spatial Archetypes (`bento_12_col`, `workbench_split_view`, `command_center_grid`, `editorial_65ch`, `spatial_hud_dock`, `vector_a4_print`) in [`references/style_archetypes_tokens_and_menus.md`](references/style_archetypes_tokens_and_menus.md).
   - Consult [`references/intuitive_ux_rsc_and_agentic_ui.md`](references/intuitive_ux_rsc_and_agentic_ui.md) for RSC architecture, Next.js 15+ async `params`, Mobile-First adaptive postures, and `DOM == Tab Order`.

2. **Phase 2 — Perceptual 5-Plane `OKLCH 60-30-10` Polarity Palette:**
   - Lock Light & Dark `light-dark()` surfaces: `--bg-well`, 60% `--bg-canvas` (never `#000000`), `--bg-card`, `--bg-card-lit`, `--bg-key`, and 10% `--brand-primary` (`C <= 0.20`, hard cap `C > 0.22`; danger `15°..40°` `<= 0.24`; `color-mix(in oklab, ...)`).
   - Specify Light 3-layer shadows (`-1px..-8px` negative spread + `drop-shadow <= 6px`) and Dark `--light-zenith` + stepped rim light. Ban blur blobs, confetti badges, dashed wireframes, and neon glows.

3. **Phase 3 — Variable Typography, Stitch Spacing & Verified `24x24` SVG Catalog:**
   - Lock Google Fonts variable `@font-face` (`font-optical-sizing: auto`, body `text-rendering: auto`, heading `optimizeLegibility`) and Stitch spacing ($\text{Inner} < \text{Pad} \le \text{Gap} < \text{Section}$) per [`references/external_assets_stitch_figma_fonts_3d.md`](references/external_assets_stitch_figma_fonts_3d.md).
   - Choose ONE web SVG library (`Lucide`, `Material Symbols`, `Phosphor`, or `Fluent`) and copy canonical `24x24` `<symbol>` paths from [`references/design_md_and_plan_template.md`](references/design_md_and_plan_template.md).

4. **Phase 4 — External Toolkits & 8-Section `DESIGN.md` Blueprint Emission:**
   - Integrate `Google Stitch`, `Figma` MCP, `modern-web-guidance` (or offline L3 fallback), or `Unity`/`Three.js` budgets and emit the 8-section `DESIGN.md` blueprint + [`rules/audit_criteria.md`](rules/audit_criteria.md).

5. **Phase 5 — Disjoint Bounded DAG Compilation:**
   - Run the deterministic DAG compiler (`--json` stdout in read-only sandbox; optional `--out <dag.json>` outside sandbox):
     - Plugin path (`pwsh`/POSIX): `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-brand-ux-planner/scripts/ui_dag_compiler.py" <target> --style <archetype> [--spatial <slug>] --hue <deg> --mode <auto|greenfield|refactor> --json` (or `"%USERPROFILE%\.gemini\..."` in `cmd.exe`)
     - Repo fallback: `uv run python skills/ui-brand-ux-planner/scripts/ui_dag_compiler.py <target> --style <archetype> [--spatial <slug>] --hue <deg> --mode <auto|greenfield|refactor> --json`
   - Verify `owned_files == []` on read-only nodes, disjoint `owned_files` across parallel `ui-worker` nodes, and `<= 5` rules/node.

## Gotchas
- **Zero-Write Isolation:** Emit `DESIGN.md` verbatim for `ui-worker` to materialize; default to `--json` stdout in sandbox rather than writing inside read-only sessions.
- **Canonical Style Slugs:** Pass `--style hi-tech` (compiler normalizes `hitech` alias) and pair with one of the 6 `SpatialArchetype` CLI slugs.
- **No Unverified SVG Paths:** Copy verified `24x24` paths or mark `npx svgo` optimization explicitly.

## Output
- Complete **8-Section `DESIGN.md` Blueprint** and compiled `UIExecutionDAG` JSON.

## User Communication
Present architectural choices, ergonomic dial tables, verified icon plans, and DAG phases to the user in **Portuguese (`pt-BR`)**, keeping `DESIGN.md` tokens and DAG schemas in Technical English.
