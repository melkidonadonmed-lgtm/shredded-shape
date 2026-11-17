"""Deterministic & adversarial test suite for shredded-shape UI/UX skills and subagents."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts import _ss_core
from scripts.sync_shredded_shape import sync_shredded_shape
from scripts.validate_shredded_shape import (
    validate_ecosystem,
    validate_repository,
    validate_skill_dir,
)


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
tactile_qa = _load_mod("ss_tactile_qa", "skills/ui-quality-judge/scripts/audit_tactile_ui.py")
complex_zero = _load_mod("ss_complex_zero", "skills/complex-zero/scripts/complex_zero_ast_auditor.py")


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
    assert raw_res.verdict == "[PASS]" and len(raw_res.files_checked) == 3
    assert all(f.passed and len(f.sha256) == 64 for f in raw_res.files_checked)

    judge_res = judge.evaluate_ui(atlas, wcag_level="AA")
    assert judge_res.verdict == "PASSED" and judge_res.wcag_level == "AA"
    assert judge_res.contrast_ratio_min >= 10.0 and judge_res.findings == []

    ux_res = legacy_ux.evaluate_target(atlas)
    assert ux_res.verdict == "PASS" and ux_res.final_score >= 95.0 and ux_res.max_dom_depth <= 12
    assert ux_res.divsoup_ratio <= 0.45 and ux_res.dimension_scores["iconography"] == 100.0

    tactile_res = tactile_qa.run_audit(atlas)
    assert tactile_res["verdict"] == "PASS" and tactile_res["readiness_score"] >= 90.0

    cz_res = complex_zero.audit_source_bundle(complex_zero._collect_target_files(atlas), root_dir=atlas.parent)
    assert cz_res["verdict"] == "[PASS]" and cz_res["total_score"] == 100


def test_self_tests_and_dag_compiler_adversarial() -> None:
    """Run all 7 script self-tests and reject invalid DAG nodes (>5 rules, read-only ownership, collisions)."""
    assert analyst._run_self_test() == 0
    assert planner._run_self_test() == 0
    assert worker_raw._run_self_test() == 0
    assert judge._run_self_test() == 0
    assert legacy_ux._run_self_test() == 0
    assert tactile_qa._run_self_test() == 0
    assert complex_zero.run_self_test() == 0

    assert len(planner.compile_default_dag(ROOT_DIR, mode="greenfield").nodes) == 3
    assert len(planner.compile_default_dag(ROOT_DIR, mode="refactor").nodes) == 4

    with pytest.raises(ValidationError, match="Read-only agent"):
        planner.DAGTaskNode(
            step_id="ro_write_fail", title="InvalidReadOnly", owner_agent="ui-analyst",
            reasoning_pattern="CoT", active_rules_count=3, read_targets=["src"],
            owned_files=["src/a.tsx"], acceptance_gate="passes", fallback_branch="fb1",
        )
    with pytest.raises(ValidationError, match="less than or equal to 5"):
        planner.DAGTaskNode(
            step_id="too_many_rules", title="Overflow", owner_agent="ui-worker",
            reasoning_pattern="ReAct", active_rules_count=6, owned_files=["a.tsx"],
            acceptance_gate="passes", fallback_branch="fb2",
        )
    with pytest.raises(ValidationError, match="collision"):
        planner.UIExecutionDAG(
            project_name="proj", style_archetype="tactile", complexity_tier="tier_1_static",
            brand_oklch_hue=220, recommended_stack=["HTML5"], style_tokens={},
            nodes=[
                planner.DAGTaskNode(step_id="node_1", title="Worker 1", owner_agent="ui-worker", reasoning_pattern="ReAct", active_rules_count=3, owned_files=["src/Card.tsx"], dependencies=[], acceptance_gate="passes", fallback_branch="fb1"),
                planner.DAGTaskNode(step_id="node_2", title="Worker 2", owner_agent="ui-worker", reasoning_pattern="ReAct", active_rules_count=3, owned_files=["src/Card.tsx"], dependencies=[], acceptance_gate="passes", fallback_branch="fb2"),
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
    skill_meta: dict[str, dict[str, str]] = {}
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
    assert (plugin_root / "assets" / "atlas_styles.css").is_file()
    assert (plugin_root / "assets" / "atlas_app.js").is_file()
    assert (plugin_root / "agents" / "ui-planner.md").is_file()
    assert len(list((tmp_path / "agents").glob("ui-*.md"))) == 4



def test_v120_oklab_svg_blob_neon_and_comment_hygiene(tmp_path: Path) -> None:
    """Verify exact OKLab luminance, SVG craft gates, blur-blob/neon bans, and comment hygiene."""
    assert _ss_core.oklch_to_relative_luminance(0.50) == pytest.approx(0.125, abs=1e-3)

    empty_svg = '<svg viewBox="0 0 24 24"></svg>'
    bloop_cloud = '<svg viewBox="0 0 24 24"><circle cx="8" cy="12" r="5"/><circle cx="12" cy="10" r="6"/><circle cx="16" cy="12" r="5"/></svg>'
    lucide_branch = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="6" x2="6" y1="3" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>'
    sprite_use = '<svg width="20" height="20" aria-hidden="true"><use href="#ic-cloud"/></svg>'
    assert _ss_core.inspect_inline_svgs(empty_svg)
    assert _ss_core.inspect_inline_svgs(bloop_cloud)
    assert _ss_core.inspect_inline_svgs(lucide_branch) == []
    assert _ss_core.inspect_inline_svgs(sprite_use) == []

    svg_bad = tmp_path / "SlopIcons.tsx"
    svg_bad.write_text(f"export function S() {{ return <div>{empty_svg}{bloop_cloud}</div>; }}", encoding="utf-8")
    svg_rep = analyst.scan_frontend(svg_bad)
    assert svg_rep.verdict != "[PASS]" and svg_rep.ai_slop_score > 15
    assert any("AUDIT-VIS-BAD-SVG" in d for d in svg_rep.spacing_and_style_defects)
    assert judge.evaluate_ui(svg_bad).verdict == "REJECTED"

    assert _ss_core.SLOP_BLOB_RE.search('<div class="blur-3xl rounded-full"></div>')
    assert _ss_core.SLOP_BLOB_RE.search(".orb { filter: blur(64px); }")
    assert _ss_core.SLOP_BLOB_RE.search(".matte-frosted { backdrop-filter: blur(18px) saturate(145%); }") is None

    assert len(_ss_core.find_neon_violations("color: #00ffff; accent-color: oklch(0.75 0.30 195);")) >= 2
    assert _ss_core.NEON_GLOW_RE.search(".btn { box-shadow: 0 0 18px #00ffff; }")
    assert _ss_core.find_neon_violations("color: #ef4444;") == []
    assert _ss_core.NEON_GLOW_RE.search(
        ".card { box-shadow: inset 0 1px 0 0 oklch(1 0 0 / 0.14), 0 10px 22px -6px oklch(0.62 0.15 245 / 0.14); }"
    ) is None

    gamed = tmp_path / "Gamed.tsx"
    gamed.write_text("// idle | loading | error | success\nexport const X = () => <main>ok</main>;", encoding="utf-8")
    gamed_rules = {f.rule_id for f in judge.evaluate_ui(gamed).findings}
    assert "AUDIT-STATE-GAMING" in gamed_rules

    clean_css = tmp_path / "clean_tokens.css"
    clean_css.write_text(
        "/* Never use #000000 or --neon-pink or blur-3xl */\n"
        ":root { --ink-primary: light-dark(oklch(0.20 0.02 245), oklch(0.95 0.01 245));\n"
        "  --surface-card: light-dark(oklch(0.99 0.004 245), oklch(0.215 0.016 245)); }\n"
        ".engraved-pill { background: var(--surface-card); }\n"
        ":focus-visible { outline: 2px dashed currentColor; }\n",
        encoding="utf-8",
    )
    assert judge.evaluate_ui(clean_css).verdict == "PASSED"

    assert _ss_core.DASHED_BOX_SLOP_RE.search(".flow { border: 1px dashed #666; }")
    assert _ss_core.DASHED_BOX_SLOP_RE.search(":focus-visible { outline: 2px dashed currentColor; }") is None
    assert _ss_core.has_confetti_badge_slop(".mono-tag.warn{} .mono-tag.danger{} .mono-tag.ok{}")
    assert not _ss_core.has_confetti_badge_slop(".engraved-pill {} .lum-bead {}")

    slop_wire_confetti = tmp_path / "SlopWireframeConfetti.css"
    slop_wire_confetti.write_text(
        ".flow { border: 1px dashed oklch(0.5 0.02 250); }\n"
        ".mono-tag.warn { color: oklch(0.7 0.1 70); }\n"
        ".mono-tag.danger { color: oklch(0.6 0.1 25); }\n"
        ".mono-tag.ok { color: oklch(0.7 0.1 155); }\n",
        encoding="utf-8",
    )
    wc_rules = {f.rule_id for f in judge.evaluate_ui(slop_wire_confetti).findings}
    assert "ANTI-SLOP-WIREFRAME" in wc_rules and "ANTI-SLOP-CONFETTI" in wc_rules
    assert analyst.scan_frontend(slop_wire_confetti).ai_slop_score > 15


def test_v140_theme_polarity_bundle_dom_cli_and_raw_gates(tmp_path: Path) -> None:
    """Verify v1.4.0 polarity isolation, .sus-grid AAA, multi-file DOM/TS generics, CLI positional args, and RAW gates."""
    dag_alias = planner.compile_default_dag(tmp_path, style="hitech", hue=230, mode="greenfield")
    assert dag_alias.style_archetype == "hi-tech"
    out_dag = tmp_path / "out" / "dag.json"
    dag_proc = subprocess.run(
        [sys.executable, str(ROOT_DIR / "skills/ui-brand-ux-planner/scripts/ui_dag_compiler.py"), str(tmp_path), "--style", "hitech", "--out", str(out_dag)],
        check=False, capture_output=True, text=True,
    )
    assert dag_proc.returncode == 0 and out_dag.is_file()
    assert json.loads(out_dag.read_text(encoding="utf-8"))["style_archetype"] == "hi-tech"

    atlas = str(ROOT_DIR / "assets" / "ui_skills_architecture_atlas.html")
    for rel_script in (
        "skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py",
        "skills/ui-clean-worker/scripts/verify_raw_frontend.py",
        "skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py",
        "skills/ui-quality-judge/scripts/audit_tactile_ui.py",
        "skills/ui-quality-judge/scripts/ui_ux_frontend_auditor.py",
        "skills/complex-zero/scripts/complex_zero_ast_auditor.py",
    ):
        res = subprocess.run([sys.executable, str(ROOT_DIR / rel_script), atlas], check=False, capture_output=True, text=True)
        assert res.returncode == 0, f"Positional CLI failed for {rel_script}: {res.stderr}"

    bad_theme = tmp_path / "bad_theme.css"
    bad_theme.write_text(
        ":root { color-scheme: light dark; --ink-primary: light-dark(oklch(0.18 0.02 250), oklch(0.95 0.01 250)); "
        "--bg-canvas: light-dark(oklch(0.97 0.005 250), oklch(0.20 0.02 250)); "
        "--bg-card: light-dark(oklch(0.99 0.002 250), oklch(0.24 0.02 250)); }\n"
        "[data-theme='bad-dark'] { color-scheme: dark; --bg-canvas: oklch(0.25 0.02 250); --bg-card: oklch(0.18 0.02 250); --bg-key: oklch(0.45 0.05 250); --ink-on-key: oklch(0.40 0.05 250); }\n"
        ".btn { background: color-mix(in oklch, oklch(0.6 0.15 240) 20%, transparent); transition: border-top-color 0.2s ease; }\n"
        ":focus-visible { outline: 2px solid currentColor; }\n",
        encoding="utf-8",
    )
    bad_rep = judge.evaluate_ui(bad_theme)
    bad_ids = {f.rule_id for f in bad_rep.findings}
    assert bad_rep.verdict == "REJECTED" and "OPTICS-DARK-ELEVATION" in bad_ids
    assert "WCAG-1.4.3-OKLCH" in bad_ids and "OPTICS-COLOR-MIX-OKLAB" in bad_ids
    assert _ss_core.REFLOW_TRANSITION_RE.search("transition: border-top-color 0.2s ease;") is None
    assert _ss_core.REFLOW_TRANSITION_RE.search("transition: all 0.2s ease;") is not None

    sus_css = tmp_path / "sus.css"
    sus_css.write_text(":root { --ink-primary: light-dark(oklch(0.18 0.02 250), oklch(0.95 0.01 250)); --bg-card: light-dark(oklch(0.99 0.002 250), oklch(0.22 0.02 250)); } .sus-grid { display: grid; }\n", encoding="utf-8")
    assert judge.evaluate_ui(sus_css).wcag_level == "AAA"

    bundle_dir = tmp_path / "app"
    bundle_dir.mkdir()
    (bundle_dir / "index.html").write_text("<!DOCTYPE html><html lang='en'><meta name='viewport' content='width=device-width'><link rel='stylesheet' href='s.css?v=1.4.0'><script src='a.js' defer></script><main><h1>Hi</h1></main></html>", encoding="utf-8")
    (bundle_dir / "a.js").write_text("const tpl = '<svg><circle cx=\"5\" cy=\"5\" r=\"4\"/></svg>';\nconst t = setTimeout(() => 1, 10);", encoding="utf-8")
    (bundle_dir / "App.tsx").write_text("export function App(){ const [s, setS] = useState<{id: string}>({id:'1'}); return <section>{s.id}</section>; }", encoding="utf-8")
    (bundle_dir / "s.css").write_text("body{-webkit-font-smoothing:antialiased;font-optical-sizing:auto;} .c{padding:16px;border-top:1px solid oklch(1 0 0 / 0.1);box-shadow:0 2px 4px oklch(0.1 0 0 / 0.2),0 8px 16px -2px oklch(0.1 0 0 / 0.2);} :focus-visible{outline:2px solid currentColor;} @media (prefers-reduced-motion:reduce){*{transition:none;}}", encoding="utf-8")
    b_rep = legacy_ux.evaluate_target(bundle_dir)
    assert b_rep.max_dom_depth <= 5 and b_rep.dimension_scores["iconography"] == 100.0

    bad_worker = tmp_path / "Reflow.css"
    bad_worker.write_text(".x{border:1px dashed oklch(0.5 0.02 250);transition:width 0.2s;}\n" + "\n".join([".p{gap:4px;}"] * 602), encoding="utf-8")
    w_res = worker_raw.verify_raw_frontend(bad_worker, min_bytes=10, run_tsc=True)
    assert w_res.verdict == "[TYPE-ERROR]" and not w_res.tsc_passed
    w_issues = " ".join(w_res.files_checked[0].issues)
    assert "ANTI-SLOP-WIREFRAME" in w_issues and "PERF-REFLOW" in w_issues and "CAP-600L" in w_issues

    missing_repo = tmp_path / "bad_agents"
    (missing_repo / "agents").mkdir(parents=True)
    (missing_repo / "rules").mkdir(parents=True)
    (missing_repo / "plugin.json").write_text('{"name":"x","logo":"m.svg"}', encoding="utf-8")
    (missing_repo / "agents" / "ui-analyst.md").write_text("---\nname: ui-analyst\ndescription: x\nsubagent: true\nmainAgent: false\nmodel: inherit\ntools:\n  - read_file\n---\nNo language tag.\n", encoding="utf-8")
    eco_errs = validate_ecosystem(missing_repo)
    assert any("send_message" in e for e in eco_errs) and any("pt-BR" in e for e in eco_errs)


def test_optical_contrast_grain_stacking_and_font_shadowing(tmp_path: Path) -> None:
    """Verify OPTICS-GRAIN-ABOVE-TEXT, WCAG-1.4.3-BRAND-FILL, OPTICS-OPAQUE-KEY-SHEEN, TYP-DEAD-FONT-FALLBACK, and <use> filter."""
    grain_bad = tmp_path / "grain_bad.css"
    grain_bad.write_text(".card::after { background-image: url(\"data:image/svg+xml,<feTurbulence/>\"); }\n", encoding="utf-8")
    assert any(f.rule_id == "OPTICS-GRAIN-ABOVE-TEXT" for f in judge.evaluate_ui(grain_bad).findings)

    grain_ok = tmp_path / "grain_ok.css"
    grain_ok.write_text(
        ":root { --ink-primary: light-dark(oklch(0.18 0.02 250), oklch(0.95 0.01 250)); "
        "--bg-card: light-dark(oklch(0.99 0.002 250), oklch(0.20 0.02 250)); }\n"
        ".card { position: relative; isolation: isolate; } "
        ".card::after { z-index: -1; background-image: url(\"data:image/svg+xml,<feTurbulence/>\"); }\n",
        encoding="utf-8",
    )
    assert judge.evaluate_ui(grain_ok).verdict == "PASSED"

    brand_bad = tmp_path / "brand_bad.css"
    brand_bad.write_text(
        ":root { --brand-hue: 255; --brand-primary: light-dark(oklch(0.49 0.16 var(--brand-hue)), oklch(0.67 0.15 var(--brand-hue))); }\n"
        ".btn-primary-bevel { background-color: var(--brand-primary); color: oklch(0.99 0.002 0); }\n",
        encoding="utf-8",
    )
    assert any(f.rule_id == "WCAG-1.4.3-BRAND-FILL" for f in judge.evaluate_ui(brand_bad).findings)

    sheen_bad = tmp_path / "sheen_bad.css"
    sheen_bad.write_text(
        ":root { --light-key: linear-gradient(180deg, light-dark(oklch(1 0 0), oklch(1 0 0 / 0.08)) 0%, transparent 100%); }\n"
        "[data-theme='nexus-slate'] { color-scheme: light; --bg-key: oklch(0.43 0.14 238); --ink-on-key: oklch(0.99 0.002 0); }\n",
        encoding="utf-8",
    )
    assert any(f.rule_id == "OPTICS-OPAQUE-KEY-SHEEN" for f in judge.evaluate_ui(sheen_bad).findings)

    font_html = tmp_path / "font_and_use.html"
    font_html.write_text(
        "<style>.m { font-family: 'JetBrains Mono', ui-monospace, 'Cascadia Code', monospace; }</style>"
        "<svg width='16' height='16' viewBox='0 0 24 24'><use href='#ic-menu'/></svg><a href='/home'>Home</a>",
        encoding="utf-8",
    )
    inv = analyst.scan_frontend(font_html)
    assert any("TYP-DEAD-FONT-FALLBACK" in d for d in inv.spacing_and_style_defects)
    assert "#ic-menu" not in inv.navigation_targets and "/home" in inv.navigation_targets
    assert legacy_ux.evaluate_source("<!DOCTYPE html><html><meta name='viewport' content='width=device-width'><main><p><code>:user-invalid</code> (AA-123)</p><section><p>Next</p></section></main></html>").max_dom_depth <= 5
