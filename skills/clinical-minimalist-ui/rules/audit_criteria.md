# Clinical Minimalist UI — Audit Criteria (`clinical-minimalist-ui`)

1. **WCAG 2.2 AAA, 3-Layer Clinical Nav & Anti-Slop Sterility:**
   - `[PASS]` All text/vitals/alerts reach `>= 7.0:1` (`--wcag AAA`), dark surfaces use matte `OKLCH` with crisp rim hairlines (zero `#000000`), tabular numerals cover every clinical metric, body sets `text-rendering: auto`, navigation uses unique `<nav aria-label>` + silent CSS `::before` breadcrumbs + GPU `.skip-link`, and icons use ONE clean SVG library (`Material Symbols` or `Lucide`).
   - `[FAIL]` Contrast `< 7.0:1`, `#000000` OLED crush, neon chromatic pollution (`C > 0.22` outside red `15°..40°`), blur blobs, confetti badges, dashed wireframes, gradient text, decorative side-stripes, mystery icon-only nav, reflow animations, emojis in clinical controls, amateur SVGs, or `forwardRef`.

2. **A4 `.sus-grid` Print & Calculator Integrity:**
   - `[PASS]` `@media print` enforces `@page { size: A4; margin: 12mm; }`, strips `box-shadow` and `backdrop-filter`, preserves `.sus-grid` vector hairlines, honors Stage Role Guards, and passes deterministic calculator bounds + `ui_judge_gatekeeper.py --wcag AAA --composite`.
   - `[FAIL]` Dark background or screen shadows leaking into print, clipped tables (`!break-inside: avoid`), non-tabular clinical numbers, or mutated files during read-only stages (`ui-analyst`/`ui-planner`/`ui-judge`).
