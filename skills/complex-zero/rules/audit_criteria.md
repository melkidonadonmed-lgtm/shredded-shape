# Complex-Zero — Audit Criteria (`complex-zero`)

1. **AST, Dagre/Windows Paths, Next.js 15+ & Telemetry Integrity:**
   - `[PASS]` `complex_zero_ast_auditor.py` returns `[PASS]`, zero fake `setTimeout` stubs, zero dangling Ghost Nodes inside target bounds, valid Rules of Hooks order, hoisted/memoized `nodeTypes`/`edgeTypes`, Dagre `TB`/`LR` + `setCenter` log sync, Windows `replace(/\\/g, "/")` watcher paths, Next.js 15+ `(group)/`/`_components/` + `await params`, `150ms` WebSocket/chokidar batching, per-sink `DOMPurify.sanitize()`, and modules `<= 600` lines.
   - `[FAIL]` Sync `params.id` dereference, inline `nodeTypes={{` or unhoisted `nodeTypes`, unnormalized `path.relative()`, un-throttled `setNodes`, conditional hook calls, swallowed `catch {}`, `forwardRef`, or `> 600`-line monoliths.

2. **ReAct CDP Optical & Craft Gates:**
   - `[PASS]` `visual_hierarchy_and_cdp_probe.py` passes exact 2.4 W3C luminance contrast (`>= 4.5:1`), `<= 6` primary tabs, `<= 3` `<nav>` landmarks, `>= 8px` nav gap & `>= 44px` hit targets, collapsed-rail tooltips, stable `Performance Monitor` DOM/heap counts, INP `<= 200ms`, `text-rendering: auto` on node bodies, crisp single-library `24x24` SVGs, zero `#000000`, zero neon glows, and clean `ui_judge_gatekeeper.py --composite` pass.
   - `[FAIL]` Mixed icon packs, amateur SVGs, blur blobs, confetti badges, dashed wireframes, gradient text, reflow transitions, `> 6` primary tabs, mystery icon rails lacking tooltips, unbounded heap/DOM growth, or violating Stage Role Guards during read-only inspection.
