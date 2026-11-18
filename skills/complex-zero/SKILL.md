---
name: complex-zero
description: "Use when auditing or refactoring dense frontend apps via ReAct CDP DevTools and AST for @xyflow/react infinite canvas, 150ms WebSocket/chokidar telemetry, ghost nodes, fake stubs, and Next.js 15+ async params without violating hook order or typography rules. Do NOT use for simple pages or backend-only APIs."
license: MIT
compatibility: "Antigravity 2.0, Chrome DevTools MCP, Python 3.12+ (uv), React 19, Next.js 15+"
allowed-tools: "read_file run_command"
metadata:
  author: "shredded-shape"
  version: "1.5.1"
  updated_at: "2026-11-18"
  category: "domain-ui-pack"
  tags: "complex-zero, xyflow, react-flow, nextjs-15, async-params, websocket-batch, chokidar, cdp-devtools, ghost-nodes"
---

# `complex-zero` — ReAct/CDP, `@xyflow/react` & Anti-Fake AST Auditor

## Overview
Empirical auditor pairing Chrome DevTools MCP (`take_screenshot`, `take_snapshot`, `evaluate_script`) with AST checks ([`scripts/complex_zero_ast_auditor.py`](scripts/complex_zero_ast_auditor.py), [`scripts/visual_hierarchy_and_cdp_probe.py`](scripts/visual_hierarchy_and_cdp_probe.py), bridged to `SGA`/`TIF` in `system-project-auditor`) for `@xyflow/react`, `150ms` `WebSocket`+`chokidar`, and Next.js 15+ async `params`.

- **When NOT to Use:** Static pages (`ui-clean-worker`), `DESIGN.md` planning (`ui-brand-ux-planner`), 3D physics (`adk-go-mcp-router`), or UI-less backends (`system-project-auditor`).

## Inputs
- **`target_path` (required) & `live_url`:** `.tsx`/`.ts`/`.css`/`.html` or `mcp_apps_ui_*.go` plus live URL (`http://localhost:3000`).
- **Zero-Trust Stage Role Guardrail:** Strictly **read-only** in `ui-analyst`, `ui-planner`, and `ui-judge`; fixes apply only inside `ui-worker`. Consult `google-developer-knowledge` only for `WebSocket`/`@google/genai`/JSON-RPC 2.0 targets.

## Procedure
Consult only needed L3 files: [`references/axes_and_cdp_cycle.md`](references/axes_and_cdp_cycle.md), [`references/cdp_playwright_probe_patterns.md`](references/cdp_playwright_probe_patterns.md), [`references/ast_ghost_node_integrity_patterns.md`](references/ast_ghost_node_integrity_patterns.md), and [`references/xyflow_node_and_ws_batch_patterns.md`](references/xyflow_node_and_ws_batch_patterns.md):

1. **`[1. THOUGHT]` (Read-Only):** Map domain tabs, `<nav>` slots (`<= 6` tabs, `<= 3` navs), and modules `> 600` lines.
2. **`[2. ACTION]` (Read-Only):** Run AST + CDP probe (`--target "<path>" [--live-url "<url>"] --json`):
   - Plugin (`pwsh`/POSIX): `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/complex-zero/scripts/complex_zero_ast_auditor.py" "<target_path>" [--live-url "<url>"] --json`
   - Repo fallback: `uv run python skills/complex-zero/scripts/complex_zero_ast_auditor.py "<target_path>" [--live-url "<url>"] --json`
   In Chrome DevTools MCP, capture `navigate_page` -> `take_screenshot` -> `take_snapshot` -> `evaluate_script` (`CSS Overview`, `Issues`, `Performance Monitor`).
3. **`[3. OBSERVATION]` (Read-Only Terminal Bound for `ui-analyst`/`ui-planner`/`ui-judge`):** Cross-check `hierarchyMonotonic`, `crampedMenus`, exact W3C `2.4` gamma contrast, `text-rendering: auto` body typography, confined Ghost Nodes, `createContext` exemptions, `{}`/`setTimeout` stubs, legacy `reactflow`, and sync `params.slug`.
4. **`[4. SELF-CORRECTION]` (`ui-worker` Only + Read-After-Write Checklist):** Fix cramped nav (`>= 13px`, `gap >= 8px`, `>= 44px` hit-boxes), interactive-scoped `:focus-visible`, SVG favicon, `OKLCH 60-30-10`, `150ms` `BATCH_UPDATE`, `await params`, `DOMPurify.sanitize()`, and verify `total_score >= 90/100`.

## Gotchas
- **Confined Ghost Node Resolution:** Resolve local imports inside `target_root` and exempt React `createContext()` providers without props.
- **Exact `2.4` Gamma & Body Typography:** Never approximate sRGB gamma as `2.2`, and keep `text-rendering: auto` on dense logs/nodes.
- **Fail-Closed Stop Criteria:** Return `[UNVERIFIED]` if `target_path` is missing or `live_url` is unreachable.

## Output
Emit `Target | URL | Complex-Zero Score [XX/100] | SGA [XX.XX/100]` across 4 Axes (`25 pts` each; `[PASS] >= 90`, `[WARN] >= 75`, `[FAIL] < 75`) per [`rules/audit_criteria.md`](rules/audit_criteria.md) with `file:line` fixes and clean SVG checks.

## User Communication
Keep schemas and TypeScript node diagnostics in Technical English; formulate all direct user-facing conversation, explanations, status reports, and deliverables in **Portuguese (`pt-BR`)**.
