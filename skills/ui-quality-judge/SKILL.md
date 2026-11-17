---
name: ui-quality-judge
description: "Use when running the read-only Actor-Critic WCAG 2.2 AA/AAA OKLab/OKLCH contrast judge (FNR < 0.001), 4-Pillar Readiness (>= 90), 6-Dimension UI/UX composite score (>= 85), static WAI-ARIA audit, divsoup <= 0.45, 48x48px targets, :focus-visible, DOM==Tab order, anti-XSS, and anti-AI-Slop gate, returning PASSED or REJECTED. Do NOT use for writing UI code."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv)"
metadata:
  author: shredded-shape
  version: "1.4.0"
  updated_at: "2026-11-17"
  category: frontend-verification
  tags:
    - wcag-22
    - oklab-contrast
    - actor-critic
    - anti-ai-slop
    - wai-aria
    - accessibility
---

# Zero-Tolerance WCAG 2.2 & Actor-Critic UI Judge (`ui-quality-judge`)

## Overview
Serve as the **strictly read-only** Stage 3 Actor-Critic Judge. Audit polarity-isolated `OKLab -> WCAG Y` contrast, WAI-ARIA landmarks, keyboard ergonomics, XSS hygiene, file modularity (`<= 600` lines), and 12-Vector Anti-AI-Slop gates across built UIs, emitting deterministic `PASSED` or `REJECTED` verdicts.

## Inputs
- Target UI path (single HTML file, multi-file asset bundle, component folder, or Next.js/React app built by `ui-worker`).
- Target compliance level (`AA` default; auto-escalated to `AAA` when `clinical-day`, `clinical-night`, or `.sus-grid` files are detected).

## Procedure
Execute in strict read-only order (never edit target source files):

1. **Phase 1 — Composite Multi-Pillar Gate Execution:**
   - Run the unified composite judge (`--composite --json` orchestrating `ui_judge_gatekeeper.py`, `audit_tactile_ui.py`, and `ui_ux_frontend_auditor.py`):
     - Plugin path: `python "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py" <target> --wcag AA --composite --json`
     - Repo fallback: `uv run python skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py <target> --wcag AA --composite --json`
   - Pass `--wcag AAA` explicitly on clinical/EHR/medical routes (or let `--composite` auto-escalate on `.sus-grid`).

2. **Phase 2 — Polarity-Isolated Björn Ottosson `OKLab` & Anti-Slop Audit:**
   - Audit findings against [`references/wcag22_oklch_actor_critic_rubric.md`](references/wcag22_oklch_actor_critic_rubric.md) and [`rules/audit_criteria.md`](rules/audit_criteria.md).
   - Verify contrast per `:root` and every `[data-theme]` polarity block (`>= 4.5:1` AA, `>= 7.0:1` AAA/clinical, Dark elevation `well < canvas < card < card-lit`, zero `#000000`, `C <= 0.22` cap, semantic red `15°..40°` `<= 0.24`, zero neon/blobs/confetti/dashed wireframes/amateur SVGs, warn on `color-mix(in oklch)`).

3. **Phase 3 — Static WAI-ARIA, Ergonomics, File Caps & Security Check:**
   - Verify static WAI-ARIA semantics (`role="group"` + `<button aria-pressed>`, zero clickable `<div>`), `DOM == Tab Order`, `:focus-visible` (`>= 2px`), `>= 44x44px` (`48x48px` coarse touch), `divsoup <= 0.45`, per-file DOM depth isolation across `.html`/`.tsx`/`.vue`, `<= 600` lines/file, zero layout reflow transitions, Next.js 15+ `await params`, and zero unsanitized HTML sinks.
   - Pair with `a11y-debugging` from `chrome-devtools-plugin` when inspecting a live browser URL.

4. **Phase 4 — Structured Actor-Critic Verdict (`PASSED` / `REJECTED`):**
   - Return `PASSED` only if all composite sub-auditors clear (`gatekeeper.verdict == "PASSED"`, `tactile_readiness.readiness_score >= 90`, `ui_ux_6dim.final_score >= 85`, zero critical findings).
   - Otherwise return `REJECTED` with exact `[file:line]` fixes, bounded to `<= 3` self-refine cycles back to `ui-worker`.

## Gotchas
- **Named `[data-theme]` Polarity Mixing:** Single-polarity `[data-theme]` blocks inherit fallback `--ink-*` tokens strictly from the matching `:root` polarity (`dark` vs `light`), preventing false cross-theme failures.
- **External JS/TS Separation in DOM Parsing:** Composite audits run `evaluate_target(target_path)` so external `.js`/`.css` strings never pollute HTML tag nesting counts.
- **No Unfounded `axe-core` Claims:** Built-in scripts perform deterministic static checks unless live `chrome-devtools-plugin` runs against a served URL.

## Output
- Unified composite JSON (`overall_verdict`: `PASSED | REJECTED`, `gatekeeper`, `tactile_readiness`, `ui_ux_6dim`).
- Actionable fix list if `REJECTED` (capped at `3` refinement cycles).

## User Communication
Keep JSON reports and optical math in Technical English; present the final `PASSED`/`REJECTED` scorecard and prioritized defects to the user in **Portuguese (`pt-BR`)**.
