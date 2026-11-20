# Intuitive Zero-Verbiage UX, Spacing Engineering & Tailwind v4 `@theme`

## 1. 5 Usage & Intuitiveness Questions (Zero-Verbiage UX)
Before drafting tokens or layouts, answer:
1. **How will it be used?** (Primary daily task, mouse vs. touch frequency, glance vs. deep edit).
2. **What is the optimal & ideal usage mode?** (Keyboard shortcuts, live telemetry focus, `<= 3`-click flow).
3. **Which color polarity & theme fit the domain?** (Light/Dark `OKLCH 60-30-10`, calm contrast without neon).
4. **Which typography & single SVG family fit?** (M3 scale `1.2`/`1.5`, `tabular-nums`, `text-wrap: balance/pretty`, `24x24` Lucide/Material).
5. **How is intuitiveness achieved without explanatory prose?** Use visual structure as information (hairline dividers, recessed `.engraved-pill` counters, spatial proximity, affordance cues) so tutorial walls vanish.
- **Target & Order Ergonomics:** Enforce `>= 44x44px` hitboxes (`::before`/`::after` expansion on `20-24px` swatches/icon buttons and `input[type="range"]`; `>= 48x48px` + `8px` spacing under `any-pointer: coarse` with `touch-action: manipulation`), nav `gap >= 0.5rem` (`8px`), mobile tab labels `>= 0.8125rem` (`13px`), interactive-scoped `:focus-visible` (`>= 3:1`, zero rings on `main[tabindex="-1"]`), LVHA links, `<link rel="icon" type="image/svg+xml">`, and `DOM == Tab Order` (ban `row-reverse`, positive `order`, `grid-auto-flow: dense`).
- **60–80 Word Viewport Discipline:** Cap prose width at `max-inline-size: 60ch..65ch` (`line-height` `1.1–1.25` headings, `1.4–1.6` body).

## 2. Tactile Pointer Matrix, BFC Margin Control & Spacing
- **`pointer: fine` (Mouse/Trackpad):** `150ms cubic-bezier(0.2, 0.8, 0.2, 1)` hover transitions, tactile `:active { scale: 0.99; }`, native semantic cursors.
- **`any-pointer: coarse` (Touch):** `min-inline-size: 48px; min-block-size: 48px;`, `>= 8px` target separation, `touch-action: manipulation`, and `overscroll-behavior-y: contain` inside scrollable drawers.
- **Box Model & Margin Collapse Guard ($M = \max(M_1, M_2)$):** Enforce `*, *::before, *::after { box-sizing: border-box; }`, logical properties (`padding-inline`, `margin-block`, `inline-size`, `100dvh`), `gap` inside Flex/Grid, `display: flow-root` BFC isolation on sections, and `.prose > * + * { margin-block-start: 1.25em; }`.

## 3. Recommended Stack, Macro/Micro & Next.js App Router Boundaries
| Complexity Tier | Stack & Folder Structure | Layout & CSS Strategy |
| :--- | :--- | :--- |
| **Tier 1 (Static / Atlas)** | Modular HTML5 + local ES/IIFE bundle (`<= 600`L/file, zero CDN) | `@layer tokens, reset, layout, components, utilities, motion;` + `light-dark()` |
| **Tier 2 (Feature SPA)** | React 19 + Vite + TypeScript strict (`src/{styles,components,features}`) | Tailwind v4 `@theme inline` + `tokens.css` + CSS Grid + `@container` |
| **Tier 3 (Fullstack PWA)** | Next.js 15+ App Router (`app/layout.tsx`, `loading.tsx`, `error.tsx`, `_components/`) | Persistent RSC shell `layout.tsx`, `'use client'` leaves, `await params` |

- **Macro vs. Micro:** Page shells use CSS Grid + `100dvh`; inner cards use `@container (min-width: ...)` (`container-type: inline-size`) — **never** `@media (min-width)` inside isolated components. Set `scroll-padding-top: 4.5rem;`.

## 4. Silent Chrome, Expandable Menus & Tailwind v4 `@theme inline` Shadows
- **Silent Breadcrumbs & Skip Link:** `<ol role="list">` with `aria-current="page"` and CSS `li + li::before { content: "/"; }` (never literal `/` in HTML); unique `<nav aria-label>` without repeating `"navigation"`; GPU `.skip-link` (`transform: translateY(-120%)` -> `0`) targeting `<main id="main-content" tabindex="-1">`.
- **Tailwind v4 `@theme inline` Elevation:** Map `--shadow-elevation-low`, `--shadow-elevation-medium`, `--shadow-elevation-high`, and `--shadow-inset-sunken` in `@theme inline` pointing to polarity-reactive `:root` / `[data-theme="dark"]` OKLCH variables (eliminates duplicate `dark:shadow-*` classes; animate `transform, box-shadow, background-color`, never `transition-all`).
- **Native Progressive Disclosure:** `<details>`/`<summary>`, `[popover="auto"]`, `<dialog>` (`@starting-style` + `allow-discrete`), `<= 3 <nav>` (`<= 6` concise links each); in AI UIs wrap traces in `<details>` and gate irreversible mutations behind `<dialog>` HITL.
