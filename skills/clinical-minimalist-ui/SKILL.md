---
name: clinical-minimalist-ui
description: "Use when auditing, designing, planning, or building clinical interfaces, electronic health records (EHR/PEP dashboards), A4 vector print sheets (.sus-grid), and medical calculators with WCAG AAA precision and zero AI slop. Do NOT use for generic SaaS, e-commerce, or non-clinical dashboards."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv) and Modern CSS"
metadata:
  author: shredded-shape
  version: "1.5.0"
  updated_at: "2026-11-18"
  category: domain-ui-pack
  tags:
    - clinical
    - ehr
    - pep
    - ".sus-grid"
    - medical-calculators
    - wcag-aaa
    - a4-print
---

# Clinical Minimalist UI & A4 Vector Print Pack (`clinical-minimalist-ui`)

## Overview
Domain specialty skill enforcing clinical sterility, high-stakes **WCAG 2.2 AAA (`>= 7.0:1`)** legibility, **A4 `@page` `.sus-grid` millimeter-accurate print sheets**, and deterministic medical calculators across the 4-stage Actor-Critic workflow.

## Inputs
- Target EHR/PEP component, prescription/exam sheet, or clinical risk calculator scope.
- Active Actor-Critic stage role (`ui-analyst`, `ui-planner`, `ui-worker`, or `ui-judge`).

## Procedure
Respect strict **Stage Role Guards**: operate **read-only** when bound inside `ui-analyst`, `ui-planner`, or `ui-judge`; mutate source files **only** when invoked inside `ui-worker` or direct feature execution.

1. **Phase 1 — Clinical Polarity & `OKLCH` Safety Calibration:**
   - Apply [`references/clinical_polarities_architecture.md`](references/clinical_polarities_architecture.md) and [`references/clinical_a4_tokens_guide.md`](references/clinical_a4_tokens_guide.md): Day Clinic Light (`OKLCH(0.985 0.006 240)`) + Night Shift Dark (`OKLCH(0.165 0.015 245)`, never `#000000`), enforcing `>= 7.0:1` WCAG AAA contrast on dosages, lab alerts, and patient identifiers.
   - Constrain primary chrome accents to `C <= 0.12` (`_ss_core` `clinical` preset; semantic status ok/warn `C <= 0.16`) and restrict clinical red alerts (`15°..40°` hue) to `C <= 0.24`. Zero neon glows, blur blobs, or decorative slop.

2. **Phase 2 — Typography, Single-Library SVGs & Clinical Data Clarity:**
   - Use `font-variant-numeric: tabular-nums;` on all lab values, timestamps, and doses; set `text-rendering: auto; font-optical-sizing: auto;` on `body` (protects form INP latency) and `optimizeLegibility` strictly on `h1..h3`.
   - Use a single clean SVG library (`Material Symbols` or `Lucide`, `24x24` crisp stroke vectors) for vitals/alerts; zero Unicode emojis or amateur circle-cloud SVGs.

3. **Phase 3 — A4 `.sus-grid` Vector Print Projection (`@media print`):**
   - Implement `@page { size: A4; margin: 12mm; }` with `.sus-grid` hairline vector rules (`0.25mm`), forced Light high-contrast black-on-white print polarity (`color-adjust: exact`), zero `box-shadow`/`backdrop-filter` in print, and explicit `break-inside: avoid;` on prescription/signature blocks.

4. **Phase 4 — Calculator & Verification Gate:**
   - Isolate deterministic medical calculator logic (`<= 60` lines/function, unit-tested boundary validation) and verify via `ui-quality-judge` with `--wcag AAA --composite` before clinical release.

## Gotchas
- **Stage Role Isolation:** Never write files when invoked from read-only `ui-planner` or `ui-judge` personas; emit token specifications or `--wcag AAA` rejection findings only.
- **Clinical Alert Red Exception:** True critical alerts use `15°..40°` hue with `C <= 0.24` (e.g. `#ef4444`); arbitrary magenta/cyan neons remain strictly forbidden.
- **Print Ink Bleeding & Template Isolation:** Leaving dark glass fills or screen `box-shadow` active inside `@media print` ruins medical prescriptions; static `.ts` HTML prescription catalogs (`susDocumentsCatalog`) must stay isolated from interactive screen `globals.css` (`>= 12px` legibility remains mandatory for all interactive UI controls).

## Output
- WCAG AAA compliant PEP/EHR layout, deterministic medical calculator UI, and pixel/millimeter-clean A4 `.sus-grid` print CSS verified by `ui_judge_gatekeeper.py --wcag AAA`.

## User Communication
Keep CSS tokens, `.sus-grid` classes, and clinical formula docs in Technical English; explain ergonomic decisions, print checks, and AAA scorecards to the user in **Portuguese (`pt-BR`)**.
