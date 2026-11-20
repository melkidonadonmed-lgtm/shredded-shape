"""v1.6.0 calibration & adversarial tests for intent-first DAG, 3-axis judge, and craft/AppSec guards."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import _ss_craft_guards, validate_shredded_shape


def _load(rel_path: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, ROOT / rel_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ANALYST = _load("skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py", "ss_analyst_v160")
PLANNER = _load("skills/ui-brand-ux-planner/scripts/ui_dag_compiler.py", "ss_planner_v160")
WORKER = _load("skills/ui-clean-worker/scripts/verify_raw_frontend.py", "ss_worker_v160")
JUDGE = _load("skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py", "ss_judge_v160")
AXIS_JUDGE = _load("skills/ui-quality-judge/scripts/artifact_axis_judge.py", "ss_axis_v160")
CZ_AUD = _load("skills/complex-zero/scripts/complex_zero_ast_auditor.py", "ss_cz_v160")


def test_client_secret_leaks_redacted_and_public_allowlist(tmp_path: Path) -> None:
    secret_tok = "sk-live-" + "1234567890abcdefghijkl"
    bad = tmp_path / "ClientLeak.tsx"
    bad.write_text(f"const k = '{secret_tok}';\nconst e = process.env.NEXT_PUBLIC_OPENAI_SECRET;\n", encoding="utf-8")
    inv = ANALYST.scan_frontend(bad)
    assert inv.verdict == "[FAIL]" and any("AUDIT-SEC-ENV-LEAK" in d for d in inv.spacing_and_style_defects)
    raw_res = WORKER.verify_raw_frontend(bad, min_bytes=10)
    assert raw_res.verdict == "[RAW-VIOLATION]"
    j_rep = JUDGE.evaluate_ui(bad)
    assert j_rep.verdict == "REJECTED" and any(f.rule_id == "AUDIT-SEC-ENV-LEAK" for f in j_rep.findings)
    assert secret_tok not in j_rep.model_dump_json() and "[REDACTED]" in j_rep.model_dump_json()

    ok = tmp_path / "ClientPublicOk.tsx"
    ok.write_text(
        "export const cfg = { stripe: process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY, supa: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY, url: process.env.NEXT_PUBLIC_APP_URL };\n",
        encoding="utf-8",
    )
    assert JUDGE.evaluate_ui(ok).verdict == "PASSED" and ANALYST.scan_frontend(ok).verdict == "[PASS]"


def test_placeholder_omissions_comments_only_and_spread_safe(tmp_path: Path) -> None:
    omitted = tmp_path / "Omitted.tsx"
    omitted.write_text(
        "export function Panel() {\n  // ... rest of code\n  return <section>{/* resto do código continua aqui */}ok</section>;\n}\n",
        encoding="utf-8",
    )
    assert ANALYST.scan_frontend(omitted).verdict == "[FAIL]"
    assert WORKER.verify_raw_frontend(omitted, min_bytes=20).verdict == "[RAW-VIOLATION]"
    assert any(f.rule_id == "AUDIT-STUB-PLACEHOLDER" for f in JUDGE.evaluate_ui(omitted).findings)

    clean = tmp_path / "SpreadOk.tsx"
    clean.write_text("export function SpreadOk(props: any) { return <input placeholder='Filtrar...' {...props} />; }\n", encoding="utf-8")
    assert JUDGE.evaluate_ui(clean).verdict == "PASSED" and ANALYST.scan_frontend(clean).verdict == "[PASS]"


def test_unsafe_html_sinks_per_occurrence_fouc_scoped(tmp_path: Path) -> None:
    fouc_tag = "<" + "script dangerouslySetInnerHTML={{__html: \"localStorage.getItem('t');setAttribute('data-theme','dark')\"}} />"
    mixed = tmp_path / "MixedXss.tsx"
    mixed.write_text(
        f"export function Page({{ user }}: any) {{ return <main>{fouc_tag}<div dangerouslySetInnerHTML={{{{__html: user}}}} /></main>; }}\n",
        encoding="utf-8",
    )
    assert any(f.rule_id == "AUDIT-SEC-01" for f in JUDGE.evaluate_ui(mixed).findings)
    assert WORKER.verify_raw_frontend(mixed, min_bytes=20).verdict == "[RAW-VIOLATION]"
    assert ANALYST.scan_frontend(mixed).verdict == "[FAIL]"
    assert any(f.get("rule") == "UNSANITIZED_HTML_SINK" for f in CZ_AUD.audit_source_bundle({"MixedXss.tsx": mixed.read_text(encoding="utf-8")})["findings"])

    ev_sink = tmp_path / "EvalSink.ts"
    ev_sink.write_text("export function run(code: string) { return " + "ev" + "al(code); }\n", encoding="utf-8")
    assert any(f.rule_id == "AUDIT-SEC-01" for f in JUDGE.evaluate_ui(ev_sink).findings)

    safe = tmp_path / "SafeHtml.tsx"
    safe.write_text(
        f"export function Safe({{ raw }}: any) {{ const clean = DOMPurify.sanitize(raw); return <main>{fouc_tag}<div dangerouslySetInnerHTML={{{{__html: clean}}}} /></main>; }}\n",
        encoding="utf-8",
    )
    assert JUDGE.evaluate_ui(safe).verdict == "PASSED"


def test_gradient_text_dense_grid_and_redundant_nav_aria(tmp_path: Path) -> None:
    bad_css = tmp_path / "slop.css"
    bad_css.write_text(
        ".hero { -webkit-background-clip: text; color: transparent; background-image: linear-gradient(in oklch, red, blue); }\n"
        ".grid { display: grid; grid-auto-flow: row dense; }\n",
        encoding="utf-8",
    )
    j_rules = {f.rule_id for f in JUDGE.evaluate_ui(bad_css).findings}
    assert "ANTI-SLOP-GRADIENT-TEXT" in j_rules and "WCAG-1.3.2" in j_rules

    bad_nav = tmp_path / "NavWarn.tsx"
    bad_nav.write_text(
        "export function Nav() { return <div className='bg-clip-text text-transparent bg-linear-to-r'><aside aria-label='Navegacao por capitulos'><nav aria-label='Navegação Principal'><a href='/'>Home</a></nav></aside></div>; }\n",
        encoding="utf-8",
    )
    n_findings = JUDGE.evaluate_ui(bad_nav).findings
    assert any(f.rule_id == "ANTI-SLOP-GRADIENT-TEXT" and f.severity == "CRITICAL" for f in n_findings)
    assert any(f.rule_id == "A11Y-NAV-REDUNDANT-LABEL" and f.severity == "WARNING" for f in n_findings)

    good_nav = tmp_path / "NavOk.tsx"
    good_nav.write_text("<aside aria-label='Navegacao por capitulos'><nav aria-label='Primary'><a href='/'>Home</a></nav></aside>\n", encoding="utf-8")
    assert JUDGE.evaluate_ui(good_nav).findings == []


def test_fecolormatrix_isolated_vs_same_filter_gooey(tmp_path: Path) -> None:
    isolated = tmp_path / "color_matrix_ok.html"
    isolated.write_text(
        "<!DOCTYPE html><html lang='en'><head><meta name='viewport' content='width=device-width'></head><body>"
        "<svg hidden width='0' height='0'><defs>"
        "<filter id='protanopia'><feColorMatrix type='matrix' values='0.567 0.433 0 0 0 0.558 0.442 0 0 0 0 0.242 0.758 0 0 0 0 0 1 0'/></filter>"
        "<filter id='softblur'><feGaussianBlur stdDeviation='2'/></filter>"
        "</defs></svg><main><h1>Color Matrix</h1></main></body></html>",
        encoding="utf-8",
    )
    assert ANALYST.scan_frontend(isolated).ai_slop_score == 0 and JUDGE.evaluate_ui(isolated).verdict == "PASSED"

    gooey = tmp_path / "gooey_bad.html"
    gooey.write_text(
        "<svg><defs><filter id='goo'><feGaussianBlur stdDeviation='10'/><feColorMatrix type='matrix' values='1 0 0 0 0'/></filter></defs></svg>",
        encoding="utf-8",
    )
    assert ANALYST.scan_frontend(gooey).verdict == "[FAIL]"
    assert any(f.rule_id == "ANTI-SLOP-BLOB" for f in JUDGE.evaluate_ui(gooey).findings)


def test_advisory_root_hygiene_and_menu_audit_non_blocking(tmp_path: Path) -> None:
    proj = tmp_path / "app"
    (proj / "src").mkdir(parents=True)
    (proj / "package-lock.json").write_text("{}", encoding="utf-8")
    (proj / "pnpm-lock.yaml").write_text("", encoding="utf-8")
    (proj / "tsconfig.json").write_text('{"compilerOptions": {"strict": false}}', encoding="utf-8")
    (proj / "package.json").write_text('{"dependencies": {"reactflow": "11", "@xyflow/react": "12"}}', encoding="utf-8")
    (proj / "src" / "Nav.tsx").write_text(
        "export function Nav(){return <nav aria-label='Main'><ol><li>/</li></ol><a href='/a'>This Very Long Navigation Menu Label Exceeds Limit</a></nav>;}\n",
        encoding="utf-8",
    )
    rep = ANALYST.scan_frontend(proj)
    assert len(rep.root_hygiene_warnings) >= 3 and len(rep.menu_label_audit) >= 2 and rep.ai_slop_score == 0
    assert ANALYST.scan_frontend(proj / "src" / "Nav.tsx").root_hygiene_warnings == []

    atlas_rep = ANALYST.scan_frontend(ROOT / "assets" / "ui_skills_architecture_atlas.html")
    assert atlas_rep.ai_slop_score == 0 and atlas_rep.menu_label_audit == [] and atlas_rep.root_hygiene_warnings == []


def test_dag_planner_directed_src_tier_and_complex_zero_checks(tmp_path: Path) -> None:
    dag_pd = PLANNER.compile_default_dag(ROOT, mode="planner_directed", style="tactile", spatial="bento_12_col")
    assert len(dag_pd.nodes) == 5 and dag_pd.style_tokens["spatial"] == "bento_12_col"
    assert all(n.active_rules_count <= 5 for n in dag_pd.nodes)

    nx_root = tmp_path / "nx"
    (nx_root / "src").mkdir(parents=True)
    (nx_root / "package.json").write_text("{}", encoding="utf-8")
    (nx_root / "next.config.mjs").write_text("export default {};", encoding="utf-8")
    assert PLANNER.compile_default_dag(nx_root / "src").complexity_tier == "tier_3_fullstack_pwa"

    bad_src = {
        "Canvas.tsx": "import { ReactFlow } from '@xyflow/react'; export function C(){ return <ReactFlow nodeTypes={{ n: N }} />; }\n",
        "watcher.ts": "import path from 'node:path'; export const rel = (a: string, b: string) => path.relative(a, b);\n",
    }
    res = CZ_AUD.audit_source_bundle(bad_src)
    rules = {f["rule"] for f in res["findings"]}
    assert "XYFLOW_UNHOISTED_NODE_TYPES" in rules and "WINDOWS_PATH_SEPARATOR_UNNORMALIZED" in rules

    good_src = {
        "Canvas.tsx": "import { ReactFlow } from '@xyflow/react'; const nodeTypes = { n: N }; export function C(){ return <ReactFlow nodeTypes={nodeTypes} />; }\n",
        "watcher.ts": "import path from 'node:path'; export const rel = (a: string, b: string) => path.relative(a, b).replace(/\\\\/g, '/');\n",
    }
    good_rules = {f["rule"] for f in CZ_AUD.audit_source_bundle(good_src)["findings"]}
    assert "XYFLOW_UNHOISTED_NODE_TYPES" not in good_rules and "WINDOWS_PATH_SEPARATOR_UNNORMALIZED" not in good_rules


def test_artifact_axis_judge_axis2_plan_and_axis3_audit(tmp_path: Path) -> None:
    assert AXIS_JUDGE._run_self_test() == 0
    dag_file = tmp_path / "dag.json"
    dag_file.write_text(PLANNER.compile_default_dag(ROOT, mode="planner_directed").model_dump_json(), encoding="utf-8")
    assert AXIS_JUDGE.evaluate_execution_plan(dag_file).verdict == "PASSED"

    ws = tmp_path / "ws"
    (ws / "src").mkdir(parents=True)
    (ws / "src" / "App.tsx").write_text("export const x = 1;\n", encoding="utf-8")
    clareza_bad = tmp_path / "clareza.md"
    clareza_bad.write_text(
        "1. Token OKLCH\n2. Typography\n3. Slop SVG\n4. DevTools\n5. Navigation\n```mermaid\nflowchart LR\nA-->B\n```\n7. Before After\nFake hit at src/nonexistent.tsx:999\n",
        encoding="utf-8",
    )
    rep = AXIS_JUDGE.evaluate_technical_audit(clareza_bad, workspace=ws)
    assert rep.verdict == "REJECTED" and any(f["rule_id"] == "AUDIT-HALLUCINATED-CITATION" for f in rep.findings)

    design_ok = tmp_path / "DESIGN.md"
    design_ok.write_text(
        "# 1. Brand Soft Archetype\n## 2. OKLCH 5-Plane\n## 3. Depth Shadows\n## 4. Typography\n## 5. SVG\n## 6. Adaptive Layout\n## 7. State FSM Security\n## 8. Acceptance Scope Lock\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(ROOT / "skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py"), str(design_ok), "--axis", "execution_plan", "--json"],
        check=False, capture_output=True, text=True,
    )
    assert proc.returncode == 0 and json.loads(proc.stdout)["verdict"] == "PASSED"


def test_v160_release_parity_l3_caps_devtools_and_f1() -> None:
    assert json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))["version"] == "1.6.0"
    assert json.loads((ROOT / "plans" / "ui_actor_critic_dag.json").read_text(encoding="utf-8"))["version"] == "1.6.0"
    for ref in (
        ROOT / "skills/ui-brand-ux-planner/references/context_engineering_and_ambiguity_protocol.md",
        ROOT / "skills/complex-zero/references/xyflow_dagre_layout_and_camera_sync.md",
    ):
        assert ref.is_file() and len(ref.read_text(encoding="utf-8").splitlines()) <= 150
    probe_js = (ROOT / "skills/ui-frontend-analyst/scripts/devtools_live_probe.js").read_text(encoding="utf-8")
    for key in ("wrappedNavItems", "mysteryIconOnlyNavCount", "gradientTextCount", "skipLinkPresent"):
        assert key in probe_js

    passed, total, errors = validate_shredded_shape.validate_repository(ROOT, strict_mode=True)
    assert errors == [] and passed == total == 7
    assert len(_ss_craft_guards.__file__) > 0

    meta: dict[str, dict[str, str]] = {}
    for sm in sorted((ROOT / "skills").glob("*/SKILL.md")):
        parsed = yaml.safe_load(sm.read_text(encoding="utf-8").split("---", 2)[1])
        meta[parsed["name"]] = {"desc": str(parsed["description"]).lower(), "tags": str(parsed["metadata"]["tags"]).lower()}
    v160_queries = [
        ("ui-quality-judge", "Run double-pass 3-axis-judge WCAG 2.2 OKLab accessibility contrast audit"),
        ("complex-zero", "Fix dagre-layout node overlap, fitview camera-sync, and @xyflow/react async params"),
        ("ui-brand-ux-planner", "Perform ambiguity-triage, spacing-engineering, OKLCH palette, and DESIGN.md dag-compiler"),
        ("ui-frontend-analyst", "Execute intent-first scoped-probe DevTools navigation-clareza and ai-slop audit"),
    ]
    for expected, q in v160_queries:
        q_toks = {t for t in q.lower().replace(",", "").split() if len(t) > 2}
        best = max(meta, key=lambda s: sum(3 for t in q_toks if t in meta[s]["tags"]) + sum(1 for t in q_toks if t in meta[s]["desc"].split("do not use")[0]))
        assert best == expected
