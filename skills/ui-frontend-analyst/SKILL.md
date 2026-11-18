---
name: ui-frontend-analyst
description: "Use when auditing existing frontend apps via DevTools (CSS Overview, INP/LCP, scrollWidth clip), AST inventory, REA bundles, modern-web-guidance, and 12-vector Anti-Slop (Unicode glyphs, <40px targets, >600L splits), emitting a 7-section CLAREZA diagram. Do NOT use for planning brand systems, writing code, or backend-only audits."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv) and Chrome DevTools"
metadata:
  author: shredded-shape
  version: "1.5.0"
  updated_at: "2026-11-18"
  category: frontend-audit
  tags:
    - chrome-devtools
    - ai-slop
    - css-overview
    - inp
    - modern-web-guidance
    - navigation-clareza
---

# UI Frontend Forensic & Anti-AI-Slop Analyst (`ui-frontend-analyst`)

## Overview
Perform a **strictly read-only** Stage 0 forensic audit before any redesign or refactor. Expose color/typography/icon debt, >600-line monoliths, Chrome DevTools INP/LCP regressions, and concrete **12-Vector AI Slop** artifacts, emitting a structured **7-Section CLAREZA** report.

## Inputs
- Target source path, component folder, single HTML file, live URL, or compiled JS bundle.
- Optional Chrome DevTools target ID or `.context/spec.md` constraints.

## Procedure (4-Step Read-Only `CoT` Trace)
Execute strictly in causal Chain-of-Thought (`CoT`) order without mutating target files (load only the 1–2 `references/*.md` files needed):

1. **Phase 1 (`[CoT-1]`) — Target Classification & Static Inventory:**
   - Run the deterministic AST/Slop scanner:
     - Plugin path (`pwsh`/POSIX): `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py" <target> --json` (or `"%USERPROFILE%\.gemini\..."` in `cmd.exe`)
     - Repo fallback: `uv run python skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py <target> --json`
   - If `@xyflow/react` or live telemetry appears, chain `complex-zero` (`complex_zero_ast_auditor.py <target> --json`, halting at `[3. OBSERVATION]`). If auditing compiled JS/Electron bundles, run `rea` (`analyze_web_bundle` / `inspect_web_page`).
   - Flag any `.py/.js/.ts/.tsx/.html/.css` file exceeding `600` lines for modular decomposition, Unicode/ASCII pseudo-icons (`+`/`×`/`≡`/`▾`/`▸`), and CSS/Tailwind interactive hit targets `< 40px` (always scan project `src/` root excluding `__tests__`).

2. **Phase 2 (`[CoT-2]`) — Modern Web Guidance & 12-Vector Anti-AI-Slop Debt Check:**
   - Activate the installed `modern-web-guidance` plugin skill **first** for HTML/CSS/DOM diagnostics (or fall back to local L3 references if offline in sandbox).
   - Evaluate source findings against the **12-vector checklist** in [`references/taste_anti_slop_and_style_debt.md`](references/taste_anti_slop_and_style_debt.md) and [`rules/audit_criteria.md`](rules/audit_criteria.md).

3. **Phase 3 (`[CoT-3]`) — Live Chrome DevTools & `web.dev` CWV Telemetry Probe:**
   - Load [`references/devtools_webdev_and_modernweb_probe.md`](references/devtools_webdev_and_modernweb_probe.md) alongside `chrome-devtools-plugin` skills (`chrome-devtools`, `a11y-debugging`, `debug-optimize-lcp`, `memory-leak-debugging`).
   - Run [`scripts/devtools_live_probe.js`](scripts/devtools_live_probe.js) via `evaluate_script` and capture DevTools `CSS Overview`, `Issues`, `Performance Monitor`, `routeManifest`, `clippedControlsCount`, `openOverlaysInspected`, INP (`<= 200ms`), and LCP (`<= 2.5s`).

4. **Phase 4 (`[CoT-4]`) — 7-Section CLAREZA Synthesis & Stage 1 Handoff:**
   - Compile the **7-Section CLAREZA** output formatted per [`references/navigation_diagram_and_before_after_patterns.md`](references/navigation_diagram_and_before_after_patterns.md), including valid `As-Is` and `To-Be` Mermaid flows and recommended `(style_archetype, spatial_archetype)` inputs for `ui-brand-ux-planner`.
   - For backend/repo parity beyond DOM scope, recommend `system-project-auditor` rather than modifying code here.

## Gotchas
- **Hex & `color-mix(in oklch)` Traps:** Saturated hex accents like `#00ffff` emit neon luminance; `color-mix(in oklch)` can produce Chromium gamut-arc shifts compared to `color-mix(in oklab)`.
- **Body `optimizeLegibility` INP Penalty:** Mandate `text-rendering: auto` on `body` text and reserve `optimizeLegibility` for `h1, h2, h3`.
- **No Unpinned `npx @latest`:** Invoke the locally installed `modern-web-guidance` skill or fall back to bundled L3 references offline.

## Output
- Machine-readable `FrontendInventoryReport` JSON (`verdict`, `ai_slop_score`, `spacing_and_style_defects`, `imported_icon_libs`, `before_after_proposals`, `font_families`).
- Human-readable **7-Section CLAREZA** forensic audit ready for `ui-brand-ux-planner`.

## User Communication
Keep internal scripts and schemas in Technical English; deliver the **7-Section CLAREZA** summary, friction tables, and Mermaid proposals directly to the user in **Portuguese (`pt-BR`)**.
