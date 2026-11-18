# Translating Stitch Outputs to `shredded-shape` `OKLCH 60-30-10`

Bridge Stitch Canvas designs (`designTheme`, `#hex`, HTML/Tailwind v3) into `shredded-shape`'s 8-section `DESIGN.md` and production React/Next/HTML code without losing visual intent or triggering Anti-Slop rejections.

## 1. Bidirectional Token Mapping (`Stitch <-> shredded-shape`)
| Stitch `designTheme` / HTML | `shredded-shape` `DESIGN.md` (`OKLCH 60-30-10`) | Notes |
| :--- | :--- | :--- |
| `namedColors.background` / `surface` | `--bg-well` / `--bg-canvas` (`60%`, `light-dark()`) | Clamp `#000000` -> `OKLCH(0.145 0.014 H)`. |
| `surface_container` / `surface_container_high` | `--bg-card` / `--bg-card-lit` (`30%`) | Enforce `well < canvas < card < card-lit` in Dark. |
| `primary` / `overridePrimaryColor` | `--brand-primary` (`10%`, `C <= 0.20`, cap `0.22`) | Never ship neon chroma; mix via `color-mix(in oklab, ...)`. |
| `error` | `--danger` (`15°..40°` hue, `C <= 0.24`) | Reserve saturated red strictly for destructive/critical alerts. |
| `spacingScale` / `spacing` (`4px/8px`) | Stitch Gestalt Proximity (`Inner < Card <= Grid < Section`) | Derive concentric radii: `R_in = max(4px, R_out - P)`. |
| `headlineFont` / `bodyFont` | Self-hosted Variable WOFF2 (`font-optical-sizing: auto`) | Body `text-rendering: auto`; headings `optimizeLegibility`. |

## 2. Mandatory Cleanup Before Stage 2 Implementation
1. **Strip Legacy CDN Boilerplate:** Remove inline `tailwind.config` runtime blocks and CDN links; emit CSS-first Tailwind v4 `@theme` + `@layer tokens` (`light-dark()`) instead.
2. **Replace Placeholder Links & Icons:** Convert every `href="#"` anchor into verified `<Link>`/route targets; map mixed or inline amateur SVGs to ONE verified `24x24` library (`Lucide`, `Material Symbols`, `Phosphor`, or `Fluent`).
3. **Ban AI-Filler & Slop Signals:** Reject invented metrics (`"99.98% UPTIME"`, `"124ms AVG"`), fake stat blocks (`"BY THE NUMBERS"`), `"LABEL // YEAR"` headers, emojis, blur blobs, confetti badges, dashed wireframes, and `< 44px` (`48px` coarse) interactive targets.
4. **Add 3-Layer Depth & 5-State FSM:** Pair Light 3-layer shadows (`-1px..-8px` spread) + Dark `--light-zenith` rim lighting with real `idle | loading | empty | error | success` states and GPU-only (`transform`/`opacity`) motion.
