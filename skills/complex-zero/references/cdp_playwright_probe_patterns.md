# ReAct CDP Probe, Exact 2.4 sRGB Math & Typography Latency Patterns

Run live verification against dense SPAs and HTML Atlases with `chrome-devtools-plugin` and `visual_hierarchy_and_cdp_probe.py`.

## 1. Exact W3C WCAG 2.2 Relative Luminance (`2.4` Gamma)
Always linearize 8-bit sRGB channels (`0..255 -> 0..1`) via the canonical piecewise WCAG 2.x curve (never approximate as `c ** 2.2`):
```javascript
export function channelToLinear(srgb) {
  const c = srgb / 255;
  return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}
export function relativeLuminance(r, g, b) {
  return 0.2126 * channelToLinear(r) + 0.7152 * channelToLinear(g) + 0.0722 * channelToLinear(b);
}
```

## 2. ReAct CDP Telemetry Cycle (`chrome-devtools` + `Issues` + `Performance Monitor`)
1. **Attach & Capture:** Open target URL (`navigate_page`), inspect `list_console_messages` and `Issues`, and ensure zero hydration, CORS, or CSP failures.
2. **Heap & Layout Recalc Stability:** While streaming WebSocket bursts (`150ms`), watch `Performance Monitor` (`< 1,500` DOM nodes, flat post-GC heap sawtooth, layout recalcs `< 15/s`). Run `memory-leak-debugging` if nodes climb across tab switches.
3. **Typography & INP Check:** Verify computed `text-rendering: auto` on `body` and dense nodes (`h1..h3` only may set `optimizeLegibility`), confirm `--dump-cdp-script` (`CHROME_DEVTOOLS_EVALUATE_SCRIPT`) reports `hierarchyMonotonic: true` and `passed: true`, and hold INP `<= 200ms`.
4. **Posture & Focus Matrix:** Capture screenshots across `Compact (390px)`, `Medium (680px)`, and `Expanded (1440px)` viewports via `take_screenshot`, verifying crisp `:focus-visible` outlines, zero horizontal overflow, and strict `DOM == Tab Order`.
