---
name: ui-clean-worker
description: "Use when implementing or refactoring React 19, Next.js 15, Tailwind v4, or HTML/CSS UIs from DESIGN.md with 3-layer shadows, dark rim lighting, matte frosted glass, @container/subgrid, mobile-first layouts, verified 24x24 Lucide/Material SVGs, Single-DOM navigation, 5-state FSM, and RAW SHA-256 verification. Do NOT use for planning DESIGN.md alone or read-only audits."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv), React 19, Next.js 15+, Tailwind v4"
metadata:
  author: shredded-shape
  version: "1.4.0"
  updated_at: "2026-11-17"
  category: frontend-implementation
  tags:
    - optical-shadows
    - oklch
    - react-19
    - tailwind-v4
    - lucide-svg
    - raw-verification
---

# Clean Optical & Craft UI Worker (`ui-clean-worker`)

## Overview
Serve as the Stage 2 Tactical ReAct Implementer. Materialize `<project_root>/DESIGN.md` and implement production Light/Dark UI modules cleanly inside disjoint DAG-owned files (`<= 600` lines/file, `<= 60` lines/function), verifying every mutation via SHA-256 Read-After-Write.

## Inputs
- Approved **8-Section `DESIGN.md` Blueprint** and assigned DAG node (`owned_files`, `style_archetype`, `brand_oklch_hue`).
- Optional Stage 0 CLAREZA findings or Stage 3 `ui-judge` rejection list (`max_self_refine_rounds <= 3`).

## Procedure
Execute in causal order inside your DAG node's `owned_files` (load only needed L3 references):

1. **Phase 1 — Context Lock & `modern-web-guidance` Pre-Check:**
   - Load `DESIGN.md` and keep every edited file `<= 600` lines (`<= 60` lines/function).
   - Activate `modern-web-guidance` **first** for standard HTML/CSS/DOM behavior (`<dialog>`, `[popover]`, `appearance: base-select`, sanitization), or use [`references/clean_components_cards_motion_and_fsm.md`](references/clean_components_cards_motion_and_fsm.md) offline.

2. **Phase 2 — Materialize `DESIGN.md` & 5-Plane `OKLCH 60-30-10` Tokens:**
   - Write `<project_root>/DESIGN.md` and 5-Plane `light-dark()` + `oklch()` tokens (`tokens.css` / Tailwind v4 `@theme` + `color-mix(in oklab, ...)`) per [`references/optical_shadows_matte_and_dynamic_lighting.md`](references/optical_shadows_matte_and_dynamic_lighting.md): zero `#000000`, `C <= 0.20` accent, Light 3-layer shadows, Dark `--light-zenith` + stepped rim, matte frosted glass (`prefers-reduced-transparency: reduce`), and heading-only `optimizeLegibility`.

3. **Phase 3 — Adaptive Layouts, Flexbox/Grid/@container & Verified SVGs:**
   - Implement Mobile-First postures (`Compact`/`Medium`/`Expanded`), Flexbox (`min-inline-size: 0`, `safe center`), `@container` isolated from `subgrid`, scroll-snap fade (`mask-image`), expandable menus (`0fr -> 1fr`, `<details>`), 4 `<article>` Cards, and verified `24x24` SVGs (`stroke-linecap="round"`). Zero blobs, confetti pills, dashed wireframes, emojis, or neon glows.

4. **Phase 4 — Real 5-State FSM, Motion, A11y & Security:**
   - Wire executable `idle | loading | empty | error | success` states, GPU-only `transform`/`opacity` (`allow-discrete` + `@starting-style`), interactive-scoped `:focus-visible` (`>= 3:1` ring; suppress structural `main[tabindex="-1"]:focus` outline and skip eager `.focus()` on initial load), `:user-invalid`, `DOM == Tab Order`, `>= 44x44px` fine (`::before`/`::after` hit-expansion on compact swatches + `input[type="range"]`) / `>= 48x48px` coarse targets, nav `gap >= 0.5rem` (`>= 13px` tabs), `<link rel="icon" type="image/svg+xml">`, Next.js 15+ `await params`, React 19 native `ref`, and `DOMPurify.sanitize()`.

5. **Phase 5 — Mandatory Read-After-Write Verification (`RAW SHA-256`):**
   - Run the deterministic RAW verifier + [`rules/audit_criteria.md`](rules/audit_criteria.md) after every edit:
     - Plugin path: `python "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-clean-worker/scripts/verify_raw_frontend.py" <target> --json`
     - Repo fallback: `uv run python skills/ui-clean-worker/scripts/verify_raw_frontend.py <target> --json`
   - Append `--run-tsc` whenever modifying `.ts`/`.tsx` modules (`tsc --noEmit` fail-closed on missing `tsconfig.json` or errors).

## Gotchas
- **Inline Style & Comment Hygiene:** Keep structural colors in CSS variables; never leave forbidden tokens or reflow `transition: width/all` in shipped styles.
- **No Fail-Open Typechecks:** `--run-tsc` fails closed if `tsconfig.json` is absent or `tsc` fails.
- **`file://` Compatibility:** When building standalone static HTML bundles, use classic `<script defer>` IIFE (never `type="module"`) and `<textarea readonly>` clipboard fallback.

## Output
- Materialized `<project_root>/DESIGN.md` plus clean UI tokens, components, and state logic in DAG-owned files (`<= 600` lines each).
- Verified `RAWVerificationResult` JSON (`verdict == "[PASS]"`, 64-char SHA-256 checksums, zero slop flags).

## User Communication
Keep code, CSS tokens, and comments in Technical English; summarize modified files, verified SHA-256 checks, and optical/accessibility improvements to the user in **Portuguese (`pt-BR`)**.
