# Style Archetypes, Token Geometry, Menu Chrome & `taste-skill` Dials

## 1. The 7 Token & Menu Archetypes (`DESIGN.md` Style Lock)

| Style | Radius Scale | Surface & Depth Physics | Menu Chrome & Typography | `taste-skill` Dials (`Variance / Motion / Density`) |
| :--- | :--- | :--- | :--- | :--- |
| **`soft`** | `18px–24px` (`1.35rem`), pills | Low-chroma frosted panels, wide ambient soft shadow (light) / subtle `L+0.05` & translucent border (dark) | Floating rounded sidebar items (`gap: 12px`), `Plus Jakarta Sans` + `Inter` | `4 / 3 / 3` |
| **`hi-tech`** | `4px–6px` (`0.35rem`) | Crisp `1px` structural hairlines, dark specular rim catch-light, non-neon cool cyan/slate halo (`C <= 0.14`) | Precision rail (`2px` inline-start bar), `tabular-nums`, `Geist` / `IBM Plex Sans` + `JetBrains Mono` | `3 / 4 / 5` |
| **`tactile`** | `12px–16px` (`0.95rem`) | Light: 3-layer Umbra + negative Penumbra + top Catch-Light; Dark: `L=0.16->0.27` + specular rim + `--shadow-inset` press | Physical `48px` interactive targets, `translateY(-1px..0px)` clicks, `Inter` + `JetBrains Mono` | `3 / 4 / 4` |
| **`elevated`** | `14px–18px` (`1.1rem`) | Stacked frosted topbar + elevated cards (`--shadow-elevation-2..3`) with `isolation: isolate` | Sticky translucent header + floating command dialog `<dialog>`, clean sans | `4 / 3 / 3` |
| **`retro`** | `2px–4px` (`0.25rem`) | Crisp `2px` border + controlled solid offset shadow (WCAG AA checked, zero blur clutter) | Geometric block navigation tabs, grotesk sans + crisp monospace indices | `5 / 2 / 4` |
| **`vintage`** | `6px–8px` (`0.5rem`) | Warm low-chroma paper (`H=75..85, C<=0.025`) light / warm charcoal dark with gentle zenith rim | Editorial `65ch` measure, `Instrument Serif` / `Newsreader` headings + `IBM Plex Sans` body | `4 / 2 / 3` |
| **`clinical`** | `6px–8px` (`0.5rem`) | `WCAG AAA >= 14:1` calm surfaces, zero glare, contained `6px` status dots, vector A4 `.sus-grid` | Predictable `<=3`-click EHR sidebar + `tabular-nums` + anti-squish `mg/dL` | `1 / 1 / 5` |

## 2. Strict `OKLCH 60-30-10` Brand Calibration

- **60% Dominant Canvas (`--surface-canvas`):** Neutral hue aligned with brand (`C <= 0.02`, Dark `L = 0.16`, Light `L = 0.975`).
- **30% Secondary Structure (`--surface-card`, `--surface-elevated`):** Distinct lightness step (`Dark: 0.22 -> 0.27`).
- **10% Focal Accent (`--brand-primary`):** Restrained chroma (`C <= 0.20`), derived hover/bg via `oklch(from var(--brand-primary) calc(l - 0.08) c h)` and `color-mix(in oklab, ...)`. Neon (`C > 0.23` on large blocks) is strictly banned.
