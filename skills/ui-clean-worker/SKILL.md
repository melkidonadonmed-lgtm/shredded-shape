---
name: ui-clean-worker
description: "Use when implementing or refactoring React 19, Next.js 15, Tailwind v4, or HTML/CSS UIs from DESIGN.md with 3-layer shadows, dark rim light, matte frosted glass, @container/subgrid, 44/48px targets, verified 24x24 SVGs, Single-DOM nav, 5-state FSM, and RAW SHA-256 verification. Do NOT use for planning DESIGN.md or read-only audits."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv), React 19, Next.js 15+, Tailwind v4"
allowed-tools: "read_file write_file edit_file run_command"
metadata:
  author: "shredded-shape"
  version: "1.5.1"
  updated_at: "2026-11-18"
  category: "frontend-implementation"
  tags: "optical-shadows, oklch, react-19, tailwind-v4, lucide-svg, raw-verification"
---

# Clean Optical & Craft UI Worker (`ui-clean-worker`)

## Overview
Stage 2 Tactical ReAct Implementer. Materialize `<project_root>/DESIGN.md` and implement clean Light/Dark UI modules strictly inside disjoint DAG-owned files (`<= 600` lines/file, `<= 60` lines/function), verifying every mutation via SHA-256 Read-After-Write.

## Inputs
- Approved **8-Section `DESIGN.md` Blueprint** and assigned DAG node (`owned_files`, `style_archetype`, `brand_oklch_hue`).
- Optional Stage 0 CLAREZA diffs or Stage 3 `ui-judge` rejections (`max_self_refine_rounds <= 3`).

## Procedure
Execute in causal order under **Zero-Trust DAG Ownership Guardrails** (never edit outside `owned_files`; load only needed L3 references):

1. **Phase 1 — Context Lock & `modern-web-guidance` Pre-Check:**
   - Load `DESIGN.md` and keep edited modules `<= 600` lines (`<= 60` lines/function).
   - Query `modern-web-guidance` **first** for standard HTML/CSS/DOM APIs (`<dialog>`, `[popover]`, `appearance: base-select`, sanitization), or use [`references/clean_components_cards_motion_and_fsm.md`](references/clean_components_cards_motion_and_fsm.md) offline.

2. **Phase 2 — Materialize `DESIGN.md` & 5-Plane `OKLCH 60-30-10` Tokens:**
   - Write `<project_root>/DESIGN.md` and `light-dark()` + `oklch()` tokens (`tokens.css` / Tailwind v4 `@theme` + `color-mix(in oklab, ...)`) per [`references/optical_shadows_matte_and_dynamic_lighting.md`](references/optical_shadows_matte_and_dynamic_lighting.md): zero `#000000`, `C <= 0.20`, Light 3-layer shadows, Dark `--light-zenith` + rim light, matte glass (`prefers-reduced-transparency: reduce`), and heading-only `optimizeLegibility`.

3. **Phase 3 — Adaptive Layouts, `@container` & Verified `24x24` SVGs:**
   - Implement `Compact`/`Medium`/`Expanded` postures, Flexbox (`min-inline-size: 0`, `safe center`), `@container` isolated from `subgrid`, `scroll-snap` `mask-image`, `0fr -> 1fr`/`<details>` menus, 4 `<article>` Cards, and verified `24x24` SVGs. Zero blobs, confetti pills, dashed wireframes, emojis, or neon glows.

4. **Phase 4 — 5-State FSM, Motion, A11y & Security:**
   - Wire real `idle | loading | empty | error | success` states, GPU `transform`/`opacity` (`allow-discrete` + `@starting-style`), interactive `:focus-visible` (`>= 3:1`, suppress `main[tabindex="-1"]` rings), `:user-invalid`, `DOM == Tab Order`, `>= 44x44px` (`48x48px` coarse) targets, nav `gap >= 8px` (`>= 13px`), SVG `<link rel="icon">`, Next.js 15+ `await params`, React 19 `ref`, and `DOMPurify.sanitize()`.

5. **Phase 5 (`[ReAct: OBSERVATION -> SELF-CORRECTION]`) — Read-After-Write Checklist (`RAW SHA-256`):**
   - Run the deterministic RAW verifier + [`rules/audit_criteria.md`](rules/audit_criteria.md) after every edit (append `--run-tsc` on `.ts`/`.tsx`):
     - Plugin (`pwsh`/POSIX): `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-clean-worker/scripts/verify_raw_frontend.py" <target> --json`
     - Repo fallback: `uv run python skills/ui-clean-worker/scripts/verify_raw_frontend.py <target> --json`

## Gotchas
- **Inline Style & Comment Hygiene:** Keep structural colors in CSS vars; never leave stub handlers or `transition: width/all` reflows.
- **Fail-Closed Typechecks:** `--run-tsc` rejects missing `tsconfig.json` or any `tsc` error.
- **`file://` Compatibility:** When building standalone static HTML bundles, use classic `<script defer>` IIFE (never `type="module"`) and `<textarea readonly>` clipboard fallback.

## Output
- Materialized `<project_root>/DESIGN.md` plus clean UI tokens, components, and state logic in DAG-owned files (`<= 600` lines each).
- Verified `RAWVerificationResult` JSON (`verdict == "[PASS]"`, 64-char SHA-256 checksums, zero slop flags).

## User Communication
Keep code, CSS tokens, and comments in Technical English; summarize modified files, verified SHA-256 checks, and optical/accessibility improvements to the user in **Portuguese (`pt-BR`)**.
