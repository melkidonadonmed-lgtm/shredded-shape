# AGENTS.md — Repository Delta & Actor-Critic Topology (`shredded-shape` v1.4.0 / Triad v2.1)

> **Global & Optical Inheritance:** Universal Golden Rules (1–8) and the Self-Refine Closing Block inherit from `quality-efficiency-guidelines.md` (`always_on`); 9-Axis `OKLCH 60-30-10` and 3-layer optical physics load via [`rules/frontend-9-axes-guidelines.md`](file:///C:/Users/melki/dev/repos/shredded-shape/rules/frontend-9-axes-guidelines.md) (`trigger: glob`).

## 0. PROJECT CONTEXT & COMMANDS

- **Project:** `shredded-shape` (**UI/UX Architecture, Forensic DevTools/REA Analyst, Brand & Style Planner, Clean Optical Worker, and WCAG 2.2 OKLCH Actor-Critic Judge Suite**).
- **Active Stack:** Python 3.12+ (`uv` / `pyproject.toml`, `pydantic`, `pyyaml`, `pytest`) + Chrome DevTools Live Probe JS + Modern CSS (`OKLCH`, `light-dark()`, `@container`, `subgrid`, Tailwind v4 `@theme`) + Windows 11 (`pwsh`).
- **Executable Commands (`Command-First`):**
  - **Deterministic Skill & Plugin Validator (`6/6` skills, `4/4` subagents):** `uv run python scripts/validate_shredded_shape.py --strict`
  - **Unit, Optical Math & Adversarial Test Suite:** `uv run pytest -q`
  - **Plugin & Ecosystem Sync (`~/.gemini/config/plugins/shredded-shape/`):** `uv run python scripts/sync_shredded_shape.py`
- **State Triad:** [`.context/context.md`](file:///C:/Users/melki/dev/repos/shredded-shape/.context/context.md) | [`.context/spec.md`](file:///C:/Users/melki/dev/repos/shredded-shape/.context/spec.md)

## 1. 4-STAGE ACTOR-CRITIC SUBAGENTS (`agents/*.md`) & 6 SKILLS (`skills/*`)

| Stage / Role | Subagent (`agents/*.md`) | Core Skill (`skills/*`) | Mode & Max Rules |
| :--- | :--- | :--- | :--- |
| **Stage 0 — Forensic Analyst** | [`ui-analyst`](file:///C:/Users/melki/dev/repos/shredded-shape/agents/ui-analyst.md) | [`ui-frontend-analyst`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/ui-frontend-analyst/SKILL.md), [`complex-zero`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/complex-zero/SKILL.md), `chrome-devtools`, `a11y-debugging`, `debug-optimize-lcp`, `memory-leak-debugging`, `modern-web-guidance` | Read-Only CoT (`sandbox`, `<= 5` rules) |
| **Stage 1 — Brand & DAG Planner** | [`ui-planner`](file:///C:/Users/melki/dev/repos/shredded-shape/agents/ui-planner.md) | [`ui-brand-ux-planner`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/ui-brand-ux-planner/SKILL.md), [`clinical-minimalist-ui`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/clinical-minimalist-ui/SKILL.md), `complex-zero`, `modern-web-guidance` | Read-Only ToT (`sandbox`, `<= 5` rules) |
| **Stage 2 — Clean Optical Worker** | [`ui-worker`](file:///C:/Users/melki/dev/repos/shredded-shape/agents/ui-worker.md) | [`ui-clean-worker`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/ui-clean-worker/SKILL.md), `clinical-minimalist-ui`, `complex-zero`, `modern-web-guidance` | ReAct + RAW SHA-256 (`auto`, `<= 5` rules) |
| **Stage 3 — WCAG 2.2 Judge** | [`ui-judge`](file:///C:/Users/melki/dev/repos/shredded-shape/agents/ui-judge.md) | [`ui-quality-judge`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/ui-quality-judge/SKILL.md), `clinical-minimalist-ui`, `complex-zero`, `a11y-debugging` | Read-Only Self-Refine Gatekeeper (`sandbox`, `<= 5` rules) |

## 2. REPOSITORY INVARIANTS & EVOLUTIONARY MEMORY

- **Skill & Module Budgets (`<= 600` lines):** Keep `SKILL.md <= 500` lines (`description <= 420` chars), L3 `references/*.md <= 150` lines, Python/HTML/JS/CSS files `<= 600` lines (`<= 60` lines/function), vendor `scripts/_ss_core.py` via `sync_shredded_shape.py`, and enforce `DOMPurify.sanitize()` on dynamic HTML.
- **`[SSOT-UI-03]` Bounded Actor-Critic Isolation (`<= 5` rules/node):** Keep `ui-analyst`, `ui-planner`, and `ui-judge` strictly read-only (`sandbox`); `ui-planner` compiles the `DESIGN.md` blueprint and `ui-worker` materializes `<project_root>/DESIGN.md` and UI files verified via SHA-256 `Read-After-Write`.
