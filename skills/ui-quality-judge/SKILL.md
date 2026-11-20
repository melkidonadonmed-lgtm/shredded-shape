---
name: ui-quality-judge
description: "Use when running the read-only Actor-Critic WCAG 2.2 AA/AAA OKLab judge (FNR < 0.001), 4-Pillar Readiness (>= 90), 6-Dim UI/UX (>= 85), isolated print/test checks, fail-closed UNVERIFIED scope gates, WAI-ARIA, 44/48px targets (<40px blocker), anti-XSS, and anti-AI-Slop, returning PASSED, REJECTED, or UNVERIFIED. Do NOT use for writing UI code."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv)"
allowed-tools: "read_file run_command"
metadata:
  author: "shredded-shape"
  version: "1.6.0"
  updated_at: "2026-11-19"
  category: "frontend-verification"
  tags: "wcag-22, oklab-contrast, actor-critic, anti-ai-slop, wai-aria, accessibility, double-pass, 3-axis-judge"
---

# Zero-Tolerance Double-Pass 3-Axis UI Judge (`ui-quality-judge`)

## Overview
Strictly **read-only** Stage 3 Severe Double-Pass (`Macro + Micro`) Actor-Critic Judge covering **3 Axes** (`ui_code`, `execution_plan`, `technical_audit`). Enforce polarity-isolated `OKLab -> WCAG Y` contrast, WAI-ARIA, microcopy brevity, intuitiveness, `@container` spacing/reactivity, AppSec, and Anti-Slop gates, emitting `PASSED`, `REJECTED`, or `UNVERIFIED`.

## Inputs
- Target UI path (`src/` root, HTML/TSX, multi-file bundle), `DESIGN.md`/DAG `.json` (`--axis execution_plan`), or CLAREZA report (`--axis technical_audit --workspace <root>`).
- Compliance level (`AA` default; auto-escalated to `AAA` when `clinical-day`, `clinical-night`, or `.sus-grid` files appear).

## Procedure
Execute under **Zero-Trust Read-Only Guardrails** (zero source mutations):

1. **Phase 1 — Double-Pass (`Macro + Micro`) & Polymorphic Axis Gate:** Run composite/axis verifier (`--wcag AAA` on clinical routes):
   - `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py" <target> --wcag AA --axis <auto|ui_code|execution_plan|technical_audit> [--workspace <root>] --composite --json` (fallback: `uv run python skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py ...`)
2. **Phase 2 — `OKLab` Polarity, Reactivity & Anti-Slop Audit:** Enforce [`references/wcag22_oklch_actor_critic_rubric.md`](references/wcag22_oklch_actor_critic_rubric.md) + [`rules/audit_criteria.md`](rules/audit_criteria.md): contrast per `:root`/`[data-theme]` (`>= 4.5:1` AA, `>= 7.0:1` AAA), Dark `well < canvas < card < card-lit`, `#000000` absent, `C <= 0.20` target (hard cap `0.22`, red `15°..40° <= 0.24`), `color-mix(in oklab)`, zero slop/gradient-text/side-stripes/bad SVGs, `flow-root`/8pt spacing, and `@container` reactivity.
3. **Phase 3 — WAI-ARIA, Brevity, Intuitiveness & AppSec:** Verify `<button aria-pressed>`, zero `<div onClick>`, `DOM == Tab Order` (zero `grid-auto-flow: dense`), `:focus-visible`, `>= 44/48px` targets, concise nav microcopy + mystery-free affordances + silent breadcrumbs + `.skip-link`, `divsoup <= 0.45`, `<= 600`L/file, Next.js 15+ `await params`, zero `AUDIT-SEC-ENV-LEAK`/`AUDIT-STUB-PLACEHOLDER`, and per-sink `DOMPurify.sanitize()`.
4. **Phase 4 (`[Self-Refine]`) — Causal 4-Stage Verdict (`PASSED` | `REJECTED` | `UNVERIFIED`):** Emit `UNVERIFIED` on truncation/`scope_narrowed`; emit `PASSED` only if `gatekeeper == "PASSED"`, `Readiness >= 90`, `UI/UX >= 85`, and zero critical defects; else `REJECTED` with `P0..P3` 4-Stage Causal Verdict (`<= 3` cycles before `HITL_ESCALATION_REQUIRED`).

## Gotchas
- **Never Narrow to `styles/` Alone:** Componentless CSS audits miss TSX defects, triggering fail-closed `UNVERIFIED`; `--axis auto` always routes directories to `ui_code`.
- **Print & Standalone Isolation:** `.sus-grid`/`@media print`/`.ts` print templates isolate separately; standalone `.tsx` files skip global-CSS deductions.
- **No Unfounded Tool Claims:** Report deterministic script outcomes separately from semantic double-pass review; keep `axe-core` claims tied to live CDP runs.

## Output
- Composite or `AxisJudgeReport` JSON (`PASSED | REJECTED | UNVERIFIED`, `findings`, `scope_narrowed`, `unverified_routes`).
- 4-stage `[file:line]` causal fix matrix (`P0_BLOCKER..P3_NIT`) when `REJECTED`.

## User Communication
Keep JSON reports and optical math in Technical English; present the final `PASSED`/`REJECTED` scorecard and prioritized `P0..P3` defects in **Portuguese (`pt-BR`)**.
