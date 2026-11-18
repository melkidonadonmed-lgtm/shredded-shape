# Stitch Canvas Bridge — Audit Criteria (`stitch-canvas`)

1. **Credential & URL Hygiene (Zero-Trust):**
   - `[PASS]` Uses `~/.stitch.json` or MCP `stitch` headers (`https://stitch.googleapis.com/mcp`), resolves Canvas links via `stitch url`, and restricts asset downloads to verified HTTPS Google Stitch domains (`*.googleusercontent.com`, `storage.googleapis.com`, `stitch.googleapis.com`).
   - `[FAIL]` Any literal API key inside repo files, CLI `--api-key` logs, constructed Canvas URLs, or unvalidated download URLs.

2. **Protocol & Handoff Integrity:**
   - `[PASS]` `apply_design_system` passes only `{id, sourceScreen}` (excluding `DESIGN_SYSTEM_INSTANCE`), screenshots include `=w{width}`, downloaded artifacts pass SHA-256 Read-After-Write, and translated UI enters `ui-brand-ux-planner` -> `ui-clean-worker` -> `ui-quality-judge` (`OKLCH 60-30-10`, Tailwind v4 `@theme`, zero fake metrics or `#000000`).
   - `[FAIL]` Low-res thumbnail downloads missing `=w{width}`, position keys inside `selectedScreenInstances`, raw Tailwind v3 CDN boilerplate in production, or unconfirmed `stitch config set project` / batch uploads.
