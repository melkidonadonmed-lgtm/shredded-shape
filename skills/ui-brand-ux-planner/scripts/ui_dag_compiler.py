#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.7.0"]
# ///
"""Closed-schema UI Execution DAG compiler with Complexity Wall shield (<= 5 rules/node)."""

from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path
from typing import Literal, get_args

from pydantic import BaseModel, ConfigDict, Field, model_validator

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_HERE = Path(__file__).resolve().parent
for _cand in (*(p / "scripts" for p in _HERE.parents if (p / "pyproject.toml").is_file()), _HERE, *(p / "scripts" for p in _HERE.parents)):
    if (_cand / "_ss_core.py").is_file() and str(_cand) not in sys.path:
        sys.path.insert(0, str(_cand))
        break

import _ss_core

StyleArchetype = Literal["soft", "hi-tech", "tactile", "elevated", "retro", "vintage", "clinical"]
SpatialArchetype = Literal[
    "workbench_split_view", "bento_12_col", "command_center_grid",
    "editorial_65ch", "spatial_hud_dock", "vector_a4_print",
]
ExecutionMode = Literal["greenfield", "refactor"]
READ_ONLY_OWNERS = frozenset({"ui-analyst", "ui-planner", "ui-judge"})
STYLE_PRESETS = _ss_core.STYLE_PRESETS


class DAGTaskNode(BaseModel):
    """Single bounded task node inside UIExecutionDAG."""

    model_config = ConfigDict(extra="forbid")
    step_id: str = Field(min_length=3)
    title: str = Field(min_length=3)
    owner_agent: Literal["ui-analyst", "ui-planner", "ui-worker", "ui-judge"]
    reasoning_pattern: Literal["CoT", "ToT", "ReAct", "Self-Refine"]
    active_rules_count: int = Field(ge=1, le=5)
    read_targets: list[str] = Field(default_factory=list)
    owned_files: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    acceptance_gate: str = Field(min_length=5)
    fallback_branch: str = Field(min_length=3)

    @model_validator(mode="after")
    def _enforce_least_privilege_ownership(self) -> DAGTaskNode:
        if self.owner_agent in READ_ONLY_OWNERS:
            if self.owned_files:
                raise ValueError(f"Read-only agent '{self.owner_agent}' cannot own write files; use read_targets")
            if not self.read_targets:
                raise ValueError(f"Read-only agent '{self.owner_agent}' must declare >= 1 read_targets")
        elif not self.owned_files:
            raise ValueError("ui-worker node must declare >= 1 owned_files")
        return self


class UIExecutionDAG(BaseModel):
    """Strict UI planning output preventing Complexity Wall and parallel file collisions."""

    model_config = ConfigDict(extra="forbid")
    project_name: str = Field(min_length=2)
    style_archetype: StyleArchetype
    spatial_archetype: SpatialArchetype = "workbench_split_view"
    execution_mode: ExecutionMode = "refactor"
    complexity_tier: Literal["tier_1_static", "tier_2_spa", "tier_3_fullstack_pwa"]
    brand_oklch_hue: int = Field(ge=0, le=360)
    max_self_refine_rounds: int = Field(default=3, ge=1, le=3)
    recommended_stack: list[str] = Field(min_length=1)
    style_tokens: dict[str, str]
    nodes: list[DAGTaskNode] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_acyclic_and_disjoint_files(self) -> UIExecutionDAG:
        node_map = {n.step_id: n for n in self.nodes}
        if len(node_map) != len(self.nodes):
            raise ValueError("Duplicate step_id detected in UIExecutionDAG")
        indegree = {n.step_id: 0 for n in self.nodes}
        adj: dict[str, list[str]] = {n.step_id: [] for n in self.nodes}
        for node in self.nodes:
            for dep in node.dependencies:
                if dep not in node_map:
                    raise ValueError(f"Unknown dependency '{dep}' in node '{node.step_id}'")
                adj[dep].append(node.step_id)
                indegree[node.step_id] += 1
        waves: dict[str, int] = {k: 0 for k in node_map}
        queue = deque(k for k, d in indegree.items() if d == 0)
        visited = 0
        while queue:
            cur = queue.popleft()
            visited += 1
            for nxt in adj[cur]:
                waves[nxt] = max(waves[nxt], waves[cur] + 1)
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        if visited != len(self.nodes):
            raise ValueError("Cycle detected in UIExecutionDAG dependencies")
        _assert_no_same_wave_file_collision(self.nodes, waves)
        return self


def _assert_no_same_wave_file_collision(nodes: list[DAGTaskNode], waves: dict[str, int]) -> None:
    seen_per_wave: dict[int, dict[str, str]] = {}
    for node in nodes:
        if node.owner_agent != "ui-worker":
            continue
        bucket = seen_per_wave.setdefault(waves[node.step_id], {})
        for fp in node.owned_files:
            norm = fp.replace("\\", "/").lower()
            if norm in bucket:
                raise ValueError(f"File write collision on wave {waves[node.step_id]} for '{fp}' ({bucket[norm]} vs {node.step_id})")
            bucket[norm] = node.step_id


def _detect_mode_and_tier(
    scope_target: Path, mode: Literal["auto", "greenfield", "refactor"]
) -> tuple[ExecutionMode, Literal["tier_1_static", "tier_2_spa", "tier_3_fullstack_pwa"]]:
    is_dir = scope_target.is_dir()
    has_pkg = is_dir and (scope_target / "package.json").is_file()
    has_next = is_dir and any((scope_target / f"next.config.{ext}").is_file() for ext in ("js", "mjs", "ts"))
    tier: Literal["tier_1_static", "tier_2_spa", "tier_3_fullstack_pwa"] = (
        "tier_3_fullstack_pwa" if has_next else ("tier_2_spa" if has_pkg else "tier_1_static")
    )
    if mode != "auto":
        return mode, tier
    if scope_target.is_file() and scope_target.suffix.lower() in _ss_core.UI_EXTS:
        return "refactor", tier
    if is_dir and (has_pkg or (scope_target / "index.html").is_file() or any(
        (scope_target / sub).is_dir() and _ss_core.collect_ui_files(scope_target / sub, limit=1)
        for sub in ("src", "app", "pages", "components", "assets")
    )):
        return "refactor", tier
    return "greenfield", tier


def compile_default_dag(
    scope_target: Path,
    style: str = "tactile",
    hue: int = 235,
    mode: Literal["auto", "greenfield", "refactor"] = "auto",
    spatial: SpatialArchetype | None = None,
) -> UIExecutionDAG:
    """Compile a canonical 3-stage (greenfield) or 4-stage (refactor) UIExecutionDAG."""
    canon_style: StyleArchetype = _ss_core.normalize_style_archetype(style)  # type: ignore[assignment]
    resolved_mode, tier = _detect_mode_and_tier(scope_target, mode)
    resolved_spatial: SpatialArchetype = spatial or _ss_core.STYLE_SPATIAL_DEFAULTS[canon_style]  # type: ignore[assignment]
    stack_map = {
        "tier_3_fullstack_pwa": ["Next.js 15+ App Router", "React 19", "TypeScript", "Tailwind v4 @theme", "OKLCH"],
        "tier_2_spa": ["React 19", "TypeScript", "Tailwind v4 @theme", "OKLCH"],
        "tier_1_static": ["HTML5", "CSS @layer OKLCH", "Vanilla ES"],
    }
    worker_files_map = {
        "tier_3_fullstack_pwa": ["DESIGN.md", "src/app/globals.css", "src/app/layout.tsx", "src/app/page.tsx"],
        "tier_2_spa": ["DESIGN.md", "src/styles/tokens.css", "src/components/AppShell.tsx"],
        "tier_1_static": ["DESIGN.md", "index.html", "styles/tokens.css"],
    }
    worker_files = worker_files_map[tier]
    nodes: list[DAGTaskNode] = []
    if resolved_mode == "refactor":
        nodes.append(DAGTaskNode(
            step_id="step_00_forensic_inventory", title="Run Forensic Token, DevTools/REA and Anti-Slop Inventory",
            owner_agent="ui-analyst", reasoning_pattern="CoT", active_rules_count=4,
            read_targets=[str(scope_target.name or ".")], owned_files=[], dependencies=[],
            acceptance_gate="ai_slop_score computed + 7-section CLAREZA plan + As-Is/To-Be Mermaid",
            fallback_branch="fallback_static_ast_inventory",
        ))
    nodes.extend([
        DAGTaskNode(
            step_id="step_01_tokens_design_contract", title="Emit 5-Plane OKLCH Tokens, Spatial Archetype and 8-Section DESIGN.md Blueprint",
            owner_agent="ui-planner", reasoning_pattern="ToT", active_rules_count=4,
            read_targets=["README.md", str(scope_target.name or ".")], owned_files=[],
            dependencies=["step_00_forensic_inventory"] if resolved_mode == "refactor" else [],
            acceptance_gate="OKLCH 60-30-10 C<=0.20 + light-dark + style & spatial archetype locked",
            fallback_branch="fallback_standard_neutral_tokens",
        ),
        DAGTaskNode(
            step_id="step_02_shell_and_route_impl", title="Materialize DESIGN.md and Implement Optical Shell, Matte Header and Route",
            owner_agent="ui-worker", reasoning_pattern="ReAct", active_rules_count=5,
            read_targets=["DESIGN.md"], owned_files=worker_files, dependencies=["step_01_tokens_design_contract"],
            acceptance_gate="RAW SHA-256 + tsc/syntax pass + dark rim light + 3-layer light shadows",
            fallback_branch="fallback_single_column_shell",
        ),
        DAGTaskNode(
            step_id="step_03_wcag_actor_critic_judge", title="Run Read-Only WCAG 2.2 OKLCH, 4-Pillar and 6-Dimension Judge",
            owner_agent="ui-judge", reasoning_pattern="Self-Refine", active_rules_count=4,
            read_targets=worker_files, owned_files=[], dependencies=["step_02_shell_and_route_impl"],
            acceptance_gate="verdict == PASSED, contrast >= 4.5:1, zero blobs/neon/bad-SVGs, DOM == Tab order",
            fallback_branch="trigger_worker_self_refine_max_3",
        ),
    ])
    return UIExecutionDAG(
        project_name=scope_target.name or "ui-project", style_archetype=canon_style,
        spatial_archetype=resolved_spatial, execution_mode=resolved_mode, complexity_tier=tier,
        brand_oklch_hue=hue, recommended_stack=stack_map[tier], style_tokens=STYLE_PRESETS[canon_style], nodes=nodes,
    )


def _run_self_test() -> int:
    dag_ref = compile_default_dag(Path("."), style="hi-tech", hue=230, mode="refactor")
    assert dag_ref.style_archetype == "hi-tech" and len(dag_ref.nodes) == 4 and all(n.active_rules_count <= 5 for n in dag_ref.nodes)
    dag_gf = compile_default_dag(Path("nonexistent_greenfield_dir"), style="tactile", hue=235, mode="greenfield")
    assert dag_gf.execution_mode == "greenfield" and len(dag_gf.nodes) == 3
    print(json.dumps({"self_test": "UI_DAG_COMPILER_OK", "refactor_nodes": len(dag_ref.nodes), "greenfield_nodes": len(dag_gf.nodes)}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile and validate bounded UIExecutionDAG JSON")
    parser.add_argument("target", nargs="?", default=None, help="Target frontend file or workspace")
    parser.add_argument("--target", dest="target_flag", default=None, help="Explicit --target workspace")
    parser.add_argument("--scope", dest="scope_flag", default=None, help="Alias --scope workspace")
    parser.add_argument("--style", default="tactile", choices=sorted([*STYLE_PRESETS.keys(), *_ss_core.STYLE_ALIASES.keys()]))
    parser.add_argument("--hue", type=int, default=235)
    parser.add_argument("--mode", default="auto", choices=["auto", "greenfield", "refactor"])
    parser.add_argument("--spatial", default=None, choices=list(get_args(SpatialArchetype)))
    parser.add_argument("--out", type=str, default="", help="Optional output file path for compiled DAG JSON")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    scope_target = _ss_core.resolve_cli_target(args.target, args.target_flag or args.scope_flag)
    dag = compile_default_dag(scope_target, style=args.style, hue=args.hue, mode=args.mode, spatial=args.spatial)
    payload = dag.model_dump_json(indent=2)
    if args.out.strip():
        out_path = Path(args.out).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload + "\n", encoding="utf-8", newline="\n")
    print(payload if args.json else f"[PASS] compiled {len(dag.nodes)} DAG nodes ({dag.style_archetype}/{dag.execution_mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
