#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.7.0"]
# ///
"""Deterministic Axis-2 (Execution Plans) and Axis-3 (Technical Audits) Judge for v1.6.0."""

from __future__ import annotations

import json
import re
import sys
from collections import deque
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_HERE = Path(__file__).resolve().parent
for _cand in (*(p / "scripts" for p in _HERE.parents if (p / "pyproject.toml").is_file()), _HERE, *(p / "scripts" for p in _HERE.parents)):
    if (_cand / "_ss_core.py").is_file() and str(_cand) not in sys.path:
        sys.path.insert(0, str(_cand))
        break

import _ss_core

_DESIGN_BUCKETS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("1_brand_archetype", re.compile(r"\b(?:brand\w*|archetype\w*|polarit\w*|dial\w*)\b", re.IGNORECASE)),
    ("2_oklch_5plane", re.compile(r"\b(?:oklch|60-30-10|5-plane|palette\w*)\b", re.IGNORECASE)),
    ("3_depth_shadows", re.compile(r"\b(?:shadow\w*|depth|elevation\w*|frosted|radi(?:us|i))\b", re.IGNORECASE)),
    ("4_typography", re.compile(r"\b(?:typograph\w*|font\w*|clamp|tabular-nums|m3)\b", re.IGNORECASE)),
    ("5_svg_catalog", re.compile(r"\b(?:svg\w*|icon\w*|symbol\w*|lucide|material)\b", re.IGNORECASE)),
    ("6_adaptive_layout", re.compile(r"\b(?:adaptive|layout\w*|container\w*|chrome|posture\w*|grid\w*)\b", re.IGNORECASE)),
    ("7_state_security", re.compile(r"\b(?:state\w*|fsm|securit\w*|dompurify|focus\w*|params)\b", re.IGNORECASE)),
    ("8_acceptance_scope", re.compile(r"\b(?:accept\w*|raw|sha-256|wcag|scope\s*lock|phase\s*0|stop)\b", re.IGNORECASE)),
)
_CLAREZA_BUCKETS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("1_tokens_polarity", re.compile(r"\b(?:token\w*|polarit\w*|oklch|color\w*)\b", re.IGNORECASE)),
    ("2_typography_spacing", re.compile(r"\b(?:typograph\w*|spacing|clamp|font\w*)\b", re.IGNORECASE)),
    ("3_slop_icons", re.compile(r"\b(?:slop|icon\w*|svg\w*|600)\b", re.IGNORECASE)),
    ("4_devtools_telemetry", re.compile(r"\b(?:devtools|cwv|inp|lcp|probe\w*|telemetry)\b", re.IGNORECASE)),
    ("5_nav_friction", re.compile(r"\b(?:navigation|friction|landmark\w*|menu\w*)\b", re.IGNORECASE)),
    ("6_mermaid_flow", re.compile(r"```mermaid[\s\S]*?\b(?:flowchart|graph)\b", re.IGNORECASE)),
    ("7_before_after", re.compile(r"\b(?:before|after|refactor\w*|matrix)\b", re.IGNORECASE)),
)
_CSS_FENCE_RE = re.compile(r"```css\s*\r?\n([\s\S]*?)```", re.IGNORECASE)
_PLACEHOLDER_PLAN_RE = re.compile(r"\b(?:TODO|TBD|FIXME)\b|\.\.\.\s*(?:rest\s+of|existing\s+code|more\s+here)", re.IGNORECASE)
_CITATION_RE = re.compile(r"(?<![:/\w])([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\.(?:tsx|ts|jsx|js|css|html|py|md)):(\d+)\b")
_RO_AGENTS = frozenset({"ui-analyst", "ui-planner", "ui-judge"})


class AxisJudgeReport(BaseModel):
    """Strict output for Axis 2 (execution_plan) and Axis 3 (technical_audit)."""

    model_config = ConfigDict(extra="forbid")
    axis: Literal["execution_plan", "technical_audit"]
    verdict: Literal["PASSED", "REJECTED", "UNVERIFIED"]
    target: str
    checks_passed: int
    findings: list[dict[str, str]] = Field(default_factory=list)
    semantic_double_pass_required: list[str] = Field(default_factory=list)


def _add_finding(
    findings: list[dict[str, str]], rule_id: str, tier: str, loc: str, msg: str, rem: str
) -> None:
    findings.append({"rule_id": rule_id, "tier": tier, "location": loc, "message": msg, "remediation": rem})


def _validate_dag_json(data: Any, target_name: str, findings: list[dict[str, str]]) -> int:
    if not isinstance(data, dict) or not isinstance(data.get("nodes"), list) or not data["nodes"]:
        _add_finding(findings, "PLAN-DAG-SCHEMA", "P0_BLOCKER", target_name, "Execution DAG JSON must define non-empty 'nodes' array.", "Emit valid UIExecutionDAG JSON.")
        return 0
    nodes = data["nodes"]
    by_id: dict[str, dict[str, Any]] = {}
    for n in nodes:
        sid = str(n.get("step_id", ""))
        if not sid or sid in by_id:
            _add_finding(findings, "PLAN-DAG-DUP-ID", "P0_BLOCKER", target_name, f"Duplicate or empty step_id '{sid}'.", "Assign unique step_id per node.")
        by_id[sid] = n
        if int(n.get("active_rules_count", 0)) > 5:
            _add_finding(findings, "PLAN-DAG-RULES", "P0_BLOCKER", sid, "active_rules_count exceeds 5.", "Bound rules <= 5 per node.")
        owner = str(n.get("owner_agent", ""))
        owned = n.get("owned_files", [])
        if owner in _RO_AGENTS and owned:
            _add_finding(findings, "PLAN-DAG-RO-WRITE", "P0_BLOCKER", sid, f"Read-only agent '{owner}' cannot own write files.", "Clear owned_files and use read_targets.")
        if any(".." in Path(str(p)).parts for p in [*owned, *n.get("read_targets", [])]):
            _add_finding(findings, "PLAN-DAG-PATH-ESCAPE", "P0_BLOCKER", sid, "Parent escape '..' detected in node file path.", "Use project-relative paths only.")
    indeg = {sid: 0 for sid in by_id}
    adj: dict[str, list[str]] = {sid: [] for sid in by_id}
    for sid, n in by_id.items():
        for dep in n.get("dependencies", []):
            if dep not in by_id:
                _add_finding(findings, "PLAN-DAG-DEP", "P0_BLOCKER", sid, f"Unknown dependency '{dep}'.", "Reference valid upstream step_id.")
            else:
                adj[dep].append(sid)
                indeg[sid] += 1
    q = deque(k for k, d in indeg.items() if d == 0)
    seen = 0
    waves = {k: 0 for k in by_id}
    while q:
        cur = q.popleft()
        seen += 1
        for nxt in adj[cur]:
            waves[nxt] = max(waves[nxt], waves[cur] + 1)
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    if seen != len(by_id):
        _add_finding(findings, "PLAN-DAG-CYCLE", "P0_BLOCKER", target_name, "Cycle detected in DAG dependencies.", "Unroll cyclic hops into distinct acyclic step_ids.")
    if int(data.get("max_self_refine_rounds", 3)) > 3:
        _add_finding(findings, "PLAN-DAG-BOUND", "P1_HIGH", target_name, "max_self_refine_rounds exceeds 3.", "Cap refinement loop at <= 3.")
    return 4 if not findings else 1


def _validate_design_md(text: str, target_name: str, findings: list[dict[str, str]]) -> int:
    passed = 0
    for name, pat in _DESIGN_BUCKETS:
        if pat.search(text):
            passed += 1
        else:
            _add_finding(findings, "PLAN-DESIGN-SECTION", "P0_BLOCKER", target_name, f"Missing mandatory DESIGN.md section '{name}'.", "Include all 8 required blueprint sections.")
    if m := _PLACEHOLDER_PLAN_RE.search(text):
        _add_finding(findings, "PLAN-PLACEHOLDER", "P0_BLOCKER", target_name, f"Unresolved plan placeholder '{m.group(0)}'.", "Replace TODO/TBD placeholders with concrete specifications.")
    low = text.lower()
    if not any(s in low for s in _ss_core.STYLE_PRESETS):
        _add_finding(findings, "PLAN-STYLE-MISSING", "P1_HIGH", target_name, "No canonical StyleArchetype locked in DESIGN.md.", f"Specify one of {sorted(_ss_core.STYLE_PRESETS)}.")
    min_cr = 7.0 if ("clinical-day" in low or ".sus-grid" in low or "wcag aaa" in low) else 4.5
    for idx, css in enumerate(_CSS_FENCE_RE.findall(text), 1):
        stripped = _ss_core.strip_comments(css)
        if _ss_core.PURE_BLACK_RE.search(stripped):
            _add_finding(findings, "OPTICS-NO-BLACK", "P0_BLOCKER", f"{target_name}:css#{idx}", "Pure #000000 banned in DESIGN.md tokens.", "Use matte OKLCH dark canvas (L >= 0.145).")
        for msg in _ss_core.find_neon_violations(stripped):
            _add_finding(findings, "OPTICS-NO-NEON", "P0_BLOCKER", f"{target_name}:css#{idx}", msg, "Keep OKLCH chroma C <= 0.20 (hard max 0.22).")
        for tname, toks in _ss_core.extract_theme_oklch_maps(stripped).items():
            ink = toks.get("--ink-primary") or toks.get("--text-primary")
            bg = toks.get("--bg-card") or toks.get("--surface-card") or toks.get("--bg-canvas")
            if ink and bg:
                cr = _ss_core.calculate_oklch_contrast(ink[0], bg[0], ink[1], ink[2], bg[1], bg[2])
                if cr < min_cr:
                    _add_finding(findings, "WCAG-1.4.3-OKLCH", "P0_BLOCKER", f"{target_name}:{tname}", f"Contrast {cr}:1 below {min_cr}:1.", "Increase lightness delta.")
    return passed


def evaluate_execution_plan(target: Path) -> AxisJudgeReport:
    """Validate Axis 2 artifacts (UIExecutionDAG .json or 8-section DESIGN.md blueprint)."""
    sem = ["Brand-tone & user-intent fit", "Zero-verbiage UX & 5-question intuitiveness", "Ambiguity triage & Phase 0 Scope Lock"]
    if not target.is_file():
        return AxisJudgeReport(axis="execution_plan", verdict="UNVERIFIED", target=str(target), checks_passed=0, semantic_double_pass_required=sem)
    text = target.read_text(encoding="utf-8", errors="ignore")
    findings: list[dict[str, str]] = []
    if target.suffix.lower() == ".json":
        try:
            checks = _validate_dag_json(json.loads(text), target.name, findings)
        except ValueError as exc:
            _add_finding(findings, "PLAN-JSON-SYNTAX", "P0_BLOCKER", target.name, f"Invalid JSON: {exc}", "Fix JSON syntax.")
            checks = 0
    else:
        checks = _validate_design_md(text, target.name, findings)
    has_blocker = any(f["tier"] in {"P0_BLOCKER", "P1_HIGH"} for f in findings)
    return AxisJudgeReport(axis="execution_plan", verdict="REJECTED" if has_blocker else "PASSED", target=str(target), checks_passed=checks, findings=findings, semantic_double_pass_required=sem)


def _check_citations_on_disk(text: str, workspace: Path, findings: list[dict[str, str]]) -> int:
    ws_root = workspace.resolve()
    checked = 0
    for rel_s, ln_s in _CITATION_RE.findall(text)[:80]:
        if rel_s.startswith(("http", "//")):
            continue
        checked += 1
        cand = (ws_root / rel_s).resolve()
        if not cand.is_relative_to(ws_root) or not cand.is_file():
            _add_finding(findings, "AUDIT-HALLUCINATED-CITATION", "P0_BLOCKER", f"{rel_s}:{ln_s}", f"Cited file '{rel_s}' does not exist under workspace.", "Verify file paths directly before citing.")
            continue
        max_ln = len(cand.read_text(encoding="utf-8", errors="ignore").splitlines())
        if not (1 <= int(ln_s) <= max_ln):
            _add_finding(findings, "AUDIT-HALLUCINATED-CITATION", "P0_BLOCKER", f"{rel_s}:{ln_s}", f"Cited line {ln_s} out of bounds (1..{max_ln}).", "Cite exact observed line numbers.")
    return checked


def evaluate_technical_audit(target: Path, workspace: Path | None = None) -> AxisJudgeReport:
    """Validate Axis 3 artifacts (FrontendInventoryReport .json or 7-section CLAREZA .md)."""
    sem = ["Intent-First alignment (CoT-0)", "Causal Friction X -> Impact Y depth", "Completeness of AppSec & architectural risks"]
    if not target.is_file():
        return AxisJudgeReport(axis="technical_audit", verdict="UNVERIFIED", target=str(target), checks_passed=0, semantic_double_pass_required=sem)
    text = target.read_text(encoding="utf-8", errors="ignore")
    findings: list[dict[str, str]] = []
    checks = 0
    if target.suffix.lower() == ".json":
        try:
            data = json.loads(text)
            req = {"verdict", "target", "files_scanned", "detected_stack", "spacing_and_style_defects", "ai_slop_score"}
            if not isinstance(data, dict) or not req.issubset(data.keys()):
                _add_finding(findings, "AUDIT-JSON-SCHEMA", "P0_BLOCKER", target.name, "Missing required FrontendInventoryReport keys.", "Emit valid FrontendInventoryReport JSON.")
            else:
                checks += 1
                if data.get("verdict") == "[PASS]" and any("SCOPE-TRUNCATED" in str(d) for d in data.get("spacing_and_style_defects", [])):
                    _add_finding(findings, "AUDIT-FAIL-OPEN-PASS", "P0_BLOCKER", target.name, "Report claims [PASS] despite SCOPE-TRUNCATED defect.", "Emit fail-closed [UNVERIFIED] or [FAIL] when truncated.")
                if int(data.get("files_scanned", 0)) > 0 and not data.get("detected_stack"):
                    _add_finding(findings, "AUDIT-EMPTY-STACK", "P1_HIGH", target.name, "detected_stack is empty for scanned files.", "Populate detected_stack.")
        except ValueError as exc:
            _add_finding(findings, "AUDIT-JSON-SYNTAX", "P0_BLOCKER", target.name, f"Invalid JSON: {exc}", "Fix JSON syntax.")
    else:
        for name, pat in _CLAREZA_BUCKETS:
            if pat.search(text):
                checks += 1
            else:
                _add_finding(findings, "AUDIT-CLAREZA-SECTION", "P0_BLOCKER", target.name, f"Missing 7-section CLAREZA component '{name}'.", "Include all 7 sections and Mermaid flow.")
        if m := _PLACEHOLDER_PLAN_RE.search(text):
            _add_finding(findings, "AUDIT-PLACEHOLDER", "P0_BLOCKER", target.name, f"Unresolved placeholder '{m.group(0)}' in audit report.", "Complete every section without omissions.")
        if workspace is not None and workspace.is_dir():
            checks += _check_citations_on_disk(text, workspace, findings)
    has_blocker = any(f["tier"] in {"P0_BLOCKER", "P1_HIGH"} for f in findings)
    return AxisJudgeReport(axis="technical_audit", verdict="REJECTED" if has_blocker else "PASSED", target=str(target), checks_passed=checks, findings=findings, semantic_double_pass_required=sem)


def _run_self_test() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        plan = d / "DESIGN.md"
        plan.write_text("# 1. Brand Soft Archetype\n## 2. OKLCH 5-Plane\n```css\n:root{--bg-card:oklch(0.99 0.002 250);--ink-primary:oklch(0.18 0.02 255);}\n```\n## 3. Depth Shadows\n## 4. Typography\n## 5. SVG\n## 6. Adaptive Layout\n## 7. State FSM Security\n## 8. Acceptance Scope Lock\n", encoding="utf-8")
        assert evaluate_execution_plan(plan).verdict == "PASSED"
        bad_plan = d / "BAD.md"
        bad_plan.write_text("# 1. Brand\n```css\n.x{background:#000000;}\n```\n", encoding="utf-8")
        assert evaluate_execution_plan(bad_plan).verdict == "REJECTED"
        src = d / "App.tsx"
        src.write_text("export const x = 1;\n", encoding="utf-8")
        clareza = d / "clareza.md"
        clareza.write_text("1. Token OKLCH Polarity\n2. Typography Spacing\n3. Slop SVG\n4. DevTools CWV\n5. Navigation Friction\n```mermaid\nflowchart LR\nA-->B\n```\n7. Before After Matrix\nHit at App.tsx:1\n", encoding="utf-8")
        assert evaluate_technical_audit(clareza, workspace=d).verdict == "PASSED"
    print(json.dumps({"self_test": "ARTIFACT_AXIS_JUDGE_OK"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(_run_self_test())
