# Intuitive Zero-Verbiage UX, Next.js 15+ RSC Boundaries & AI/LLM UI Patterns

## 1. Zero-Verbiage Intuitive Hierarchy

- **Show, Don't Lecture:** Interfaces must communicate state and affordance through spatial grouping (Gestalt proximity), clear 1–2 word labels, and crisp icons — **never add explanatory helper paragraphs, onboarding banners, or "How this works" text walls over obvious controls**.
- **60–80 Word Screen Budget:** Keep microcopy tight, scannable, and factual (`.prose` max-inline-size `65ch`).

## 2. Recommended Stack & Architectural Boundaries

| Complexity Tier | Stack & Folder Structure | CSS Strategy |
| :--- | :--- | :--- |
| **Tier 1 (Static / Atlas)** | Single-file or modular HTML5 + vanilla ES Modules (`<= 150 KB`) | `@layer reset, tokens, layout, components, styles, motion;` + `light-dark()` |
| **Tier 2 (Feature SPA)** | React 19 + Vite + TypeScript strict (`src/{app,styles,components/{ui,layout},features/<domain>}`) | CSS Modules or Tailwind v4 `@theme` consuming `src/styles/tokens.css` |
| **Tier 3 (Fullstack PWA)** | Next.js 15+ App Router (`(marketing)/`, `(workspace)/`, `_components/`, `Viewport` API + anti-FOUC `<head>`) | Unified `design-system.css` with Tailwind v4 `@theme`, `Promise<...>` async `params` |

- **Server vs. Client Discipline:** Keep pages and layouts as React Server Components; isolate `'use client'` exclusively to interactive leaf components (`Leaf Components`).

## 3. Agentic / AI UI Standards

- Use collapsible `<details class="reasoningAccordion">` for CoT traces with auto-scroll pause on manual scroll.
- Render MCP Tool Calls as semantic cards displaying `pending | running | success | error`, latency (`tabular-nums`), and typed input/output summaries.
- Gate destructive actions behind explicit HITL confirmation surfaces inside native `<dialog>` top-layer elements.
