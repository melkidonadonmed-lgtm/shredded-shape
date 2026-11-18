# Stitch 18-Tool MCP & CLI `0.13.0` Reference

Reference table for operating Google Stitch via remote MCP (`https://stitch.googleapis.com/mcp`) and `@google/stitch@0.13.0` CLI on Windows/POSIX without bash `.sh` dependencies.

## 1. Remote MCP Tools (`18` Tools via `stitch` Server)
- **Projects:** `list_projects`, `get_project`, `create_project`, `update_project`, `delete_project` (HITL confirm before `delete_*`).
- **Screens & Assets:** `list_screens`, `get_screen`, `update_screen`, `download_file`.
- **Generation & Iteration:** `generate_screen_from_text`, `edit_screens`, `generate_variants`.
- **Design Systems:** `list_design_systems`, `create_design_system`, `upload_design_md`, `create_design_system_from_design_md`, `update_design_system`, `apply_design_system`.

## 2. Critical Payload Rules
- **`selectedScreenInstances` (`apply_design_system`):** Retrieve `screenInstances` from `get_project`, filter out entries with `type == "DESIGN_SYSTEM_INSTANCE"`, and keep strictly `{"id": "...", "sourceScreen": "projects/.../screens/..."}`. Omitting `x`, `y`, `width`, and `height` prevents `"invalid argument"` API rejections.
- **Full-Res Screenshot URLs:** Append `=w{width}` (using `screen.width` from `get_screen`) to `screenshot.downloadUrl` before HTTP GET, or run `stitch_asset_bridge.py download-screen`.
- **Prompt Scope Rule:** When `list_design_systems` returns an active Design System for the project, keep `generate_screen_from_text` prompts restricted to platform, layout zones, and copy; omit hex codes and font families (use hex overrides only in targeted `edit_screens` calls).

## 3. CLI `0.13.0` Commands (`stitch` Binary, Reads `~/.stitch.json`)
- **Probe & Auth Status:** `stitch status --flow=design --json`, `stitch find projects --limit 10 --json`, `stitch url project <id>`, `stitch url screen <sid> --project <pid>`.
- **Capture Live App (Replaces Custom Puppeteer):**
  - Direct URL: `stitch capture http://localhost:5173/dashboard -o .stitch/dashboard.html`
  - Open DevTools tab (behind auth/modal): `stitch capture browser --page 1 -o .stitch/captured-dom.html --json`
  - Preview screens locally: `stitch serve -p <project-id> --port 3000`
- **Upload & Sync:** `stitch upload screen .stitch/captured-dom.html --route /dashboard --title "/dashboard"` and `stitch upload design DESIGN.md --project <id>` (avoids passing `--api-key` in CLI args).
