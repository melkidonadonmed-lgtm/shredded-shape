---
name: stitch-canvas
description: "Use when bridging Google Stitch Canvas via stitch CLI v0.13.0 or 18-tool Stitch MCP: capturing live routes, creating/generating screens or variants, syncing DESIGN.md, and downloading HTML/PNG (=w{width}) for OKLCH translation. Do NOT use for local DevTools slop audits (ui-frontend-analyst) or final WCAG judging (ui-quality-judge)."
license: MIT
compatibility: "Antigravity 2.0 / Claude Code / Gemini CLI with Python 3.12+ (uv), Node.js 20+, and @google/stitch CLI"
allowed-tools: "read_file write_file edit_file run_command call_mcp_tool"
metadata:
  author: "shredded-shape"
  version: "1.6.0"
  updated_at: "2026-11-19"
  category: "stitch-canvas-bridge"
  tags: "stitch-canvas, stitch-cli, stitch-mcp, capture-screen, generate-screen, canvas-bridge, stitch-variants"
---

# Stitch Canvas Bridge & Handoff (`stitch-canvas`)

## Overview
Decoupled bridge between **Google Stitch** (`@google/stitch` CLI `0.13.0` + 18-tool remote MCP `stitch`) and `shredded-shape`'s `OKLCH 60-30-10` Actor-Critic pipeline (`Code -> Stitch`, `Canvas` screens/variants, `Stitch -> OKLCH`).

## Inputs
- Stitch `projectId`/`screenId`, local URL (`http://localhost:<port>`), or 8-section `DESIGN.md`.
- Mode: `code-to-stitch`, `canvas-generate`, or `stitch-to-oklch`.

## Procedure
Operate under **Zero-Trust Secret Hygiene** (`~/.stitch.json` / MCP headers only; never pass API keys in CLI flags or logs):

1. **Phase 1 — Flow Probe:** Run `stitch status --flow=design --json` and `stitch find projects --json` (or MCP `list_projects`). Load [`references/stitch_mcp_18_tools_and_cli.md`](references/stitch_mcp_18_tools_and_cli.md) for the 18 MCP tools vs. CLI `0.13.0` commands.
2. **Phase 2 — `Code -> Stitch` Capture & Upload:** Capture hydrated routes via `stitch capture <url> -o .stitch/captured-dom.html` (or `stitch capture browser --page 1` after `chrome-devtools` login; never edit `src/` to bypass auth). Confirm with the user before `stitch config set project` or batch `stitch upload screen`/`design` (or MCP `upload_design_md` + `create_design_system_from_design_md`).
3. **Phase 3 — `Canvas` Screens, Variants & Design Systems:** Check `list_design_systems` first; when active, keep `generate_screen_from_text` focused strictly on layout/copy (no conflicting hex/font overrides). Before `apply_design_system`, filter `get_project().screenInstances` via `stitch_asset_bridge.py filter-instances` (excludes `DESIGN_SYSTEM_INSTANCE`, keeps `{id, sourceScreen}` only).
4. **Phase 4 — `Stitch -> OKLCH` Download & Handoff:** Append `=w{width}` to screenshot URLs and verify SHA-256 via `stitch_asset_bridge.py`:
   - Plugin (`pwsh`/POSIX): `uv run "$HOME/.gemini/config/plugins/shredded-shape/skills/stitch-canvas/scripts/stitch_asset_bridge.py" --self-test`
   - Repo fallback: `uv run python skills/stitch-canvas/scripts/stitch_asset_bridge.py --self-test`
   Translate artifacts via [`references/stitch_to_oklch_translation.md`](references/stitch_to_oklch_translation.md) into `ui-brand-ux-planner` (`5-Plane OKLCH`, `Tailwind v4 @theme`) -> `ui-clean-worker` -> `ui-quality-judge` against [`rules/audit_criteria.md`](rules/audit_criteria.md).

## Gotchas
- **Full-Res Screenshots:** Always pass `=w{width}` via `normalize-url` to avoid low-res thumbnails.
- **Zero Production Slop:** Strip Stitch Tailwind v3 CDN/config blocks, `#000000`, `href="#"`, fake `"99.98% UPTIME"` stats, `"LABEL // YEAR"` headers, gradient-text clips, decorative side-stripes, and ALL-CAPS eyebrow clutter before shipping.
- **Canonical URLs:** Always resolve Canvas links with `stitch url project <id>` / `stitch url screen <sid> --project <id>`.

## Output
- Synced `.stitch/` state, SHA-256-verified HTML/PNG assets, or `OKLCH` `DESIGN.md` handoff.

## User Communication
Keep scripts, JSON payloads, and tokens in Technical English; present Canvas links (`[Open in Stitch Canvas](<url>)`) and confirmations in **Portuguese (`pt-BR`)**.
