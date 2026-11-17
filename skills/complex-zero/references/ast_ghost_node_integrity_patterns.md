# AST Ghost Node, Hook Order & Fake-Stub Integrity Patterns

`complex_zero_ast_auditor.py` enforces structural integrity across dense TypeScript/TSX telemetry applications and multi-file HTML/CSS/JS bundles before browser verification.

## 1. Confined Ghost Node & Multi-File Bundle Boundaries
- Resolve local `@/` and relative paths strictly inside `target_root` (`candidate.resolve().is_relative_to(target_root)`), flagging unresolved Ghost Nodes without escaping the project directory.
- When auditing single `.html` entrypoints (e.g., `assets/ui_skills_architecture_atlas.html`), `_collect_target_files()` calls `_ss_core.collect_ui_files(target)` so linked local stylesheets and scripts are audited together against `target.parent`.
- Exempt legitimate React `createContext()` default providers while tracking legacy `forwardRef` usage separately for React 19 migration.

## 2. Deterministic Code Smell & Safety Matrix
| Audit Check | Rejected Anti-Pattern (`[FAIL]`) | Required Remediation (`[PASS]`) |
| :--- | :--- | :--- |
| **Fake Async Stubs** | `onClick={() => {}}`, `console.log`-only handlers, `setTimeout(() => setState(mock))`, `Math.random()` telemetry. | Bind real `fetch`/`WebSocket` + `AbortController` streams mapped to `idle | loading | empty | error | success`. |
| **Placebo Verification** | Hardcoded `' [PASS]'` string concatenation or `oklchContrastValid: true` stubs. | Compute real runtime state/metrics without hardcoded pass badges (`<= 2` node badges). |
| **React Rules of Hooks** | Conditional `useState` / `useEffect` inside branches or after early `return` guards. | Hoist all React hooks unconditionally above guard returns. |
| **Swallowed Errors & Security** | Empty `catch {}` blocks, raw `dangerouslySetInnerHTML`, or `eval()`. | Transition UI FSM explicitly to `error` state; sanitize dynamic markup via `DOMPurify.sanitize()`. |
| **File Modularity** | `.tsx`/`.ts`/`.html`/`.css`/`.js` files exceeding `600` lines (`<= 60` lines/fn). | Split cleanly by concern (`hooks/`, `nodes/`, `atlas_styles.css`, `atlas_app.js`). |
