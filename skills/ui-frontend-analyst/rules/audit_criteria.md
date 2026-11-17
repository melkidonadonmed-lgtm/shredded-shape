# Audit Criteria — `ui-frontend-analyst`

- **`[PASS]`**: `frontend_inventory_and_slop_scanner.py` ran cleanly on real disk files (plus `devtools_live_probe.js` when a live URL was provided), all tokens/colors/fonts/menus/icons/spacing/contracts/stack are inventoried by location, `ai_slop_score` is computed deterministically, and a Mermaid Current Navigation Diagram + `Before vs. After` comparison table are emitted.
- **`[FAIL]`**: Report omitted per-file color/token locations, guessed metrics without running the scanner/DevTools probe, or failed to propose route/sidebar decompositions for overloaded navigation.
- **`[UNVERIFIED]`**: `target_path` contained zero `.html`/`.css`/`.tsx`/`.jsx`/`.vue` assets or `live_url` could not be reached by Chrome DevTools MCP.
