---
name: ui-clean-worker
description: "Use when implementing or refactoring React 19, Next.js 15, Tailwind v4, or HTML/CSS UIs from DESIGN.md with 3-layer shadows, dark rim light, matte frosted glass, @container/subgrid, 44/48px targets (<40px blocker), verified 24x24 SVGs, Single-DOM nav, 5-state FSM, and RAW SHA-256 checks. Do NOT use for planning DESIGN.md or read-only audits."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv), React 19, Next.js 15+, Tailwind v4"
allowed-tools: "read_file write_file edit_file run_command"
metadata:
  author: "shredded-shape"
  version: "1.6.0"
  updated_at: "2026-11-19"
  category: "frontend-implementation"
  tags: "optical-shadows, oklch, react-19, tailwind-v4, lucide-svg, raw-verification"
---

# Clean Optical & Craft UI Worker (`ui-clean-worker`)

## Overview
Stage 2 Tactical ReAct Implementer. Materialize `<project_root>/DESIGN.md` and clean Light/Dark UI modules inside DAG `owned_files` (`<= 600`L/file, `<= 60`L/fn), verifying every edit via SHA-256 Read-After-Write.

## Inputs
- Approved **8-Section `DESIGN.md` Blueprint** and DAG node (`owned_files`, `style_archetype`, `brand_oklch_hue`).
- Optional Stage 0 CLAREZA diffs or Stage 3 `ui-judge` rejections (`max_self_refine_rounds <= 3`).

## Procedure
Execute under **Zero-Trust Guardrails** in causal order inside `owned_files` (load only needed L3 refs):

1. **Phase 1 — Context Lock & `modern-web-guidance`:** Load `DESIGN.md` (`<= 600`L/file, `<= 60`L/fn). Query `modern-web-guidance` **first** for standard DOM APIs, or use [`references/clean_components_cards_motion_and_fsm.md`](references/clean_components_cards_motion_and_fsm.md) offline.
2. **Phase 2 — Materialize `DESIGN.md` & `@theme inline`:** Write `<project_root>/DESIGN.md` + 5-Plane `light-dark()`/`oklch()`/`color-mix(in oklab)` + RCS + P3 (`C <= 0.20`, no `#000000`), `@theme inline` `--shadow-elevation-*`, Light 3-layer shadows, Dark `--light-zenith` + rim, `isolation: isolate` + standalone `<feColorMatrix>`, matte glass (`prefers-reduced-transparency`), and heading-only `optimizeLegibility` per [`references/optical_shadows_matte_and_dynamic_lighting.md`](references/optical_shadows_matte_and_dynamic_lighting.md).
3. **Phase 3 — Adaptive BFC Layouts, `@container` & Silent Chrome:** Build `Compact`/`Medium`/`Expanded` postures, `flow-root`, `.prose > * + *`, `100dvh`, `overscroll-behavior-y: contain`, `min-inline-size: 0`, `@container` + `cqw` isolated from `subgrid`, `text-wrap: balance/pretty`, silent CSS breadcrumbs (`::before`), GPU `.skip-link`, collapsed-rail tooltips, `0fr -> 1fr`/`<details>`/`popover`, 4 Cards, and `24x24` SVGs (zero slop/blobs/gradient-text/side-stripes/emojis).
4. **Phase 4 — 5-State FSM, Motion, A11y & AppSec:** Wire `idle | loading | empty | error | success`, GPU `transform`/`opacity` (`allow-discrete` + `@starting-style`), `:focus-visible`, `:user-invalid`, `DOM == Tab Order` (no `grid-auto-flow: dense`), `>= 44/48px` targets, SVG favicon, Next.js 15+ `await params`, React 19 `ref`, per-sink `DOMPurify.sanitize()`, zero `NEXT_PUBLIC_*`/`VITE_*` secrets, and zero omission comments.
5. **Phase 5 (`[ReAct]`) — RAW Verification:** Run [`rules/audit_criteria.md`](rules/audit_criteria.md) verifier after every edit (`--run-tsc` on `.ts`/`.tsx`):
   - `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-clean-worker/scripts/verify_raw_frontend.py" <target> --json` (repo: `uv run python skills/ui-clean-worker/scripts/verify_raw_frontend.py <target> --json`)

## Gotchas
- **Inline Style & Comment Hygiene:** Keep structural colors in CSS vars; ban stub handlers or `transition: width/all`.
- **Fail-Closed Typechecks & Truncation:** `--run-tsc` fails on missing `tsconfig.json` or `tsc` errors; `verify_raw_frontend.py` fails closed on `> 500` file truncation, and `<feColorMatrix>` stays isolated from `<feGaussianBlur>`.
- **`file://` Compatibility:** When building standalone static HTML bundles, use classic `<script defer>` IIFE (never `type="module"`) and `<textarea readonly>` clipboard fallback.

## Output
- Materialized `<project_root>/DESIGN.md` plus clean UI tokens, components, and state logic in DAG-owned files (`<= 600` lines each).
- Verified `RAWVerificationResult` JSON (`verdict == "[PASS]"`, 64-char SHA-256 checksums, zero slop flags).

## User Communication
Keep code, CSS tokens, and comments in Technical English; summarize modified files, verified SHA-256 checks, and optical/accessibility improvements to the user in **Portuguese (`pt-BR`)**.
