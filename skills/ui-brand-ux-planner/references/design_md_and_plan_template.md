# 8-Section `DESIGN.md` Blueprint, DAG Example & Verified `24x24` SVG Catalog

Every Stage 1 plan emits this exact blueprint structure so `ui-worker` materializes `<project_root>/DESIGN.md` deterministically with zero guesswork.

## 1. Mandatory 8-Section `DESIGN.md` Blueprint Contract
1. **Brand, Polarity & Ergonomic Dials:** Brand voice, `site-kind`, Style Archetype (`1` of `7`), Spatial Archetype slug (`1` of `6`), `color-scheme: light dark`, and numeric Dials (`Variance / Motion / Density`).
2. **5-Plane `OKLCH 60-30-10` Color Matrix:** Light & Dark `light-dark()` pairs (`--bg-well`, `--bg-canvas`, `--bg-card`, `--bg-card-lit`, `--bg-key`, `--ink-primary`, `--ink-muted`, `--ink-on-key`, `--brand-primary` `C <= 0.20` hard cap `0.22`, `--danger` `15°..40°` `<= 0.24`, `color-mix(in oklab, ...)`). Zero `#000000`, zero neon hex, zero confetti classes.
3. **Optical Depth, Concentric Radii & Frosted Glass Spec:** Light 3-layer shadows (`-1px..-8px` + neutral `drop-shadow <= 6px`); Dark `well < canvas < card < card-lit` progression + `--light-zenith` + rim hairline; $R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$; `@media (prefers-reduced-transparency: reduce)` solid fallback.
4. **Typography & Material/MDN Scale:** Google Fonts WOFF2 `@font-face` (`font-display: swap`), `font-optical-sizing: auto`, `text-rendering: auto` (`body`) vs `optimizeLegibility` (`h1..h3`), M3 scale (`1.2` / `1.5`), `clamp()`, `65ch`, `tabular-nums`, `font-synthesis: none`.
5. **Single-Library SVG Craft Catalog:** Named library (Lucide / Material Symbols SVG / Phosphor / Fluent), `<symbol>` sprite list, and copied `24x24` geometry below.
6. **Adaptive Chrome, Flexbox/Grid/`@container` & Tailwind v4 `@theme`:** Mobile-First postures (`Compact < 600px`, `Medium 600–839px`, `Expanded >= 840px`), `min-inline-size: 0`, `@container` isolated from `subgrid`, scroll-snap `mask-image` tabs, `0fr -> 1fr`/`<details>`/`popover`, 4 `<article>` Cards, and `>= 44px` (`48px` coarse) targets.
7. **State, Routing & Security Matrix:** Executable 5-state FSM (`idle | loading | empty | error | success`), GPU motion (`allow-discrete` + `@starting-style`), `DOM == Tab Order`, Next.js 15+ `await params`, and `DOMPurify.sanitize()`.
8. **File Split & Anti-Slop Acceptance Gates:** Modules `<= 600` lines (`<= 60` lines/fn), RAW SHA-256 checksums, zero reflow transitions, and `--wcag AA` (or `AAA` clinical) `--composite` pass.

## 2. Canonical `UIExecutionDAG` JSON Example (Disjoint 4-Stage)
```json
{
  "project_name": "app-shell",
  "style_archetype": "tactile",
  "spatial_archetype": "workbench_split_view",
  "execution_mode": "refactor",
  "complexity_tier": "tier_3_fullstack_pwa",
  "brand_oklch_hue": 245,
  "max_self_refine_rounds": 3,
  "nodes": [
    {"step_id": "step_00", "owner_agent": "ui-analyst", "active_rules_count": 4, "read_targets": ["src"], "owned_files": []},
    {"step_id": "step_01", "owner_agent": "ui-planner", "active_rules_count": 4, "read_targets": ["src"], "owned_files": [], "dependencies": ["step_00"]},
    {"step_id": "step_02", "owner_agent": "ui-worker", "active_rules_count": 5, "read_targets": ["DESIGN.md"], "owned_files": ["DESIGN.md", "src/app/globals.css"], "dependencies": ["step_01"]},
    {"step_id": "step_03", "owner_agent": "ui-judge", "active_rules_count": 4, "read_targets": ["src/app/globals.css"], "owned_files": [], "dependencies": ["step_02"]}
  ]
}
```

## 3. Verified `24x24` Lucide SVG Path Catalog (`viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"`)
- **`cloud`:** `<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>`
- **`cloud-upload`:** `<path d="M12 13v8"/><path d="m8 17 4-4 4 4"/><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/>`
- **`trash-2`:** `<path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/>`
- **`search`:** `<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>`
- **`sliders-horizontal`:** `<line x1="21" x2="14" y1="4" y2="4"/><line x1="10" x2="3" y1="4" y2="4"/><line x1="21" x2="12" y1="12" y2="12"/><line x1="8" x2="3" y1="12" y2="12"/><line x1="21" x2="16" y1="20" y2="20"/><line x1="12" x2="3" y1="20" y2="20"/><line x1="14" x2="14" y1="2" y2="6"/><line x1="8" x2="8" y1="10" y2="14"/><line x1="16" x2="16" y1="18" y2="22"/>`
- **`check`:** `<path d="M20 6 9 17l-5-5"/>`
- **`x`:** `<path d="M18 6 6 18"/><path d="m6 6 12 12"/>`
- **`alert-triangle`:** `<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>`
- **`git-branch`:** `<line x1="6" x2="6" y1="3" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>`
- **`layers`:** `<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m2 12 8.58 3.91a2 2 0 0 0 1.66 0L22 12"/><path d="m2 17 8.58 3.91a2 2 0 0 0 1.66 0L22 17"/>`
