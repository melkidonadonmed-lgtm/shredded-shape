# WCAG 2.2 `OKLab` Polarity Math, Theme Resolution & Actor-Critic Rubric

All luminance checks run via `scripts/_ss_core.py` using Björn Ottosson's exact `OKLab -> LMS^3 -> linear sRGB -> CIE 1931 Y` conversion (`FNR < 0.001`).

## 1. Exact Björn Ottosson `OKLab -> WCAG Y` Benchmarks
Never approximate lightness via `L^1.8` (which over-estimates mid-gray `Y(0.50)` as `0.287` instead of true `0.125`).

| Input `oklch(L C H)` | True WCAG Luminance (`Y`) | Verdict & Threshold Impact |
| :--- | :--- | :--- |
| `oklch(0.50 0 0)` | `0.125` | Mid-gray reference (`abs <= 1e-3`). Needs `L <= 0.42` vs light or `L >= 0.72` vs dark for `4.5:1`. |
| `oklch(0.145 0.014 260)` | `~0.013` | Clean matte Dark canvas (`well=0.118 < canvas=0.145 < card=0.195 < card-lit=0.235`). |
| `oklch(0.962 0.007 250)` | `~0.905` | Clean matte Light canvas; `#000000` (`Y = 0.0`) hard-rejects (`OPTICS-NO-BLACK`). |
| `#ef4444` (`oklch(0.64 0.208 25.3)`) | `~0.24` | Valid semantic danger accent (`15° <= H <= 40°`, `C <= 0.24`). |
| `#00ffff` / `oklch(0.75 0.30 195)` | Out-of-bounds | Hard `[REJECTED]` via HSL saturation check (`s >= 0.99`) or `C > 0.22` (`OPTICS-NO-NEON`). |

## 2. Polarity-Isolated `[data-theme]` & 5-Plane Resolution Rules
`_ss_core.extract_theme_oklch_maps()` isolates `:root:light`, `:root:dark`, `@media (prefers-color-scheme: dark|light)`, `.dark`/`.light`, and every `[data-theme="<name>"]` block:
1. **No Cross-Theme Contamination:** Each named `[data-theme]` block infers polarity (`color-scheme: dark|light` or canvas/card `L < 0.50`) and inherits missing tokens (`--ink-*`, `var(--alias)`) strictly from matching `:root:dark` or `:root:light`.
2. **Primary Surface Contrast Tracking:** `contrast_ratio_min` tracks `--ink-primary` / `--text-primary` against `--bg-card` (`--surface-card`) and `--bg-canvas` (`>= 4.5:1` AA; `>= 7.0:1` AAA or automatic AAA escalation on `clinical-day`, `clinical-night`, or `.sus-grid`).
3. **Keycap, Muted Ink, Focus Scope & Dark Elevation:** Verify `--ink-secondary`/`--ink-muted` vs canvas and `--ink-on-key` vs `--bg-key` (`>= 4.5:1`), interactive-only `:focus-visible` (`>= 3:1`, never suppressed without replacement; never paint unintended outlines on non-interactive `<main tabindex="-1">` landmarks), `>= 44x44px` hitboxes (including swatches & range inputs), plus Dark Mode surface order `well < canvas < card < card-lit` (`OPTICS-DARK-ELEVATION`).
4. **Mix & File Cap Checks:** Emit `WARNING` (`OPTICS-COLOR-MIX-OKLAB`) on `color-mix(in oklch)` UI rules; keep all UI files `<= 600` lines.

## 3. Composite Scorecards (`--composite`) & Termination Bound
| Gate Script | Passing Threshold | Hard Critical Rejections / Fail-Closed `UNVERIFIED` |
| :--- | :--- | :--- |
| **`ui_judge_gatekeeper.py`** | `verdict == "PASSED"`, `findings == []` critical, `contrast_ratio_min >= 4.5` (`7.0` AAA), `truncated == false`, `scope_narrowed == false` | `REJECTED`: `#000000`, `C > 0.22`, neon/blobs/confetti/wireframes, bad SVGs, emojis, pseudo-icons (`+`/`×`/`≡`), `< 40px` hit targets, `<div onClick>` (balanced JSX scan), print `box-shadow` leaks, raw `innerHTML`, missing `:focus-visible`. `UNVERIFIED`: file limit truncation or `styles/` narrowing with parent TSX/HTML siblings. |
| **`audit_tactile_ui.py`** | 4-Pillar Readiness `>= 90.0` | Missing 5-Plane/`--surface-*` semantic tokens, flat shadows, missing FSM attributes, `tabular-nums`, or reduced-motion rules (excluding `__tests__`). |
| **`ui_ux_frontend_auditor.py`** | 6-Dim UI/UX `>= 85.0` (`evaluate_target()` isolates markup, `.ts` print templates, and parent `index.html` viewport) | Mixed icon packs, body `optimizeLegibility`, arbitrary non-4px screen margins/padding, `transition: all/width/height`, `< 12px` screen text, `divsoup > 0.45`, DOM depth `> 12`. |
- **Actor-Critic Bound:** Loop feedback back to `ui-worker` for at most `max_self_refine_rounds = 3` before escalating unresolved blockers.
