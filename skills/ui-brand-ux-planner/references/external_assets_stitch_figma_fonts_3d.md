# External Asset Pipelines: Google Stitch, Figma MCP, Google Fonts & 3D / Unity

## 1. Google Stitch Palette & Concept Extraction (`agent-browser`)

1. Request HITL confirmation before opening external web sessions if restricted, then launch `agent-browser` targeting Google Stitch (`stitch.withgoogle.com`).
2. Feed the product brand brief + target archetype (`Soft`, `Hi-Tech`, `Tactile`, etc.) to explore visual directions and extract hex/OKLCH palette values.
3. Convert every extracted color into 3-layer `oklch(L C H / alpha)` + `light-dark()` tokens inside `DESIGN.md`, clamping chroma to `C <= 0.20` (zero neon) and verifying Dark Mode `L_card > L_canvas`.

## 2. Vector Icons & Design System Tokens via Figma MCP

1. Query connected Figma MCP (`figma` server when active) to inspect frame variables, typography scales, spacing primitives, and export clean single-stroke vector `.svg` icons (`stroke-width: 1.5..1.75`, `16/20/24px`).
2. Fallback when Figma MCP is not configured: standardize on **Lucide** (`lucide-react`) or **Phosphor** (`@phosphor-icons/react`) — never draw amateur custom icons or mix stroke weights.

## 3. Google Fonts Download & Variable Font Pairing

- **Preferred Web Delivery:** Download `.woff2` variable subsets locally (`public/fonts/` or `assets/fonts/`) or wire `next/font/google` (`display: 'swap'`, `variable: '--font-sans'`) so zero layout shift (CLS `<= 0.1`) occurs and `font-synthesis: none` holds.
- **Canonical 3-Font Budget (Max 2–3 Families):**
  - UI Sans: `Inter`, `Plus Jakarta Sans`, `Geist`, or `IBM Plex Sans`.
  - Data / Code Mono (`tabular-nums`): `JetBrains Mono`, `IBM Plex Mono`, or `Geist Mono`.
  - Optional Editorial Serif (`vintage`/`editorial` only): `Instrument Serif` or `Newsreader`.

## 4. 3D Pipeline (`Three.js`, `@react-three/fiber` & Local `Unity Hub 3.22.6`)

- Only activate 3D assets when requested by product scope (never inject decorative 3D bloat).
- **WebGL / `Three.js`:** Use `@react-three/fiber` + `@react-three/drei`, compress meshes to `.glb` (`Draco` / `Meshopt`), cap active WebGL contexts (`<= 4`), and schedule `code-quality-audit-3d-physics` on hot loops.
- **Local Desktop Toolchain (`Unity Hub 3.22.6` / Blender CLI):** When building interactive 3D scenes/models locally, invoke Unity/Blender CLI export pipelines cleanly for `.glb`/WebGL builds, documenting asset budgets (`< 5 MB` compressed scene) inside `DESIGN.md`.
