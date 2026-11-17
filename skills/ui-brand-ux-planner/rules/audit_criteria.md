# Audit Criteria — `ui-brand-ux-planner`

- **`[PASS]`**: `<project_root>/DESIGN.md` defines brand purpose, `60-30-10` `OKLCH` tokens (zero neon, zero `#000000`), one explicit style archetype (`soft|hi-tech|tactile|elevated|retro|vintage|clinical`), font/icon/asset sources (`Google Stitch`, `Figma MCP`, `Google Fonts`, `3D/Unity` if applicable), zero-verbiage UX rules, and a `ui_dag_compiler.py`-validated DAG (`<= 5` rules/node, zero parallel write collisions).
- **`[FAIL]`**: Plan exceeds `5` active constraints per DAG node, omits `fallback_branch`, recommends neon colors or explanatory text clutter, or omits style archetype/stack choices.
- **`[UNVERIFIED]`**: Product scope is missing or external MCP/browser asset retrieval could not run when explicitly required.
