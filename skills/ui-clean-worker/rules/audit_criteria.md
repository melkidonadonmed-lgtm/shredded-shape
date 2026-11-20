# UI Clean Worker — Audit Criteria (`ui-clean-worker`)

1. **Read-After-Write (RAW), AppSec & Toolchain Gates:**
   - `[PASS]` `verify_raw_frontend.py <target>` returns `verdict == "[PASS]"` (fail-closed on `> 500`-file truncation), 64-char SHA-256 checksums, zero client secret leaks (`AUDIT-SEC-ENV-LEAK`), zero AI omission placeholders (`AUDIT-STUB-PLACEHOLDER`), per-sink `DOMPurify.sanitize()` (`AUDIT-SEC-01`), zero gradient text (`ANTI-SLOP-GRADIENT-TEXT`), zero `grid-auto-flow: dense`, zero reflow transitions, zero files `> 600` lines, and `--run-tsc` exit code `0`.
   - `[FAIL]` Missing SHA-256 verification, unrun/missing `tsconfig.json` under `--run-tsc`, truncated scan, exposed `NEXT_PUBLIC_*`/`VITE_*` secrets, `// ... rest` omission comments, unsanitized HTML/`eval` sinks, reflow animations, or monolith files `> 600` lines.

2. **Optical, BFC Spacing & Craft Implementation Gates:**
   - `[PASS]` Valid 5-Plane `OKLCH 60-30-10` + `light-dark()` + Tailwind v4 `@theme inline` `--shadow-elevation-*` (`color-mix(in oklab)`, P3 within `C <= 0.20`, `#000000` absent), Light 3-layer shadows, Dark `--light-zenith`, `isolation: isolate` + standalone `<feColorMatrix>`, matte frosted glass, `flow-root` + `.prose > * + *`, `text-wrap: balance/pretty`, silent CSS breadcrumbs (`::before`), GPU `.skip-link`, `@container` isolated from `subgrid`, verified `24x24` SVGs, Next.js 15+ `await params`, `:user-invalid`, and 5-state FSM.
   - `[FAIL]` Presence of blur blobs, neon glows, confetti pills, dashed wireframes, gradient text, decorative side-stripes, amateur SVGs, `forwardRef` in React 19, unsanitized HTML sinks, or `setTimeout` mock data.
