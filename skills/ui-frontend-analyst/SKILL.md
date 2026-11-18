---
name: ui-frontend-analyst
description: "Use when auditing existing frontend apps via DevTools (CSS Overview, INP/LCP, scrollWidth clip), AST inventory, REA bundles, modern-web-guidance, and 12-vector Anti-Slop (Unicode glyphs, <40px targets, >600L splits), emitting a 7-section CLAREZA diagram. Do NOT use for planning brand systems, writing code, or backend-only audits."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv) and Chrome DevTools"
allowed-tools: "read_file run_command"
metadata:
  author: "shredded-shape"
  version: "1.5.1"
  updated_at: "2026-11-18"
  category: "frontend-audit"
  tags: "chrome-devtools, ai-slop, css-overview, inp, modern-web-guidance, navigation-clareza"
---

# UI Frontend Forensic & Anti-AI-Slop Analyst (`ui-frontend-analyst`)

## Overview
Strictly **read-only** Stage 0 forensic auditor. Expose color, typography, SVG, `>600`-line monolith, Chrome DevTools INP/LCP regressions, and **12-Vector AI Slop** defects, emitting `FrontendInventoryReport` JSON + **7-Section CLAREZA** output.

## Inputs
- Target `src/` root, component directory, HTML file, live URL, or compiled JS bundle.
- Optional Chrome DevTools target ID or `.context/spec.md` constraints.

## Procedure (4-Step Read-Only `CoT` Trace)
Execute in Chain-of-Thought order under **Zero-Trust Read-Only Guardrails** (zero target mutations; load only 1–2 `references/*.md` files):

1. **Phase 1 (`[CoT-1]`) — Target Classification & Static Inventory:**
   - Run the AST/Slop scanner (`src/` root automatically excludes `__tests__/`):
     - Plugin (`pwsh`/POSIX): `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py" <target> --json`
     - Repo fallback: `uv run python skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py <target> --json`
   - Chain `complex-zero` (`complex_zero_ast_auditor.py`, halt at `[3. OBSERVATION]`) for `@xyflow/react`/live telemetry, or `rea` (`analyze_web_bundle`) for compiled bundles.
   - Flag `>600`-line files, Unicode/ASCII pseudo-icons (`+`/`×`/`≡`/`▾`), and hit targets `< 40px`.

2. **Phase 2 (`[CoT-2]`) — Modern Web Guidance & 12-Vector Anti-Slop Checklist:**
   - Activate `modern-web-guidance` **first** for HTML/CSS/DOM diagnostics (or L3 references offline).
   - Score findings against [`references/taste_anti_slop_and_style_debt.md`](references/taste_anti_slop_and_style_debt.md) and [`rules/audit_criteria.md`](rules/audit_criteria.md).

3. **Phase 3 (`[CoT-3]`) — Live Chrome DevTools & `web.dev` CWV Probe:**
   - Pair [`references/devtools_webdev_and_modernweb_probe.md`](references/devtools_webdev_and_modernweb_probe.md) with `chrome-devtools-plugin` (`chrome-devtools`, `a11y-debugging`, `debug-optimize-lcp`, `memory-leak-debugging`).
   - Run [`scripts/devtools_live_probe.js`](scripts/devtools_live_probe.js) via `evaluate_script` (`CSS Overview`, `Issues`, `routeManifest`, `clippedControlsCount`, `openOverlaysInspected`, INP `<= 200ms`, LCP `<= 2.5s`).

4. **Phase 4 (`[CoT-4]`) — 7-Section CLAREZA Synthesis & Stage 1 Handoff:**
   - Emit the **7-Section CLAREZA** report per [`references/navigation_diagram_and_before_after_patterns.md`](references/navigation_diagram_and_before_after_patterns.md) (`As-Is`/`To-Be` Mermaid + `(style_archetype, spatial_archetype)` for `ui-brand-ux-planner`); defer backend parity to `system-project-auditor`.

## Gotchas
- **Hex & `color-mix(in oklch)` Traps:** Saturated `#hex` triggers neon luminescence; `color-mix(in oklch)` risks Chromium gamut-arc shifts vs `color-mix(in oklab)`.
- **Body `optimizeLegibility` INP Penalty:** Mandate `text-rendering: auto` on `body` text; reserve `optimizeLegibility` for `h1, h2, h3`.
- **No Unpinned `npx @latest`:** Use local `modern-web-guidance` or bundled L3 fallbacks offline.

## Output
- `FrontendInventoryReport` JSON (`verdict`, `ai_slop_score`, `spacing_and_style_defects`, `imported_icon_libs`, `before_after_proposals`, `font_families`).
- **7-Section CLAREZA** forensic audit for `ui-brand-ux-planner`.

## User Communication
Keep internal scripts and schemas in Technical English; deliver the **7-Section CLAREZA** summary, friction tables, and Mermaid proposals directly to the user in **Portuguese (`pt-BR`)**.
