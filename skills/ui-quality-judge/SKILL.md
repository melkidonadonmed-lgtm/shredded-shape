---
name: ui-quality-judge
description: "Use when running the read-only Actor-Critic Quality and Accessibility Gatekeeper (WCAG 2.2 AA/AAA OKLCH contrast FNR<0.001, 48x48px targets, :focus-visible, DOM==Tab order, anti-XSS, anti-AI-Slop, and FSM checks) returning PASSED or REJECTED. Do NOT use for writing UI code or authoring DESIGN.md."
compatibility: "Antigravity 2.0, Python 3.12+, Jest/Vitest/Playwright"
metadata:
  author: "Shredded-Shape"
  version: "1.0.0"
  updated_at: "2026-11-16"
  category: "Read-Only Actor-Critic UI/UX Quality & WCAG 2.2 Gatekeeper"
  tags: ["ui-quality-judge", "wcag-2-2", "oklch", "actor-critic", "self-refine", "a11y", "anti-xss", "fsm", "anti-slop", "audit_tactile_ui", "ui_ux_frontend_auditor", "juiz-ui"]
---

# `ui-quality-judge` — Read-Only Actor-Critic UI/UX & WCAG 2.2 Judge

## 1. Overview & Scope

Executes deterministic static, mathematical, and accessibility gates on frontend deliverables under strict Least Privilege (read-only sandbox), issuing `PASSED` or `REJECTED` JSON verdicts to trigger surgical `Self-Refine` loops in `ui-clean-worker`.

- **When NOT to Use:** Do NOT use to edit/write UI code (`ui-clean-worker`), diagnose greenfield brand/style specs (`ui-brand-ux-planner`), perform live browser inventory (`ui-frontend-analyst`), or run backend-only tests (`test-quality-auditor`).

## 2. Inputs & Prerequisites

- **`target_path` (required) & `wcag_level` (optional):** Frontend `.tsx`/`.css`/`.html` directory or file; `AA` (default, `>= 4.5:1`) or `AAA` (`>= 7.0:1`).
- **Engines & Rubric:**
  - [scripts/ui_judge_gatekeeper.py](scripts/ui_judge_gatekeeper.py) (`--target <path> [--wcag AA|AAA] --json`)
  - [scripts/ui_ux_frontend_auditor.py](scripts/ui_ux_frontend_auditor.py) & [scripts/audit_tactile_ui.py](scripts/audit_tactile_ui.py)
  - [references/wcag22_oklch_actor_critic_rubric.md](references/wcag22_oklch_actor_critic_rubric.md)

## 3. Step-by-Step Procedure

1. **Run Primary WCAG 2.2 & OKLCH Gatekeeper:** Execute `ui_judge_gatekeeper.py --target <path> --wcag <AA|AAA> --json` computing CIE 1931 $Y$ perceptual OKLCH contrast ratios ($FNR < 0.001$) and file SHA-256 checksums.
2. **Run Complementary Tactile & Optical Auditors:** Run `ui_ux_frontend_auditor.py` and `audit_tactile_ui.py` to cross-verify 3-layer light shadows, dark-mode rim/halo illumination, `@container`/`subgrid`, Base64 `< 50KB`, and Real-State FSM.
3. **Verify 5 Mandatory Batteries:** (A) OKLCH Contrast & zero `#000000` / zero neon; (B) Touch targets `>= 48x48px` (`any-pointer: coarse`); (C) `:focus-visible` + zero `outline: none`; (D) `DOM == Visual Order` (ban `order`/`row-reverse`); (E) `prefers-reduced-motion`, anti-XSS, and zero UI emojis.
4. **Emit Verdict & Loop Control:** Issue `PASSED` to clear merge, or `REJECTED` with exact `file:line` `[OBSERVED FACT]` findings to `ui-clean-worker`.

## 4. Gotchas & Edge Cases

- **Strict Read-Only Mandate:** Never edit `.tsx`/`.css`/`.html` files inside this skill or `ui-judge`.
- **Anti-Gaming Rejections:** Immediately flag comment-gamed FSM strings (`// idle loading error`) and single-pass `rgba(0,0,0)` shadows.
- **Stop Criteria:** Emit `UNVERIFIED` if no eligible frontend source files exist at `target_path`.

## 5. Output Schema & Validation Criteria

Emit structured `UIJudgeReport` JSON (`verdict: PASSED | REJECTED`, `contrast_ratio_min`, `sha256_hashes`, `findings`) conforming to [rules/audit_criteria.md](rules/audit_criteria.md).

## 6. User Communication Rule

Always formulate all direct user-facing conversation, audit verdicts, violation explanations, and summaries in **Portuguese (Brazil / `pt-BR`)**, unless the user explicitly requests otherwise.
