# Intuitive Zero-Verbiage UX, Next.js 15+ RSC Boundaries & Expandable Patterns

## 1. Zero-Verbiage Intuitive Hierarchy & Focus Rhythm
- **Show, Don't Lecture:** Convey workflow affordances via spatial grouping, concise 1–2 word labels, etched `.engraved-pill` counters, and crisp icons — eliminate multi-sentence tutorial walls above interactive controls.
- **Target & Order Ergonomics:** Enforce `>= 44x44px` interactive hitboxes (`::before`/`::after` expansion on `20-24px` swatches/icon buttons and `input[type="range"]`; `>= 48x48px` under `any-pointer: coarse` with `touch-action: manipulation`), nav `gap >= 0.5rem` (`8px`), mobile tab labels `>= 0.8125rem` (`13px`), crisp interactive-scoped `:focus-visible` outlines (`>= 3:1` contrast, suppressing rings on structural `main[tabindex="-1"]` landmarks and skipping eager `.focus()` on initial `DOMContentLoaded`), LVHA link order, `<link rel="icon" type="image/svg+xml">`, and `DOM == Tab Order` (zero `row-reverse` or positive `tabindex`).
- **60–80 Word Viewport Discipline:** Keep microcopy scannable and prose columns capped at `max-inline-size: 65ch`.

## 2. Recommended Stack, Macro Layout & Next.js App Router Boundaries
| Complexity Tier | Stack & Folder Structure | Layout & CSS Strategy |
| :--- | :--- | :--- |
| **Tier 1 (Static / Atlas)** | Modular HTML5 + classic/ES local bundle (`<= 600`L/file, zero external JS CDN) | `@layer reset, tokens, layout, components, styles, motion;` + `light-dark()` |
| **Tier 2 (Feature SPA)** | React 19 + Vite + TypeScript strict (`src/{styles,components,features}`) | Tailwind v4 `@theme` + `tokens.css` + CSS Grid RAM & `@container` |
| **Tier 3 (Fullstack PWA)** | Next.js 15+ App Router (`app/layout.tsx`, `loading.tsx`, `error.tsx`, `_components/`) | Persistent shell in RSC `layout.tsx`, `'use client'` leaves, `await params` |

- **Server vs. Client Split:** Render shell navigation, headings, and initial data in React Server Components (`layout.tsx` / `page.tsx`), stream slow leaves via `Suspense` + `loading.tsx`, and set `scroll-padding-top: 4.5rem;` for anchored routes.

## 3. Expandable Menus, Progressive Disclosure & Agentic AI Controls
- **Native Progressive Disclosure:** Prefer `<details>` + `<summary>` for secondary specs, `[popover="auto"]` + Anchor Positioning for dropdowns/sheets, and native `<dialog>` (`@starting-style` + `transition-behavior: allow-discrete`) for modal exports and confirmations.
- **Navigation Menu Sprawl Cap:** Keep primary `<nav>` containers `<= 3` per document and `<= 6` clickable links/buttons inside each `<nav>` or horizontal `scroll-snap` bar.
- **Agentic / AI Workloads:** Render reasoning traces inside `<details class="reasoningAccordion">`, render tool calls with executable FSM states (`pending | running | success | error`) and `tabular-nums` latency, and gate irreversible actions behind `<dialog>` HITL confirmation.
