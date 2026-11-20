# UI Frontend Analyst — Audit Criteria (`ui-frontend-analyst`)

1. **Intent-First, Deterministic Scanner & AppSec Thresholds:**
   - `[PASS]` `[CoT-0]` locks intent (or infers `baseline_forensic_audit` headless-safely on concrete targets); `frontend_inventory_and_slop_scanner.py` returns `verdict == "[PASS]"`, `ai_slop_score <= 15`, zero mixed icon libraries, zero client secret leaks (`AUDIT-SEC-ENV-LEAK`, logged `[REDACTED]`), zero omission comments (`AUDIT-STUB-PLACEHOLDER`), zero raw HTML/`eval` sinks (`AUDIT-SEC-01`), valid `60-30-10` OKLCH, and standalone `<feColorMatrix>` isolated from `<feGaussianBlur>`.
   - `[FAIL]` Any presence of `#000000`, neon (`#00ffff`, `C > 0.22`), blur/gooey blobs, confetti badges, dashed wireframes, gradient text (`ANTI-SLOP-GRADIENT-TEXT`), `grid-auto-flow: dense`, reflow transitions, `DOM != Tab` order, client secret leaks, placeholder omission comments, or `ai_slop_score > 15`.

2. **Modularity, Advisory Hygiene & Telemetry Thresholds:**
   - `[PASS]` All UI modules `<= 600` lines, body uses `text-rendering: auto` with heading-only `optimizeLegibility`, live INP `<= 200ms`, LCP `<= 2.5s`, zero mystery icon-only nav (`mysteryIconOnlyNavCount == 0`), causal `Friction X -> Impact Y` 7-section CLAREZA report, and advisory `root_hygiene_warnings` / `menu_label_audit` surfaced cleanly without polluting `ai_slop_score`.
   - `[FAIL]` Monolith UI files `> 600` lines unflagged, mixed icon packages, `forwardRef` legacy patterns, missing `modern-web-guidance` check, or missing navigation Mermaid graphs.
