---
name: ui-brand-ux-planner
description: "Use when diagnosing product scope, brand identity, OKLCH 60-30-10 palette, style archetype (Soft, Hi-Tech, Tactile, Elevated, Retro, Vintage, Clinical), external Stitch/Figma/Fonts/3D assets, DESIGN.md, and bounded UI DAGs (<=5 rules/node). Do NOT use for live DevTools audits or writing code."
compatibility: "Antigravity 2.0, Figma MCP, agent-browser, Python 3.12+"
metadata:
  author: "Shredded-Shape"
  version: "1.0.0"
  updated_at: "2026-11-16"
  category: "Brand Direction, UX Architecture, Asset Orchestration & DAG Planning"
  tags: ["ui-brand-ux-planner", "design-md", "branding", "oklch", "stitch", "figma", "google-fonts", "threejs", "unity", "soft", "hi-tech", "tactile", "elevated", "retro", "vintage", "dag-planejador"]
---

# `ui-brand-ux-planner` — Brand, Style Archetypes, Asset Pipeline & DAG Planner

## 1. Overview & Scope

Translates product scope (or `ui-frontend-analyst` findings) into a cohesive brand identity, intuitive zero-verbiage UX hierarchy, `<project_root>/DESIGN.md`, and a closed-schema execution DAG (`ui_execution_dag.json` with `<= 5` rules/node, CoT/ToT, and zero parallel file collisions).

- **When NOT to Use:** Do NOT use for inspecting live existing apps (`ui-frontend-analyst`), editing `.tsx`/`.css` files (`ui-clean-worker`), running final WCAG 2.2 Judge audits (`ui-quality-judge`), or backend API specs.

## 2. Inputs & Prerequisites

- **`project_brief_or_root` (required) & `analyst_report` (optional):** Product purpose, audience, stack preference, or existing repo root.
- **Compiler & References:**
  - [scripts/ui_dag_compiler.py](scripts/ui_dag_compiler.py) (`--scope <path> --style <archetype> --json`)
  - [references/style_archetypes_tokens_and_menus.md](references/style_archetypes_tokens_and_menus.md)
  - [references/external_assets_stitch_figma_fonts_3d.md](references/external_assets_stitch_figma_fonts_3d.md)
  - [references/intuitive_ux_rsc_and_agentic_ui.md](references/intuitive_ux_rsc_and_agentic_ui.md)

## 3. Step-by-Step Procedure

1. **Brand, Objective & `OKLCH 60-30-10`:** Calibrate hue ($H$) and restrained chroma ($C \le 0.20$, zero neon) to domain purpose, locking `light-dark()` pairs (`L = 0.16 -> 0.22 -> 0.27` dark elevation).
2. **Select Token & Menu Style Archetype:** Pick `soft`, `hi-tech`, `tactile`, `elevated`, `retro`, `vintage`, or `clinical` plus `taste-skill` dials (`DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY`).
3. **Orchestrate External Assets & Tools:** Source palettes/concepts via **Google Stitch** (`agent-browser`), extract clean SVG icons/tokens via **Figma MCP**, download **Google Fonts** (`.woff2` variable Sans + Mono), and configure **3D (`Three.js` / `Unity Hub`)** only when requested by scope.
4. **Intuitive Navigation & Stack Architecture:** Structure Single-DOM Adaptive Navigation (Bottom Bar <-> Collapsible `256px` Sidebar Rail), Next.js 15+ Server vs. Leaf `'use client'` boundaries, Tailwind v4 `@theme`, and ban tutorial text explaining obvious controls.
5. **Compile `DESIGN.md` & Bounded DAG:** Run `ui_dag_compiler.py` (`<= 5` rules/node, ToT/CoT, `fallback_branch`, vertical route ownership) before dispatching `ui-clean-worker`.

## 4. Gotchas & Edge Cases

- **Read-Only Planning Reservation:** Reserve cognitive budget for architecture, tokens, and DAG compilation — never write production `.tsx`/`.css` components directly.
- **Zero-Verbiage Discipline:** Never pad dashboards with explanatory cards describing how to click buttons; let layout hierarchy guide action.
- **Stop Criteria:** Emit `[UNVERIFIED]` if product scope is empty or requested external asset source is unreachable.

## 5. Output Schema & Validation Criteria

Deliver `<project_root>/DESIGN.md` plus validated `ui_execution_dag.json` (`extra="forbid"`, `max_rules_per_node <= 5`, zero file collisions) complying with [rules/audit_criteria.md](rules/audit_criteria.md).

## 6. User Communication Rule

Always formulate all direct user-facing conversation, style recommendations, asset summaries, and deliverables in **Portuguese (Brazil / `pt-BR`)**, unless the user explicitly requests otherwise.
