# 7 Style Archetypes, 6 Spatial Archetypes & 5-Plane `OKLCH` Matrix

Select 1 canonical Style Archetype, 1 Spatial Archetype CLI slug, and `site-kind` upfront; pair them with numeric **Ergonomic Dials** (`Variance / Motion / Density` `1..10`) aligned 1:1 with `_ss_core.STYLE_PRESETS`.

## 1. The 7 Style Archetypes (`_ss_core.STYLE_PRESETS` SSOT)

| Style Slug | Radius (`_ss_core`) | Canonical Font (`_ss_core`) | Chroma Cap & Default Spatial | Optical Surface & Menu Chrome | Dials (`V/M/D`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`soft`** | `1.35rem` | `Plus Jakarta Sans` | `C <= 0.12` / `bento_12_col` | `135°` Soft Tactile dual shadows (`8px 8px 20px / -8px -8px 20px`), `rounded_pill_sidebar`, concentric nested radii. | `V:4 / M:5 / D:3` |
| **`hi-tech`** | `0.375rem` | `Space Grotesk` | `C <= 0.14` / `command_center_grid` | `--light-zenith` sheen, `0.058` side hairline, `--rim-top`, `precision_rail_2px`, recessed `.search-well`. | `V:7 / M:6 / D:7` |
| **`tactile`** | `1.0rem` | `Plus Jakarta Sans` | `C <= 0.16` / `workbench_split_view` | 5-Plane **Tactile Matte** (`--bg-well`..`--bg-key`), `tactile_48px_rail`, `.tactile-key` & `.engraved-pill` + `6px` `.lum-bead`. | `V:6 / M:5 / D:5` |
| **`elevated`** | `1.10rem` | `Inter` | `C <= 0.15` / `bento_12_col` | Multi-layer Umbra + negative-spread Penumbra, `frosted_sticky_header` (`blur(18px) saturate(145%)`). | `V:5 / M:4 / D:5` |
| **`retro`** | `0.25rem` | `Space Grotesk` | `C <= 0.17` / `workbench_split_view` | Crisp architectural borders, `geometric_block_tabs`, controlled offset elevation, warm neutral ground. | `V:8 / M:3 / D:6` |
| **`vintage`** | `0.50rem` | `Instrument Serif` | `C <= 0.11` / `editorial_65ch` | Quiet Titanium / editorial dual-tone frames, `editorial_toc_65ch`, serif headings + `tabular-nums`. | `V:6 / M:2 / D:4` |
| **`clinical`** | `0.50rem` | `IBM Plex Sans` | `C <= 0.12` / `workbench_split_view` | `7.0:1` WCAG AAA legibility, `ehr_3click_sidebar`, zero `box-shadow` in `@media print`, `.sus-grid` A4 mm precision. | `V:2 / M:2 / D:8` |

Note: CLI `--style hitech` normalizes automatically to canonical **`hi-tech`** via `_ss_core.normalize_style_archetype()`.

## 2. The 6 `SpatialArchetype` CLI Slugs (`ui_dag_compiler.py`)
1. **`bento_12_col`** (`--spatial bento_12_col`): 12-column asymmetric Bento grid (`span-8` / `span-4`, `gap >= 20px`) pairing recessed slots with raised cards.
2. **`workbench_split_view`** (`--spatial workbench_split_view`): Adaptive Single-DOM sidebar (`248px <-> 64px` / Mobile Bottom Bar) paired with a sticky detail/inspector workspace.
3. **`command_center_grid`** (`--spatial command_center_grid`): Telemetry HUD combining recessed command search, category filter rail, and live inspector drawer (`M3 1.2`).
4. **`editorial_65ch`** (`--spatial editorial_65ch`): Centered `65ch` prose cadence (`M3 1.5`) with sticky ToC rail and generous vertical rhythm.
5. **`spatial_hud_dock`** (`--spatial spatial_hud_dock`): `@xyflow/react` infinite viewport anchored by frosted `top-left` / `bottom-center` floating docks (`<= 6` actions).
6. **`vector_a4_print`** (`--spatial vector_a4_print`): Triage top header + dual-column form/prescription flow projecting cleanly to `@page A4` `.sus-grid` print sheets.

## 3. Unified 5-Plane `OKLCH 60-30-10` Surface Ladder
- **`--bg-well` / `--surface-sunken`** (`L = 0.118` Dark / `0.922` Light): Deeply carved wells for `.search-well`, `.engraved-pill`, and `.inset-panel`.
- **`--bg-canvas` / `--surface-canvas`** (`L = 0.145` Dark / `0.962` Light): 60% mineral canvas (never `#000000`).
- **`--bg-card` / `--surface-card`** (`L = 0.195` Dark / `0.994` Light): 30% anodized slab carrying `--light-zenith` + `inset 0 1px 0 var(--rim-top)`.
- **`--bg-card-lit` / `--surface-elevated`** (`L = 0.235` Dark / `1.000` Light): Active/hover surface (`-2px` lift + `--light-zenith-hover`, zero glowing cyan borders).
- **`--bg-key` / `--surface-key`** (`L = 0.262` Dark / `0.996` Light): Physical `.tactile-key` caps paired with `--ink-on-key` (`CR >= 4.5:1`). Use `color-mix(in oklab, ...)` for dynamic mix states, `@media (color-gamut: p3)` within `C <= 0.20`, Dark `0.14 -> 0.18 -> 0.22` matte metal step + machined top bevel (`inset 0 1px 0`), `text-wrap: balance/pretty`, and neutral `.engraved-pill` + `6px` `.lum-bead` LEDs instead of confetti, gradient text, side-stripes, or `01/02/03` clutter.
