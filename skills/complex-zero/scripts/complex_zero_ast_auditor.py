#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Deterministic 4-Axis AST, @xyflow/react, Next.js 15+ async params, and CDP auditor."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
for _cand in (*(p / "scripts" for p in SCRIPT_DIR.parents if (p / "pyproject.toml").is_file()), SCRIPT_DIR, *(p / "scripts" for p in SCRIPT_DIR.parents)):
    if (_cand / "_ss_core.py").is_file() and str(_cand) not in sys.path:
        sys.path.insert(0, str(_cand))
        break
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import _ss_core
import _ss_craft_guards
import _ss_guards
from visual_hierarchy_and_cdp_probe import (
    CHROME_DEVTOOLS_EVALUATE_SCRIPT,
    UnifiedVisualOrgReport,
    analyze_visual_hierarchy_and_organization,
    probe_live_url_metadata,
)

FRONTEND_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".css", ".html"}
EMPTY_ARROW_OR_FN_RE = re.compile(r"(?:=>\s*\{\s*\}|function\s+[a-zA-Z0-9_]*\s*\([^)]*\)\s*\{\s*\})")
CONSOLE_ONLY_BODY_RE = re.compile(r"=>\s*\{\s*console\.log\([^}]*\)\s*;?\s*\}")
FAKE_TELEMETRY_RANDOM_RE = re.compile(r"(?:fps|cpu|latency|memory|metric)[a-zA-Z0-9_]*\s*:\s*[^,\n]*Math\.random\(\)", re.IGNORECASE)
HARDCODED_OKLCH_VALID_RE = re.compile(r"oklchContrastValid\s*:\s*true\b")
OUTLINE_NONE_RE = re.compile(r"outline\s*:\s*(?:none|0)\b")
FOCUS_VISIBLE_RE = re.compile(r":focus-visible\b")
POINTER_COARSE_RE = re.compile(r"any-pointer\s*:\s*coarse|pointer\s*:\s*coarse")
REDUCED_MOTION_RE = re.compile(r"prefers-reduced-motion\s*:\s*reduce")
CONTAINER_QUERY_RE = re.compile(r"@container\b|container-type\s*:\s*inline-size")
OKLCH_RE = re.compile(r"oklch\(")
TABULAR_NUMS_RE = re.compile(r"tabular-nums")
LEGACY_REACTFLOW_IMPORT_RE = re.compile(r"from\s+['\"]reactflow['\"]")
SYNC_NEXT15_PARAMS_RE = re.compile(r"export\s+default\s+function\s+\w+\s*\(\s*\{\s*params\s*\}\s*:\s*\{\s*params\s*:\s*\{\s*\w+\s*:\s*string")
ASYNC_NEXT15_PARAMS_RE = re.compile(r"Promise<\s*\{[^}]*\}\s*>")
EMPTY_CATCH_RE = re.compile(r"\bcatch\s*(?:\([^)]*\))?\s*\{\s*\}")
FORWARD_REF_RE = re.compile(r"\bforwardRef\s*(?:<|\()")
_RF_TAG_RE = re.compile(r"<ReactFlow\b", re.IGNORECASE)
_INLINE_RF_TYPES_RE = re.compile(r"\b(?:nodeTypes|edgeTypes)\s*=\s*\{\{")
_LOCAL_RF_TYPES_RE = re.compile(r"\b(?:const|let)\s+(?:nodeTypes|edgeTypes)\s*=\s*\{")
_PATH_REL_RE = re.compile(r"\bpath\.relative\s*\(")
_BARE_REL_RE = re.compile(r"(?<![.\w])relative\s*\(")
_NORM_PATH_RE = re.compile(r"posix\.relative|replace(?:All)?\([^)]*\\\\|split\([^)]*\)\.join\(|normalize\w*Path")


def _evaluate_axis_1(
    combined: str, has_css: bool, org_rep: UnifiedVisualOrgReport, findings: list[dict[str, Any]], div_clicks: int = 0
) -> int:
    score = 25
    if div_clicks > 0:
        pen = min(10, div_clicks * 5)
        score -= pen
        findings.append({"axis": 1, "severity": "WARN", "rule": "SEMANTIC_BUTTON", "detail": f"{div_clicks} <div onClick> without role (-{pen} pts)"})
    if OUTLINE_NONE_RE.search(combined) and not FOCUS_VISIBLE_RE.search(combined):
        score -= 10
        findings.append({"axis": 1, "severity": "CRITICAL", "rule": "FOCUS_VISIBLE_MISSING", "detail": "outline: none without :focus-visible (-10 pts)"})
    if has_css and not POINTER_COARSE_RE.search(combined):
        score -= 5
        findings.append({"axis": 1, "severity": "WARN", "rule": "FITTS_COARSE_POINTER", "detail": "Missing @media (any-pointer: coarse) for >= 48x48px targets (-5 pts)"})
    if has_css and not REDUCED_MOTION_RE.search(combined):
        score -= 5
        findings.append({"axis": 1, "severity": "WARN", "rule": "VESTIBULAR_SAFETY", "detail": "Missing @media (prefers-reduced-motion: reduce) (-5 pts)"})
    if org_rep.cramped_menu_violations:
        pen = min(15, len(org_rep.cramped_menu_violations) * 5)
        score -= pen
        findings.append({"axis": 1, "severity": "CRITICAL", "rule": "CRAMPED_MENU_OR_BAD_TYPOGRAPHY", "detail": f"{len(org_rep.cramped_menu_violations)} cramped menu violations (-{pen} pts)", "examples": org_rep.cramped_menu_violations[:5]})
    return max(0, score)


def _evaluate_axis_2(combined: str, has_css: bool, org_rep: UnifiedVisualOrgReport, findings: list[dict[str, Any]]) -> int:
    score = 25
    if has_css and not CONTAINER_QUERY_RE.search(combined):
        score -= 10
        findings.append({"axis": 2, "severity": "CRITICAL", "rule": "MICRO_CONTAINER_QUERY", "detail": "Missing container-type: inline-size / @container (-10 pts)"})
    if has_css and not OKLCH_RE.search(combined):
        score -= 10
        findings.append({"axis": 2, "severity": "WARN", "rule": "OKLCH_COLOR_SPACE", "detail": "Missing perceptual oklch() tokens (-10 pts)"})
    if not TABULAR_NUMS_RE.search(combined):
        score -= 5
        findings.append({"axis": 2, "severity": "WARN", "rule": "TABULAR_NUMS_METRICS", "detail": "Missing tabular-nums telemetry alignment (-5 pts)"})
    if HARDCODED_OKLCH_VALID_RE.search(combined):
        score -= 15
        findings.append({"axis": 2, "severity": "CRITICAL", "rule": "PLACEBO_CONTRAST_CHECK", "detail": "Hardcoded oklchContrastValid: true (-15 pts)"})
    if org_rep.sprawl_and_org_violations:
        pen = min(15, len(org_rep.sprawl_and_org_violations) * 6)
        score -= pen
        findings.append({"axis": 2, "severity": "CRITICAL", "rule": "TAB_AND_NAV_SPRAWL_NO_SLOT_REUSE", "detail": f"Tab/nav sprawl detected (-{pen} pts): {'; '.join(org_rep.sprawl_and_org_violations)}"})
    if org_rep.hierarchy_violations:
        pen = min(15, len(org_rep.hierarchy_violations) * 5)
        score -= pen
        findings.append({"axis": 2, "severity": "CRITICAL", "rule": "VISUAL_HIERARCHY_FLATNESS", "detail": f"Flat visual hierarchy / micro-fonts (-{pen} pts)", "examples": org_rep.hierarchy_violations[:5]})
    return max(0, score)


def _count_non_context_empty_fns(combined: str) -> int:
    filtered = "\n".join(line for line in combined.splitlines() if "createContext" not in line and "= () => {}" not in line)
    return len(EMPTY_ARROW_OR_FN_RE.findall(filtered))


def _has_nested_rf_types(stripped: str) -> bool:
    masked_str = _ss_core._TOKENIZER_RE.sub(lambda m: " " * len(m.group(0)), stripped)
    depth = 0
    for line in masked_str.splitlines():
        if depth > 0 and _LOCAL_RF_TYPES_RE.search(line) and "useMemo" not in line:
            return True
        depth = max(0, depth + line.count("{") - line.count("}"))
    return False


def _check_xyflow_and_path_hygiene(sources: dict[str, str], findings: list[dict[str, Any]]) -> int:
    penalty = 0
    unhoisted_hit = False
    path_hit = False
    for rel, raw_src in sources.items():
        if Path(rel).suffix.lower() not in {".ts", ".tsx", ".js", ".jsx"}:
            continue
        stripped = _ss_core.strip_comments(raw_src)
        for m in _RF_TAG_RE.finditer(stripped):
            tag, _ = _ss_guards._scan_jsx_opening_tag(stripped, m.start())
            if _INLINE_RF_TYPES_RE.search(tag):
                unhoisted_hit = True
        if not unhoisted_hit and _has_nested_rf_types(stripped):
            unhoisted_hit = True
        has_path_imp = bool(re.search(r"from\s+['\"](?:node:)?path['\"]", stripped))
        lines = stripped.splitlines()
        for idx, line in enumerate(lines):
            if _PATH_REL_RE.search(line) or (has_path_imp and _BARE_REL_RE.search(line)):
                win = "\n".join(lines[max(0, idx - 1) : min(len(lines), idx + 3)])
                if not _NORM_PATH_RE.search(win):
                    path_hit = True
    if unhoisted_hit:
        penalty += 10
        findings.append({"axis": 3, "severity": "CRITICAL", "rule": "XYFLOW_UNHOISTED_NODE_TYPES", "detail": "Inline or component-scoped nodeTypes/edgeTypes causes 60fps remount thrashing (-10 pts)"})
    if path_hit:
        penalty += 5
        findings.append({"axis": 3, "severity": "WARN", "rule": "WINDOWS_PATH_SEPARATOR_UNNORMALIZED", "detail": "path.relative() without '/' normalization breaks Windows chokidar/WebSocket matching (-5 pts)"})
    return penalty


def _evaluate_axis_3(combined: str, sources: dict[str, str], root_dir: Path | None, org_rep: UnifiedVisualOrgReport, findings: list[dict[str, Any]]) -> int:
    score = 25
    if LEGACY_REACTFLOW_IMPORT_RE.search(combined):
        score -= 10
        findings.append({"axis": 3, "severity": "WARN", "rule": "XYFLOW_MODERN_PACKAGE", "detail": "Legacy 'reactflow' import; use '@xyflow/react' (-10 pts)"})
    empty_fns = _count_non_context_empty_fns(combined)
    console_stubs = len(CONSOLE_ONLY_BODY_RE.findall(combined))
    if empty_fns > 0 or console_stubs > 0:
        score -= 15
        findings.append({"axis": 3, "severity": "CRITICAL", "rule": "AST_FAKE_FUNCTION_STUB", "detail": f"Detected {empty_fns} empty handlers and {console_stubs} console stubs (-15 pts)"})
    if FAKE_TELEMETRY_RANDOM_RE.search(combined):
        score -= 15
        findings.append({"axis": 3, "severity": "CRITICAL", "rule": "FAKE_TELEMETRY_MATH_RANDOM", "detail": "Simulated Math.random() telemetry (-15 pts)"})
    if org_rep.graph_node_violations:
        pen = min(15, len(org_rep.graph_node_violations) * 8)
        score -= pen
        findings.append({"axis": 3, "severity": "CRITICAL", "rule": "GRAPH_NODE_PLACEBO_OR_OVERSTUFFING", "detail": f"Graph node pollution/placebo (-{pen} pts)"})
    if EMPTY_CATCH_RE.search(combined):
        score -= 10
        findings.append({"axis": 3, "severity": "CRITICAL", "rule": "SWALLOWED_CATCH_BLOCK", "detail": "Empty catch {} block swallows errors (-10 pts)"})
    if FORWARD_REF_RE.search(combined):
        score -= 5
        findings.append({"axis": 3, "severity": "WARN", "rule": "REACT19_LEGACY_FORWARD_REF", "detail": "Legacy forwardRef detected; pass ref as prop in React 19 (-5 pts)"})
    if any(_ss_craft_guards.find_unsafe_html_sinks(Path(k), v) for k, v in sources.items()):
        score -= 15
        findings.append({"axis": 3, "severity": "CRITICAL", "rule": "UNSANITIZED_HTML_SINK", "detail": "Unsanitized HTML/eval sink detected (-15 pts)"})
    score -= _check_xyflow_and_path_hygiene(sources, findings)
    if oversized := [k for k, v in sources.items() if len(v.splitlines()) > 600]:
        score -= 10
        findings.append({"axis": 3, "severity": "CRITICAL", "rule": "CAP_600L_EXCEEDED", "detail": f"Files exceed 600 lines: {', '.join(oversized[:3])} (-10 pts)"})
    if root_dir is not None:
        resolved_root = root_dir.resolve()
        ref_paths = set(sources.keys()) | {m.group(1) for m in re.finditer(r"""(?:filePath|sourcePath|nodePath)\s*:\s*['"]([^'"]+\.(?:tsx|ts|jsx|js|py|go|css))['"]""", combined)}
        for rel_path in sorted(ref_paths):
            cand = (resolved_root / rel_path).resolve()
            if not cand.is_relative_to(resolved_root) or not cand.exists():
                score -= 15
                findings.append({"axis": 3, "severity": "CRITICAL", "rule": "GHOST_NODE_DISK_MISMATCH", "detail": f"Ghost node or path escape: {rel_path} (-15 pts)"})
    return max(0, score)


def _evaluate_axis_4(combined: str, live_url: str, findings: list[dict[str, Any]]) -> tuple[int, dict[str, Any]]:
    s4 = 25
    if SYNC_NEXT15_PARAMS_RE.search(combined) and not ASYNC_NEXT15_PARAMS_RE.search(combined):
        s4 -= 15
        findings.append({"axis": 4, "severity": "CRITICAL", "rule": "NEXTJS15_SYNC_PARAMS", "detail": "Legacy synchronous params access without Promise<{...}> (-15 pts)"})
    live_res: dict[str, Any] = {"executed": False}
    if live_url.strip():
        live_res = probe_live_url_metadata(live_url.strip())
        live_res["executed"] = True
        if not live_res.get("reachable"):
            s4 = max(0, s4 - 10)
            findings.append({"axis": 4, "severity": "WARN", "rule": "LIVE_URL_UNREACHABLE", "detail": f"Unreachable live URL ({live_url}): {live_res.get('error')}"})
    return s4, live_res


def _bridge_sga_score(root_dir: Path | None) -> dict[str, Any]:
    if root_dir is None or not root_dir.exists():
        return {"bridged": False}
    candidates = [
        SCRIPT_DIR.parent.parent / "system-project-auditor" / "scripts",
        SCRIPT_DIR.parents[2] / "franklin-skills" / "skills" / "system-project-auditor" / "scripts" if len(SCRIPT_DIR.parents) >= 3 else Path("."),
        Path.home() / ".gemini" / "config" / "plugins" / "franklin-skills" / "skills" / "system-project-auditor" / "scripts",
    ]
    nav_dir = next((c for c in candidates if (c / "deterministic_scorer.py").exists()), None)
    if nav_dir is None:
        return {"bridged": False}
    if str(nav_dir) not in sys.path:
        sys.path.insert(0, str(nav_dir))
    try:
        import deterministic_scorer as nav_scorer  # type: ignore

        ev, diag = nav_scorer.scan_project_tree(root_dir)
        rep = nav_scorer.calculate_architecture_score(ev, "COMPLEX_ZERO_FUSION")
        return {"bridged": True, "sga_global_score": rep.sga_global_score, "tif_verdict": rep.tif_verdict, "verdict": rep.verdict, "diagnostics": diag}
    except Exception as exc:  # noqa: BLE001
        return {"bridged": False, "error": str(exc)}


def audit_source_bundle(sources: dict[str, str], root_dir: Path | None = None, live_url: str = "") -> dict[str, Any]:
    """Compute deterministic 4-Axis score (0..100), hierarchy report, and optional SGA bridge."""
    combined = _ss_core.strip_comments("\n".join(sources.values()))
    has_css = any(k.endswith(".css") or "<style>" in v for k, v in sources.items())
    findings: list[dict[str, Any]] = []
    div_clicks = sum(len(_ss_guards.find_unsemantic_div_clicks(Path(k), v)) for k, v in sources.items())
    org_rep = analyze_visual_hierarchy_and_organization(combined)
    s1 = _evaluate_axis_1(combined, has_css, org_rep, findings, div_clicks=div_clicks)
    s2 = _evaluate_axis_2(combined, has_css, org_rep, findings)
    s3 = _evaluate_axis_3(combined, sources, root_dir, org_rep, findings)
    s4, live_res = _evaluate_axis_4(combined, live_url, findings)
    total = s1 + s2 + s3 + s4
    verdict = "[PASS]" if total >= 90 else ("[WARN]" if total >= 75 else "[FAIL]")
    return {
        "skill": "complex-zero", "version": "1.6.0", "verdict": verdict, "total_score": total,
        "axes": {"eixo_1_interatividade_fitts": s1, "eixo_2_macro_micro_oklch": s2, "eixo_3_xyflow_ast_antifake": s3, "eixo_4_nextjs15_async_params": s4},
        "visual_organization_and_hierarchy": asdict(org_rep),
        "nav_x_func_bridge": _bridge_sga_score(root_dir),
        "live_browser_probe": live_res,
        "chrome_devtools_mcp_protocol": {"mandatory_steps": ["1. navigate_page", "2. take_screenshot", "3. take_snapshot", "4. evaluate_script (--dump-cdp-script)"]},
        "files_analyzed": len(sources),
        "findings": findings,
    }


def _collect_target_files(target: Path) -> dict[str, str]:
    if target.is_file():
        files = _ss_core.collect_ui_files_scoped(target, limit=500)[0] or [target]
        root = target.parent
        return {
            (fp.relative_to(root).as_posix() if fp.is_relative_to(root) else fp.name): fp.read_text(encoding="utf-8", errors="replace")
            for fp in files
        }
    bundle: dict[str, str] = {}
    for fp in _ss_core.collect_ui_files_scoped(target, limit=500, include_tests=False)[0]:
        if fp.suffix.lower() in FRONTEND_EXTENSIONS:
            bundle[fp.relative_to(target).as_posix()] = fp.read_text(encoding="utf-8", errors="replace")
    for p in sorted(target.rglob("mcp_apps_ui_*.go")):
        if not p.is_file() or any(part in _ss_core.IGNORED_DIRS for part in p.parts):
            continue
        bundle[p.relative_to(target).as_posix()] = p.read_text(encoding="utf-8", errors="replace")
    return bundle


def run_self_test() -> int:
    """Validate healthy bundle (>=90) vs cramped/placebo bundle (<40)."""
    healthy = {
        "styles.css": ".card-wrapper{container-type:inline-size;} @container (min-width:380px){.card{background:oklch(0.22 0.02 260);font-variant-numeric:tabular-nums;}} .mode-switcher{display:flex;gap:10px;padding:8px;} .mode-btn{font-size:14px;min-block-size:44px;padding:10px 16px;} .btn:focus-visible{outline:2px solid oklch(0.68 0.17 237);} @media (any-pointer:coarse){.btn{min-width:48px;min-height:48px;}} @media (prefers-reduced-motion:reduce){.btn{transition:none;}}",
        "page.tsx": "import { ReactFlow } from '@xyflow/react'; export default async function Page({ params }: { params: Promise<{ slug: string }> }) { const { slug } = await params; return <main><nav aria-label='Main'><button className='mode-btn'>{slug}</button></nav></main>; }",
    }
    res_ok = audit_source_bundle(healthy)
    assert res_ok["verdict"] == "[PASS]" and res_ok["total_score"] == 100
    broken = {
        "bad.css": ".btn:focus{outline:none;} .mode-switcher{gap:4px;} .chip-btn{font-size:12px;padding:4px 8px;min-block-size:36px;} .sub{font-size:11px;}",
        "bad.tsx": "import ReactFlow from 'reactflow'; const f = () => {}; const m = { fps: Math.random(), oklchContrastValid: true }; export default function Page({ params }: { params: { slug: string } }) { return <div onClick={f}><nav style='gap:4px'><button style='font-size:11px'>A</button></nav><nav/><nav/><nav/><button role='tab' onClick={() => switchCanvasTab('1')}>T1</button><button onClick={() => switchNodesSubview('s')}>[DIR] [PASS]</button>{params.slug}</div>; }",
    }
    res_bad = audit_source_bundle(broken)
    assert res_bad["verdict"] == "[FAIL]" and res_bad["total_score"] < 40
    print(json.dumps({"status": "[PASS]", "healthy_score": res_ok["total_score"], "broken_score": res_bad["total_score"]}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified complex-zero 4-Axis AST & CDP Auditor")
    parser.add_argument("target", nargs="?", default=None, help="Target frontend file or workspace")
    parser.add_argument("--target", dest="target_flag", type=str, default=None, help="Explicit --target path")
    parser.add_argument("--live-url", type=str, default="")
    parser.add_argument("--dump-cdp-script", action="store_true")
    parser.add_argument("--json", action="store_true", help="Emit JSON output (default)")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.dump_cdp_script:
        print(CHROME_DEVTOOLS_EVALUATE_SCRIPT)
        return 0
    if args.self_test:
        return run_self_test()
    if not (args.target or args.target_flag):
        print(json.dumps({"error": "Provide <target>, --target <path>, --dump-cdp-script, or --self-test"}))
        return 1
    target_path = _ss_core.resolve_cli_target(args.target, args.target_flag)
    if not target_path.exists():
        print(json.dumps({"error": f"Target not found: {target_path}"}))
        return 1
    report = audit_source_bundle(_collect_target_files(target_path), root_dir=(target_path if target_path.is_dir() else target_path.parent), live_url=args.live_url)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["total_score"] >= 75 else 1


if __name__ == "__main__":
    raise SystemExit(main())
