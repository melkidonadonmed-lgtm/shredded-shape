#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Deterministic 4-Pillar Tactile Architecture, 3-Layer OKLCH Tokens, Shadow & FSM Auditor."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_HERE = Path(__file__).resolve().parent
for _cand in (*(p / "scripts" for p in _HERE.parents if (p / "pyproject.toml").is_file()), _HERE, *(p / "scripts" for p in _HERE.parents)):
    if (_cand / "_ss_core.py").is_file() and str(_cand) not in sys.path:
        sys.path.insert(0, str(_cand))
        break

import _ss_core

GAMED_FSM_COMMENT_RE = re.compile(
    r"//\s*(?:empty|idle)\s*\|\s*loading\s*\|\s*(?:success|pressed)\s*\|\s*error",
    re.IGNORECASE,
)

EXECUTABLE_FSM_PATTERNS = (
    re.compile(r"data-state\s*="),
    re.compile(r"data-theme\s*="),
    re.compile(r"data-variant\s*="),
    re.compile(r"aria-busy\s*="),
    re.compile(r"aria-pressed\s*="),
    re.compile(r"aria-selected\s*="),
    re.compile(r"aria-current\s*="),
    re.compile(r'role\s*=\s*["\'](?:status|alert|tab|list)["\']'),
    re.compile(r"useState\s*<[^>]*?(?:idle|loading|error|pressed|UIState|ComponentFSMState)"),
    re.compile(r"['\"](?:idle|loading|error|pressed)['\"]"),
)

REQUIRED_ATOMIC_DIRS = (
    "src/components/ui",
    "src/components/bento",
    "src/components/layout",
    "src/config",
    "src/styles",
    "src/types",
)

SEMANTIC_TOKEN_FAMILIES: tuple[tuple[str, ...], ...] = (
    ("--surface-canvas", "--surface-card", "--ink-primary"),
    ("--surface-canvas", "--surface-sunken", "--surface-card"),
    ("--surface-canvas", "--surface-card", "--text-primary"),
    ("--bg-canvas", "--bg-card", "--ink-primary"),
    ("--bg-canvas", "--bg-card", "--text-primary"),
    ("--bg-well", "--bg-canvas", "--bg-card"),
    ("--bg-canvas", "--bg-surface-1", "--text-primary"),
    ("--bg-canvas", "--bg-surface-1", "--bg-surface-2"),
    ("--bg-canvas", "--bg-surface", "--ink-primary"),
    ("--surface-canvas", "--surface-primary", "--ink-primary"),
    ("--surface-canvas", "--surface-raised", "--text-primary"),
    ("--color-surface-canvas", "--color-surface-card", "--color-ink-primary"),
)

ELEVATION_MARKERS = (
    "--shadow-elevation-1", "--shadow-elevation-2", "--shadow-elevation-3",
    "--shadow-elevation-low", "--shadow-elevation-medium", "--shadow-elevation-high",
    "--shadow-layer-sm", "--shadow-layer-md", "--shadow-layer-lg",
    "--shadow-inset", "--shadow-inset-sunken", "--shadow-clean-card",
    "--shadow-well", "--shadow-key", "--light-zenith", "--rim-top",
    "--elevation-1", "--elevation-2", "--elevation-3", "--elevation-low",
    "--elevation-medium", "--elevation-high", "--elevation-pressed-inset",
    "--catch-light", "--shadow-sculpted", "--rim-light", "--shadow-card",
    "--shadow-1", "shadow-elevation-1", "shadow-elevation-2", "shadow-elevation-3",
    "sculpted-card", "card-interactive", "ui-card-soft",
    "bento-card", "inset 0 1px 0", "inset 0px 1px 0px",
)


@dataclass
class AuditFinding:
    """Single tactile readiness audit finding."""

    rule_id: str
    severity: str
    file: str
    message: str


def strip_comments(source: str) -> str:
    """Strip CSS/JS/HTML comments safely without corrupting URLs."""
    return _ss_core.strip_comments(source)


def collect_frontend_files(target: Path) -> list[Path]:
    """Collect frontend source and stylesheet files while skipping test suites, .venv, and node_modules."""
    files, _, _ = _ss_core.collect_ui_files_scoped(target, limit=500, include_tests=False)
    return files


def _check_orphan_cards(files: list[Path], findings: list[AuditFinding]) -> float:
    penalty = 0.0
    for comp_name in ("SoftCard", "SurfaceCard"):
        comp_defs = [f for f in files if f.name == f"{comp_name}.tsx"]
        consumers = [
            f for f in files
            if f.name != f"{comp_name}.tsx"
            and f.suffix.lower() in {".tsx", ".jsx"}
            and comp_name in f.read_text(encoding="utf-8", errors="ignore")
        ]
        if comp_defs and not consumers:
            penalty += 25.0
            findings.append(AuditFinding("AUDIT-VIS-01", "CRITICAL", comp_defs[0].name, f"Component <{comp_name} /> is orphan (never imported)."))
    return penalty


def _audit_tokens_and_layers(combined_stripped: str, files: list[Path], findings: list[AuditFinding]) -> float:
    """Audit 3-layer semantic tokens, elevation markers, orphan cards, and anti-slop defects."""
    s_tokens = 100.0
    if not any(all(tok in combined_stripped for tok in fam) for fam in SEMANTIC_TOKEN_FAMILIES):
        s_tokens -= 20.0
        findings.append(AuditFinding("AUDIT-VIS-01", "MEDIUM", "global", "Missing 3-layer semantic tokens (--surface-canvas/--surface-card/--ink-primary)."))
    if not any(m in combined_stripped for m in ELEVATION_MARKERS):
        s_tokens -= 15.0
        findings.append(AuditFinding("AUDIT-VIS-01", "MEDIUM", "global", "Missing multi-layer elevation tokens (--shadow-elevation-1..3 / --catch-light)."))
    s_tokens -= _check_orphan_cards(files, findings)
    slop_checks = (
        (_ss_core.NEON_GLOW_RE.search(combined_stripped), "OPTICS-NEON-GLOW", "Omnidirectional neon glow detected."),
        (_ss_core.SLOP_BLOB_RE.search(combined_stripped), "ANTI-SLOP-BLOB", "Decorative blur blob or organic bloop detected."),
        (_ss_core.SLOP_TOKEN_RE.search(combined_stripped), "ANTI-SLOP-TOKEN", "Cosmetic neon/violet slop token or gradient detected."),
        (_ss_core.DASHED_BOX_SLOP_RE.search(combined_stripped), "ANTI-SLOP-WIREFRAME", "Dashed wireframe border detected; use recessed wells or 1px subtle hairlines."),
        (_ss_core.has_confetti_badge_slop(combined_stripped), "ANTI-SLOP-CONFETTI", ">=3 multicolored pill/badge variants detected; use neutral .engraved-pill + 6px .lum-bead."),
        (bool(_ss_core.inspect_inline_svgs(combined_stripped)), "AUDIT-VIS-BAD-SVG", "Empty, unboxed, or bloop-cloud inline <svg> detected."),
    )
    for hit, rule_id, msg in slop_checks:
        if hit:
            s_tokens -= 20.0
            findings.append(AuditFinding(rule_id, "HIGH", "global", msg))
    return max(0.0, s_tokens)


def _audit_fsm(combined_raw: str, combined_stripped: str, findings: list[AuditFinding]) -> float:
    """Audit executable 5-state finite state machine coverage (S_FSM)."""
    s_fsm = 100.0
    if GAMED_FSM_COMMENT_RE.search(combined_raw):
        s_fsm -= 25.0
        findings.append(AuditFinding("AUDIT-STATE-01", "HIGH", "global", "Comment-gaming detected simulating FSM states."))
    matched_fsm = sum(1 for pat in EXECUTABLE_FSM_PATTERNS if pat.search(combined_stripped))
    if matched_fsm == 0:
        s_fsm -= 40.0
        findings.append(AuditFinding("AUDIT-STATE-01", "CRITICAL", "global", "No executable FSM state attributes (data-state, aria-busy, role=alert) found."))
    elif matched_fsm < 2:
        s_fsm -= 15.0
    return max(0.0, s_fsm)


def _audit_a11y(combined_stripped: str, findings: list[AuditFinding]) -> float:
    """Audit WAI-ARIA attributes, keyboard focus visibility, tabular-nums, and reduced motion."""
    s_a11y = 100.0
    if "aria-" not in combined_stripped and "role=" not in combined_stripped:
        s_a11y -= 30.0
        findings.append(AuditFinding("AUDIT-A11Y-01", "HIGH", "global", "Missing WAI-ARIA attributes or landmark roles."))
    if not any(k in combined_stripped for k in (":focus-visible", ":focus-within")):
        s_a11y -= 15.0
        findings.append(AuditFinding("AUDIT-A11Y-02", "MEDIUM", "global", "Missing :focus-visible or :focus-within keyboard focus ring."))
    if "tabular-nums" not in combined_stripped:
        s_a11y -= 10.0
        findings.append(AuditFinding("AUDIT-A11Y-02", "LOW", "global", "Missing font-variant-numeric: tabular-nums alignment."))
    if "prefers-reduced-motion" not in combined_stripped:
        s_a11y -= 10.0
        findings.append(AuditFinding("AUDIT-A11Y-02", "LOW", "global", "Missing @media (prefers-reduced-motion: reduce) safeguard."))
    if re.search(r"transition\s*:[^;}{]*\ballow-discrete\b", combined_stripped, re.IGNORECASE):
        s_a11y -= 5.0
        findings.append(AuditFinding("AUDIT-A11Y-02", "LOW", "global", "Declare transition-behavior: allow-discrete as a standalone property after transition."))
    return max(0.0, s_a11y)


def _audit_security(files: list[Path], target_path: Path, findings: list[AuditFinding]) -> float:
    """Audit XSS sinks and unsafe eval() usage."""
    s_sec = 100.0
    for fpath in files:
        stripped = strip_comments(fpath.read_text(encoding="utf-8", errors="ignore"))
        rel = str(fpath.relative_to(target_path)) if target_path.is_dir() and fpath.is_relative_to(target_path) else fpath.name
        is_safe_theme_fouc = "localStorage.getItem" in stripped and "setAttribute('data-theme'" in stripped.replace('"', "'")
        if "dangerouslySetInnerHTML" in stripped and "DOMPurify" not in stripped and not is_safe_theme_fouc:
            s_sec -= 40.0
            findings.append(AuditFinding("AUDIT-SEC-01", "CRITICAL", rel, "dangerouslySetInnerHTML used without DOMPurify sanitization."))
        if re.search(r"\beval\s*\(", stripped):
            s_sec -= 40.0
            findings.append(AuditFinding("AUDIT-SEC-01", "CRITICAL", rel, "Unsafe eval() call detected."))
    return max(0.0, s_sec)


def run_audit(target_path: Path) -> dict[str, Any]:
    """Run deterministic 4-Pillar Tactile UI, Token, A11y, Security & FSM audit."""
    files = collect_frontend_files(target_path)
    findings: list[AuditFinding] = []
    is_tier2_or_3 = target_path.is_dir() and ((target_path / "src" / "features").exists() or (target_path / "src" / "app").exists())
    missing_dirs = (
        [] if is_tier2_or_3 else [
            d for d in REQUIRED_ATOMIC_DIRS
            if target_path.is_dir() and (target_path / "src").exists() and not (target_path / d).exists()
        ]
    )
    if not files:
        return {
            "target_path": str(target_path), "files_scanned": 0, "s_a11y": 0.0, "s_fsm": 0.0,
            "s_tokens": 0.0, "s_sec": 100.0, "readiness_score": 15.0,
            "scores": {"readiness_score": 15.0, "s_a11y": 0.0, "s_fsm": 0.0, "s_tokens": 0.0, "s_sec": 100.0},
            "verdict": "UNVERIFIED", "missing_atomic_dirs": missing_dirs, "findings": [],
        }

    combined_raw = "\n".join(f.read_text(encoding="utf-8", errors="ignore") for f in files)
    combined_stripped = strip_comments(combined_raw)
    s_tokens = round(_audit_tokens_and_layers(combined_stripped, files, findings), 2)
    s_fsm = round(_audit_fsm(combined_raw, combined_stripped, findings), 2)
    s_a11y = round(_audit_a11y(combined_stripped, findings), 2)
    s_sec = round(_audit_security(files, target_path, findings), 2)
    readiness = round((0.35 * s_a11y) + (0.30 * s_fsm) + (0.20 * s_tokens) + (0.15 * s_sec), 2)
    verdict = "PASS" if (readiness >= 90.0 and s_tokens >= 85.0 and s_fsm >= 85.0) else "FAIL"
    return {
        "target_path": str(target_path), "files_scanned": len(files),
        "s_a11y": s_a11y, "s_fsm": s_fsm, "s_tokens": s_tokens, "s_sec": s_sec,
        "readiness_score": readiness,
        "scores": {"readiness_score": readiness, "s_a11y": s_a11y, "s_fsm": s_fsm, "s_tokens": s_tokens, "s_sec": s_sec},
        "verdict": verdict, "missing_atomic_dirs": missing_dirs, "findings": [asdict(f) for f in findings],
    }


def _run_self_test() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        sample = Path(tmp) / "tactile_demo.html"
        sample.write_text(
            "<!DOCTYPE html><html lang='en'><style>"
            ":root{--bg-well:oklch(0.118 0.012 260);--bg-canvas:oklch(0.145 0.014 260);"
            "--bg-card:oklch(0.195 0.018 262);--ink-primary:oklch(0.955 0.008 255);"
            "--light-zenith:radial-gradient(120% 90% at 50% 0%, oklch(1 0 0 / 0.065), transparent);}"
            ".card{font-variant-numeric:tabular-nums;background:var(--bg-card);}"
            ".btn:focus-visible{outline:2px solid currentColor;}"
            "@media (prefers-reduced-motion:reduce){*{transition:none;}}"
            "</style><main><button type='button' aria-pressed='false' data-state='idle' class='btn'>Sync</button></main></html>",
            encoding="utf-8",
        )
        rep = run_audit(sample)
        assert rep["verdict"] == "PASS" and rep["readiness_score"] >= 90.0
    print(json.dumps({"self_test": "AUDIT_TACTILE_UI_OK"}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic 4-Pillar Tactile UI, OKLCH & FSM Auditor")
    parser.add_argument("target", nargs="?", default=None, help="Frontend directory or file path")
    parser.add_argument("--target", dest="target_flag", default=None, help="Alias --target for frontend path")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--self-test", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    target = _ss_core.resolve_cli_target(args.target, args.target_flag)
    if not target.exists():
        print(f"Error: target not found: {target}", file=sys.stderr)
        return 2
    report = run_audit(target)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"=== FRONTEND VISUAL ARCHITECTURE & FSM AUDIT: {report['verdict']} ===")
        print(f"Target: {report['target_path']} ({report['files_scanned']} files)")
        print(f"Readiness: {report['readiness_score']}/100.0 [A11y:{report['s_a11y']} FSM:{report['s_fsm']} Tokens:{report['s_tokens']} Sec:{report['s_sec']}]")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
