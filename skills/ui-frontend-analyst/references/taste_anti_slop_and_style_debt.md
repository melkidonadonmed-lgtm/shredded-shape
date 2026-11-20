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
| **10. Monoliths, Fake Data & Missing FSM** | Single UI files `> 600` lines; fake `setTimeout` data; invented metrics (`"99.98% UPTIME"`, `"124ms AVG"`), `"LABEL // YEAR"` headers; missing `loading`/`empty`/`error` states; raw `innerHTML`. | Split Gate / XSS `[FAIL]` | Domain split `<= 600` lines/file (`<= 60` lines/fn), real/explicitly labeled placeholder metrics, executable 5-state FSM, and `DOMPurify.sanitize()`. |
| **11. Layout-Thrashing Reflow Motion** | `transition: all | width | height | top | left | margin | padding`; modals without `@starting-style` + `allow-discrete`. | `+12..45` / `[FAIL]` | GPU `transform` & `opacity`, `0fr -> 1fr` accordions, standalone `transition-behavior: allow-discrete`, `@media (prefers-reduced-motion: reduce)`. |
| **12. Visual/Tab Desync & Touch Sprawl** | `flex-direction: row-reverse`, positive `order`/`tabindex`, `> 6` stacked tabs, `outline: none` without `:focus-visible`, `< 44px`/`48px` targets. | Critical A11y `[FAIL]` | Exact `DOM == Tab Order`, `<= 6` nav items per `<nav>`, `:focus-visible`, `min-block-size >= 44px` (`48px` `any-pointer: coarse`). |

## 2. Extended Craft, Layout & AppSec Debt Patterns (`v1.6.0`)
| Defect Pattern | Failing Signal (`[FAIL]` / `WARNING`) | Clean Craft Replacement (`[PASS]`) |
| :--- | :--- | :--- |
| **Gradient Text Clip** | `background-clip: text` + `transparent`, or Tailwind `bg-clip-text text-transparent`. | Crisp solid OKLCH ink (`--ink-primary`) and typographic weight hierarchy (`ANTI-SLOP-GRADIENT-TEXT`). |
| **Decorative Side-Stripes** | Thick colored `border-left >= 3px` (`border-l-4`) on generic cards/menus (qualitative heuristic). | Clean uniform surface with zenithal bevel (`inset 0 1px 0`) and subtle `::before` active rail bars. |
| **Hyper-Rounded & Fake Chrome** | Pill-shaped cards (`> 16px`), fake `01/02/03` non-sequential counters, ALL-CAPS `EXPLORE` eyebrows. | Disciplined `6px–16px` card radii (pills reserved for `.engraved-pill` tags) and concise microcopy. |
| **Mystery Nav & Card `@media`** | Icon-only `<nav>` without label/tooltip; `@media (min-width)` inside isolated cards; `grid-auto-flow: dense`. | `:is(:hover, :focus-visible)` tooltips on rails, `@container` + `cqw` inside cards, natural DOM flow. |
| **Client Secrets & Omissions** | `NEXT_PUBLIC_*`/`VITE_*` secret keys (`AUDIT-SEC-ENV-LEAK`), `// ... rest of code` (`AUDIT-STUB-PLACEHOLDER`), raw `.innerHTML`/`eval`. | Server-only secrets (`[REDACTED]` logging), full code implementation, per-sink `DOMPurify.sanitize()`. |
| **`<feColorMatrix>` Isolation** | Combining `<feGaussianBlur>` + `<feColorMatrix>` inside the **same** `<filter>` block (`has_gooey_filter_blob`). | Keep duotone/daltonism `<feColorMatrix>` filters inside standalone `<filter>` elements separate from any blur filter. |

## 3. Diagnostic Priority & Scanner Alignment
1. **Structural & Zero-Trust Blockers (`#1–#6`, `#11–#12` + `v1.6.0`):** `frontend_inventory_and_slop_scanner.py` and `verify_raw_frontend.py` fail fast via `_ss_craft_guards.py` and `_ss_guards.py` while keeping `__tests__/`, `.ts` A4 print templates, and standalone `<feColorMatrix>` filters isolated.
2. **Modular Splits Across Multi-File Bundles (`#10`):** Multi-file scans flag every `.html`/`.css`/`.js`/`.tsx` file exceeding `600` lines in `before_after_proposals` (`target_pattern: "route_split"`).
3. **UI Color Mixing Guidance:** Flag `color-mix(in oklch, ...)` in UI hover/border declarations (`OPTICS-COLOR-MIX-OKLAB`) and recommend `color-mix(in oklab, ...)` to prevent Chromium gamut-arc shifts.
