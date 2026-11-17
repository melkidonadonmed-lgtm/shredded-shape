#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.7.0"]
# ///
"""Physical Read-After-Write (RAW) SHA-256 and TypeScript verifier for ui-clean-worker."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_HERE = Path(__file__).resolve().parent
for _cand in (*(p / "scripts" for p in _HERE.parents if (p / "pyproject.toml").is_file()), _HERE, *(p / "scripts" for p in _HERE.parents)):
    if (_cand / "_ss_core.py").is_file() and str(_cand) not in sys.path:
        sys.path.insert(0, str(_cand))
        break

import _ss_core

STUB_RE = re.compile(r"alert\(['\"]coming soon|onClick=\{\(\)\s*=>\s*\{\s*\}\}|TODO:\s*implement|setTimeout\(\s*\(\)\s*=>\s*(?:\{\s*\}|[^)]*\b(?:mock|fake|dummy)\b)", re.IGNORECASE)
FORWARD_REF_RE = re.compile(r"\bforwardRef\s*(?:<|\()")
UNSAFE_HTML_RE = re.compile(r"dangerouslySetInnerHTML\s*=")


class RAWFileCheck(BaseModel):
    """Per-file Read-After-Write check result."""

    model_config = ConfigDict(extra="forbid")
    file_path: str
    size_bytes: int
    sha256: str
    passed: bool
    issues: list[str]


class RAWVerificationResult(BaseModel):
    """Strict verification payload emitted by ui-clean-worker after disk writes."""

    model_config = ConfigDict(extra="forbid")
    verdict: Literal["[PASS]", "[RAW-VIOLATION]", "[TYPE-ERROR]"]
    files_checked: list[RAWFileCheck]
    tsc_ran: bool
    tsc_passed: bool
    summary: str


def _check_single_file(fp: Path, min_bytes: int) -> RAWFileCheck:
    raw = fp.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    issues: list[str] = []
    if len(raw) < min_bytes:
        issues.append(f"[RAW-VIOLATION] Truncated file ({len(raw)} bytes < {min_bytes})")
    decoded = raw.decode("utf-8", errors="ignore")
    if len(decoded.splitlines()) > 600:
        issues.append("[CAP-600L] UI module exceeds 600-line ceiling; decompose by domain")
    stripped = _ss_core.strip_comments(decoded)
    checks = (
        (STUB_RE, "[STUB] Placeholder alert/empty handler detected"),
        (_ss_core.PURE_BLACK_RE, "[OPTICS] Pure #000000 black violates OLED Dark Mode elevation"),
        (_ss_core.EMOJI_RE, "[ANTI-SLOP] Unicode UI emoji detected"),
        (FORWARD_REF_RE, "[REACT-19] Legacy forwardRef detected; pass ref directly as a prop"),
        (_ss_core.ROW_REVERSE_RE, "[A11Y-TAB] row-reverse or CSS order breaks DOM == Tab focus order"),
        (_ss_core.FLAT_SHADOW_RE, "[OPTICS] Flat single-pass rgba(0,0,0) shadow detected"),
        (_ss_core.NEON_GLOW_RE, "[OPTICS-NEON-GLOW] Omnidirectional neon glow shadow detected"),
        (_ss_core.SLOP_BLOB_RE, "[ANTI-SLOP-BLOB] Decorative blur orb or organic bloop detected"),
        (_ss_core.SLOP_TOKEN_RE, "[ANTI-SLOP-TOKEN] Cosmetic neon or violet AI-slop token detected"),
        (_ss_core.DASHED_BOX_SLOP_RE, "[ANTI-SLOP-WIREFRAME] Dashed wireframe layout border detected"),
        (_ss_core.REFLOW_TRANSITION_RE, "[PERF-REFLOW] Layout-thrashing transition property (use transform/opacity)"),
        (_ss_core.GRAIN_ABOVE_TEXT_RE, "[OPTICS-GRAIN-ABOVE-TEXT] feTurbulence overlay missing z-index: -1"),
        (_ss_core.SHADOWED_FONT_STACK_RE, "[TYP-DEAD-FONT-FALLBACK] Named font placed after generic family"),
    )
    for pattern, msg in checks:
        if pattern.search(stripped):
            issues.append(msg)
    is_fouc = "localStorage.getItem" in stripped and "setAttribute('data-theme'" in stripped.replace('"', "'")
    if UNSAFE_HTML_RE.search(stripped) and "DOMPurify" not in stripped and not is_fouc:
        issues.append("[AUDIT-SEC-01] dangerouslySetInnerHTML used without DOMPurify.sanitize()")
    for msg in _ss_core.find_neon_violations(stripped):
        issues.append(f"[OPTICS-NO-NEON] {msg}")
    for msg in _ss_core.inspect_inline_svgs(stripped):
        issues.append(f"[AUDIT-VIS-BAD-SVG] {msg}")
    return RAWFileCheck(file_path=str(fp), size_bytes=len(raw), sha256=digest, passed=not issues, issues=issues)


def _maybe_run_tsc(target: Path, run_tsc: bool) -> tuple[bool, bool, str]:
    if not run_tsc:
        return False, True, ""
    project_dir = target if target.is_dir() else target.parent
    while project_dir != project_dir.parent and not (project_dir / "tsconfig.json").is_file():
        project_dir = project_dir.parent
    if not (project_dir / "tsconfig.json").is_file():
        return True, False, "tsconfig.json not found when --run-tsc was explicitly requested"
    cmd = ["npx.cmd" if sys.platform == "win32" else "npx", "tsc", "--noEmit"]
    try:
        proc = subprocess.run(cmd, check=False, cwd=str(project_dir), capture_output=True, text=True, timeout=60, encoding="utf-8", errors="replace")
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return True, False, f"tsc failed/unavailable: {exc}"
    return True, proc.returncode == 0, (proc.stderr or proc.stdout).strip()[:400]


def verify_raw_frontend(target_path: Path, min_bytes: int = 100, run_tsc: bool = False) -> RAWVerificationResult:
    """Verify physical existence, min bytes, SHA-256, anti-stub hygiene, and optional tsc."""
    if not target_path.exists():
        missing = RAWFileCheck(file_path=str(target_path), size_bytes=0, sha256="", passed=False, issues=["[RAW-VIOLATION] Target path does not exist"])
        return RAWVerificationResult(verdict="[RAW-VIOLATION]", files_checked=[missing], tsc_ran=False, tsc_passed=True, summary="Missing target file")

    files = _ss_core.collect_ui_files(target_path, limit=200)
    if not files:
        empty = RAWFileCheck(file_path=str(target_path), size_bytes=0, sha256="", passed=False, issues=["[RAW-VIOLATION] No eligible UI files found"])
        return RAWVerificationResult(verdict="[RAW-VIOLATION]", files_checked=[empty], tsc_ran=False, tsc_passed=True, summary="No eligible UI files")

    checks = [_check_single_file(fp, min_bytes) for fp in files]
    bundle_stripped = "\n".join(_ss_core.strip_comments(fp.read_text(encoding="utf-8", errors="ignore")) for fp in files)
    if _ss_core.has_confetti_badge_slop(bundle_stripped):
        checks[0].issues.append("[ANTI-SLOP-CONFETTI] >=3 multicolored pill/badge variants detected; use neutral .engraved-pill + .lum-bead")
        checks[0].passed = False
    tsc_ran, tsc_ok, tsc_err = _maybe_run_tsc(target_path, run_tsc)
    all_ok = all(c.passed for c in checks) and tsc_ok
    verdict: Literal["[PASS]", "[RAW-VIOLATION]", "[TYPE-ERROR]"] = "[PASS]" if all_ok else ("[TYPE-ERROR]" if not tsc_ok else "[RAW-VIOLATION]")
    summary = f"Verified {len(checks)} file(s); tsc_ok={tsc_ok}" + (f" ({tsc_err})" if tsc_err else "")
    return RAWVerificationResult(verdict=verdict, files_checked=checks, tsc_ran=tsc_ran, tsc_passed=tsc_ok, summary=summary)


def _run_self_test() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        good = Path(tmp) / "Card.tsx"
        good.write_text("export function Card({ label }: { label: string }) { return <article className='p-4'>{label}</article>; }\n", encoding="utf-8")
        res = verify_raw_frontend(good, min_bytes=40)
        assert res.verdict == "[PASS]" and len(res.files_checked[0].sha256) == 64
        missing = verify_raw_frontend(Path(tmp) / "missing.tsx")
        assert missing.verdict == "[RAW-VIOLATION]"
    print(json.dumps({"self_test": "VERIFY_RAW_FRONTEND_OK"}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Read-After-Write SHA-256 and TypeScript for UI artifacts")
    parser.add_argument("target", nargs="?", default=None, help="Target frontend file or directory")
    parser.add_argument("--target", dest="target_flag", default=None, help="Explicit --target path")
    parser.add_argument("--min-bytes", type=int, default=100)
    parser.add_argument("--run-tsc", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    resolved = _ss_core.resolve_cli_target(args.target, args.target_flag)
    res = verify_raw_frontend(resolved, min_bytes=args.min_bytes, run_tsc=args.run_tsc)
    print(res.model_dump_json(indent=2) if args.json else f"{res.verdict} {res.summary}")
    return 0 if res.verdict == "[PASS]" else 1


if __name__ == "__main__":
    raise SystemExit(main())
