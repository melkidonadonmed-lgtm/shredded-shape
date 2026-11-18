---
name: ui-quality-judge
description: "Use when running the read-only Actor-Critic WCAG 2.2 AA/AAA OKLab judge (FNR < 0.001), 4-Pillar Readiness (>= 90), 6-Dim UI/UX (>= 85), isolated print/test checks, fail-closed UNVERIFIED scope gates, WAI-ARIA, 48x48px targets, anti-XSS, and anti-AI-Slop, returning PASSED, REJECTED, or UNVERIFIED. Do NOT use for writing UI code."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv)"
allowed-tools: "read_file run_command"
metadata:
  author: "shredded-shape"
  version: "1.5.1"
  updated_at: "2026-11-18"
  category: "frontend-verification"
  tags: "wcag-22, oklab-contrast, actor-critic, anti-ai-slop, wai-aria, accessibility"
---

# Zero-Tolerance WCAG 2.2 & Actor-Critic UI Judge (`ui-quality-judge`)

## Overview
Strictly **read-only** Stage 3 Actor-Critic Judge. Audit polarity-isolated `OKLab -> WCAG Y` contrast, WAI-ARIA landmarks, keyboard ergonomics, XSS hygiene, modularity (`<= 600` lines), and 12-Vector Anti-Slop gates, emitting `PASSED`, `REJECTED`, or fail-closed `UNVERIFIED`.

## Inputs
- Target UI path (`src/` root, single HTML/TSX file, or multi-file bundle built by `ui-worker`).
- Compliance level (`AA` default; auto-escalated to `AAA` when `clinical-day`, `clinical-night`, or `.sus-grid` files appear).

## Procedure
Execute under **Zero-Trust Read-Only Guardrails** (zero source mutations):

1. **Phase 1 — Composite Multi-Pillar Gate Execution:**
   - Run the composite judge (`ui_judge_gatekeeper.py` + `audit_tactile_ui.py` + `ui_ux_frontend_auditor.py`; pass `--wcag AAA` on clinical/EHR/medical routes):
     - Plugin (`pwsh`/POSIX): `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py" <target> --wcag AA --composite --json`
     - Repo fallback: `uv run python skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py <target> --wcag AA --composite --json`

2. **Phase 2 — Polarity-Isolated Björn Ottosson `OKLab` & Anti-Slop Audit:**
   - Check [`references/wcag22_oklch_actor_critic_rubric.md`](references/wcag22_oklch_actor_critic_rubric.md) + [`rules/audit_criteria.md`](rules/audit_criteria.md): contrast per `:root` and `[data-theme]` block (`>= 4.5:1` AA, `>= 7.0:1` AAA), Dark `well < canvas < card < card-lit`, zero `#000000`, `C <= 0.22` (`<= 0.24` semantic red `15°..40°`), zero neons/blobs/confetti/wireframes/bad SVGs, warn `color-mix(in oklch)`.

3. **Phase 3 — Static WAI-ARIA, Ergonomics, Caps & Security Checklist:**
   - Verify `role="group"` + `<button aria-pressed>`, zero unsemantic `<div onClick>`, `DOM == Tab Order`, `:focus-visible`, `>= 44x44px` (`48x48px` coarse), `divsoup <= 0.45`, isolated DOM depth, `<= 600` lines/file, zero reflow transitions, Next.js 15+ `await params`, and zero XSS sinks. Pair with live `a11y-debugging` on served URLs.

4. **Phase 4 (`[Self-Refine]`) — Deterministic Verdict (`PASSED` | `REJECTED` | `UNVERIFIED`):**
   - Emit `UNVERIFIED` (fail-closed) when `truncated == true`, `scope_narrowed == true`, or targets are missing.
   - Emit `PASSED` only if `gatekeeper.verdict == "PASSED"`, `tactile_readiness.readiness_score >= 90`, `ui_ux_6dim.final_score >= 85`, and zero critical defects exist; otherwise emit `REJECTED` with `[file:line]` fixes (`<= 3` cycles before `HITL_ESCALATION_REQUIRED`).

## Gotchas
- **Never Narrow to `styles/` Alone:** Componentless CSS audits miss TSX `<div onClick>` and pseudo-icons, triggering fail-closed `UNVERIFIED`.
- **Print Templates vs. Screen CSS:** `.sus-grid`/`@media print`/`.ts` HTML print strings are masked separately from screen CSS (`>= 12px` still enforced in `globals.css`).
- **Named `[data-theme]` Polarity & Single-File Isolation:** Inherit fallback tokens within matching polarity (`dark` vs `light`) and avoid global-CSS deductions on standalone `.tsx`/`.jsx` files.
- **No Unfounded `axe-core` Claims:** Built-in scripts run static AST/CSS checks unless live `chrome-devtools-plugin` inspects a served URL.

## Output
- Composite JSON (`overall_verdict`: `PASSED | REJECTED | UNVERIFIED`, `gatekeeper`, `tactile_readiness`, `ui_ux_6dim`, `scope_narrowed`, `unverified_routes`).
- Actionable `[file:line]` fix list when `REJECTED` (`<= 3` refinement cycles).

## User Communication
Keep JSON reports and optical math in Technical English; present the final `PASSED`/`REJECTED` scorecard and prioritized defects to the user in **Portuguese (`pt-BR`)**.
