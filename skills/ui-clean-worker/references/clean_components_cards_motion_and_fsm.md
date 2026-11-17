# Clean Components, 4 Card Variants, Motion & Real-State FSM

## 1. 4 `<article>` Card Variants + `@container` + `subgrid`

- Keep `container-type: inline-size; container-name: card;` on an outer `.card-shell` wrapper—never on the exact node declaring `grid-template-rows: subgrid`.
- **Elevated:** `--surface-card` + `--shadow-elevation-2`.
- **Outlined:** `--surface-card` + `1px solid var(--border-subtle)` + `--catch-light`.
- **Filled:** `--surface-sunken` + `--shadow-inset` + concentric inner radius $R_{\text{in}} = \max(4\text{px}, R_{\text{out}} - P)$.
- **Interactive / Choice:** Stretch `a.card-link::after { content: ""; position: absolute; inset: 0; }` (`z-index: 1` on secondary controls) or style choice cards via `:has(> input:checked)` without mutating `border-width`.

## 2. Single-DOM Adaptive Navigation & GPU Motion

- Transition one `<nav aria-label="Main navigation">` from Mobile Bottom Bar (`< 48em`, `padding-block-end: env(safe-area-inset-bottom, 0px)`, `3–5` items, `>= 48x48px`) to Collapsible Sidebar Rail (`>= 48em`, `256px` <-> `72px` collapsed, `100dvh`).
- Animate only `transform` and `opacity` with `cubic-bezier(0.22, 1, 0.36, 1)`; declare `transition-behavior: allow-discrete` separately after `transition` alongside `@starting-style` for `<dialog>`/`[popover]`.
- In `@media (prefers-reduced-motion: reduce)`, collapse animations to `0.01ms`.

## 3. React 19, Next.js 15+ & Executable FSM

- **React 19:** Pass `ref` directly as a prop (zero `forwardRef`).
- **Next.js 15+:** Treat `params` and `searchParams` as `Promise<...>` (`await params` / `use(params)`); wrap `useSearchParams()` in `<Suspense>`.
- **Real-State FSM:** Wire explicit `idle | loading | empty | error | success` states (`data-state`, `aria-busy`, `role="status"`/`"alert"`) with zero `setTimeout` fakes or `alert('Coming soon')`.
