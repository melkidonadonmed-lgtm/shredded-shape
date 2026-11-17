# UI Frontend Analyst — Audit Criteria (`ui-frontend-analyst`)

1. **Deterministic Scanner & 12-Vector Slop Thresholds:**
   - `[PASS]` `frontend_inventory_and_slop_scanner.py` returns `verdict == "[PASS]"`, `ai_slop_score <= 15`, zero mixed icon libraries, zero emojis in controls, valid `60-30-10` OKLCH signal, and full 12-Vector Anti-Slop clearance.
   - `[FAIL]` Any presence of `#000000`, neon (`#00ffff`, `C > 0.22`), blur blobs (`blur-3xl`), confetti badges (`>= 3` colored pills), dashed wireframe containers (`border: 1px dashed`), amateur `<svg>` clouds, reflow transitions (`all`, `width`, `height`), `DOM != Tab` order (`row-reverse`, positive `order`), or `ai_slop_score > 15`.

2. **Modularity, Typography & Telemetry Thresholds:**
   - `[PASS]` All UI/logic modules `<= 600` lines, body uses `text-rendering: auto` with heading-only `optimizeLegibility`, live INP `<= 200ms`, LCP `<= 2.5s`, zero DevTools `Issues` blockers, and a complete 7-section CLAREZA report with `As-Is` + `To-Be` Mermaid flows.
   - `[FAIL]` Monolith UI files `> 600` lines unflagged, mixed icon packages (`lucide-react` + `react-icons`/`heroicons`), `forwardRef` legacy patterns in React 19, missing `modern-web-guidance` check, or missing navigation Mermaid graphs.
