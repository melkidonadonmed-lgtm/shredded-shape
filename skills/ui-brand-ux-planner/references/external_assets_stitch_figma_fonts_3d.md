# External Assets: Stitch Spacing, Figma `@theme`, Fonts, SVG Sprites & 3D

Pair perceptual CSS math with deterministic Stitch proximity, single-library SVGs, Figma token mapping, Variable Fonts, and hardware-accelerated 3D scenes.

## 1. Google Stitch Relational Spacing & Concentric Geometry
Enforce clear Gestalt separation where gaps always step monotonically with nesting depth:
- **Spacing Scale (`4px/8px` Grid):** `4, 8, 12, 16, 20, 24, 32, 48, 64px` (zero arbitrary `7px`/`13px`/`19px` literals).
- **Proximity Rule:** $\text{Inner Gap} < \text{Card Padding} \le \text{Grid Gap} < \text{Section Inset}$ (e.g., `8px` label-to-input `< 20px` card padding `<= 20px` grid gap `< 32px..48px` section margin).
- **Concentric Corner Rule:** $R_{\text{inner}} = \max(4\text{px}, R_{\text{outer}} - \text{Padding})$, ensuring nested buttons/wells never look pinch-cornered or visually detached.
- **Box Model Hygiene:** Mandate `*, *::before, *::after { box-sizing: border-box; }` and `display: flow-root` / CSS `gap` to prevent margin collapse.

## 2. Figma MCP -> Tailwind v4 `@theme` Mapping
1. Query Figma `get_variable_defs` and `get_design_context`, then normalize hex colors to `OKLCH` (`light-dark()`) inside `@layer tokens` and expose them via Tailwind v4 CSS-first `@theme`.
2. **Dark Polarity Mapping:** Pair `@custom-variant dark (&:where([data-theme*="dark"], .dark, .dark *));` so utility classes follow semantic surface tokens cleanly.
3. **Mixing Precision:** Map translucent/hover mixes to `color-mix(in oklab, var(--brand-primary) 16%, var(--bg-card))` rather than `color-mix(in oklch)`.

## 3. Google Fonts, M3 Type Scale & Subsetting
- **Font Loading & Metrics:** Prefer self-hosted Variable WOFF2 (with metric-adjusted system fallback stacks in static offline Atlases) and set `font-display: swap`, `font-optical-sizing: auto`, `font-synthesis: none`, `text-rendering: auto` (`body`), and `optimizeLegibility` (`h1..h3` only).
- **Material Design 3 Ratio:** `1.2` minor-third for telemetry/EHR (`tabular-nums`); `1.5` perfect-fifth for editorial showcases (`max <= 2.5 * min`, `65ch` measure).
- **Subsetting:** Shrink heavy custom variable fonts via `uvx --from fonttools pyftsubset --unicodes="U+0020-007E,U+00A0-00FF"`.

## 4. Single-Library Web SVG Strategy (Zero Mixed Packs)
Select **exactly ONE** icon family per application (`npx svgo --multipass` optimized):

| Ecosystem | Format & Strategy | Best Fit | Explicit Anti-Slop Rule |
| :--- | :--- | :--- | :--- |
| **Lucide (`lucide-react` / `<symbol>`)** | `24x24` `stroke="currentColor" fill="none" stroke-width="2"` | Default React / Next.js / HTML Atlases | Copy verified paths; zero circle-cloud blobs. |
| **Material Symbols SVG** | Inline `24x24` `<svg>` (`<= 25` icons) | Android / Clinical PEP/EHR chrome | Match single optical weight (`400`/`500`) across chrome. |
| **Phosphor / Fluent Web SVGs** | `@phosphor-icons/react` or `@fluentui/react-icons` | Studio or Enterprise Web portals | Web SVG components ONLY; never mix packages. |

## 5. Next.js 15+ Async Params & 3D Unity / WebGL (`MATH_PHYSICS_3D`)
- Type dynamic routes as `Promise<...>` and unwrap via `const { id } = await params;`.
- For **Unity Hub** WebGL builds or `@react-three/fiber`, bound draw calls (`<= 100` instanced), validate PBR roughness + rim contrast, and route vector/shader math through `adk-go-mcp-router` (`MATH_PHYSICS_3D`).
