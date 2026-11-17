# UI Clean Worker — Audit Criteria (`ui-clean-worker`)

1. **Read-After-Write (RAW) & Toolchain Gates:**
   - `[PASS]` `verify_raw_frontend.py <target>` returns `verdict == "[PASS]"` with verified 64-char SHA-256 checksums, zero 12-vector slop hits, zero empty/malformed SVGs, zero reflow transitions (`all`, `width`, `height`), zero files `> 600` lines, and fail-closed `--run-tsc` exit code `0` for TS/TSX changes.
   - `[FAIL]` Missing SHA-256 verification, unrun or missing `tsconfig.json` under `--run-tsc`, untracked file mutations outside the DAG node, reflow animations, or monolith files `> 600` lines.

2. **Optical, Typography & Craft Implementation Gates:**
   - `[PASS]` Valid 5-Plane `OKLCH 60-30-10` + `light-dark()` tokens (`color-mix(in oklab, ...)`, `#000000` absent, `C <= 0.20`), Light 3-layer shadows, Dark `--light-zenith` + stepped rim, matte frosted fallback (`prefers-reduced-transparency`), Mobile-First postures, Flexbox `min-inline-size: 0`, `@container` isolated from `subgrid`, verified `24x24` `<symbol>` SVGs, `DOMPurify.sanitize()`, Next.js 15+ `await params`, `:user-invalid`, and 5-state FSM.
   - `[FAIL]` Presence of blur blobs, neon glows, confetti pills, dashed wireframes, amateur circle-cloud SVGs, `--neon-*`/`--glow-*`/`--blob-*` tokens, `forwardRef` in React 19, unsanitized `innerHTML`/`dangerouslySetInnerHTML`, or `setTimeout` mock data.
