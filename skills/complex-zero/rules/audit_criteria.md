# Complex-Zero — Audit Criteria (`complex-zero`)

1. **AST, Next.js 15+ & Telemetry Integrity:**
   - `[PASS]` `complex_zero_ast_auditor.py` returns `[PASS]`, zero fake `setTimeout` stubs, zero dangling Ghost Nodes inside target bounds, valid Rules of Hooks order, explicit `await params` / `use(params)` in Next.js 15+, coalesced `150ms` WebSocket/chokidar batching, `DOMPurify.sanitize()` on rich telemetry HTML, and modules `<= 600` lines.
   - `[FAIL]` Sync `params.id` dereference in Next.js 15+, un-throttled per-message `setNodes`, conditional hook calls, swallowed `catch {}`, `forwardRef` legacy patterns, or `> 600`-line monoliths.

2. **ReAct CDP Optical & Craft Gates:**
   - `[PASS]` `visual_hierarchy_and_cdp_probe.py` passes exact 2.4 W3C luminance contrast (`>= 4.5:1`), `<= 6` primary tabs, `<= 3` `<nav>` landmarks, stable `Performance Monitor` DOM/heap counts, INP `<= 200ms`, `text-rendering: auto` on node bodies, crisp single-library `24x24` SVGs, zero `#000000`, zero neon glows, and clean `ui_judge_gatekeeper.py --composite` pass.
   - `[FAIL]` Mixed icon packs, amateur SVGs, blur blobs, confetti badges, dashed wireframes, reflow transitions, `> 6` primary tabs, unbounded heap/DOM growth during live socket telemetry, or violating Stage Role Guards during read-only inspection.
