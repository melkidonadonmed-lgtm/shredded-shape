---
name: complex-zero
description: "Use when auditing dense frontend apps via ReAct CDP DevTools and AST for @xyflow/react infinite canvas, 150ms WebSocket/chokidar telemetry, ghost nodes, fake stubs, and Next.js 15+ async params without violating hook order or typography rules. Do NOT use for simple pages or backend-only APIs."
license: MIT
compatibility: "Antigravity 2.0, Chrome DevTools MCP, Python 3.12+ (uv), React 19, Next.js 15+"
metadata:
  author: "shredded-shape"
  version: "1.4.0"
  updated_at: "2026-11-17"
  category: "domain-ui-pack"
  tags:
    - complex-zero
    - xyflow
    - react-flow
    - nextjs-15
    - async-params
    - websocket-batch
    - chokidar
    - cdp-devtools
    - ghost-nodes
---

# `complex-zero` — ReAct/CDP, `@xyflow/react` & Anti-Fake AST Auditor

## Overview
Empirical auditor pairing Chrome DevTools MCP (`chrome-devtools-plugin`: `take_screenshot`, `take_snapshot`, `evaluate_script`) with static AST checks ([`scripts/complex_zero_ast_auditor.py`](scripts/complex_zero_ast_auditor.py), [`scripts/visual_hierarchy_and_cdp_probe.py`](scripts/visual_hierarchy_and_cdp_probe.py), bridged to `SGA`/`TIF` in `system-project-auditor`) for dense UIs: `@xyflow/react`, `150ms` `WebSocket` + `chokidar` telemetry, and Next.js 15+ async `params`.

- **When NOT to Use:** Exclude simple static pages (`ui-clean-worker`), standalone `DESIGN.md` authoring (`ui-brand-ux-planner`), 3D physics (`adk-go-mcp-router` `MATH_PHYSICS_3D`), or UI-less backend servers (`system-project-auditor`).

## Inputs
- **`target_path` (required) & `live_url` (recommended):** Target path (`.tsx`, `.ts`, `.css`, `.html`, `mcp_apps_ui_*.go`) and live server URL (`http://localhost:3000`).
- **Stage Role Guard & Pre-Flight:** Operate strictly **read-only** when bound inside `ui-analyst`, `ui-planner`, or `ui-judge`; write fixes only inside `ui-worker`. Load only needed `references/*.md` files. Consult `google-developer-knowledge`, `gemini_get_doc`, and `system-project-auditor` only when `target_path` uses `WebSocket`, `@google/genai`, or JSON-RPC 2.0.

## Procedure
See [`references/axes_and_cdp_cycle.md`](references/axes_and_cdp_cycle.md), [`references/cdp_playwright_probe_patterns.md`](references/cdp_playwright_probe_patterns.md), [`references/ast_ghost_node_integrity_patterns.md`](references/ast_ghost_node_integrity_patterns.md), and [`references/xyflow_node_and_ws_batch_patterns.md`](references/xyflow_node_and_ws_batch_patterns.md):

1. **`[1. THOUGHT]` (Read-Only):** Map domain tabs, nav slots, and graph nodes (`<= 6` tabs, `<= 3` `<nav>` landmarks); flag files `> 600` lines.
2. **`[2. ACTION]` (Read-Only):** Run positional `<target>` or `--target "<target_path>" [--live-url "<url>"] --json` (`--dump-cdp-script`):
   - Plugin path: `python "$HOME/.gemini/config/plugins/shredded-shape/skills/complex-zero/scripts/complex_zero_ast_auditor.py" "<target_path>" [--live-url "<url>"] --json`
   - Fallback: `uv run python skills/complex-zero/scripts/complex_zero_ast_auditor.py "<target_path>" [--live-url "<url>"] --json`
   In Chrome DevTools MCP, run `navigate_page` -> `take_screenshot` -> `take_snapshot` -> `evaluate_script` (`CSS Overview`, `Issues`, `Performance Monitor`).
3. **`[3. OBSERVATION]` (Read-Only):** Cross-check screenshot against probe JSON (`hierarchyMonotonic`, `crampedMenus`, duplicate tabs, exact W3C `2.4` gamma luminance, `text-rendering: auto` body typography) and AST checks (confined Ghost Nodes, `createContext` exemption, `{}` handlers, `setTimeout` stubs, legacy `reactflow`, sync `params.slug`).
4. **`[4. SELF-CORRECTION]` (`ui-worker` Only):** Fix cramped menus (`>= 13px`, `gap >= 0.5rem` / `8px`, `min-block-size >= 44px` including compact `::before` swatches & `input[type="range"]`), scope `:focus-visible` to interactive controls (suppress `<main tabindex="-1">` box outlines & add `<link rel="icon" type="image/svg+xml">`), apply `OKLCH 60-30-10` + 3-layer shadows + `@container`, batch `WebSocket` at `150ms` (`BATCH_UPDATE`), migrate Next.js 15+ routes to `Promise<...>` (`await params`), sanitize streamed HTML with `DOMPurify.sanitize()`, and verify `total_score >= 90/100`.

## Gotchas
- **Confined Ghost Node Imports & Valid Context:** Resolve local imports strictly inside `target_root` and exempt React `createContext()` providers without props.
- **Exact `2.4` Gamma & Body Typography:** Never approximate sRGB gamma as `2.2`, and keep `text-rendering: auto` on dense logs/nodes (heading-only `optimizeLegibility`).
- **Stop Criteria:** Stop with `[UNVERIFIED]` if `target_path` is missing or `live_url` is unreachable.

## Output
Emit `Target | URL | Complex-Zero Score [XX/100] | SGA [XX.XX/100]` across 4 Axes (`25 pts` each, `[PASS] >= 90`, `[WARN] >= 75`, `[FAIL] < 75`) per [`rules/audit_criteria.md`](rules/audit_criteria.md) with `file:line` fixes and clean SVG/anti-slop checks.

## User Communication
Keep schemas and TypeScript node diagnostics in Technical English; formulate all direct user-facing conversation, explanations, status reports, and deliverables in **Portuguese (`pt-BR`)**.
