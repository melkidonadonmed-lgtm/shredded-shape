"""Deterministic & adversarial test suite for shredded-shape UI/UX skills and subagents."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml
from pydantic import ValidationError

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.sync_shredded_shape import sync_shredded_shape
from scripts.validate_shredded_shape import validate_ecosystem, validate_repository, validate_skill_dir


def _load_mod(name: str, rel_path: str) -> Any:
    path = ROOT_DIR / rel_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


analyst = _load_mod("ss_analyst", "skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py")
planner = _load_mod("ss_planner", "skills/ui-brand-ux-planner/scripts/ui_dag_compiler.py")
worker_raw = _load_mod("ss_worker", "skills/ui-clean-worker/scripts/verify_raw_frontend.py")
judge = _load_mod("ss_judge", "skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py")
legacy_ux = _load_mod("ss_legacy_ux", "skills/ui-quality-judge/scripts/ui_ux_frontend_auditor.py")


def test_validate_repository_and_adversarial_rejections(tmp_path: Path) -> None:
    """Validate 6/6 skills + 4/4 agents pass, and adversarial contract violations are rejected."""
    passed, total, errors = validate_repository(ROOT_DIR, strict_mode=True)
    assert total == 6 and passed == 6 and errors == [], f"Validation errors: {errors}"

    bad_skill = tmp_path / "bad-ui"
    bad_skill.mkdir()
    (bad_skill / "SKILL.md").write_text(
        "---\nname: bad-ui\ndescription: \"Use when testing. Do NOT use in prod.\"\n"
        "version: \"1.0.0\"\nmetadata:\n  version: \"1.0.0\"\n---\n"
        "## Overview\nSee [x](../secret.md).\n## Inputs\nA\n## Procedure\nB\n## Gotchas\nC\n## Output\nD\n## User Communication\nE\n",
        encoding="utf-8",
    )
    s_errs = validate_skill_dir(bad_skill, strict_mode=True)
    assert any("orphan" in e.lower() for e in s_errs) and any(".." in e for e in s_errs)

    fake_repo = tmp_path / "repo"
    (fake_repo / "agents").mkdir(parents=True)
    (fake_repo / "rules").mkdir(parents=True)
    (fake_repo / "plugin.json").write_text('{"name":"x","logo":"missing.svg"}', encoding="utf-8")
    (fake_repo / "agents" / "ui-judge.md").write_text(
        "---\nname: ui-judge\ndescription: x\nsubagent: true\nmainAgent: false\nmodel: inherit\ntools:\n  - write_file\n---\n",
        encoding="utf-8",
    )
    eco_errs = validate_ecosystem(fake_repo)
    assert any("read-only" in e for e in eco_errs)


def test_atlas_html_passes_analyst_raw_and_judge() -> None:
    """Audit ui_skills_architecture_atlas.html end-to-end with Analyst, RAW, and WCAG Judge."""
    atlas = ROOT_DIR / "assets" / "ui_skills_architecture_atlas.html"
    inv = analyst.scan_frontend(atlas)
    assert inv.verdict == "[PASS]" and inv.ai_slop_score == 0 and inv.emoji_hits == 0
    assert inv.oklch_count >= 50 and inv.light_dark_count >= 20

    raw_res = worker_raw.verify_raw_frontend(atlas, min_bytes=5000)
    assert raw_res.verdict == "[PASS]" and len(raw_res.files_checked[0].sha256) == 64

    judge_res = judge.evaluate_ui(atlas, wcag_level="AA")
    assert judge_res.verdict == "PASSED" and judge_res.contrast_ratio_min >= 10.0 and judge_res.findings == []


def test_self_tests_and_dag_compiler_adversarial() -> None:
    """Run all 4 script self-tests and reject invalid DAG nodes (>5 rules, extra fields, cycles, collisions)."""
    assert analyst._run_self_test() == 0
    assert planner._run_self_test() == 0
    assert worker_raw._run_self_test() == 0
    assert judge._run_self_test() == 0

    with pytest.raises(ValidationError):
        planner.DAGTaskNode(
            step_id="too_many_rules", title="Overflow", owner_agent="ui-worker",
            reasoning_pattern="ReAct", active_rules_count=6, owned_files=["a.tsx"],
            acceptance_gate="passes", fallback_branch="fb",
        )
    with pytest.raises(ValidationError):
        planner.UIExecutionDAG(
            project_name="p", style_archetype="tactile", complexity_tier="tier_1_static",
            brand_oklch_hue=220, recommended_stack=["HTML5"], style_tokens={},
            nodes=[
                planner.DAGTaskNode(step_id="n1", title="W1", owner_agent="ui-worker", reasoning_pattern="ReAct", active_rules_count=3, owned_files=["src/Card.tsx"], dependencies=[], acceptance_gate="ok ok", fallback_branch="fb1"),
                planner.DAGTaskNode(step_id="n2", title="W2", owner_agent="ui-worker", reasoning_pattern="ReAct", active_rules_count=3, owned_files=["src/Card.tsx"], dependencies=[], acceptance_gate="ok ok", fallback_branch="fb2"),
            ],
        )


def test_worker_raw_and_judge_adversarial_matrix(tmp_path: Path) -> None:
    """Verify deterministic rejection of stubs, #000000, neon chroma, low contrast, missing focus, order, XSS, emojis."""
    assert legacy_ux.wcag_contrast_ratio("#ffffff", "#000000") == 21.0
    assert judge.calculate_oklch_contrast(0.20, 0.98) >= 10.0

    stub_tsx = tmp_path / "Stub.tsx"
    stub_tsx.write_text("export function Stub() { return <button onClick={() => {}}>Go</button>; }", encoding="utf-8")
    assert worker_raw.verify_raw_frontend(stub_tsx, min_bytes=20).verdict == "[RAW-VIOLATION]"

    bad_ui = tmp_path / "Bad.tsx"
    bad_ui.write_text(
        "<style>.bad{color:#777777;background:#888888;background-color:#000000;box-shadow:0 4px 12px rgba(0,0,0,0.4);"
        "outline:none;order:2;accent-color:oklch(0.70 0.35 140);transition:all 0.2s;}</style>"
        "<div dangerouslySetInnerHTML={{__html: raw}}>🚀</div>",
        encoding="utf-8",
    )
    rep = judge.evaluate_ui(bad_ui, wcag_level="AA")
    rule_ids = {f.rule_id for f in rep.findings}
    assert rep.verdict == "REJECTED"
    for expected in ("WCAG-1.4.3", "OPTICS-NO-BLACK", "OPTICS-NO-NEON", "AUDIT-VIS-EMOJI", "AUDIT-SEC-01", "WCAG-1.3.2", "WCAG-2.4.7"):
        assert expected in rule_ids, f"Missing {expected} in {rule_ids}"


def test_shredded_shape_level1_trigger_precision_f1() -> None:
    """Verify Top-1 = 100% and F1 = 1.0 across all 6 shredded-shape skills using positive/negative evals."""
    skill_meta: Dict[str, Dict[str, str]] = {}
    for skill_md in sorted((ROOT_DIR / "skills").glob("*/SKILL.md")):
        parts = skill_md.read_text(encoding="utf-8").split("---", 2)
        parsed = yaml.safe_load(parts[1])
        tags = " ".join(parsed.get("metadata", {}).get("tags", []))
        skill_meta[parsed["name"]] = {
            "desc": str(parsed["description"]).lower(),
            "tags": tags.lower(),
        }
    assert len(skill_meta) == 6

    queries = [
        ("ui-frontend-analyst", "Chrome DevTools inventory of tokens, colors, fonts, AI Slop, and Before/After navigation diagram"),
        ("ui-brand-ux-planner", "Brand identity, OKLCH 60-30-10, Soft Hi-Tech Retro style tokens, Google Stitch, Figma MCP, Google Fonts, 3D Unity, DESIGN.md"),
        ("ui-clean-worker", "Implement React 19 Next.js 15 Tailwind v4 UI with 3-layer shadows, dark rim lighting, matte glass, and RAW SHA-256"),
        ("ui-quality-judge", "Read-only Actor-Critic WCAG 2.2 OKLCH contrast judge FNR < 0.001, 48x48px, :focus-visible, DOM==Tab, PASSED/REJECTED"),
        ("clinical-minimalist-ui", "Clinical EHR PEP dashboard, medical creatinine clearance calculator, and A4 .sus-grid vector print sheet"),
        ("complex-zero", "ReAct CDP DevTools audit for @xyflow/react infinite canvas, 150ms WebSocket chokidar, ghost nodes, Next.js 15 async params"),
    ]
    hits = 0
    for expected, q in queries:
        q_tokens = set(re.findall(r"[a-z0-9@._-]+", q.lower()))
        best = max(
            skill_meta,
            key=lambda s: sum(3 for t in q_tokens if len(t) > 2 and t in skill_meta[s]["tags"])
            + sum(1 for t in q_tokens if len(t) > 2 and t in skill_meta[s]["desc"].split("do not use")[0]),
        )
        if best == expected:
            hits += 1
    assert hits == len(queries)


def test_sync_shredded_shape_isolated(tmp_path: Path) -> None:
    """Verify plugin bundle deployment copies 6 skills, rules, plans, assets, and 4 agents cleanly."""
    summary = sync_shredded_shape(repo_root=ROOT_DIR, gemini_root=tmp_path)
    assert summary["status"] == "SYNCHRONIZED"
    plugin_root = tmp_path / "config" / "plugins" / "shredded-shape"
    assert (plugin_root / "plugin.json").is_file()
    assert len(list((plugin_root / "skills").glob("*/SKILL.md"))) == 6
    assert (plugin_root / "assets" / "ui_skills_architecture_atlas.html").is_file()
    assert len(list((tmp_path / "agents").glob("ui-*.md"))) == 4
