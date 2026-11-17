# Navigation Diagramming & `Before vs. After` Refactoring Patterns

## 1. Current Navigation Diagram (`As-Is`)

Extract all `<Link>`, `<a href>`, `<nav>`, route files (`app/**/page.tsx`, `routes`), top-bar tabs, and modal/drawer triggers into a deterministic Mermaid flowchart highlighting:
- **Overloaded Root Hubs:** Screens exceeding `5` primary navigation destinations or mixing unrelated admin/backend tabs into primary user workflows.
- **Dead-Ends:** Nested views lacking breadcrumbs (`<ol role="list">`) or back anchors.
- **Duplicate Triggers:** Multiple buttons/tabs triggering the same underlying filter or route.

## 2. Canonical `Before vs. After` Structural Mutations

| Observed Structural Problem (`Before`) | Recommended Refactoring (`After`) | Target Layout Primitive |
| :--- | :--- | :--- |
| Top navbar overflows on `1024px–1280px` or packs `> 5` actions | Extract secondary groups into a **`240px–260px` Collapsible Sidebar Rail** (collapsed `72px` icon rail with tooltips) + `< 48em` Mobile Bottom Bar (`3–5` primary items) | Single-DOM `.adaptive-nav` + `ResizeObserver` / `popover="auto"` |
| Single dashboard page piles 6+ vertical sections (`> 3` viewports tall) | Split unrelated workflows (e.g., Settings, Audit Logs, Token Catalog) into dedicated child routes with `<ol role="list">` Breadcrumbs | Next.js App Router `(workspace)/<route>/page.tsx` |
| Complex filters and inspectors crowd the canvas | Move secondary controls into a collapsible right Inspector Pane or `<dialog>` / Slide-over Drawer (`overscroll-behavior-y: contain`) | Workbench Split-View Archetype |
| Dense card grid hides actions behind raw text blocks | Convert to 4 `<article>` `subgrid` card regions with `a.card-link::after` stretched click target and crisp icon actions (`z-index: 1`) | RAM Grid + `@container` |
