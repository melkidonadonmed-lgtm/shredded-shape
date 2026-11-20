---
trigger: glob
globs: "**/*.css, **/*.scss, **/*.html, **/*.tsx, **/*.jsx, **/*.vue, **/DESIGN.md"
description: "Shredded-Shape 9-Axis UI/UX guardrails (lean SSOT): OKLCH 60-30-10, polarity depth, matte glass, @container/Flex/Grid, WCAG 2.2 AA/AAA, Single-DOM nav, GPU motion, and AppSec hygiene."
---

# Shredded-Shape 9-Axis UI/UX Guardrails (Lean SSOT)

> **Principle (Craft vs Slop):** Keep chrome quiet and concentrate richness into 1–2 product-specific moments. Load detailed palettes and CSS examples from `shredded-shape` L3 references:
> - Palettes, Stitch SaaS tokens & Unslop Direction: `skills/ui-brand-ux-planner/references/curated_palettes_and_unslop_direction.md`
> - Copy-paste Tokens, Flexbox, Grid & Shadow examples: `skills/ui-clean-worker/references/practical_css_examples_tokens_flex_grid_shadows.md`

1. **Axis 1 — 4-Stage Actor-Critic & Direction:** Follow `ui-analyst` -> `ui-planner` (5-line Direction Brief + `DESIGN.md` + bounded DAG) -> `ui-worker` (ReAct + RAW SHA-256) -> `ui-judge` (3-Axis WCAG 2.2 judge; fail-closed `UNVERIFIED`).
2. **Axis 2 — `OKLCH` 60-30-10 & Quiet Neutrals:** Use 1 tinted neutral ramp (`oklch()` + `light-dark()` + `color-mix(in oklab)`), 5 planes (`well < canvas < card < card-lit < key`), zero `#000000`, 3 text roles, and 1 focal accent (`C <= 0.20`, hard cap `0.22`, red `<= 0.24`). Ban hue-to-hue gradients, gradient text, neon glows, blur blobs, confetti badges, dashed wireframes, and side stripes.
3. **Axis 3 — Polarity-Aware Depth:** Light Mode uses neutral soft/3-layer shadows (`135°` or umbra + negative-spread penumbra + top catch-light); Dark Mode uses surface steps + quiet `6–10%` hairlines + `inset 0 1px 0` top rim (zero glowing borders).
4. **Axis 4 — Mineral Matte Glass:** Translucent `color-mix(in oklab, ...)` (`~74%`) + `backdrop-filter: blur(16px–18px) saturate(145%)` + `isolation: isolate` + `@media (prefers-reduced-transparency: reduce)` solid fallback.
5. **Axis 5 — Archetype Lock:** Lock 1 Style (`soft | hi-tech | tactile | elevated | retro | vintage | clinical`) and 1 Spatial (`bento_12_col | workbench_split_view | command_center_grid | editorial_65ch | spatial_hud_dock | vector_a4_print`) in `DESIGN.md`.
6. **Axis 6 — 4px Grid, Flexbox, Grid & `@container`:** Keep spacing on a `4px` scale (`Inner < Card <= Grid < Section`), concentric radii (`R_in = max(4px, R_out - P)`), `min-inline-size: 0` on Flex/Grid children, Tailwind v4 `@theme inline` shadows, and `@container` isolated from `subgrid`.
7. **Axis 7 — Single-DOM Adaptive Nav:** 3 Mobile-First postures (`<600px` Bottom Bar, `600–839px` Rail, `>=840px` Collapsible Sidebar), `<= 3` `<nav>` with unique `aria-label`, `<= 6` items (`gap >= 8px`), GPU `.skip-link`, and silent CSS breadcrumbs (`::before`).
8. **Axis 8 — Copy, Type, SVGs & WCAG 2.2:** Sentence case, zero `!` / greeting headlines / hype words / emojis / pseudo-icons; 1 line-icon set (`16–24px` `1.5` stroke); weights `400–600`, `tabular-nums`, `clamp()`, `:focus-visible >= 3:1`, `DOM == Tab Order`, and `>= 44/48px` targets (`< 40px` blocker).
9. **Axis 9 — GPU Motion, AppSec & FSM:** Animate only `transform`/`opacity`/`color` with `cubic-bezier(0.22, 1, 0.36, 1)` + `prefers-reduced-motion`; React 19 `ref`, Next.js 15+ `await params`, `DOMPurify.sanitize()`, zero client secrets/stubs, and real 5-state FSM (`idle | loading | empty | error | success`).
