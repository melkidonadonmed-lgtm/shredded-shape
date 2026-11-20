# Curated Color Palettes, Stitch SaaS Tokens & Unslop Direction

> **Attribution:** Direction brief, 9-pass redline order, neutral ramps, and copy/chart restraint adapted in part from `unslop` by Damir Sokolovsky (`@heydamir`, `https://heydamir.design/unslop`), licensed under **CC BY 4.0**. Keep this credit in copies and adaptations.

## 1. The 5-Line Direction Brief (Before Touching Code)
Derive from the product itself—never from trends or generic adjectives (`clean`, `modern`, `sleek`, `minimal`, `premium`):
- **Product:** What it does and for whom in 1 plain sentence.
- **Character:** 2–3 concrete words (e.g., `calm, exact, warm` or `fast, technical, tactile`).
- **World:** Physical place or material (paper/ink, night studio, coastal stone, botanical glass) that tints neutrals and accent.
- **Moments:** 1–2 spots carrying rich color/craft (a main chart, rendered product object, or live canvas); keep all surrounding chrome quiet.
- **Signature:** 1 consistent product-specific detail (live status dot, keycaps, IPA chip, route line—never 5).
- **Template Check:** If swapping the product name still fits another app, sharpen copy, visual moment, and signature.

## 2. 9-Pass Redline Order (Finish Each Pass Before the Next)
1. **Spacing (`4px` grid)** -> 2. **Color (1 ramp + 1 accent)** -> 3. **Icons (1 set, `16–18px`, `1.5` stroke, zero emojis)** -> 4. **Copy (plain, sentence case, zero `!`, zero `"Welcome back!"`, no trailing periods on labels)** -> 5. **Type (`400–600` weights, `tabular-nums`, zero negative tracking `< 16px`)** -> 6. **Layout (real proportions, asymmetric split/scene hero)** -> 7. **Details (concentric radii, 1 main chart + ranked list, numbers-only stat cards)** -> 8. **Visuals (real product view or 1 scene, zero blobs/orbs)** -> 9. **Motion (`cubic-bezier(0.22, 1, 0.36, 1)`, zero `transition-all` / `animate-pulse` on static items)**.

## 3. Curated Color Models (`OKLCH 60-30-10` Ready)

### A. Midnight Noir *(Studio Dark / Technical Slate)*
| Swatch Hex | OKLCH Approx | Suggested Role |
| :--- | :--- | :--- |
| `#0B1017` | `oklch(0.16 0.016 255)` | `--bg-well` / Dark canvas (`60%`) |
| `#1C2733` | `oklch(0.26 0.024 248)` | `--bg-card` / Structural panel (`30%`) |
| `#36495C` | `oklch(0.40 0.038 245)` | `--bg-card-lit` / Active row / hairline base |
| `#677C92` | `oklch(0.58 0.042 246)` | `--ink-muted` / Secondary slate accent |
| `#AEBFCE` | `oklch(0.79 0.028 242)` | `--ink-secondary` (Dark) / Light border |
| `#E9EEF2` | `oklch(0.95 0.008 240)` | `--ink-primary` (Dark) / Light canvas |

### B. Horizon Code *(Cloud / Developer SaaS — Dark Navy + Warm Cream Highlight)*
| Swatch Hex | OKLCH Approx | Suggested Role |
| :--- | :--- | :--- |
| `#0B1430` | `oklch(0.18 0.055 265)` | `--bg-well` / Deep navy canvas (`60%`) |
| `#1F3570` | `oklch(0.34 0.105 264)` | `--bg-card` / Elevated surface (`30%`) |
| `#3E64B0` | `oklch(0.51 0.135 260)` | `--brand-fill` / Focal cobalt (`10%`, `C <= 0.20`) |
| `#7FA6E0` | `oklch(0.72 0.095 256)` | `--brand-primary` (Dark text/ring accent) |
| `#C9DDF5` | `oklch(0.89 0.042 252)` | `--ink-secondary` / Subtle tint |
| `#FFF6E8` | `oklch(0.97 0.020 82)` | `--ink-primary` (Dark) / Warm cream CTA or Light ground |

### C. Moss River *(Organic / Clinical Calm / Wellness)*
| Swatch Hex | OKLCH Approx | Suggested Role |
| :--- | :--- | :--- |
| `#101812` | `oklch(0.20 0.018 148)` | `--bg-well` / Dark forest ground (`60%`) |
| `#274132` | `oklch(0.36 0.044 152)` | `--bg-card` / Anodized sage panel (`30%`) |
| `#476754` | `oklch(0.50 0.048 152)` | `--brand-fill` / Calm moss accent (`10%`) |
| `#72927E` | `oklch(0.64 0.045 152)` | `--ink-muted` / Secondary accent |
| `#A9C1B3` | `oklch(0.79 0.032 152)` | `--ink-secondary` (Dark) / Soft border |
| `#EDF3EE` | `oklch(0.96 0.010 148)` | `--ink-primary` (Dark) / Light mineral canvas |

### D. Deep Oceanic Blue *(Marine Technical / Telemetry)*
- Ramp: `#021024` (deep well) -> `#052659` (panel) -> `#5483B3` (focal steel-blue accent, `C <= 0.12`) -> `#7DA0CA` (muted ink/chart) -> `#C1E8FF` (ice highlight / Light pill). Pair `#021024` text on `#C1E8FF` buttons for `> 12:1` AAA contrast.

### E. Horizon Warm SaaS *(Stitch Remix — Editorial Warm Ivory Light Mode)*
Extracted from the curated Stitch SaaS reference (`Plus Jakarta Sans`):
- **Tonal Light Ladder (zero harsh `#FFFFFF` page wash):** Canvas `#FFF9EE` (`oklch(0.98 0.015 90)`), Low `#F9F3E8`, Container `#F3EDE2`, High `#EDE8DD`, Highest `#E8E2D7`, Card Lowest `#FFFFFF`.
- **Ink & Accents:** Primary Ink `#1D1C15` (`> 15:1` on `#FFF9EE`), Secondary `#56423C`, Focal Terracotta `#9F4122` (WCAG AA/AAA text/CTA) + `#FF8A65` (container highlight), Olive Secondary `#556500`, Slate Tertiary `#326578`.
- **SaaS Landing Rhythm & Type:** Base `8px`, Gutter `32px`, Card Padding `40px`, Container Padding `64px`, Section Gap `120px`; `display-xl: 64px / 1.1 / -0.04em`, `headline-lg: 40px / 1.2 / -0.02em`, `body-md: 16px / 1.6`.

## 4. Baseline Neutral Ramps (`Graphite / Warm / Ink` — Unslop)
Keep app/dashboard surfaces neutral so content carries the color; tint landings slightly toward the world:

| Role | Dark Graphite | Dark Warm | Dark Ink | Light Graphite | Light Warm | Light Ink |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Deepest / Sidebar | `#0F0F10` | `#12110F` | `#07080D` | `#F4F4F5` | `#EFE9DF` | `#ECEFF4` |
| Page Canvas (`60%`) | `#141415` | `#161513` | `#0B0D14` | `#FAFAFA` | `#F7F4EE` | `#F5F7FA` |
| Card (`30%`) | `#19191B` | `#1C1A18` | `#11141C` | `#FFFFFF` | `#FDFBF7` | `#FFFFFF` |
| Raised / Active | `#232325` | `#262421` | `#1A1E28` | `#F4F4F5` | `#EFE9DF` | `#ECEFF4` |
| Primary Ink | `#EDEDED` | `#EFE9DE` | `#EEF0F5` | `#171717` | `#1F1B16` | `#111827` |
| Muted Ink (`~4.5:1`) | `#85858B` | `#8A847A` | `#7A8296` | `#737373` | `#7B7266` | `#6B7487` |
| Hairline Border | `ink @ 8%` | `ink @ 8%` | `ink @ 8%` | `ink @ 8%` | `ink @ 8%` | `ink @ 8%` |

- **Semantic Pairings:** Positive `#4CC38A` (Dark) / `#16A34A` (Light); Negative `#E5484D` (Dark) / `#DC2626` (Light).
- **Dashboard Craft:** 3–4 compact numbers-only stat cards (label + big tabular figure + comparison delta, no decorative sparklines) above 1 wide main chart (`>= 2/3` width, 1 accent) paired with 1 narrower ranked list or table.
