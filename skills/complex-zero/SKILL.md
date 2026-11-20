---
name: complex-zero
description: "Use when auditing or refactoring @xyflow/react infinite canvases, Dagre layout, 150ms WebSocket/chokidar telemetry, ghost nodes, fake stubs, and Next.js 15+ async params via ReAct CDP and AST without violating hook order or typography rules. Do NOT use for general landing/CRUD audits (ui-frontend-analyst), simple pages, or backend-only APIs."
license: MIT
compatibility: "Antigravity 2.0, Chrome DevTools MCP, Python 3.12+ (uv), React 19, Next.js 15+"
allowed-tools: "read_file run_command"
metadata:
  author: "shredded-shape"
  version: "1.6.0"
  updated_at: "2026-11-19"
  category: "domain-ui-pack"
  tags: "complex-zero, xyflow, react-flow, nextjs-15, async-params, websocket-batch, chokidar, cdp-devtools, ghost-nodes, dagre-layout, camera-sync, fitview"
---

# `complex-zero` — ReAct/CDP, `@xyflow/react` & Anti-Fake AST Auditor

## Overview
Empirical auditor pairing Chrome DevTools MCP (`take_screenshot`, `take_snapshot`, `evaluate_script`) with AST checks ([`scripts/complex_zero_ast_auditor.py`](scripts/complex_zero_ast_auditor.py), [`scripts/visual_hierarchy_and_cdp_probe.py`](scripts/visual_hierarchy_and_cdp_probe.py), bridged to `SGA`/`TIF` in `system-project-auditor`) for `@xyflow/react`, `150ms` `WebSocket`+`chokidar`, and Next.js 15+ async `params`.

- **When NOT to Use:** Static pages (`ui-clean-worker`), `DESIGN.md` planning (`ui-brand-ux-planner`), 3D physics (`adk-go-mcp-router`), or UI-less backends (`system-project-auditor`).

## Inputs
- **`target_path` (required) & `live_url`:** `.tsx`/`.ts`/`.css`/`.html` or `mcp_apps_ui_*.go` plus live URL (`http://localhost:3000`).
- **Zero-Trust Stage Role Guardrail:** Strictly **read-only** in `ui-analyst`, `ui-planner`, and `ui-judge`; fixes apply only inside `ui-worker`. Consult `google-developer-knowledge` only for `WebSocket`/`@google/genai`/JSON-RPC 2.0 targets.

## Procedure
Consult only needed L3 files: [`references/cdp_ast_and_axes_guide.md`](references/cdp_ast_and_axes_guide.md), [`references/xyflow_node_and_ws_batch_patterns.md`](references/xyflow_node_and_ws_batch_patterns.md), and [`references/xyflow_dagre_layout_and_camera_sync.md`](references/xyflow_dagre_layout_and_camera_sync.md):

1. **`[1. THOUGHT]` (Read-Only):** Map domain tabs, `<nav>` slots (`<= 6` tabs, `<= 3` navs), and modules `> 600` lines.
2. **`[2. ACTION]` (Read-Only):** Run AST + CDP (`"uv run $HOME/.gemini/config/plugins/shredded-shape/skills/complex-zero/scripts/complex_zero_ast_auditor.py"` or `uv run python skills/complex-zero/scripts/complex_zero_ast_auditor.py "<target>" [--live-url "<url>"] --json`), plus Chrome DevTools (`navigate_page -> take_screenshot -> take_snapshot -> evaluate_script`).
3. **`[3. OBSERVATION]` (Read-Only Terminal Bound for `ui-analyst`/`ui-planner`/`ui-judge`):** Check `hierarchyMonotonic`, `crampedMenus`, 2.4 gamma, `text-rendering: auto`, Ghost Nodes, `createContext`, stubs, legacy `reactflow`, unhoisted `nodeTypes`, unnormalized `path.relative()`, per-sink XSS, and sync `params.slug`.
4. **`[4. SELF-CORRECTION]` (`ui-worker` Only):** Fix nav (`>= 13px`, `gap >= 8px`, `>= 44px`), rail tooltips, `OKLCH 60-30-10`, Dagre `TB`/`LR` + `setCenter` + hoisted `nodeTypes`, `150ms` WS + `/` normalization, `await params`, `DOMPurify.sanitize()`, and verify `>= 90/100`.

## Gotchas
- **Confined Ghost Node Resolution:** Resolve local imports inside `target_root` and exempt React `createContext()` providers without props.
- **Exact `2.4` Gamma & Body Typography:** Never approximate sRGB gamma as `2.2`, and keep `text-rendering: auto` on dense logs/nodes.
- **Fail-Closed Stop Criteria:** Return `[UNVERIFIED]` if `target_path` is missing or `live_url` is unreachable.

## Output
Emit `Read-After-Write`-verified `Target | URL | Complex-Zero Score [XX/100] | SGA [XX.XX/100]` across 4 Axes (`25 pts` each; `[PASS] >= 90`, `[WARN] >= 75`, `[FAIL] < 75`) per [`rules/audit_criteria.md`](rules/audit_criteria.md) with `file:line` Self-Refine fixes.

## User Communication
Keep schemas and TypeScript node diagnostics in Technical English; formulate all direct user-facing conversation, explanations, status reports, and deliverables in **Portuguese (`pt-BR`)**.
