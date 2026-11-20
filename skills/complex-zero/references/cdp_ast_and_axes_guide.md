# 4 Axes, ReAct CDP Telemetry & Anti-Fake AST Guide — `complex-zero`

Consolidated L3 reference pairing `complex_zero_ast_auditor.py`, `visual_hierarchy_and_cdp_probe.py`, and `chrome-devtools` MCP (`xyflow_node_and_ws_batch_patterns.md` + `xyflow_dagre_layout_and_camera_sync.md` cover graph/WS patterns).

## 1. 5 Blocked Failures & Scoring Matrix (`25 pts`/Axis, `>= 90 [PASS]`)
1. **Real Chrome DevTools (Zero Pseudo-ReAct):** Run `navigate_page` -> `take_screenshot` -> `take_snapshot` -> `evaluate_script` (`CSS Overview`, `Issues`, `Performance Monitor`) whenever `live_url` is served.
2. **Navigation & Tab Cohesion:** Keep `<nav>` `<= 3`, primary tabs `<= 6`, simultaneous text inputs `<= 3`, zero nested sub-tabs or plumbing tabs (`sql_raw`, `redis_keys`).
3. **Monotonic Hierarchy & Ergonomics:** Enforce $H_1 > H_2 > H_3 \ge \text{Body} \ge 14\text{px} > \text{Caption} \ge 12\text{px}$; menu `font-size >= 13px`, `gap >= 8px`, `44/48px` targets (`<40px` blocker), zero `scrollWidth > clientWidth`.
4. **Confined Ghost Node & Anti-Fake AST:** Resolve `@/` and relative imports strictly inside `target_root` (exempt React `createContext()` providers; track legacy `forwardRef`); audit linked local CSS/JS on single `.html` entrypoints via `_ss_core.collect_ui_files(target)`.
5. **Next.js 15+ & Real State:** Ban `() => {}` stubs, `Math.random()` metrics, hardcoded `'[PASS]'` badges (`<= 2` node badges), empty `catch {}`, raw `dangerouslySetInnerHTML` or dynamic JS code execution, conditional hooks, unhoisted `nodeTypes`, raw Windows `path.relative()`, files `> 600`L (`<= 60`L/fn), and sync `params.slug`.

| Axis | Deterministic Criteria | Primary Penalty |
| :--- | :--- | :--- |
| **1. Interactivity, Fitts & INP (`25 pts`)** | Native controls, `:focus-visible`, `44/48px` targets (`<40px` blocker), `prefers-reduced-motion`, standalone `allow-discrete`, menus `>= 13px`/`gap >= 8px`. | `-15 pts` cramped menu; `-10 pts` missing `:focus-visible`. |
| **2. Cohesion, Hierarchy & `OKLCH` (`25 pts`)** | `<= 3 <nav>`, `<= 6` primary tabs, monotonic headings, `@container`, `oklch()` (`C <= 0.20`, cap `0.22`), 3-layer shadows. | `-15 pts` tab sprawl or flat hierarchy. |
| **3. Real-State Graph & Anti-Fake (`25 pts`)** | Zero stubs/`Math.random()`/Ghost Nodes, hoisted `nodeTypes`, `150ms` WS batching + `/` normalization, `DOMPurify.sanitize()`, `<= 2` badges/node. | `-15 pts` per stub, Ghost Node, or XSS sink. |
| **4. DevTools Probe & Next.js 15+ (`25 pts`)** | `<title>`, `<meta name="viewport">`, `evaluate_script` telemetry, `Promise<...>` async `params`, App Router `(group)/` + `_components/`. | `-15 pts` DOM check failure or sync `params`. |

## 2. Exact W3C WCAG 2.2 Luminance (`2.4` Gamma) & CDP Cycle
Linearize 8-bit sRGB channels via the piecewise WCAG 2.2 curve (never approximate as `c ** 2.2`):
```javascript
export const channelToLinear = (srgb) => {
  const c = srgb / 255;
  return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
};
export const relativeLuminance = (r, g, b) =>
  0.2126 * channelToLinear(r) + 0.7152 * channelToLinear(g) + 0.0722 * channelToLinear(b);
```
- **Attach & Inspect:** `navigate_page` + `list_console_messages` + `Issues` (zero hydration/CORS/CSP failures).
- **Heap & Typography (`<= 200ms` INP):** Hold `< 1,500` DOM nodes, flat post-GC heap sawtooth, layout recalcs `< 15/s`, `text-rendering: auto` on `body`/nodes (`optimizeLegibility` on `h1..h3` only), and `hierarchyMonotonic: true`.
- **Posture Matrix:** Verify `Compact (390px)`, `Medium (680px)`, and `Expanded (1440px)` with crisp `:focus-visible`, zero horizontal overflow, and `DOM == Tab Order`.
