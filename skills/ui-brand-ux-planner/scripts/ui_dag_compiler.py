#!/usr/bin/env python3
"""Closed-schema UI Execution DAG compiler with Complexity Wall shield (<= 5 rules/node)."""

from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path
from typing import Dict, List, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

StyleArchetype = Literal["soft", "hi-tech", "tactile", "elevated", "retro", "vintage", "clinical"]

STYLE_PRESETS: Dict[str, Dict[str, str]] = {
    "soft": {"radius": "1.35rem", "chroma_cap": "0.12", "menu": "rounded_pill_sidebar", "font": "Plus Jakarta Sans"},
    "hi-tech": {"radius": "0.35rem", "chroma_cap": "0.14", "menu": "precision_rail_2px", "font": "Geist"},
    "tactile": {"radius": "0.95rem", "chroma_cap": "0.16", "menu": "tactile_48px_rail", "font": "Inter"},
    "elevated": {"radius": "1.10rem", "chroma_cap": "0.15", "menu": "frosted_sticky_header", "font": "Inter"},
    "retro": {"radius": "0.25rem", "chroma_cap": "0.17", "menu": "geometric_block_tabs", "font": "Space Grotesk"},
    "vintage": {"radius": "0.50rem", "chroma_cap": "0.11", "menu": "editorial_toc_65ch", "font": "Instrument Serif"},
    "clinical": {"radius": "0.50rem", "chroma_cap": "0.12", "menu": "ehr_3click_sidebar", "font": "IBM Plex Sans"},
}


class DAGTaskNode(BaseModel):
    """Single bounded task node inside UIExecutionDAG."""

    model_config = ConfigDict(extra="forbid")
    step_id: str = Field(min_length=3)
    title: str = Field(min_length=3)
    owner_agent: Literal["ui-analyst", "ui-planner", "ui-worker", "ui-judge"]
    reasoning_pattern: Literal["CoT", "ToT", "ReAct", "Self-Refine"]
    active_rules_count: int = Field(ge=1, le=5)
    owned_files: List[str] = Field(min_length=1)
    dependencies: List[str] = Field(default_factory=list)
    acceptance_gate: str = Field(min_length=5)
    fallback_branch: str = Field(min_length=3)


class UIExecutionDAG(BaseModel):
    """Strict UI planning output preventing Complexity Wall and parallel file collisions."""

    model_config = ConfigDict(extra="forbid")
    project_name: str = Field(min_length=2)
    style_archetype: StyleArchetype
    complexity_tier: Literal["tier_1_static", "tier_2_spa", "tier_3_fullstack_pwa"]
    brand_oklch_hue: int = Field(ge=0, le=360)
    recommended_stack: List[str] = Field(min_length=1)
    style_tokens: Dict[str, str]
    nodes: List[DAGTaskNode] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_acyclic_and_disjoint_files(self) -> "UIExecutionDAG":
        node_map = {n.step_id: n for n in self.nodes}
        if len(node_map) != len(self.nodes):
            raise ValueError("Duplicate step_id detected in UIExecutionDAG")
        indegree = {n.step_id: 0 for n in self.nodes}
        adj: Dict[str, List[str]] = {n.step_id: [] for n in self.nodes}
        for node in self.nodes:
            for dep in node.dependencies:
                if dep not in node_map:
                    raise ValueError(f"Unknown dependency '{dep}' in node '{node.step_id}'")
                adj[dep].append(node.step_id)
                indegree[node.step_id] += 1
        waves: Dict[str, int] = {k: 0 for k in node_map}
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


def _assert_no_same_wave_file_collision(nodes: List[DAGTaskNode], waves: Dict[str, int]) -> None:
    seen_per_wave: Dict[int, Dict[str, str]] = {}
    for node in nodes:
        if node.owner_agent != "ui-worker":
            continue
        wave = waves[node.step_id]
        bucket = seen_per_wave.setdefault(wave, {})
        for fp in node.owned_files:
            norm = fp.replace("\\", "/").lower()
            if norm in bucket:
                raise ValueError(f"File write collision on wave {wave} for '{fp}' ({bucket[norm]} vs {node.step_id})")
            bucket[norm] = node.step_id


def compile_default_dag(scope_target: Path, style: StyleArchetype = "tactile", hue: int = 235) -> UIExecutionDAG:
    """Compile a canonical 4-stage Actor-Critic UIExecutionDAG for a project scope."""
    has_pkg = (scope_target / "package.json").is_file() if scope_target.is_dir() else False
    tier: Literal["tier_1_static", "tier_2_spa", "tier_3_fullstack_pwa"] = "tier_2_spa" if has_pkg else "tier_1_static"
    stack = ["React 19", "TypeScript", "Tailwind v4 @theme", "OKLCH"] if has_pkg else ["HTML5", "CSS @layer OKLCH", "Vanilla ES"]
    nodes = [
        DAGTaskNode(
            step_id="step_01_tokens_design_contract", title="Author 3-Layer OKLCH Tokens and DESIGN.md",
            owner_agent="ui-planner", reasoning_pattern="CoT", active_rules_count=4,
            owned_files=["DESIGN.md"], dependencies=[], acceptance_gate="OKLCH 60-30-10 + light-dark + style archetype locked",
            fallback_branch="fallback_standard_neutral_tokens",
        ),
        DAGTaskNode(
            step_id="step_02_shell_and_route_impl", title="Implement Optical Shell, Matte Header and Vertical Route",
            owner_agent="ui-worker", reasoning_pattern="ReAct", active_rules_count=5,
            owned_files=["src/styles/tokens.css", "src/components/AppShell.tsx"], dependencies=["step_01_tokens_design_contract"],
            acceptance_gate="RAW SHA-256 + tsc --noEmit pass + dark rim light + 3-layer light shadows",
            fallback_branch="fallback_single_column_shell",
        ),
        DAGTaskNode(
            step_id="step_03_wcag_actor_critic_judge", title="Run Read-Only WCAG 2.2 OKLCH and Anti-Slop Judge",
            owner_agent="ui-judge", reasoning_pattern="Self-Refine", active_rules_count=4,
            owned_files=["src/components/AppShell.tsx"], dependencies=["step_02_shell_and_route_impl"],
            acceptance_gate="verdict == PASSED, contrast >= 4.5:1, zero emojis, DOM == Tab order",
            fallback_branch="trigger_worker_self_refine",
        ),
    ]
    return UIExecutionDAG(
        project_name=scope_target.name or "ui-project", style_archetype=style, complexity_tier=tier,
        brand_oklch_hue=hue, recommended_stack=stack, style_tokens=STYLE_PRESETS[style], nodes=nodes,
    )


def _run_self_test() -> int:
    dag = compile_default_dag(Path("."), style="hi-tech", hue=230)
    assert dag.style_archetype == "hi-tech" and all(n.active_rules_count <= 5 for n in dag.nodes)
    print(json.dumps({"self_test": "UI_DAG_COMPILER_OK", "nodes": len(dag.nodes)}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile and validate bounded UIExecutionDAG JSON")
    parser.add_argument("--scope", default=".")
    parser.add_argument("--style", default="tactile", choices=sorted(STYLE_PRESETS.keys()))
    parser.add_argument("--hue", type=int, default=235)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    dag = compile_default_dag(Path(args.scope).resolve(), style=args.style, hue=args.hue)
    print(dag.model_dump_json(indent=2) if args.json else f"[PASS] compiled {len(dag.nodes)} DAG nodes ({dag.style_archetype})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
