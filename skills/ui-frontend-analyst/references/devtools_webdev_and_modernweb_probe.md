# Chrome DevTools, Local Plugin Toolkits & `web.dev` CWV Probe

Run Stage 0 live probes after static AST scanning by combining installed local plugins with `scripts/devtools_live_probe.js` (or falling back to bundled L3 checklists when offline in sandbox).

## 1. Installed Local Toolkits (`Command-First`)
1. **`modern-web-guidance` plugin:** Activate **before** inspecting or prescribing HTML/CSS/DOM behavior (`css-layout`, `responsive-design`, `size-aware-styling`, `animate-to-intrinsic-sizes`, `natural-interactions`, `design-token-reactivity`, `soft-edge-content-fade`, `dark-mode`, `color`, `accessibility`). Never run floating `npx @latest`.
2. **`chrome-devtools-plugin` skills:**
   - `chrome-devtools`: Attach via CDP (`list_pages`, `navigate_page`, `evaluate_script`, `take_screenshot`, `list_network_requests`, `list_console_messages`).
   - `a11y-debugging`: Inspect accessibility tree, `:focus-visible` rings, `:user-invalid` feedback, and landmark roles.
   - `debug-optimize-lcp`: Trace LCP resource priority, render-blocking stylesheets, external CDN latency, and TTFB.
   - `memory-leak-debugging`: Capture heap snapshots (`take_heapsnapshot`) across repeated drawer/chapter switches.

## 2. Chrome DevTools Panels & Audit Protocol
| DevTools Panel | Mandatory Evidence to Capture | Red Flag (`[FAIL]`) |
| :--- | :--- | :--- |
| **CSS Overview** | Unique colors, unused declarations, font counts, contrast errors. | Contrast issues `> 0`, `> 3` font families, `#000000` canvas/card colors. |
| **Issues & Console** | CSP blocks, CORS errors on `file://` ESM scripts, `/favicon.ico` 404 or missing fonts/icons, hydration warnings. | `<script type="module">` CORS failure on `file://`, missing `<link rel="icon" type="image/svg+xml">`, or missing WOFF2 assets. |
| **Performance Monitor** | CPU %, JS heap size sawtooth, active DOM nodes (`< 1,500`), Layouts/sec. | Monotonic DOM/heap growth or layout thrashing from `transition: width/height/all`. |
| **Elements / Styles** | Mobile-First postures (`360px`, `680px`, `1280px`), `@container`, `min-inline-size: 0`. | Horizontal page overflow (`scrollWidth > innerWidth`) or missing `:focus-visible`. |
| **Accessibility -> Contrast** | Computed luminosity across every `[data-theme]` Light & Dark preset. | Contrast `< 4.5:1` AA (`< 3.0:1` large) or `< 7.0:1` AAA on clinical routes. |

## 3. `devtools_live_probe.js` Telemetry & `web.dev` Checkpoints
When injected via `evaluate_script`, `devtools_live_probe.js` verifies:
- **`dashedWireframeCount`:** Computed dashed border count (non-`:focus-visible`) must equal `0`.
- **`bodyOptimizeLegibility`:** `getComputedStyle(document.body).textRendering === 'optimizelegibility'` must be `false` (`auto` on `body`, `optimizeLegibility` strictly on `h1..h3`) to protect INP `<= 200ms`.
- **`smallTouchTargetsCount` & `crampedMenus`:** Target height/width `>= 44px` including swatch/icon buttons (`::before` optical dot inside `44x44px` `<button>`) and `input[type="range"]` (`>= 48px` under `any-pointer: coarse`), menu font `>= 13px` (`0.8125rem`), menu `gap >= 8px` (`>= 0.5rem`; probe flags `< 8px`), safe label lookup via `CSS.escape(inp.id)`, and `mainFocusOutline` (`false`) flagging unintended `:focus-visible` outlines painted on `<main tabindex="-1">` on load or click.
- **Route Manifest, Clipped Controls & Overlay Probing:** Capture `interactiveTotal`/`interactiveTruncated`, `pseudoIconControlsCount`, `clippedControlsCount` (`scrollWidth > clientWidth + 1`), `routeManifest`, and `openOverlaysInspected` across modals/drawers (`dialog[open]`, `[popover]:popover-open`).
- **Baseline Platform & Core Web Vitals:** Flag horizontal overflow (`scrollWidth > innerWidth`), missing `content-visibility: auto` on off-screen panels, missing `scroll-padding-top` for anchor links, and obsolete JS animation wrappers where `0fr -> 1fr`, `@starting-style`, `transition-behavior: allow-discrete`, and native `<dialog>`/`popover="auto"` work natively.
