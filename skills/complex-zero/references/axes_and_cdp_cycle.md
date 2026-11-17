# The 4 Axes, Menu Governance & ReAct/CDP Cycle — `complex-zero`

Extended reference consumed by `SKILL.md`, paired with [`cdp_playwright_probe_patterns.md`](cdp_playwright_probe_patterns.md), [`ast_ghost_node_integrity_patterns.md`](ast_ghost_node_integrity_patterns.md), [`xyflow_node_and_ws_batch_patterns.md`](xyflow_node_and_ws_batch_patterns.md), and `system-project-auditor`.

## 5 Blocked Structural Failures
1. **No Pseudo-ReAct (Real Chrome DevTools):** Require `navigate_page` -> `take_screenshot` -> `take_snapshot` -> `evaluate_script` (`getComputedStyle`, `getBoundingClientRect`, `CSS Overview`, `Issues`) whenever `live_url` is served.
2. **Navigation & Tab Sprawl Limits:** Keep `<nav>` landmarks `<= 3` per document, primary tabs (`role="tab"` or stacked switchers) `<= 6`, `<= 3` simultaneous text inputs, zero duplicate/backend plumbing tabs (`sql_raw`, `redis_keys`), and zero nested sub-tabs inside tabs. Group large chapter lists into 2 clean `<nav>` groups or collapsible accordions.
3. **Monotonic Visual Hierarchy:** Enforce $H_1 > H_2 > H_3 \ge \text{Body} \ge 14\text{px} > \text{Caption} \ge 12\text{px}$; reject inline micro-font clutter (`<= 13px`).
4. **Legible Menus & Touch Ergonomics:** Reject `<nav>` / menu controls with `font-size < 13px`, `gap < 6px`, `min-block-size < 40px` (`>= 44px` standard, `>= 48px` coarse), or `scrollWidth > clientWidth`.
5. **Anti-Fake AST & Next.js 15+:** Reject Ghost Nodes, `() => {}` handlers, `Math.random()` metrics, hardcoded `'[PASS]'` badges, `> 2` metric badges per graph node, and sync `params.slug`.

## Scoring Matrix (`25 pts` per Axis, `>= 90 [PASS]`)
| Axis | Deterministic Criteria | Primary Penalty |
| :--- | :--- | :--- |
| **1. Interactivity, Fitts, INP & Menus (`25 pts`)** | Native controls, `:focus-visible`, `any-pointer: coarse` `>= 48px`, `prefers-reduced-motion`, standalone `transition-behavior: allow-discrete`, menus `>= 13px`/`gap >= 6px`/`min-block-size >= 44px`. | `-15 pts` cramped menu; `-10 pts` missing `:focus-visible`. |
| **2. Tab Cohesion, Hierarchy & `OKLCH` (`25 pts`)** | `<= 3 <nav>`, `<= 6` primary tabs, monotonic headings, `@container`, `oklch()`, and 3-layer shadows. | `-15 pts` tab/nav sprawl; `-15 pts` flat hierarchy/micro-fonts. |
| **3. Real-State Graph & Anti-Fake AST (`25 pts`)** | Zero stubs/`Math.random()`/`'[PASS]'`; disk-verified nodes, `150ms` WS batching, `<= 2` badges/node. | `-15 pts` per stub, overstuffed node, or Ghost Node. |
| **4. DevTools Probe & Next.js 15+ Routes (`25 pts`)** | `<title>`, `<meta name="viewport">`, `evaluate_script` telemetry, `Promise<...>` async `params`. | `-15 pts` DOM check failure or sync `params` access. |
