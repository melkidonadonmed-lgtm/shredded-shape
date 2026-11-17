# Audit Criteria — `ui-clean-worker`

- **`[PASS]`**: Target `.tsx`/`.css`/`.html` files exist physically on disk (`size >= 100` bytes), `verify_raw_frontend.py` passes with valid SHA-256 checksum, zero `#000000`, zero UI emojis, zero placebo stubs, zero `tsc` errors (when `tsconfig.json` is present), dual Light/Dark optical lighting implemented, and real FSM states wired.
- **`[FAIL]`**: Any missing/truncated file (`[RAW-VIOLATION]`), placeholder `onClick={() => {}}` / `alert('Coming soon')`, neon chroma, flat 1-pass `rgba(0,0,0)` shadow, or uncontained horizontal overflow.
- **`[UNVERIFIED]`**: `target_path` cannot be written or build toolchain (`tsc`) is unavailable in the environment without explicit fallback notice.
