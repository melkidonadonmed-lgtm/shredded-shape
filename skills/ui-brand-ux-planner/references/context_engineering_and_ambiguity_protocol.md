# Context Engineering, Unrolled Modes & Ambiguity Triage Protocol

Single Source of Truth for Stage 1 (`ui-brand-ux-planner`) order-dependent planning, prompt/spec scaffolding, risk-based ambiguity resolution, and Phase 0 Scope Lock.

## 1. Bidirectional Unrolled Execution Modes (`ui-analyst <-> ui-planner`)
To keep `UIExecutionDAG` strictly acyclic while supporting any request order:
- **`refactor` (Audit-First):** `ui-analyst` emits full 7-Section CLAREZA (`step_00`) -> `ui-planner` emits `DESIGN.md` + DAG (`step_01`).
- **`greenfield` (Pure Creation):** `ui-planner` diagnoses brand/intent directly (`step_01`) -> `ui-worker` -> `ui-judge`.
- **`planner_directed` (Intent-First Discovery, `max_discovery_hops: 1`):** `ui-planner` diagnoses goal/unknowns and issues a typed `ScopedAuditRequest` (`FORENSIC_BRIEF_HANDOFF` via `send_message`) -> `ui-analyst` executes bounded `step_00b_directed_forensic_probe` returning `CLAREZA_DELTA` -> `ui-planner` compiles final `DESIGN.md` + DAG (`step_01`). Never loop a 2nd discovery hop automatically.

## 2. 4 Execution Routing Intents vs. 4 UI Interface Archetypes
Keep workflow routing separate from visual spatial selection:
- **4 Execution Routing Intents:** `Greenfield Creation` (`greenfield`), `Forensic Refactor` (`refactor`), `Targeted Polish/Fix` (`planner_directed` scoped brief), `Audit-Only Review` (read-only `ui-analyst` + `ui-judge`, zero writes).
- **4 UI Interface Intent Archetypes:** `Operational / Dashboard` -> `workbench_split_view` / `command_center_grid`; `Infinite Canvas / Graph` -> `spatial_hud_dock` (`@xyflow/react` + Dagre); `Editorial / Documentation` -> `editorial_65ch`; `Transactional / Mobile` -> single-column bottom-anchored `Compact` posture.

## 3. High-Fidelity Context Engineering & OWASP LLM01 Scaffolding
- **4-Layer Prompt/Spec Stack:** (1) Structural (`CLAREZA` / Role + Format) + (2) Cognitive (`ToT` branch comparison + `ReAct` verification) + (3) Guardrail Layer (explicit Negative Constraints: zero `#000000`, zero stubs, zero secret leaks) + (4) Silent `Self-Refine` acceptance check.
- **XML Hard Scaffolding (OWASP LLM01:2025):** Isolate authoritative rules (`<system_instructions>`) and verified repo artifacts (`<context>`) from external inputs (`<untrusted_user_input>`), preventing indirect prompt injection from READMEs or user text.
- **Epistemic Grounding Labels:** Tag every non-obvious claim `[OBSERVED FACT]` (disk/probe verified), `[TECHNICAL INFERENCE]` (derived logically), or `[GAP]` (missing parameter; never invent undocumented metrics).

## 4. Risk-Based Ambiguity Triage & Phase 0 Scope Lock
| Ambiguity Class | Domain Examples | Action Rule |
| :--- | :--- | :--- |
| **Low-Risk Cosmetic / Structural** | Missing radius preference, neutral hue choice, card grid column count | **Do NOT stall:** select highest-craft standard default (`OKLCH 60-30-10`, `4px/8px` scale) and explicitly state adopted assumptions. |
| **High-Risk Critical / Irreversible** | Clinical calculator formulas/bounds, auth/RBAC rules, destructive deletes, secret/env boundaries, billing side effects | **Pause (HITL Gate):** ask **1–3 surgical questions** resolving the exact gap before compiling worker mutations. |

- **3 Delivery Modes:** `Direct Execution` (low-risk, pre-authorized), `Blueprint / Prompt Spec` (single clean Markdown `DESIGN.md` + DAG JSON), `Phased Plan` (ordered phases + **Phase 0 Scope Lock** requiring confirmation before destructive refactors and defining exact `stop_condition`).

## 5. Plan Mode Read-Only Tool Allowlist & Minimum Pre-Execution Checklist

Keep `ui-brand-ux-planner` strictly read-only until the blueprint/DAG is approved; select the allowlist by UI request type:

| UI Request Type | Allowed Read-Only Tools (Plan Mode Allowlist) | Blocked Until Worker Stage |
| :--- | :--- | :--- |
| **`greenfield` (New UI / Landing / SaaS)** | `read_file`, `modern-web-guidance`, `stitch`/`figma` read-only, `ask_question` (`<= 3`) | `write_file`, `edit_file`, `DESIGN.md` writes, `npm/vite` builds |
| **`refactor` / `planner_directed` (Existing App)** | `read_file`, `rg`, `git status`/`diff`, `chrome-devtools` snapshot/screenshot, `frontend_inventory_and_slop_scanner.py`, `ui_dag_compiler.py --json` | Any CSS/TSX/HTML mutation, package installs, destructive deletes |
| **`audit_only` (Review / Scorecard)** | Read-only DevTools + AST + `ui_judge_gatekeeper.py` / `artifact_axis_judge.py` | All write tools (zero mutations) |

### Minimum 6-Item Pre-Execution Checklist (Mandatory Before Hand-Off to `ui-worker`)
- [ ] **1. Read-Only Isolation:** Zero source files or `DESIGN.md` were mutated during planning.
- [ ] **2. Direction Brief & Non-Goals:** 5-line Direction (`Product / Character / World / Moments / Signature`), 1 Style + 1 Spatial Archetype, and explicit **Non-Goals** (e.g., preserve A4 `#FFFFFF` print sheet or clinical logic).
- [ ] **3. Verified Target Files & Routes:** Existing routes, tokens, and target `owned_files` were inspected on disk (or explicitly marked `greenfield`).
- [ ] **4. Tool Allowlist Declared:** Required implementation/verification tools (`modern-web-guidance`, `verify_raw_frontend.py --run-tsc`, `ui_judge_gatekeeper.py`, `stitch-canvas` if needed) are listed per stage.
- [ ] **5. Complexity Cap (`<= 5` rules/node):** Disjoint `owned_files` per worker, `max_discovery_hops <= 1`, and `max_self_refine_rounds <= 3`.
- [ ] **6. Measurable Acceptance & HITL Gate:** Target WCAG 2.2 AA/AAA, `ai_slop_score == 0`, SHA-256 RAW verification, and HITL pause for clinical/auth/destructive changes.
