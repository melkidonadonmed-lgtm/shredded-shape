# Clean Components, Adaptive Postures, Grid/Flex/`@container` & Real FSM

Build resilient UI modules (`<= 600` lines/file, `<= 60` lines/function) using Mobile-First Single-DOM layouts, GPU transitions, verified vectors, and executable FSM states.

## 1. Macro Shell & Next.js App Router Boundaries
- Keep persistent chrome (`<header>`, `<nav>`, `<aside>`) inside `app/layout.tsx` and stream child views through `loading.tsx` skeletons; reserve `'use client'` strictly for interactive leaves.
- Anchor deep-linked headings cleanly below sticky headers via `html { scroll-padding-top: 4.5rem; scroll-behavior: smooth; }`.
- Unwrap dynamic parameters in Server/Client components with async safety (`const { id } = await params;` or React 19 `use(params)`), pass `ref` directly as a prop (zero `forwardRef`), and sanitize dynamic HTML with `DOMPurify.sanitize()`.

## 2. Mobile-First Adaptive Postures & Single-DOM Navigation
Render **one** DOM navigation tree that adapts cleanly across 3 canonical viewport postures without horizontal overflow (`min-inline-size: 0` on Grid/Flex children):
- **`Compact (< 600px)`:** Single-column stack + bottom action bar respecting `padding-block-end: env(safe-area-inset-bottom)` and native `<dialog>` / `[popover]` sheets (`min-block-size: 48px`).
- **`Medium (600px–839px)`:** Vertical 64px–72px Navigation Rail on inline-start + scrollable content pane (`content-visibility: auto`).
- **`Expanded (>= 840px)`:** Collapsible Sidebar (`248px–264px <-> 64px–72px`, translated via `grid-template-columns` or transform drawer without layout thrashing) + Supporting Detail Pane.

```css
@layer tokens, reset, layout, components, styles, utilities, motion;

@layer layout {
  .app-shell { display: grid; grid-template-columns: minmax(0, 1fr); min-block-size: 100dvh; }
  .chapter-view:not([hidden]) { display: flex; flex-direction: column; gap: 1.5rem; } /* Explicit gap; avoid content-visibility: auto on shadow cards */
  .side-rail { scrollbar-gutter: stable; overscroll-behavior: contain; }
  .drawer-scrim { position: fixed; inset: 4rem 0 0 0; opacity: 0; pointer-events: none; transition: opacity 0.2s ease; }
  .scroll-tabs {
    display: flex; gap: 0.5rem; overflow-x: auto; scroll-snap-type: x proximity; scrollbar-width: none;
    mask-image: linear-gradient(90deg, transparent 0, #111 1.25rem, #111 calc(100% - 1.25rem), transparent);
  }
  .scroll-tabs > * { scroll-snap-align: start; flex: 0 0 auto; }
  @media (min-width: 52.5rem) {
    .app-shell { grid-template-columns: 16.5rem minmax(0, 1fr); transition: grid-template-columns 0.24s var(--ease-out); }
    .app-shell[data-rail="collapsed"] { grid-template-columns: 4.5rem minmax(0, 1fr); }
    .app-shell[data-rail="collapsed"] .side-rail { overflow: visible; }
    .app-shell[data-rail="collapsed"] .rail-label { display: none; }
  }
}

@layer utilities {
  .flex-row { display: flex; flex-direction: row; align-items: safe center; justify-content: space-between; gap: 0.75rem; flex-wrap: wrap; min-inline-size: 0; }
}
```
- **Collapsible Sidebar Rail & Mobile Backdrop Drawer:** Animate desktop collapse via `grid-template-columns: 264px <-> 72px`, mark `.rail-btn[aria-current="page"]::before` active bar, float `[data-tooltip]::after` (`opacity`/`transform`) with `overflow: visible` when collapsed, and pair `< 52.5rem` slide-out drawer with `.drawer-scrim` + `main.inert = true` + `Escape` close.

## 3. Flexbox, CSS Grid RAM, `@container` (Isolated from `subgrid`) & Card Variants
Never declare `container-type: inline-size` and `grid-template-rows: subgrid` on the same element (`@container` establishes containment that breaks outer track sizing): put `container-type` on a wrapper and `subgrid` on aligned inner rows. Keep `@layer utilities` AFTER `components` so `.flex-row` beats `.card { flex-direction: column }`, use `min-block-size` (never fixed `block-size`) on bars with text, keep `.card-head` `flex-wrap: nowrap` with `flex: 1 1 0; min-inline-size: 0` on titles, and align card footers via `.card-foot { margin-block-start: auto; }`.
```css
@layer components {
  .ram-grid { display: grid; gap: 1.25rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr)); }
  .card-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 0.75rem; flex-wrap: nowrap; min-inline-size: 0; }
  .card-head-main { flex: 1 1 0; min-inline-size: 0; display: flex; flex-direction: column; gap: 0.25rem; }
  .card-foot { margin-block-start: auto; padding-block-start: 0.75rem; border-block-start: 1px solid var(--border-side); }
  .ratio-bar { min-block-size: 2.75rem; }
  .truncate-safe { min-inline-size: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .card-host { container: moduleBox / inline-size; }
  .card-body { display: grid; gap: 0.75rem; }
  @container moduleBox (min-width: 28rem) { .card-body { grid-template-columns: 1fr auto; align-items: center; } }
}
```
- **4 `<article>` Card Variants:** `Elevated` (primary workbench slab), `Outlined` (`1px solid var(--border-side)`), `Filled` (carved `--bg-well` track), and `Interactive` (expanded click area via `a.card-link::after { content: ""; position: inset 0; }` without `<div onClick>`).
- **Typography Defaults (`@layer base`):** Keep `-webkit-font-smoothing: antialiased; font-optical-sizing: auto; font-synthesis: none; text-rendering: auto;` on `body`; restrict `text-rendering: optimizeLegibility;` and `clamp()` ($\max \le 2.5\times \min$) to `h1, h2, h3`; enforce `max-inline-size: 65ch` on prose and `font-variant-numeric: tabular-nums;` on telemetry.

## 4. Expandable Menus, Custom `<select>`, Natural States & Interactive Lists
```css
@layer components {
  .theme-select, .theme-select::picker(select) { appearance: base-select; }
  .theme-select::picker-icon { transition: transform 0.2s var(--ease-out); }
  .theme-select:open::picker-icon { transform: rotate(180deg); }
  .theme-select::picker(select) {
    opacity: 0; transform: translateY(-4px) scale(0.98); /* Keep scrollable: NEVER overflow: hidden */
    transition: opacity 0.18s var(--ease-out), transform 0.18s var(--ease-out), display 0.18s, overlay 0.18s;
    transition-behavior: allow-discrete;
  }
  .theme-select:open::picker(select) { opacity: 1; transform: translateY(0) scale(1); }
  .seg-btn[aria-pressed="true"]::before { content: ""; inline-size: 0.375rem; block-size: 0.375rem; border-radius: 9999px; background: var(--brand-primary); }
  .nav-btn:active, .tactile-key:active { scale: 0.98; }
  .list-row-btn { min-block-size: 48px; transition: transform 0.15s var(--ease-out), scale 0.12s var(--ease-out), background-color 0.15s ease; }
  .row-action-hint { opacity: 0; transition: opacity 0.15s ease; }
  .list-row-btn:is(:hover, :focus-within, [aria-pressed="true"]) .row-action-hint { opacity: 1; }
  @media (hover: none) { .row-action-hint { opacity: 1; } }
  .accordion-panel { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 0.24s var(--ease-out); }
  .accordion-item[data-open="true"] .accordion-panel { grid-template-rows: 1fr; }
  .accordion-inner { overflow: hidden; min-block-size: 0; }
  dialog[open], [popover]:popover-open {
    opacity: 1; transform: translateY(0) scale(1);
    transition: opacity 0.2s var(--ease-out), transform 0.2s var(--ease-out), display 0.2s, overlay 0.2s;
    transition-behavior: allow-discrete;
  }
  @starting-style { dialog[open], [popover]:popover-open, .theme-select:open::picker(select) { opacity: 0; transform: translateY(0.5rem) scale(0.98); } }
  :where(a, button, input, select, textarea, summary, [tabindex="0"], [role="button"], [role="tab"]):focus-visible { outline: 2px solid var(--brand-primary); outline-offset: 2px; }
  main[tabindex="-1"]:focus, main[tabindex="-1"]:focus-visible, :where(h1, h2, h3)[tabindex="-1"]:focus, :where(h1, h2, h3)[tabindex="-1"]:focus-visible { outline: none; }
  input:user-invalid { border-color: var(--bead-danger); }
  .control-box:has(:checked) { border-color: var(--brand-primary); }
  /* Fitts hitbox expansion: 24px visual swatch inside >= 44x44px button + 44px range track + uncramped nav */
  .swatch-btn { position: relative; min-inline-size: 44px; min-block-size: 44px; }
  .swatch-btn::before { content: ""; position: absolute; inset: 0; margin: auto; inline-size: 24px; block-size: 24px; border-radius: inherit; }
  input[type="range"] { min-block-size: 44px; }
  nav :where(ul, .nav-list) { gap: 0.5rem; }
  .mobile-tab-btn { font-size: 0.8125rem; min-block-size: 44px; }
  /* In JS init(): pass { focus: false } on initial route render; add <link rel="icon" type="image/svg+xml"> to avoid /favicon.ico 404. */
  @media (any-pointer: coarse) { button, a, summary, [role="button"] { min-block-size: 48px; min-inline-size: 48px; touch-action: manipulation; } }
  @media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none; transition-duration: 0.01ms; } }
}
```
- Keep DOM source order identical to visual focus order (`DOM == Tab Order`): strictly ban `flex-direction: row-reverse` and positive `order`/`tabindex`. Apply CSS `reading-flow` only progressively where supported without breaking DOM order.

## 5. Verified `24x24` `<symbol>` SVGs & Real 5-State FSM
- Preload crisp stroke icons inside `<svg hidden aria-hidden="true" width="0" height="0"><symbol id="ic-..." viewBox="0 0 24 24">...</symbol></svg>` and reference via `<svg width="20" height="20" aria-hidden="true"><use href="#ic-check"/></svg>`.
- Bind all interactive flows to an explicit 5-state FSM (`type UIState = "idle" | "loading" | "empty" | "error" | "success"`) with retry recovery inside `role="status"` / `role="alert"` and zero placeholder stubs.
