---
name: ui-quality-judge
description: "Use when running the read-only Actor-Critic WCAG 2.2 AA/AAA OKLab judge (FNR < 0.001), 4-Pillar Readiness (>= 90), 6-Dim UI/UX (>= 85), isolated print/test checks, fail-closed UNVERIFIED scope gates, WAI-ARIA, 48x48px targets, anti-XSS, and anti-AI-Slop, returning PASSED, REJECTED, or UNVERIFIED. Do NOT use for writing UI code."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv)"
metadata:
  author: shredded-shape
  version: "1.5.0"
  updated_at: "2026-11-18"
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
     - Plugin path (`pwsh`/POSIX): `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py" <target> --wcag AA --composite --json` (or `"%USERPROFILE%\.gemini\..."` in `cmd.exe`)
     - Repo fallback: `uv run python skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py <target> --wcag AA --composite --json`
   - Pass `--wcag AAA` explicitly on clinical/EHR/medical routes (or let `--composite` auto-escalate on `.sus-grid`).

2. **Phase 2 — Polarity-Isolated Björn Ottosson `OKLab` & Anti-Slop Audit:**
   - Audit findings against [`references/wcag22_oklch_actor_critic_rubric.md`](references/wcag22_oklch_actor_critic_rubric.md) and [`rules/audit_criteria.md`](rules/audit_criteria.md).
   - Verify contrast per `:root` and every `[data-theme]` polarity block (`>= 4.5:1` AA, `>= 7.0:1` AAA/clinical, Dark elevation `well < canvas < card < card-lit`, zero `#000000`, `C <= 0.22` cap, semantic red `15°..40°` `<= 0.24`, zero neon/blobs/confetti/dashed wireframes/amateur SVGs, warn on `color-mix(in oklch)`).

3. **Phase 3 — Static WAI-ARIA, Ergonomics, File Caps & Security Check:**
   - Verify static WAI-ARIA semantics (`role="group"` + `<button aria-pressed>`, zero clickable `<div>`), `DOM == Tab Order`, `:focus-visible` (`>= 2px`), `>= 44x44px` (`48x48px` coarse touch), `divsoup <= 0.45`, per-file DOM depth isolation across `.html`/`.tsx`/`.vue`, `<= 600` lines/file, zero layout reflow transitions, Next.js 15+ `await params`, and zero unsanitized HTML sinks.
   - Pair with `a11y-debugging` from `chrome-devtools-plugin` when inspecting a live browser URL.

4. **Phase 4 (`[Self-Refine]`) — Structured Actor-Critic Verdict (`PASSED` / `REJECTED` / `UNVERIFIED`):**
   - Return `UNVERIFIED` (fail-closed) whenever file scanning truncates (`truncated == true`), audit scope narrows into `styles/`/`css/` while parent siblings exist (`scope_narrowed == true`), or target files are missing.
   - Return `PASSED` only if scope is complete and all composite sub-auditors clear (`gatekeeper.verdict == "PASSED"`, `tactile_readiness.readiness_score >= 90`, `ui_ux_6dim.final_score >= 85`, zero critical findings across interactive components and global CSS).
   - Otherwise return `REJECTED` with exact `[file:line]` fixes (using balanced JSX `<div onClick>` parsing and masking `.ts`/`@media print` A4 templates without exempting screen CSS) and `refinement_round` (`1..3`), bounded to `<= 3` cycles before `HITL_ESCALATION_REQUIRED`.

## Gotchas
- **Never Narrow to `styles/` Alone:** Auditing CSS without component siblings misses TSX `<div onClick>`, pseudo-icons, and modal traps, triggering fail-closed `UNVERIFIED`.
- **Print Templates vs. Screen CSS:** `.sus-grid` / `@media print` / `.ts` HTML print templates are masked separately from screen CSS (`>= 12px` typography and contrast still apply to `globals.css`).
- **Named `[data-theme]` Polarity Mixing:** Single-polarity `[data-theme]` blocks inherit fallback `--ink-*` tokens strictly from the matching `:root` polarity (`dark` vs `light`), preventing false cross-theme failures.
- **External JS/TS Separation in DOM Parsing:** Composite audits isolate `.js`/`.css`/test files cleanly; single-file `.tsx`/`.jsx` targets avoid false global-CSS token deductions.
- **No Unfounded `axe-core` Claims:** Built-in scripts perform deterministic static checks unless live `chrome-devtools-plugin` runs against a served URL.

## Output
- Unified composite JSON (`overall_verdict`: `PASSED | REJECTED | UNVERIFIED`, `gatekeeper`, `tactile_readiness`, `ui_ux_6dim`, `scope_narrowed`, `unverified_routes`).
- Actionable fix list if `REJECTED` (capped at `3` refinement cycles).

## User Communication
Keep JSON reports and optical math in Technical English; present the final `PASSED`/`REJECTED` scorecard and prioritized defects to the user in **Portuguese (`pt-BR`)**.
