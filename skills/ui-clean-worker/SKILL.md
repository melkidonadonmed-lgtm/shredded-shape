---
name: ui-clean-worker
description: "Use when implementing or refactoring clean, intuitive React 19, Next.js 15, Tailwind v4, or HTML/CSS UIs from DESIGN.md with 3-layer shadows, dynamic dark-mode rim illumination, superior matte glass, and SHA-256 Read-After-Write verification. Do NOT use for planning DESIGN.md alone or read-only audits."
compatibility: "Antigravity 2.0, Node 22+, React 19, Next.js 15+, Tailwind CSS v4"
metadata:
  author: "Shredded-Shape"
  version: "1.0.0"
  updated_at: "2026-11-16"
  category: "Tactical ReAct Frontend Implementation & Read-After-Write Verification"
  tags: ["ui-clean-worker", "react-19", "nextjs-15", "tailwind-v4", "oklch", "box-shadow", "matte-glass", "dynamic-lighting", "raw-sha256", "fsm", "frontend-limpo"]
---

# `ui-clean-worker` — Clean Optical Frontend Worker (`ReAct` + `RAW`)

## 1. Overview & Scope

Executes bounded UI DAG tasks inside an isolated Context Fork via `ReAct` (`Thought -> Action -> Observation -> Self-Refine`), delivering intuitive, uncluttered Light/Dark interfaces verified physically with **Read-After-Write (SHA-256 + bytes + `tsc`)**.

- **When NOT to Use:** Do NOT use for DevTools forensic analysis (`ui-frontend-analyst`), authoring `DESIGN.md` from scratch (`ui-brand-ux-planner`), read-only WCAG judging (`ui-quality-judge`), or backend API routes (`agent-server-auditor`).

## 2. Inputs & Prerequisites

- **`target_path` (required) & `design_contract` / `dag_node` (optional):** Destination `.tsx`/`.css`/`.html` path, `<project_root>/DESIGN.md`, and bounded DAG task (`<= 5` active rules).
- **Verifier & References:**
  - [scripts/verify_raw_frontend.py](scripts/verify_raw_frontend.py) (`--target <path> [--run-tsc] --json`)
  - [references/optical_shadows_matte_and_dynamic_lighting.md](references/optical_shadows_matte_and_dynamic_lighting.md)
  - [references/clean_components_cards_motion_and_fsm.md](references/clean_components_cards_motion_and_fsm.md)

## 3. Step-by-Step Procedure

1. **Apply Polarity-Aware Optical Physics:** In Light mode, render **3-layer `box-shadow`** (Umbra + negative-spread Penumbra + top Catch-Light `inset 0 1px 0 0`). In Dark mode, replace muddy dark shadows with progressive lightness (`L = 0.16 -> 0.22 -> 0.27`), subtle specular rim illumination, and soft non-neon ambient surface halo (`C <= 0.20`).
2. **Render Superior Matte Frosted Surfaces:** Apply `oklch(from var(--surface-card) l c h / 0.74)` + `backdrop-filter: blur(20px) saturate(145%)` + `isolation: isolate` + crisp `1px` specular edge and `@media (prefers-reduced-transparency: reduce)` solid fallback.
3. **Build Clean, Intuitive Components & FSM:** Implement 4 `<article>` `subgrid` cards (`@container` isolated), Single-DOM Adaptive Navigation (`Bottom Bar <-> 256px Collapsible Rail`), React 19 direct `ref` props, Next.js 15+ async `params`, zero explanatory prose bloat, zero UI emojis, and real executable FSM (`idle | loading | empty | error | success`).
4. **Enforce Physical `Read-After-Write` (`RAW`):** Run `verify_raw_frontend.py` after every file batch to confirm bytes, SHA-256 hash, zero stubs, and `tsc --noEmit` before sending artifacts to `ui-quality-judge`.

## 4. Gotchas & Edge Cases

- **No Shared File Collisions:** In parallel waves, use `workspace: "share"` with disjoint vertical route ownership (`TASK-06` lock).
- **Hard Bans:** Zero `#000000`, zero neon, zero `setTimeout` placebos or `alert('Coming soon')`, zero `row-reverse`/`order` breaking `Tab`, and zero `forwardRef` in React 19.
- **Stop Criteria:** Emit `[RAW-VIOLATION]` and self-correct up to `max_steps: 5` if TypeScript fails or stubs exist.

## 5. Output Schema & Validation Criteria

Deliver modular UI files (`<= 300` edit lines/call, `<= 600` lines/module) passing `verify_raw_frontend.py` and [rules/audit_criteria.md](rules/audit_criteria.md), ready for `ui-quality-judge`.

## 6. User Communication Rule

Always formulate all direct user-facing conversation, component change summaries, and RAW verification reports in **Portuguese (Brazil / `pt-BR`)**, unless the user explicitly requests otherwise.
