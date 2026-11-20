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
- **5-State FSM & Resizable `@container` Craft Card:** Bind interactive flows to `idle | loading | empty | error | success` inside `role="status"` / `role="alert"` (zero placeholder stubs, zero `forwardRef`). Use GPU `.skip-link`, Silent CSS Breadcrumbs (`::before`), `display: flow-root`, `.prose > * + *`, `text-wrap: balance/pretty`, and clean OKLCH `@container` cards (never `@media` inside cards, never `transition-all`):
```css
@layer components {
  .skip-link { position: fixed; inset-block-start: 1rem; inset-inline-start: 1rem; transform: translateY(-200%); transition: transform 0.16s var(--ease-out); background: var(--brand-fill); color: var(--ink-on-brand); }
  .skip-link:focus-visible { transform: translateY(0); }
  .breadcrumbs ol { display: flex; gap: 0.5rem; list-style: none; }
  .breadcrumbs li + li::before { content: "/"; margin-inline-end: 0.5rem; color: var(--ink-muted); }
  .section-bfc { display: flow-root; }
  .prose { max-inline-size: 65ch; text-wrap: pretty; }
  .prose > * + * { margin-block-start: 1.25em; }
  h1, h2, h3 { text-wrap: balance; }
  .cq-card { container: card / inline-size; resize: both; overflow: auto; min-inline-size: 280px; background: var(--bg-card); box-shadow: var(--shadow-elevation-1); border-radius: var(--r-outer); padding: clamp(1rem, 4cqw, 1.5rem); transition: transform 0.2s var(--ease-out), box-shadow 0.2s var(--ease-out); }
  .cq-grid { display: grid; grid-template-columns: 1fr; gap: 0.75rem; }
  @container card (min-width: 360px) { .cq-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
}
```
```html
<a href="#main-content" class="skip-link">Skip to content</a>
<nav class="breadcrumbs" aria-label="Breadcrumb"><ol role="list"><li><a href="/">Home</a></li><li><a href="/metrics" aria-current="page">Metrics</a></li></ol></nav>
```

## 4. Expandable Menus, Custom `<select>`, Focus/Fitts & Verified `<symbol>` SVGs
- **Native Controls & Motion:** Use `appearance: base-select` + `::picker(select)` (`opacity`/`transform`, `allow-discrete` + `@starting-style`), `0fr -> 1fr` grid accordions, native `<details>`/`[popover]`, `.seg-btn[aria-pressed="true"]::before`, and `.list-row-btn { min-block-size: 48px; }`.
- **Ergonomics, Focus & Sprites:** Keep `DOM == Tab Order` (ban `row-reverse`, positive `order`, `grid-auto-flow: dense`). Scope `:focus-visible` strictly to interactive controls (suppress `main[tabindex="-1"]`), expand compact swatches/ranges to `>= 44x44px` (`>= 48x48px` under `any-pointer: coarse` + `touch-action: manipulation`), keep `nav gap >= 0.5rem` & `.mobile-tab-btn >= 0.8125rem`, honor `@media (prefers-reduced-motion: reduce)`, add `<link rel="icon" type="image/svg+xml">`, and inline `<svg hidden><symbol id="ic-..." viewBox="0 0 24 24">` sprites referenced via `<use href="#ic-..."/>`.
