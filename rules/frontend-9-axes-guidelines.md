---
trigger: glob
globs: "**/*.css, **/*.scss, **/*.html, **/*.tsx, **/*.jsx, **/*.vue, **/DESIGN.md, **/elevationRenderer.ts"
description: "Activates the Shredded-Shape 9-Axis UI/UX SSOT: OKLCH 60-30-10 (zero neon), 3-layer shadows (light), dynamic rim/halo lighting (dark), superior matte glass, 7 style archetypes, @container, and intuitive zero-verbiage UX."
---

# Shredded-Shape 9-Axis UI/UX & Optical Physics Guidelines (SSOT)

1. Activate `ui-frontend-analyst` (inspect), `ui-brand-ux-planner` (brand/style/`DESIGN.md`), `ui-clean-worker` (build), and `ui-quality-judge` (verify) via `shredded-shape`.
2. **`60-30-10` Perceptual `OKLCH` Ratio (Zero `#000000`, Zero Neon):**
   - **60% Dominant Canvas (`--surface-canvas` / `--bg-canvas`):** `oklch()` with `light-dark()` (Dark Mode `L = 0.16`, never `#000000`).
   - **30% Structural Surfaces (`--surface-sunken` `L=0.13`, `--surface-card` `L=0.22`, `--surface-elevated` `L=0.27`):** Distinct elevation steps ensuring `L_card > L_canvas` in Dark Mode.
   - **10% Focal Accent (`--brand-primary`):** `color-mix(in oklab, ...)` and `oklch(from ...)` with restrained chroma (`C <= 0.20`; zero neon glow or chromatic noise).
3. **Polarity-Aware Optical Depth & Superior Matte Frosted Surfaces:**
   - **Light Mode (3-Layer `box-shadow`):** Contact Umbra + negative-spread Penumbra (`-1px..-8px`) + Zenithal Specular Catch-Light (`inset 0 1px 0 0 oklch(1 0 0 / 0.85)`) across `--shadow-elevation-1..3` and Tailwind v4 `@theme` (`--shadow-elevation-low/medium/high`, `--shadow-inset-sunken`).
   - **Dark Mode (Dynamic Illumination Over Muddy Shadows):** Because dark drop shadows blend into dark canvases, separate planes via progressive `L` elevation + **subtle Specular Rim Light (`inset 0 1px 0 0 oklch(1 0 0 / 0.12..0.16)` + `1px` hairline border)** + optional soft non-neon surface halo (`0 0 20px -4px oklch(from var(--brand-primary) l c h / 0.14)`).
   - **Superior Frosted / Matte Finish:** `oklch(from var(--surface-card) l c h / 0.74)` + `backdrop-filter: blur(18px) saturate(145%)` + `isolation: isolate` + crisp `1px` top specular edge + `@media (prefers-reduced-transparency: reduce)` solid fallback.
4. **7 Canonical Token & Menu Style Archetypes:**
   - Declare explicit style mode in `DESIGN.md`: `soft`, `hi-tech`, `tactile`, `elevated`, `retro`, `vintage`, or `clinical`. Calibrate border radii, hairline weight, shadow/rim intensity, typography pairing, and menu chrome accordingly without copying templates.
5. **Logical Spacing, Intuitive Zero-Verbiage UX, Macro/Micro Layout & Fluidity:**
   - Enforce `box-sizing: border-box`, logical CSS (`inline-size`, `padding-inline`, `margin-block`, `flow-root`, `gap`), `4px/8px` primitives + Stitch semantic tokens, Concentric Radii ($R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$), CSS Grid RAM + `@container` isolated from `subgrid`, 4 `<article>` Card variants (`Elevated`, `Outlined`, `Filled`, `Interactive` via `a.card-link::after`), and Single-DOM Adaptive Navigation (Bottom Bar `env(safe-area-inset-bottom)` <-> Collapsible `240px–260px` Sidebar Rail) with `<ol role="list">` Breadcrumbs.
   - **Intuitive Zero-Verbiage & Real-State:** Ban explanatory tutorial paragraphs for obvious controls, ban decorative UI emojis, enforce `clamp()` ($\max \le 2.5\times \min$, `60ch–65ch`, `tabular-nums`, `font-synthesis: none`), `any-pointer: coarse` (`>= 48x48px`), `DOM == Tab Order`, `prefers-reduced-motion`, and real executable FSM (`idle | loading | empty | error | success`).
