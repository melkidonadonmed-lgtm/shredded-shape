# Anti-AI-Slop & Style Debt Rubric (Distilled from `taste-skill` + 9-Axis SSOT)

## 1. What Triggers High `ai_slop_score` (`0..100`, target `<= 15`)

| Defect Category | Detection Signal | Penalty Weight | Required Remediation |
| :--- | :--- | :---: | :--- |
| **UI Emojis & Decoration** | Unicode emojis (`🚀`, `✨`, `🔥`, `💡`) in UI labels/cards | `+15` each (cap `30`) | Replace with crisp `16–24px` vector SVGs (`lucide-react`, `phosphor`) with uniform `stroke-width` |
| **Generic Copy Clichés** | Stock AI SaaS phrases (*"Unlock the power"*, *"Next-gen seamless"*, *"10,000+ teams"*, fake *"Priya/Apex/Lumen"* placeholder names, tutorial paragraphs) | `+10` per cluster | Replace with brief-grounded factual labels and zero-verbiage intuitive controls |
| **Chromatic & Dark-Mode Errors** | `#000000` canvas, neon accents (`chroma > 0.24`), uncalibrated `#hex`/`rgba()` sprawl instead of `oklch()`/`light-dark()`, violet gradient SaaS cliché | `+15` | Calibrate `60-30-10` `oklch()` palette with `L = 0.16 -> 0.22 -> 0.27` dark elevation |
| **Flat / Muddy Depth** | Single-pass `rgba(0,0,0,0.4)` shadows, dark drop shadows on dark canvas without rim catch-light, `!important` overrides | `+10` | Apply 3-layer optical shadows (light) and specular rim + soft surface halo (dark) |
| **Layout & Spacing Chaos** | Off-scale Tailwind (`p-[13px]`, `gap-[7px]`), missing `box-sizing: border-box`, uncontained margin collapse, cramped nav (`<13px`), fractional `scale()` on text | `+10` | Normalize to `4px/8px` primitives + Stitch semantic `--space-*` tokens |
| **Mixed Icon Sets / Bloat** | Mixing outline + solid icon packages inconsistently, hand-drawn SVG fake logos, inline Base64 images `> 50 KB` | `+10` | Standardize a single crisp vector icon family or Figma MCP export |
