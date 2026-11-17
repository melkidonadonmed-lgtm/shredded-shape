# UI Quality Judge — Audit Criteria (`ui-quality-judge`)

1. **Multi-Pillar Thresholds (`--composite`):**
   - `[PASS]` `ui_judge_gatekeeper.py` returns `PASSED` across `:root` and all `[data-theme]` polarity maps (`>= 4.5:1` AA or `>= 7.0:1` AAA on clinical/`.sus-grid` routes, Dark surface progression `well < canvas < card < card-lit`), `audit_tactile_ui.py` Readiness `>= 90.0`, `ui_ux_frontend_auditor.py` Score `>= 85.0`, `divsoup <= 0.45`, files `<= 600` lines, `color-mix(in oklab)`, and clean static WAI-ARIA + XSS posture.
   - `[FAIL]` Contrast `< 4.5:1` (`< 7.0:1` clinical), `#000000`, `C > 0.22` (`> 0.24` red), HSL neon glows, blur blobs, confetti pills, dashed wireframes, reflow transitions (`all`, `width`, `height`), empty or circle-cloud `<svg>` icons, clickable `<div>` buttons, missing `:focus-visible`, `< 44px`/`48px` hit targets, `innerHTML` without `DOMPurify`, or clinical `box-shadow` inside `@media print`.
