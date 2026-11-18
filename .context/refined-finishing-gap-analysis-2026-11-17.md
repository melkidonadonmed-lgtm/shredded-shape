# Refined UI Finishing & Gatekeeper Calibration Gap Analysis (`shredded-shape` v1.4.0 -> v1.5.0)

> **Date:** 2026-11-17 | **Evidence Baseline:** Forensic post-mortem of `PCM` (`TASK-18` CLAREZA Refactor) + live execution of `ui_judge_gatekeeper.py --wcag AAA --composite` against `c:\Users\melki\dev\repos\PCM\src` | **Language:** Technical English (`[LOCK-04]` / `[SSOT-UI-04]`)

---

## 1. Executive Summary

During `TASK-18` in `PCM`, the `shredded-shape` v1.4.0 Actor-Critic UI suite (`ui-frontend-analyst`, `ui-clean-worker`, `ui-quality-judge`, and their Python/JS verification gates) enabled clean CSS tokenization, contrast hardening, Dark Mode surface stepping, and primary-view normalization. However, a post-completion EGM review + multi-route headless Chromium inspection revealed **two coupled systemic failures**:

1. **False-Positive Gatekeeper Rejections on Real Vite/React `src/` Trees (`[GAP-04]`):** Running `ui_judge_gatekeeper.py PCM/src --wcag AAA --composite --json` fails (`overall_verdict: "REJECTED"`, `ui_ux_6dim.final_score: 71.0`, `design_tokens: 0.0`, `typography_mobile: 55.0`, plus `18` `AUDIT-A11Y-CLICK-DIV` alerts on modal propagation wrappers) even when `tactile_readiness.readiness_score == 100.0`, `ai_slop_score == 0`, and runtime WCAG/Fitts checks pass.
2. **Scope-Narrowing Incentive & Secondary-View Blind Spots (`[GAP-01..03, 05..06]`):** Because `ui_judge_gatekeeper.py src/` was blocked by unwinnable false positives, the `TASK-18` execution pipeline narrowed its static gatekeeper run to `src/styles`, leaving `~90` TSX components un-audited by Stage 3. Simultaneously, single-route DevTools sampling left collapsed header routes (`MOD-03 Hospitalar`), Unicode arrow pseudo-icons (`⇱`, `⇲`, `⬌`), and CSS utility overrides (`h-8`/`h-9`/`h-10`/`min-h-[32px]` beating `@layer components` `min-height: 44px`) undetected across secondary views (`#hospital`, `#documents/sus`, `#scores`, `#print_preview`, and closed dropdowns/modals).

This document catalogs all **6 verified failure vectors (`[GAP-01]`..`[GAP-06]`)** with exact `file:line` citations in `shredded-shape` v1.4.0 and defines the exact **v1.5.0 remediation specification** ready for implementation.

---

## 2. Empirical Baseline Observed on `PCM/src` (v1.4.0 Gatekeepers)

Running the installed v1.4.0 scripts directly against `c:\Users\melki\dev\repos\PCM\src` yields:

- **`frontend_inventory_and_slop_scanner.py PCM/src --json`:** `verdict: "[PASS]"`, `files_scanned: 207`, `ai_slop_score: 0`, `emoji_hits: 0`, `tokens_defined_count: 244`, `oklch_count: 104`, `light_dark_count: 10` — yet emits `navigation_targets` with only `4` hash literals (`#hospital-ward-module-root`, `#scoreboard-block`, `#scoreboard-catalog`, `/formularios-sus-offline.html`) and `"before_state": "4 routes / 16 <nav> containers competing horizontally"` (mis-counting `.test.tsx` fixtures and unmounted shell modes as `16` simultaneous `<nav>` elements).
- **`ui_judge_gatekeeper.py PCM/src --wcag AAA --composite --json`:** Exits `1` (`overall_verdict: "REJECTED"`):
  - `gatekeeper`: `verdict: "REJECTED"`, `files_audited: 200` (truncated out of `207` eligible files because `__tests__/*.test.*` consumed `30` slots!), `contrast_ratio_min: 8.35`, `findings`: `18 × AUDIT-A11Y-CLICK-DIV` (e.g., `DocumentEditorView.tsx:334`, `EditorLogoConfigDropdown.tsx:71`, `EditorTopActionsBar.tsx:127`, plus `15` findings reported at fallback `:1`).
  - `tactile_readiness`: `readiness_score: 100.0` (`s_a11y: 100.0`, `s_fsm: 100.0`, `s_tokens: 100.0`, `s_sec: 100.0`, `verdict: "PASS"`).
  - `ui_ux_6dim`: `final_score: 71.0` (`FAIL` < `85.0`), `dimension_scores`: `{ design_tokens: 0.0, typography_mobile: 55.0, structure_semantics: 100.0, iconography: 100.0, light_elevation: 100.0, motion_transitions: 100.0 }`, driven by `49` compact A4 print-cell pixel literals (`3px`, `5px` -> `49 × 8.0 = -392` pts), missing root `../index.html` viewport resolution (`-25.0` pts), and print-sheet `11px` rules (`-20.0` pts).

---

## 3. Root-Cause Taxonomy (`[GAP-01]` .. `[GAP-06]`)

### `[GAP-01]` CSS Cascade Layer Inversion (`@layer components` vs. `@layer utilities`) & Zero Static JSX `< 44px` Target Gate

- **Where It Failed:**
  - `skills/ui-clean-worker/scripts/verify_raw_frontend.py` (`_check_single_file`, lines `59-94`)
  - `skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py` (`_check_static_rules`, lines `217-255`)
- **Mechanism:**
  - In Tailwind CSS v4, classes inside `@layer components` (such as `.btn-tactile-primary { min-height: 44px; }` or `.btn-tactile-secondary`) have **lower cascade priority** than classes inside `@layer utilities` (`h-8`, `h-9`, `h-10`, `min-h-[32px]`, `min-h-[36px]`, `min-h-[40px]`, `p-1`, `py-1`, `w-5 h-5`).
  - When secondary components (`HospitalWardModuleView.tsx`, `SusCatalogListView.tsx`, `WatermarkSelector.tsx`, `PrintPreview.tsx`, `EditorLogoConfigDropdown.tsx`, `ScoreCatalogTabSection.tsx`) combined `btn-tactile-primary` + `h-8 min-h-[32px]`, CSS compiled cleanly while silently crushing runtime button height below `44px`.
  - Neither `verify_raw_frontend.py` nor `ui_judge_gatekeeper.py` checks JSX `<button>`, `<a>`, `[role="button"]`, or `[role="tab"]` attributes for sub-`44px` Tailwind height/square sizing utilities lacking `.touch-target` or a `44×44px` hit wrapper.

### `[GAP-02]` Narrow `EMOJI_RE` Range Missing Geometric & Arrow Unicode Pseudo-Icons

- **Where It Failed:**
  - `scripts/_ss_core.py:78` (`EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\U000026A0-\U000026FF\U00002702-\U00002712\U00002728-\U000027B0]")`)
  - `skills/ui-frontend-analyst/scripts/devtools_live_probe.js:85` (`emojiRe = /[\u{1F300}-\u{1FAFF}\u{26A0}-\u{26FF}\u{2702}-\u{27B0}]/gu`)
- **Mechanism:**
  - UI components sometimes use non-emoji geometric/arrow codepoints outside `U+2702..27B0` as pseudo-icons instead of `<Icon />` / verified SVGs — concretely `⇱` (`U+21F1`), `⇲` (`U+21F2`), and `⬌` (`U+2B0C`) in `EditorLogoConfigDropdown.tsx`.
  - Because `U+2190..21FF` (Arrows), `U+27F0..27FF` (Supplemental Arrows-A), `U+2900..297F` (Supplemental Arrows-B), and `U+2B00..2BFF` (Misc Symbols & Arrows) are excluded from both static and live regexes, `emoji_hits: 0` was emitted both statically and in Chromium while raw fallback font arrows shipped in production UI controls.

### `[GAP-03]` Syntactic `<= 6` `<nav>` Item Enforcement Without Postural Macro-Module Reachability Parity

- **Where It Failed:**
  - `skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py:100-121` (`_build_navigation_artifacts`, line `107`: `if len(unique) > 6 or raw_text.count("<nav") > 3`)
  - `rules/frontend-9-axes-guidelines.md`, `skills/ui-clean-worker/SKILL.md`
- **Mechanism:**
  - Enforcing `<= 6` items per `<nav>` and `<= 3` `<nav>` containers purely by syntactic counting creates two perverse failure modes:
    1. **Macro-Module Amputation Across Postures:** To keep `quickNavTabs <= 6` when the sidebar is collapsed, `Header.tsx` omitted Macro-Module `MOD-03` (`Hospitalar`) while retaining two secondary sub-tools (`Protocolos` and `Doses`), stranding collapsed-sidebar users from an entire clinical macro-module.
    2. **Landmark Eviction Gaming:** `Sidebar.tsx` moved primary navigation links (`aria-current="page"`) into a `<div role="region">` outside `<nav>` to stay below `<nav>` item caps, weakening landmark discoverability for assistive technologies.
    3. **String/Test Inflation:** `raw_text.count("<nav")` sums `<nav` matches across all JSX states and unit tests (`16` hits across `207` files on `PCM/src`) rather than evaluating rendered posture parity.

### `[GAP-04]` Composite Gatekeeper False Positives on Real React/Vite `src/` Directories

- **Where It Failed (5 Distinct Bugs):**
  - **`[GAP-04a]` Physical Print-Sheet Bleed into Screen Spacing/Typography (`skills/ui-quality-judge/scripts/ui_ux_frontend_auditor.py:185-248`):**
    - `_collect_spacing_px_checks` (`185-201`) and `audit_typography_and_wcag` (`239-242`) penalize pixel literals inside physical A4/print styles (`.sus-grid`, `@media print`, `a4-and-editor.css`). On `PCM/src`, `49` compact physical print cell values (`3px`, `5px`) wiped out `design_tokens` (`0.0`, penalty `-392`) despite `token_adherence_pct == 87.8%`, and `11px` print labels deducted `-20.0` pts from `typography_mobile`.
  - **`[GAP-04b]` Ancestor `index.html` Viewport Blindness (`ui_ux_frontend_auditor.py:227-229`):**
    - When `target` is `<repo>/src`, `<repo>/index.html` sits in `target.parent`. Any static `.ts`/`.tsx` export template containing `"<html"` (such as `susDocumentsCatalog.ts`) satisfies `"<html" in low` while `parser.viewport_present` stays `False`, falsely deducting `-25.0` pts (`"Set <meta name='viewport' ...>"`).
  - **`[GAP-04c]` Test Directory Pollution & Silent `limit=200` Truncation (`scripts/_ss_core.py:16-19, 155-186` & `ui_judge_gatekeeper.py:260`):**
    - `IGNORED_DIRS` does not exclude `__tests__`, `tests`, `__mocks__`, or `*.test.*`/`*.spec.*` files. On `PCM/src` (`207` UI files), `30` Vitest files are audited as UI components and consume `30` slots of `collect_ui_files(target, limit=200)`, silently dropping files `201..207` (alphabetically `utils/scores/*` or tail `components/*`).
  - **`[GAP-04d]` `PRINT_SHADOW_LEAK_RE` Regex Backtracking & Brace Escape (`ui_judge_gatekeeper.py:40`):**
    - `r"@media\s+print\b[\s\S]*?box-shadow\s*:\s*(?!none\b)[^;}{]+"` suffers two regex flaws: `\s*` can backtrack to empty string so `(?!none\b)` evaluates `" none"` and falsely rejects valid `box-shadow: none;` declarations; and `[\s\S]*?` crosses `}` boundaries out of `@media print` into subsequent normal `@layer components` CSS blocks!
  - **`[GAP-04e]` `DIV_ONCLICK_NO_ROLE_RE` Over-Matching Event-Propagation Shields & `:1` Line-Number Loss (`ui_judge_gatekeeper.py:39, 73-77`):**
    - `<div onClick={e => e.stopPropagation()}>` inside modals/dropdowns (`BackupModal`, `DoctorProfileModal`, `EditorLogoConfigDropdown`) is a backdrop event-containment wrapper, **not** an interactive clickable `<div>` masquerading as a button; additionally, `[^>]*` breaks whenever an inline TSX arrow annotation contains `>` (`onClick={(e: React.MouseEvent<HTMLDivElement>) => ...}`), and `_first_line` returns `:1` whenever attributes span multiple lines.

### `[GAP-05]` Single-Route / Closed-Popover Sampling Illusion in Live DevTools Probe

- **Where It Failed:**
  - `skills/ui-frontend-analyst/scripts/devtools_live_probe.js:35-50` (`for (const el of interactive.slice(0, 200))`)
- **Mechanism:**
  - `devtools_live_probe.js` inspects only currently mounted nodes on the single active route at evaluation time, capped at `200` elements. Secondary routes (`#hospital`, `#documents/sus`, `#scores`, `#print_preview`, `#editor`) and closed interactive overlays (popovers, dropdown menus, dialogs like `EditorLogoConfigDropdown`, `WatermarkSelector`, `LogoGeneratorModal`) receive `0` runtime bounding-box measurements unless the caller explicitly navigates and clicks open each interactive portal.

### `[GAP-06]` Missing Epistemic Scope-Parity Guard Between Subagents & Final Verdict

- **Where It Failed:**
  - `agents/ui-worker.md`, `agents/ui-judge.md`, `skills/ui-quality-judge/SKILL.md`
- **Mechanism:**
  - No rule forbids narrowing `--target <project>/src` down to `<project>/src/styles` after a composite failure, nor enforces an explicit `unverified_routes` / `scope_narrowed` field on `UIJudgeReport`. Consequently, a Stage 2/3 worker subagent can attach an honest `Skepticism Disclaimer` while its parent/final summary still reports `PASSED` / `0` defects / `100/100`.

---

## 4. Actionable v1.5.0 Upgrade Blueprint for `shredded-shape`

| Gap ID | Target Module(s) | Exact v1.5.0 Change Specification |
| :--- | :--- | :--- |
| **`[GAP-01]`** | `verify_raw_frontend.py`, `ui_judge_gatekeeper.py`, `ui-clean-worker` | Add `[A11Y-TARGET-OVERRIDE]` / `WCAG-2.5.8-TARGET`: scan JSX interactive tags (`<button`, `<a`, `role="button"`, `role="tab"`, `input`) for sub-44px Tailwind utilities (`\bh-(?:[0-9]|10)\b`, `\bmin-h-\[(?:[1-3]?[0-9]|4[0-3])px\]\b`, `\bw-(?:[0-9]|10)\b` when height also `< 44px`, `\bp-[01]\b` without `min-h-[44px]`) unless inside exempt `.sus-grid` print containers or paired with `.touch-target` + `min-h-[44px]`. Document Tailwind v4 `@layer utilities` vs `@layer components` precedence hazard in `ui-clean-worker/SKILL.md` Gotchas. |
| **`[GAP-02]`** | `scripts/_ss_core.py`, `devtools_live_probe.js` | Introduce `PSEUDO_ICON_SYMBOL_RE` (covering UI arrow/symbol pseudo-icons in `\u2190-\u21FF`, `\u27F0-\u27FF`, `\u2900-\u297F`, `\u2B00-\u2BFF` e.g. `⇱`, `⇲`, `⬌`, `\u2700-\u27BF` inside button/tab/heading labels) alongside `EMOJI_RE`, excluding typographic punctuation arrows (`→`/`←` in plain prose `<span>`/`<p>`/`aria-hidden` only if opted out or non-icon context — verify carefully on buttons/tabs). Sync identical regex to `devtools_live_probe.js`. |
| **`[GAP-03]`** | `frontend_inventory_and_slop_scanner.py`, `rules/frontend-9-axes-guidelines.md`, `ui-clean-worker/SKILL.md` | Ignore `*.test.*`/`*.spec.*` in `<nav` counts; add **Postural Reachability Parity** contract requiring every declared top-level Macro-Module (`MOD-01..MOD-N`) to remain reachable across expanded, collapsed-sidebar, and mobile postures (`quickNavTabs` / bottom bar), and forbid moving `aria-current="page"` navigation lists out of `<nav>` into `<div role="region">`. |
| **`[GAP-04a]`** | `ui_ux_frontend_auditor.py`, `_ss_core.py` | Isolate `@media print { ... }` blocks and print-sheet CSS/HTML (`.sus-grid`, `FolhaA4`, `a4-and-editor.css`, `@page`) using proper brace-matched CSS block parsing (`_iter_css_blocks` from `_ss_core.py`) before running screen spacing (`8px` grid) and screen typography (`>= 12px`) audits. Keep strict enforcement for all screen CSS rules. |
| **`[GAP-04b]`** | `ui_ux_frontend_auditor.py` | In `evaluate_target(target_path)`, check `(target_path / "index.html")` AND `(target_path.parent / "index.html")` (for `<repo>/src` invocations) for `<meta name="viewport"`; only inspect actual `.html` files for missing viewport metadata (never raw HTML string literals embedded inside `.ts`/`.tsx` bundles). |
| **`[GAP-04c]`** | `scripts/_ss_core.py`, `ui_judge_gatekeeper.py`, `verify_raw_frontend.py` | Add `"__tests__"`, `"tests"`, `"__mocks__"`, `"playwright-report"`, `".storybook"` to `IGNORED_DIRS` and skip `*.test.*` / `*.spec.*` / `*.stories.*` inside `collect_ui_files` (with explicit `--include-tests` opt-in if ever needed). Raise default `collect_ui_files(..., limit=500)` or emit a CRITICAL `SCOPE-TRUNCATED` finding if eligible files exceed `limit` so files are never silently dropped! |
| **`[GAP-04d]`** | `ui_judge_gatekeeper.py` | Replace `PRINT_SHADOW_LEAK_RE` regex with brace-balanced `@media print` extraction via `_ss_core._iter_css_blocks(stripped)`: inspect `box-shadow` declarations strictly inside blocks where `"print" in media_ctx.lower()`, checking exact normalized value `!= "none"`. Fixes both `\s*` backtracking on `box-shadow: none` and cross-brace bleed. |
| **`[GAP-04e]`** | `ui_judge_gatekeeper.py` | Parse JSX `<div ...>` opening tags cleanly without stopping at `=>` generics (`(?:=>|\{[^}]*\}|[^<>])*>` or multi-line span), ignore modal/popover backdrop-stoppers whose handler is strictly `e.stopPropagation()` / `stopPropagation()` (when accompanied by modal `role="dialog"` / trigger semantics), and compute exact line numbers via `stripped[:match.start()].count("\n") + 1` instead of `_first_line()` line-by-line fallback `:1`. |
| **`[GAP-05]`** | `devtools_live_probe.js`, `ui-frontend-analyst` | Remove arbitrary `.slice(0, 200)` truncation (or report `interactiveTruncated` + sample count), add a route+overlay checklist schema (`routeManifest`, `openOverlaysInspected`) supporting multi-route CDP iteration (`#prescription`, `#hospital`, `#documents/sus`, `#scores`, `#print_preview`, `#editor`) plus click-to-open portal verification (`EditorLogoConfigDropdown`, `WatermarkSelector`, modals). |
| **`[GAP-06]`** | `ui-judge.md`, `ui-worker.md`, `ui-quality-judge/SKILL.md`, `ui_judge_gatekeeper.py` | Add `scope_path`, `files_total_eligible`, `truncated: bool`, and `unverified_routes: list[str]` to `UIJudgeReport`. Fail-closed: if `files_audited < files_total_eligible` OR `target` points only to a `styles/` subdirectory when parent `src/` contains `.tsx`/`.html` components, emit `verdict = "UNVERIFIED"` (exit `1`) unless explicitly tagged CSS-only unit run; require parent orchestrators to surface `unverified_routes` instead of declaring `100/100 PASSED`. |

---

## 5. Verification Matrix for Future v1.5.0 Implementation (`tests/test_shredded_shape_suite.py`)

When executing `TASK-05` in `shredded-shape`, every fix above MUST ship with deterministic unit + adversarial regression tests:
1. **`test_cascade_override_catches_sub44px_button`:** Assert `.btn-tactile-primary h-8` and `min-h-[32px]` trigger `[A11Y-TARGET-OVERRIDE]` in `verify_raw_frontend.py` and `ui_judge_gatekeeper.py`, while `touch-target min-h-[44px]` passes.
2. **`test_unicode_arrow_pseudo_icons_rejected`:** Assert `⇱`, `⇲`, `⬌` inside JSX `<button>`/`<span>` labels trigger `AUDIT-VIS-EMOJI` / `[ANTI-SLOP]`.
3. **`test_print_media_brace_and_box_shadow_none`:** Assert `@media print { .card { box-shadow: none; } } .screen-card { box-shadow: 0 2px 6px rgba(...) }` **passes** `CLINICAL-PRINT-SHADOW` (zero backtracking / cross-brace leak), while `@media print { .card { box-shadow: 0 4px 12px rgba(0,0,0,0.2); } }` **fails**.
4. **`test_stop_propagation_modal_wrapper_not_flagged`:** Assert `<div onClick={(e) => e.stopPropagation()}>` does NOT trigger `AUDIT-A11Y-CLICK-DIV`, while `<div onClick={() => openItem()}>` without `role="button"` DOES trigger `AUDIT-A11Y-CLICK-DIV` at its true line number (not `:1`).
5. **`test_pcm_src_composite_benchmark`:** Run `ui_judge_gatekeeper.py c:\Users\melki\dev\repos\PCM\src --wcag AAA --composite` cleanly without narrowing to `src/styles` and verify accurate scoring once `@media print`/`.sus-grid`, ancestor `index.html`, and test exclusions are active.
