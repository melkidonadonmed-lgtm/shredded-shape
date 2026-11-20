# 5-Plane `OKLCH` Depth, Tailwind v4 `@theme`, Matte Glass & Tactile Controls

Enforce machined physical depth across Light and Dark polarities via `light-dark()`, `color-mix(in oklab, ...)`, concentric radii, 4-stage elevation, and mineral matte grain.

## 1. 5-Plane `OKLCH` Tokens & Tailwind v4 `@theme` Mapping
Never mix opposite elevations under generic tokens or emit `#000000`. Maintain strict Dark lightness progression (`well < canvas < card < card-lit < key`) and UI mixing in `oklab`:
```css
@import "tailwindcss";
@custom-variant dark (&:where([data-theme*="dark"], [data-theme="tactile-matte"], .dark, .dark *));

@theme inline {
  --color-bg-well: var(--bg-well);
  --color-bg-canvas: var(--bg-canvas);
  --color-bg-card: var(--bg-card);
  --color-bg-card-lit: var(--bg-card-lit);
  --color-bg-key: var(--bg-key);
  --color-brand-primary: var(--brand-primary);
  --shadow-elevation-low: var(--shadow-elevation-1);
  --shadow-elevation-medium: var(--shadow-elevation-2);
  --shadow-elevation-high: var(--shadow-elevation-3);
  --shadow-inset-sunken: var(--shadow-well);
  --radius-card: 1rem;
}

@layer tokens {
  :root {
    color-scheme: light dark;
    --bg-well: light-dark(oklch(0.922 0.010 250), oklch(0.118 0.012 260));
    --bg-canvas: light-dark(oklch(0.962 0.007 250), oklch(0.145 0.014 260));
    --bg-card: light-dark(oklch(0.994 0.003 250), oklch(0.195 0.018 262));
    --bg-card-lit: light-dark(oklch(1.000 0.000 0), oklch(0.235 0.022 262));
    --bg-key: light-dark(oklch(0.996 0.002 250), oklch(0.262 0.024 262));
    --ink-primary: light-dark(oklch(0.175 0.020 255), oklch(0.955 0.008 255));
    --ink-muted: light-dark(oklch(0.415 0.018 255), oklch(0.670 0.015 255));
    --ink-on-key: var(--ink-primary);
    --brand-primary: light-dark(oklch(0.46 0.15 245), oklch(0.72 0.14 235));
    --brand-fill: light-dark(oklch(0.43 0.15 245), oklch(0.75 0.14 235));
    --ink-on-brand: light-dark(oklch(0.992 0.003 255), oklch(0.140 0.022 255));
    --accent-soft: color-mix(in oklab, var(--brand-primary) 14%, var(--bg-card));
  }
}
```
- **Chroma, Brand-Fill & Mixing Guard:** Keep UI accents at `C <= 0.20` (`C > 0.22` hard rejection; semantic red `15°..40°` capped `<= 0.24`). Separate accent text/borders (`--brand-primary`) from filled CTA surfaces (`--brand-fill` + `--ink-on-brand`) so Dark/Light contrast stays `>= 4.5:1` across all hues instead of pairing white text onto pastel `--brand-primary`. Use `color-mix(in oklab, ...)` for hover/focus state mixing to avoid Chromium's `color-mix(in oklch)` hue-arc artifacts.
- **Font Fallback Order:** Place named system/ClearType fonts BEFORE terminal generic keywords (`'JetBrains Mono', 'Cascadia Code', ui-monospace, monospace` — never `ui-monospace, 'Cascadia Code'`, which shadows named fonts) and style inline `:not(pre) > code` as bordered `--bg-well` token chips (`border: 1px solid var(--border-strong)`).

## 2. Concentric Radii & 4-Stage Elevation Physics (`Inset` + `Levels 1..3`)
Always derive child container radius from parent radius minus padding (`R_in = max(4px, R_out - Pad)`):
```css
:root {
  --pad-card: 1.25rem;
  --r-outer: 1.125rem;
  --r-inner: max(0.25rem, calc(var(--r-outer) - var(--pad-card) * 0.5));
  --rim-top: light-dark(oklch(1 0 0 / 0.94), oklch(1 0 0 / 0.14));
  --rim-top-strong: light-dark(oklch(1 0 0), oklch(1 0 0 / 0.26));
  --catch-light: inset 0 1px 0 0 var(--rim-top);
  --light-zenith: radial-gradient(120% 90% at 50% 0%, light-dark(oklch(1 0 0 / 0.85), oklch(1 0 0 / 0.065)) 0%, transparent 65%);
  --shadow-well: inset 0 2px 5px light-dark(oklch(0.22 0.02 255 / 0.13), oklch(0.06 0.01 260 / 0.78)), 0 1px 0 light-dark(oklch(1 0 0 / 0.85), oklch(1 0 0 / 0.05));
  --shadow-elevation-1: 0 2px 5px light-dark(oklch(0.22 0.02 255 / 0.08), oklch(0.06 0.01 260 / 0.55)), 0 6px 14px -2px light-dark(oklch(0.22 0.02 255 / 0.06), oklch(0.06 0.01 260 / 0.40)), inset 0 1px 0 var(--rim-top-strong);
  --shadow-elevation-2: 0 2px 5px light-dark(oklch(0.22 0.02 255 / 0.06), oklch(0.06 0.01 260 / 0.45)), 0 12px 26px -4px light-dark(oklch(0.22 0.02 255 / 0.11), oklch(0.06 0.01 260 / 0.68)), var(--catch-light);
  --shadow-elevation-3: 0 8px 18px light-dark(oklch(0.22 0.02 255 / 0.09), oklch(0.06 0.01 260 / 0.55)), 0 24px 44px -6px light-dark(oklch(0.22 0.02 255 / 0.16), oklch(0.06 0.01 260 / 0.84)), inset 0 1px 0 var(--rim-top-strong);
}
```
- **Light Mode `Nexus 135°` Soft Tactile:** Pair dual opposite offsets (`8px 8px 20px oklch(0.75 0.025 248 / 0.42), -8px -8px 20px oklch(1 0 0 / 0.96)`) with carved `.inset-panel` wells (`inset 3px 3px 7px ...`) and use neutral `filter: drop-shadow(0 2px 6px oklch(0.18 0.02 255 / 0.12))` (`<= 6px`) on non-rectangular SVGs.

## 3. Tactile Hardware Controls, Mineral Matte Glass & Engraved Pills
```css
@layer components {
  .card-matte {
    position: relative; isolation: isolate;
    background-color: var(--bg-card); background-image: var(--light-zenith);
    box-shadow: var(--shadow-elevation-2); border-radius: var(--r-outer);
    transition: transform 0.18s var(--ease-out), background-color 0.18s ease;
  }
  .card-matte::after, .tactile-key::after {
    content: ""; position: absolute; inset: 0; z-index: -1; border-radius: inherit;
    pointer-events: none; opacity: 0.012; /* Always z-index: -1 beneath text inside isolation: isolate */
  }
  .card-matte:hover { background-color: var(--bg-card-lit); transform: translateY(-2px); box-shadow: var(--shadow-elevation-3); }
  .engraved-pill {
    display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.25rem 0.625rem;
    border-radius: 9999px; background: var(--bg-well); box-shadow: var(--shadow-well);
    font-size: 0.75rem; font-variant-numeric: tabular-nums;
  }
  .lum-bead { inline-size: 0.5rem; block-size: 0.5rem; border-radius: 9999px; background: var(--bead-ok, var(--brand-primary)); }
  .tactile-key, .btn-latch {
    position: relative; isolation: isolate; min-block-size: 44px; padding-inline: 1rem; border-radius: var(--r-inner);
    background-color: var(--bg-key); background-image: linear-gradient(180deg, light-dark(oklch(1 0 0 / 0.55), oklch(1 0 0 / 0.08)) 0%, oklch(1 0 0 / 0) 100%);
    color: var(--ink-on-key); box-shadow: var(--shadow-elevation-1); transition: transform 0.12s var(--ease-out);
  }
  .tactile-key:active, .btn-latch[aria-pressed="true"] {
    background-color: var(--bg-well); background-image: none; color: var(--ink-primary); box-shadow: var(--shadow-well); transform: translateY(1px);
  }
  .surface-frosted {
    isolation: isolate;
    background-color: color-mix(in oklab, var(--bg-card) 74%, transparent);
    backdrop-filter: blur(16px) saturate(145%);
  }
  @media (prefers-reduced-transparency: reduce) { .surface-frosted { backdrop-filter: none; background-color: var(--bg-card); } }
}
```
- **Translucent Key Sheen & Grain Stacking:** Keep `--light-key` translucent (`oklch(1 0 0 / 0.55)` -> `transparent`, never opaque white `oklch(1 0 0)`) and place `feTurbulence` `::after` grain on `z-index: -1` inside `position: relative; isolation: isolate;` so texture never obscures keycaps or speckle-cracks glyphs.
- **Dynamic RCS, Display-P3 Gamut & `<feColorMatrix>` Isolation:** Derive hover/active states via `oklch(from var(--brand-primary) calc(l - 0.08) c h)` and `color-mix(in oklab, ...)` (always wrap `mix-blend-mode` parents with `isolation: isolate`). Optional `@media (color-gamut: p3)` refinements must still obey the `C <= 0.20` (`<= 0.22` cap) optical ceiling. For brand duotone or Protanopia/Deuteranopia accessibility SVG color matrices, keep `<feColorMatrix>` inside a standalone `<filter>` (never combined with `<feGaussianBlur>` in the same `<filter>`).
- Ban omnidirectional neon glows, glowing cyan borders, `blur-3xl` background blobs, dashed wireframe borders (`border: 1px dashed`), gradient text (`background-clip: text`), decorative side-stripe card borders, and multicolored pill classes.

```html
<!-- Standalone SVG Color Matrix (Protanopia aid; zero feGaussianBlur in same filter) -->
<svg hidden aria-hidden="true" width="0" height="0">
  <defs>
    <filter id="protanopia-safe">
      <feColorMatrix type="matrix" values="0.567 0.433 0 0 0  0.558 0.442 0 0 0  0 0.242 0.758 0 0  0 0 0 1 0"/>
    </filter>
  </defs>
</svg>
```
