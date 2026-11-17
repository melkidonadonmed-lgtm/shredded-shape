# Clinical Minimalist UI — Audit Criteria (`clinical-minimalist-ui`)

1. **WCAG 2.2 AAA & Anti-Slop Sterility:**
   - `[PASS]` All text/vitals/alerts reach `>= 7.0:1` (`--wcag AAA`), dark surfaces use matte `OKLCH` with crisp rim hairlines (zero `#000000`), tabular numerals cover every clinical metric, body text sets `text-rendering: auto`, and icons use a single clean SVG library (`Material Symbols` or `Lucide`).
   - `[FAIL]` Contrast `< 7.0:1`, `#000000` OLED crush, neon chromatic pollution (`C > 0.22` outside semantic red `15°..40°`), blur blobs, confetti badges, dashed wireframes, reflow animations, emojis in clinical controls, amateur SVGs, or `forwardRef` legacy patterns.

2. **A4 `.sus-grid` Print & Calculator Integrity:**
   - `[PASS]` `@media print` enforces `@page { size: A4; margin: 12mm; }`, strips `box-shadow` and `backdrop-filter`, preserves `.sus-grid` vector hairlines, honors Stage Role Guards, and passes deterministic calculator bounds + `ui_judge_gatekeeper.py --wcag AAA --composite`.
   - `[FAIL]` Dark background or screen shadows leaking into print, clipped tables (`!break-inside: avoid`), non-tabular clinical numbers, or mutated files during read-only stages (`ui-analyst`/`ui-planner`/`ui-judge`).
