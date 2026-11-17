# Optical Shadows, Superior Matte Glass & Polarity-Aware Dynamic Lighting

## 1. Light Mode: 3-Layer Realistic `box-shadow` (Zenithal `90°–120°`)

Never emit single-pass `box-shadow: 0 4px 12px rgba(0,0,0,0.4)`. Combine **Contact Umbra + Negative-Spread Penumbra + Specular Catch-Light**:

```css
--catch-light: inset 0px 1px 0px 0px light-dark(oklch(1 0 0 / 0.88), oklch(1 0 0 / 0.14));
--shadow-elevation-1:
  0px 1px 2px 0px oklch(0.20 0.03 255 / 0.06),
  0px 3px 8px -2px oklch(0.20 0.03 255 / 0.06),
  var(--catch-light);
--shadow-elevation-2:
  0px 2px 4px -1px oklch(0.20 0.03 255 / 0.07),
  0px 10px 20px -4px oklch(0.20 0.03 255 / 0.08),
  var(--catch-light);
--shadow-elevation-3:
  0px 4px 8px -2px oklch(0.20 0.03 255 / 0.08),
  0px 18px 34px -6px oklch(0.20 0.03 255 / 0.11),
  var(--catch-light);
```

Also expose `text-shadow` strictly over photography/media (`.heroTitleOverGradient`) and `filter: drop-shadow()` on transparent SVGs/PNGs.

## 2. Dark Mode: Dynamic Illumination Over Muddy Shadows (Zero Neon, Zero `#000000`)

Dark drop shadows disappear or turn muddy against dark canvases. Replace heavy dark shadows with:
1. **Progressive Lightness Elevation:** `--surface-canvas: oklch(0.16 0.018 258)` -> `--surface-card: oklch(0.215 0.022 258)` -> `--surface-elevated: oklch(0.265 0.026 258)`.
2. **Specular Top & Perimeter Rim Light:** `inset 0 1px 0 0 oklch(1 0 0 / 0.14)` + `1px solid oklch(1 0 0 / 0.11)`.
3. **Soft Non-Neon Surface Halo (Active/Elevated Only):** `0px 10px 22px -6px oklch(from var(--brand-primary) l c h / 0.14)` (`C <= 0.18`).

## 3. Superior Frosted / Matte Finish

```css
.matte-frosted {
  background: oklch(from var(--surface-card) l c h / 0.74);
  backdrop-filter: blur(20px) saturate(145%);
  border: 1px solid var(--border-subtle);
  box-shadow: var(--catch-light), var(--shadow-elevation-2);
  isolation: isolate;
}
@media (prefers-reduced-transparency: reduce) {
  .matte-frosted { backdrop-filter: none; background: var(--surface-card); }
}
```
