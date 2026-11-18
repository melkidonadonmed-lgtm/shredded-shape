# Clinical `OKLCH` Tokens, AAA Forms & Vector A4 `.sus-grid` Guide

Tier-3 implementation reference for `clinical-minimalist-ui`, enforcing **WCAG 2.2 AAA (`>= 7.0:1`)**, zero screen shadows in print, tabular dosages, and millimeter `.sus-grid` sheets.

## 1. Clinical Semantic `OKLCH` Tokens (`globals.css`)
```css
@layer reset, tokens, base, layouts, components, print;

@layer base {
  html, body {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: auto; /* Protects EHR form INP responsiveness */
    font-optical-sizing: auto;
    font-synthesis: none;
  }
  h1, h2, h3 { text-rendering: optimizeLegibility; }
}

@layer tokens {
  :root {
    color-scheme: light dark;
    --bg-well: light-dark(oklch(0.945 0.006 245), oklch(0.120 0.012 250));
    --bg-canvas: light-dark(oklch(0.985 0.005 245), oklch(0.155 0.014 250));
    --bg-card: light-dark(oklch(1.000 0.000 0), oklch(0.205 0.017 250));
    --bg-card-lit: light-dark(oklch(1.000 0.000 0), oklch(0.245 0.020 250));
    --bg-key: light-dark(oklch(0.992 0.002 245), oklch(0.275 0.022 250));
    --surface-canvas: var(--bg-canvas);
    --surface-sunken: var(--bg-well);
    --surface-card: var(--bg-card);
    --surface-elevated: var(--bg-card-lit);

    --ink-primary: light-dark(oklch(0.170 0.020 255), oklch(0.960 0.005 245));
    --ink-secondary: light-dark(oklch(0.320 0.020 255), oklch(0.840 0.012 250));
    --ink-muted: light-dark(oklch(0.375 0.018 255), oklch(0.750 0.014 250));
    --ink-on-key: var(--ink-primary);

    --status-ok: oklch(0.56 0.14 162);
    --status-warn: oklch(0.64 0.15 70);
    --status-danger: oklch(0.56 0.21 25);

    --border-hairline: light-dark(oklch(0.18 0.02 255 / 0.10), oklch(1 0 0 / 0.11));
    --catch-light: inset 0 1px 0 0 light-dark(oklch(1 0 0 / 0.88), oklch(1 0 0 / 0.13));
    --shadow-elevation-1:
      0 1px 3px -1px light-dark(oklch(0.18 0.02 255 / 0.08), oklch(0.08 0.01 255 / 0.45)),
      0 3px 8px -2px light-dark(oklch(0.18 0.02 255 / 0.05), oklch(0.08 0.01 255 / 0.35)),
      var(--catch-light);
    --shadow-elevation-2:
      0 4px 10px -2px light-dark(oklch(0.18 0.02 255 / 0.10), oklch(0.08 0.01 255 / 0.58)),
      0 14px 26px -6px light-dark(oklch(0.18 0.02 255 / 0.08), oklch(0.08 0.01 255 / 0.50)),
      var(--catch-light);

    --font-sans: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
    --font-mono: 'IBM Plex Mono', 'JetBrains Mono', ui-monospace, monospace;
  }

  [data-theme="clinical-day"] { color-scheme: light; }
  [data-theme="clinical-night"] { color-scheme: dark; }
}
```

## 2. Ergonomic Inputs, Tabular Doses & Safe Contrast Forms
```css
@layer components {
  .clinical-unit {
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .clinical-field {
    display: grid; gap: 0.375rem; min-inline-size: 0;
  }
  .clinical-input {
    min-block-size: 44px; padding: 0.625rem 0.875rem; border-radius: 0.5rem;
    background: var(--bg-well); border: 1px solid var(--border-hairline);
    color: var(--ink-primary); font-variant-numeric: tabular-nums;
  }
  .clinical-input:user-invalid { border-color: var(--status-danger); background: color-mix(in oklab, var(--status-danger) 10%, var(--bg-card)); }
  .clinical-input:focus-visible { outline: 2px solid var(--ink-primary); outline-offset: 2px; }
  @media (any-pointer: coarse) { .clinical-input, button { min-block-size: 48px; } }
}
```

## 3. A4 Vector `.sus-grid` Sheet & `@media print` Isolation
```css
@layer components {
  .a4-sheet, .sus-grid {
    inline-size: min(100%, 210mm);
    min-block-size: 297mm;
    background: oklch(1 0 0);
    color: oklch(0.16 0.01 255);
    display: grid;
    grid-template-rows: auto 1fr auto;
    gap: 12px;
    padding: 15mm;
    box-shadow: var(--shadow-elevation-2);
  }
  .sus-grid-row {
    display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 8px;
    border-block-end: 0.25mm solid oklch(0.82 0.01 250);
    padding-block: 4mm;
  }
}

@layer print {
  @media print {
    @page { size: A4 portrait; margin: 12mm; }
    body { background: oklch(1 0 0); color: oklch(0.12 0 0); print-color-adjust: exact; }
    .no-print, nav, aside { display: none; }
    .a4-sheet, .sus-grid, .surface-card {
      box-shadow: none;
      backdrop-filter: none;
      border: 0.25mm solid oklch(0.78 0.01 250);
      break-inside: avoid;
    }
  }
}
```
- Presence of `clinical-day`, `clinical-night`, or `.sus-grid` triggers automatic `WCAG AAA (>= 7.0:1)` verification in `ui_judge_gatekeeper.py --composite`.
- `_ss_guards.strip_print_sheet_contexts()` masks `@media print`/`.sus-grid` CSS blocks and `.ts` A4 HTML prescription templates (`susDocumentsCatalog`, `presetClinicalTemplates`) while `find_print_shadow_leaks()` fails non-`none` `box-shadow` declarations left active inside `@media print`, and interactive `globals.css` remains subject to `>= 12px` legibility checks.
