---
name: ui-frontend-analyst
description: "Use when auditing existing frontend apps via DevTools (CSS Overview, INP/LCP, scrollWidth clip), AST inventory, REA bundles, modern-web-guidance, and 12-vector Anti-Slop (Unicode glyphs, 44/48px targets / <40px blocker, >600L splits), emitting a 7-section CLAREZA diagram. Do NOT use for planning brand systems, writing code, or backend-only audits."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv) and Chrome DevTools"
allowed-tools: "read_file run_command"
metadata:
  author: "shredded-shape"
  version: "1.6.0"
  updated_at: "2026-11-19"
  category: "frontend-audit"
  tags: "chrome-devtools, ai-slop, css-overview, inp, modern-web-guidance, navigation-clareza, intent-first, scoped-probe"
---

# UI Frontend Forensic & Anti-AI-Slop Analyst (`ui-frontend-analyst`)

## Overview
Strictly **read-only** Stage 0 forensic auditor. Execute **headless-safe Intent-First** audits (`pre-plan`, `planner-directed`, or `plan-brief`) exposing root/stack drift, color/polarity, typography, SVG, menu lengths, canvas UX, AppSec (`AUDIT-SEC-ENV-LEAK`/`AUDIT-SEC-01`), `>600`-line monoliths, Chrome DevTools INP/LCP, and **Anti-AI-Slop** defects, emitting `FrontendInventoryReport` JSON + **7-Section CLAREZA**.

## Inputs
- Target `src/` root, component directory, HTML file, live URL, or compiled JS bundle + user intent/complaint (or `ScopedAuditRequest` from `ui-planner`).
- Optional Chrome DevTools target ID or `.context/spec.md` constraints.

## Procedure (5-Step Read-Only `CoT-0..4` Trace)
Execute under **Zero-Trust Read-Only Guardrails** (zero mutations; load only 1–2 `references/*.md` files):

1. **Phase 0 (`[CoT-0]`) — Intent-First & Mode Lock:** Capture user complaint, usage mode, and objective vs. real state (`pre-plan`, `planner-directed`, or `plan-brief`); pause only if interactive input lacks both target and goal, and infer `intent: "baseline_forensic_audit"` (`intent_inferred: true`) on concrete targets.
2. **Phase 1 (`[CoT-1]`) — Root Hygiene, Mixed-Stack & AST Inventory:** Run scanner (emits `root_hygiene_warnings` + `menu_label_audit`):
   - `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py" <target> --json` (fallback: `uv run python skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py <target> --json`)
   - Chain `complex-zero` (halt at `[3. OBSERVATION]`) for `@xyflow/react`/Dagre/`ws`, or `rea` (`analyze_web_bundle`) for compiled bundles.
3. **Phase 2 (`[CoT-2]`) — Web Guidance, Anti-Slop & AppSec:** Activate `modern-web-guidance` **first**; audit [`references/taste_anti_slop_and_style_debt.md`](references/taste_anti_slop_and_style_debt.md) and [`rules/audit_criteria.md`](rules/audit_criteria.md) (gradient text, `dense` grids, `<feColorMatrix>` isolation, secret leaks, omissions, `<40px` targets, `>600`L splits).
4. **Phase 3 (`[CoT-3]`) — Live DevTools Probe:** Pair [`references/devtools_webdev_and_modernweb_probe.md`](references/devtools_webdev_and_modernweb_probe.md) with [`scripts/devtools_live_probe.js`](scripts/devtools_live_probe.js) (`CSS Overview`, `Issues`, `wrappedNavItems`, `mysteryIconOnlyNavCount`, `gradientTextCount`, `skipLinkPresent`, INP `<= 200ms`, LCP `<= 2.5s`).
5. **Phase 4 (`[CoT-4]`) — Causal `Friction X -> Impact Y` CLAREZA:** Emit 7-Section CLAREZA per [`references/navigation_diagram_and_before_after_patterns.md`](references/navigation_diagram_and_before_after_patterns.md) (`[OBSERVED FACT]`/`[TECHNICAL INFERENCE]`/`[GAP]`, `As-Is`/`To-Be` Mermaid + `(style, spatial)` for `ui-brand-ux-planner`).

## Gotchas
- **Hex & `color-mix(in oklch)` Traps:** Saturated `#hex` triggers neon luminescence; `color-mix(in oklch)` risks gamut shifts vs `color-mix(in oklab)`.
- **Body `optimizeLegibility` INP Penalty:** Keep `text-rendering: auto` on `body`; reserve `optimizeLegibility` for `h1..h3`.
- **Advisory vs. Blocker Hygiene:** Keep `root_hygiene_warnings` and `menu_label_audit` out of `ai_slop_score`; verify `[file:line]` citations exist on disk.

## Output
- Verifiable `Read-After-Write` `FrontendInventoryReport` JSON (`verdict`, `ai_slop_score`, `root_hygiene_warnings`, `menu_label_audit`, `spacing_and_style_defects`, `before_after_proposals`).
- **7-Section CLAREZA** causal audit (`Self-Refine` ready) for `ui-brand-ux-planner`.

## User Communication
Keep scripts and schemas in Technical English; deliver the **7-Section CLAREZA** summary, causal friction tables, and Mermaid proposals in **Portuguese (`pt-BR`)**.
