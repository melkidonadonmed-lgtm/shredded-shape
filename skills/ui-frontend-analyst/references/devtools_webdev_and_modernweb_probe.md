# DevTools Live Probe, `web.dev` CWV & `modern-web-guidance` Baseline

## 1. Live Chrome DevTools MCP Workflow

When auditing a running frontend (`http://localhost:*` or staging URL), collect empirical DOM evidence in 4 steps:
1. **`navigate_page`** to the target URL (`1440x900` desktop first, then `390x844` mobile emulation via `emulate`).
2. **`take_screenshot`** and **`take_snapshot`** to inspect real visual hierarchy, clipped controls, and Accessibility Tree (`role`, `name`, `aria-current`).
3. **`evaluate_script`** running the function inside `scripts/devtools_live_probe.js` to return JSON telemetry:
   - `horizontalOverflow`: `document.documentElement.scrollWidth > window.innerWidth`
   - `crampedMenuItems`: links/buttons inside `<nav>` with computed `fontSize < 13px` or `gap < 6px`
   - `smallTouchTargets`: visible interactive elements `< 44x44px`
   - `uniqueColorsSample`: distinct `color` and `backgroundColor` computed strings
   - `fontFamilies` & `syntheticFonts`: loaded `document.fonts` faces vs. missing faces
   - `domDepthMax` & `emojiHits`: maximum nesting depth and Unicode emoji count in visible text.
4. **REA Fallback (Compiled/Packaged Apps):** If source code is unavailable and only compiled JS/Electron bundles exist, call `rea` (`analyze_javascript_application` -> `inspect_analysis_view(kind="javascript-routes", detail="summary")`) while keeping raw minified bundles out of context.

## 2. `web.dev` & `modern-web-guidance` Grounding

- Always run `npx.cmd -y modern-web-guidance@latest search "<capability>"` before judging modern HTML/CSS APIs (`popover`, `<dialog>`, `@starting-style`, `light-dark()`, `subgrid`, `@container`).
- Align Core Web Vitals checks against `web.dev` thresholds: **LCP `<= 2.5s`**, **INP `<= 200ms`** (`content-visibility: auto` on long lists), and **CLS `<= 0.1`** (explicit image dimensions, stable choice-card borders).
