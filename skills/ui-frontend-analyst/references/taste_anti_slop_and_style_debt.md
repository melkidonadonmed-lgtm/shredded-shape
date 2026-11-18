# Taste Anti-AI-Slop & Style Debt Registry (12-Vector Audit)

Every Stage 0 forensic scan inspects and scores these **12 concrete AI-Slop & Craft Debt vectors** via `scripts/_ss_core.py` against machined **5-Plane Tactile Matte** and **Nexus 135°** physical baselines.

## 1. The 12-Vector Anti-AI-Slop Checklist

| Vector | Slop / Low-Quality Artifact (`[FAIL]`) | Penalty / Gate | Clean Optical & Craft Replacement (`[PASS]`) |
| :--- | :--- | :--- | :--- |
| **1. Canvas Black & Neon Chroma** | Pure `#000000` OLED crush; `oklch()` with `C > 0.22` (outside `15°..40°` red `<= 0.24`). | `+15..20` / Hard `[FAIL]` | Mineral `OKLCH(0.962 0.007 H)` Light / `OKLCH(0.145 0.014 H)` Dark + `C <= 0.20` accent. |
| **2. Neon Glows & Glowing Card Borders** | `#00ffff`/`#39ff14` neon shadows; glowing cyan active borders (`--neon-*`, `--glow-*`, `--blob-*`). | `+12` / Hard `[FAIL]` | `--light-zenith-hover` radial sheen (`0.11`) + `--rim-top-strong` lip (`inset 0 1px 0`) + `-2px` lift. |
| **3. Blur Blobs & Floating Bloops** | `filter: blur(>=40px)` / Tailwind `blur-3xl` floating circles behind cards (`aria-hidden` bloat). | `+10` / `[FAIL]` | Recessed `--bg-well` slots (`--shadow-well`) + anodized `--bg-card` surfaces (`--shadow-elevation-2`). |
| **4. Confetti Multicolored Pills** | `>= 3` colored badge classes (`.tag.warn/.danger/.ok`, rainbow translucent pills per card). | Hard `[FAIL]` | Neutral carved `.engraved-pill` (`--bg-well` + `--shadow-well`) paired with `6px` `.lum-bead` status LED. |
| **5. Dashed Wireframe Containers** | Layout/flow boxes using `border: 1px dashed` (`DASHED_BOX_SLOP_RE`, excluding `:focus-visible`). | Hard `[FAIL]` | Carved recessed `.inset-panel` tracks (`--shadow-well`) or hairline `1px` rules (`--border-side`). |
| **6. Amateur Inline SVGs & Mixed Icons** | Empty `<svg></svg>`, missing `viewBox`, `<circle>` cloud bloops, emojis, Unicode/ASCII pseudo-icons (`+`/`×`/`≡`/`▾`/`▸`/`←`/`→`), or 2+ icon libraries. | `+10..30` / `[FAIL]` | Single-library `24x24` stroke `<symbol>` paths (Lucide / Material / `@fluentui/react-icons`, `npx svgo`). |
| **7. Flat Unlit Dark Cards** | Plain matte rectangles lacking `--light-zenith` top gradient sheen or `color-mix(in oklab)` states. | Optical Debt | 5-Plane Machined Hierarchy (`--bg-well` < `--bg-canvas` < `--bg-card` < `--bg-card-lit` < `--bg-key`). |
| **8. Typography & MDN Debt** | `text-rendering: optimizeLegibility` on `body` (hurts INP); missing `font-optical-sizing: auto`; `< 12px` micro-fonts; `> 75ch`. | `+5..8` | `text-rendering: auto` on body, `optimizeLegibility` strictly on `h1..h3`, `clamp()`, `65ch`, `tabular-nums`. |
| **9. Cramped Dual-Sidebar Squeeze** | 3-pane desktop squeeze clipping pills/badges (`scrollWidth > clientWidth`) + `divsoup > 0.45`. | Layout `[FAIL]` | Adaptive `Expanded` split (`248px <-> 64px`) or `12`-col Bento (`gap >= 16px`), Flexbox `min-inline-size: 0`, HTML5 landmarks. |
| **10. Monoliths & Missing FSM** | Single UI files `> 600` lines; fake `setTimeout` data; missing `loading`/`empty`/`error` states; raw `innerHTML`. | Split Gate / XSS `[FAIL]` | Domain split `<= 600` lines/file (`<= 60` lines/fn), executable 5-state FSM, and `DOMPurify.sanitize()`. |
| **11. Layout-Thrashing Reflow Motion** | `transition: all | width | height | top | left | margin | padding`; modals without `@starting-style` + `allow-discrete`. | `+12..45` / `[FAIL]` | GPU `transform` & `opacity`, `0fr -> 1fr` accordions, standalone `transition-behavior: allow-discrete`, `@media (prefers-reduced-motion: reduce)`. |
| **12. Visual/Tab Desync & Touch Sprawl** | `flex-direction: row-reverse`, positive `order`/`tabindex`, `> 6` stacked tabs, `outline: none` without `:focus-visible`, `< 44px`/`48px` targets. | Critical A11y `[FAIL]` | Exact `DOM == Tab Order`, `<= 6` nav items per `<nav>`, `:focus-visible`, `min-block-size >= 44px` (`48px` `any-pointer: coarse`). |

## 2. Diagnostic Priority & Scanner Alignment
1. **Structural & Zero-Trust Blockers (`#1–#6`, `#11–#12`):** `frontend_inventory_and_slop_scanner.py` and `verify_raw_frontend.py` fail fast on pure black, neon chroma, blobs, confetti, dashed wireframes, UI emojis, pseudo-icons (`_ss_guards.find_pseudo_icon_hits`), explicit `< 40px` hit-target overrides (`_ss_guards.find_target_size_overrides`), reflow transitions, and visual/tab order inversion while keeping `__tests__/` and `.ts` A4 print templates isolated.
2. **Modular Splits Across Multi-File Bundles (`#10`):** Multi-file scans flag every `.html`/`.css`/`.js`/`.tsx` file exceeding `600` lines in `before_after_proposals` (`target_pattern: "route_split"`), not just single-file scans.
3. **UI Color Mixing Guidance:** Flag `color-mix(in oklch, ...)` in UI hover/border declarations (`OPTICS-COLOR-MIX-OKLAB`) and recommend `color-mix(in oklab, ...)` to prevent Chromium gamut-arc shifts.
