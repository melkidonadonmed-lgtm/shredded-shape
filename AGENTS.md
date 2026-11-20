# AGENTS.md — Repository Delta & Actor-Critic Topology (`shredded-shape` v1.6.0 / Triad v2.1)

> **Global & Optical Inheritance:** Universal Golden Rules (1–8) and the Self-Refine Closing Block inherit from `quality-efficiency-guidelines.md` (`always_on`); 9-Axis `OKLCH 60-30-10` and 3-layer optical physics load via [`rules/frontend-9-axes-guidelines.md`](file:///C:/Users/melki/dev/repos/shredded-shape/rules/frontend-9-axes-guidelines.md) (`trigger: glob`).

## 0. PROJECT CONTEXT & COMMANDS

- **Project:** `shredded-shape` (**UI/UX Architecture, Forensic DevTools/REA Analyst, Brand & Style Planner, Clean Optical Worker, and WCAG 2.2 OKLCH Actor-Critic Judge Suite**).
- **Active Stack:** Python 3.12+ (`uv` / `pyproject.toml`, `pydantic`, `pyyaml`, `pytest`) + Chrome DevTools Live Probe JS + Modern CSS (`OKLCH`, `light-dark()`, `@container`, `subgrid`, Tailwind v4 `@theme`) + Windows 11 (`pwsh`).
- **Executable Commands (`Command-First`):**
  - **Deterministic Skill & Plugin Validator (`7/7` skills, `4/4` subagents):** `uv run python scripts/validate_shredded_shape.py --strict`
  - **Unit, Optical Math & Adversarial Test Suite:** `uv run pytest -q`
  - **Plugin & Ecosystem Sync (`~/.gemini/config/plugins/shredded-shape/`):** `uv run python scripts/sync_shredded_shape.py`
- **State Triad:** [`.context/context.md`](file:///C:/Users/melki/dev/repos/shredded-shape/.context/context.md) | [`.context/spec.md`](file:///C:/Users/melki/dev/repos/shredded-shape/.context/spec.md)

## 1. 4-STAGE ACTOR-CRITIC SUBAGENTS (`agents/*.md`) & 7 SKILLS (`skills/*`)

| Stage / Role | Subagent (`agents/*.md`) | Core Skill (`skills/*`) | Mode & Max Rules |
| :--- | :--- | :--- | :--- |
| **Stage 0 — Forensic Analyst** | [`ui-analyst`](file:///C:/Users/melki/dev/repos/shredded-shape/agents/ui-analyst.md) | [`ui-frontend-analyst`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/ui-frontend-analyst/SKILL.md), [`complex-zero`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/complex-zero/SKILL.md), `chrome-devtools`, `a11y-debugging`, `debug-optimize-lcp`, `memory-leak-debugging`, `modern-web-guidance` | Read-Only CoT (`sandbox`, `<= 5` rules) |
| **Stage 1 — Brand & DAG Planner** | [`ui-planner`](file:///C:/Users/melki/dev/repos/shredded-shape/agents/ui-planner.md) | [`ui-brand-ux-planner`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/ui-brand-ux-planner/SKILL.md), [`clinical-minimalist-ui`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/clinical-minimalist-ui/SKILL.md), `complex-zero`, `modern-web-guidance` | Read-Only ToT (`sandbox`, `<= 5` rules) |
| **Stage 2 — Clean Optical Worker** | [`ui-worker`](file:///C:/Users/melki/dev/repos/shredded-shape/agents/ui-worker.md) | [`ui-clean-worker`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/ui-clean-worker/SKILL.md), `clinical-minimalist-ui`, `complex-zero`, `modern-web-guidance` | ReAct + RAW SHA-256 (`auto`, `<= 5` rules) |
| **Stage 3 — WCAG 2.2 Judge** | [`ui-judge`](file:///C:/Users/melki/dev/repos/shredded-shape/agents/ui-judge.md) | [`ui-quality-judge`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/ui-quality-judge/SKILL.md), `clinical-minimalist-ui`, `complex-zero`, `a11y-debugging` | Read-Only Self-Refine Gatekeeper (`sandbox`, `<= 5` rules) |
| **Decoupled Bridge (`Stitch`)** | Standalone Skill | [`stitch-canvas`](file:///C:/Users/melki/dev/repos/shredded-shape/skills/stitch-canvas/SKILL.md) (`@google/stitch@0.13.0` CLI + 18-tool `stitch` MCP + `stitch_asset_bridge.py`) | Zero-Trust Bridge (`OKLCH` handoff) |

## 2. REPOSITORY INVARIANTS & EVOLUTIONARY MEMORY

- **Skill & Module Budgets (`<= 600` lines):** Keep `SKILL.md <= 1,000` body tokens (`<= 500` lines, `description <= 420` chars, top-level `allowed-tools`, flat scalar `metadata:`), L3 `references/*.md <= 150` lines, Python/HTML/JS/CSS files `<= 600` lines (`<= 60` lines/function), vendor `scripts/_ss_*.py` (`_ss_core.py`, `_ss_guards.py`, `_ss_craft_guards.py`) via `sync_shredded_shape.py`, and enforce `DOMPurify.sanitize()` + zero client secrets/omission placeholders.
- **`[SSOT-UI-03]` Bounded Actor-Critic Isolation (`<= 5` rules/node) & 3-Axis Gatekeeping:** Keep `ui-analyst`, `ui-planner`, and `ui-judge` strictly read-only (`sandbox`); support unrolled `refactor`/`greenfield`/`planner_directed` (`max_discovery_hops: 1`) DAG modes, run Double-Pass 3-Axis judging (`ui_judge_gatekeeper.py --axis` + `artifact_axis_judge.py`), and require SHA-256 `Read-After-Write` from `ui-worker` with fail-closed `--run-tsc`.
- **Scoped Static Guards & Inflected Regex Stems:** Scope compound AST/regex checks to their real container (e.g., `</filter>` for `feGaussianBlur` + `feColorMatrix`, `<nav>` for redundant `aria-label`, per-occurrence FOUC checks, comment-only omissions), append `\w*` to partial stems inside `\b(?:...)\b` (e.g., `typograph\w*`, `accept\w*`) so inflected Markdown headings match, and keep advisory heuristics (`audit_advisory_nav_and_root`) decoupled from blocking `ai_slop_score` / `JudgeFinding` so clean bundles (`assets/*`) keep zero false positives.
- **Modular Core Budget & Guard-Safe Authoring:** Keep `scripts/_ss_core.py` under 600 lines by placing new static guard families in sibling `scripts/_ss_*.py` (auto-vendored via `sync_shredded_shape.py`), avoid raw script-tag or dynamic-eval literals in `edit_file`/`write_file` payloads (use tag-name regexes in scanners, string concatenation in adversarial tests, and exclude script-tag lines from edit targets), and run `uv run ruff check scripts tests skills` alongside `validate_shredded_shape.py --strict` and `pytest -v`.
