# Practical CSS Examples: Tokens, Flexbox, Grid & Shadows

Copy-ready recipes combining **Shredded-Shape `OKLCH 60-30-10`**, **Horizon Warm SaaS** rhythm, and **Unslop** (`@heydamir`, CC BY 4.0) 4px spacing, quiet chrome, and single-curve motion.

## 1. Tokens (`OKLCH` + `light-dark()` + 4px Scale + Motion)
```css
@layer tokens {
  :root {
    color-scheme: light dark;
    /* 60-30-10 Mineral Surfaces (Midnight Noir Dark <-> Warm Editorial Light) */
    --bg-well: light-dark(oklch(0.935 0.012 88), oklch(0.145 0.016 255));
    --bg-canvas: light-dark(oklch(0.978 0.014 88), oklch(0.175 0.018 255));
    --bg-card: light-dark(oklch(0.996 0.004 88), oklch(0.225 0.022 252));
    --bg-card-lit: light-dark(oklch(1.000 0.000 0), oklch(0.275 0.026 250));
    --ink-primary: light-dark(oklch(0.190 0.015 80), oklch(0.945 0.008 245));
    --ink-secondary: light-dark(oklch(0.410 0.020 65), oklch(0.760 0.022 245));
    --ink-muted: light-dark(oklch(0.510 0.018 65), oklch(0.620 0.024 246));
    --hairline: color-mix(in oklab, var(--ink-primary) 9%, transparent);
    /* 10% Focal Accent (C <= 0.20; Horizon Terracotta Light <-> Cobalt Dark) */
    --brand-fill: light-dark(oklch(0.47 0.13 38), oklch(0.56 0.14 256));
    --ink-on-brand: oklch(0.99 0.005 90);
    /* 4px Scale, Concentric Radii & Single Easing */
    --space-2: 0.5rem; --space-4: 1rem; --space-6: 1.5rem; --space-8: 2rem;
    --r-card: 1rem; --r-ctrl: max(0.25rem, calc(var(--r-card) - var(--space-2)));
    --ease-craft: cubic-bezier(0.22, 1, 0.36, 1);
  }
}
```

## 2. Flexbox Patterns (Anti-Overflow Nav, Card Header & Pinned Footer)
Use `min-inline-size: 0` on flex children so long labels truncate cleanly instead of blowing out containers:
```css
@layer components {
  .topbar {
    display: flex; align-items: safe center; justify-content: space-between;
    gap: var(--space-4); min-block-size: 3.5rem; padding-inline: var(--space-6);
    border-block-end: 1px solid var(--hairline);
  }
  .nav-list { display: flex; align-items: center; gap: var(--space-2); min-inline-size: 0; }
  .card {
    display: flex; flex-direction: column; gap: var(--space-4);
    padding: var(--space-6); border-radius: var(--r-card);
    background: var(--bg-card); border: 1px solid var(--hairline);
  }
  .card-head { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--space-2); }
  .card-title { flex: 1 1 0; min-inline-size: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .card-foot { margin-block-start: auto; padding-block-start: var(--space-4); border-block-start: 1px solid var(--hairline); }
  .stat-value { font-size: clamp(1.5rem, 2.2cqw, 2rem); font-weight: 500; font-variant-numeric: tabular-nums; }
}
```

## 3. CSS Grid: RAM Auto-Fit, Asymmetric SaaS Bento & `@container`
Keep stat cards uniform above 1 dominant chart (`span 8`) paired with a narrower ranked list (`span 4`); isolate `container-type` from `subgrid`:
```css
@layer layout {
  .page-wrap { max-inline-size: 90rem; margin-inline: auto; padding: var(--space-6); display: grid; gap: var(--space-6); }
  /* RAM Grid: 3-4 compact stat cards sharing equal height */
  .stat-grid { display: grid; gap: var(--space-4); grid-template-columns: repeat(auto-fit, minmax(min(100%, 14rem), 1fr)); }
  /* Asymmetric 12-Col SaaS Bento (Main Chart 2/3 + Ranked List 1/3) */
  .bento-12 { display: grid; gap: var(--space-6); grid-template-columns: minmax(0, 1fr); }
  @media (min-width: 64rem) {
    .bento-12 { grid-template-columns: repeat(12, minmax(0, 1fr)); }
    .bento-main { grid-column: span 8; min-inline-size: 0; }
    .bento-side { grid-column: span 4; min-inline-size: 0; }
  }
  /* Isolated @container card (never put subgrid on the same node) */
  .cq-host { container: metricCard / inline-size; }
  .cq-row { display: grid; gap: var(--space-2); grid-template-columns: minmax(0, 1fr); }
  @container metricCard (min-width: 24rem) { .cq-row { grid-template-columns: 1fr auto; align-items: center; } }
}
```

## 4. Shadows, Polarity Depth & Matte Glass
Light Mode uses soft neutral elevation; Dark Mode relies on surface steps + quiet hairlines + top specular rim (`inset 0 1px 0`), never glowing borders:
```css
@layer components {
  :root {
    --rim-top: light-dark(oklch(1 0 0 / 0.90), oklch(1 0 0 / 0.12));
    --shadow-sm: 0 1px 2px light-dark(oklch(0.18 0.02 255 / 0.06), oklch(0.05 0.01 260 / 0.45)), inset 0 1px 0 var(--rim-top);
    --shadow-md: 0 2px 6px light-dark(oklch(0.18 0.02 255 / 0.06), oklch(0.05 0.01 260 / 0.45)),
                 0 12px 26px -4px light-dark(oklch(0.18 0.02 255 / 0.10), oklch(0.05 0.01 260 / 0.68)),
                 inset 0 1px 0 var(--rim-top);
    --shadow-soft-135: 8px 8px 20px oklch(0.75 0.02 248 / 0.35), -8px -8px 20px oklch(1 0 0 / 0.92);
  }
  .elevated-card {
    background: var(--bg-card); box-shadow: var(--shadow-md); border-radius: var(--r-card);
    transition: transform 160ms var(--ease-craft), background-color 160ms var(--ease-craft);
  }
  .elevated-card:hover { background: var(--bg-card-lit); transform: translateY(-2px); }
  .btn-primary {
    min-block-size: 2.75rem; padding-inline: 1.25rem; border-radius: var(--r-ctrl);
    background: var(--brand-fill); color: var(--ink-on-brand); font-weight: 500;
    box-shadow: var(--shadow-sm); transition: transform 140ms var(--ease-craft), opacity 140ms var(--ease-craft);
  }
  .btn-primary:active { transform: scale(0.98); }
  .matte-glass {
    isolation: isolate; background: color-mix(in oklab, var(--bg-card) 74%, transparent);
    backdrop-filter: blur(16px) saturate(145%); border: 1px solid var(--hairline);
    box-shadow: inset 0 1px 0 var(--rim-top);
  }
  @media (prefers-reduced-transparency: reduce) { .matte-glass { backdrop-filter: none; background: var(--bg-card); } }
  @media (prefers-reduced-motion: reduce) { .elevated-card, .btn-primary { transition: none; transform: none; } }
}
```
