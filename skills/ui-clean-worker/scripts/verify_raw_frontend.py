#!/usr/bin/env python3
"""Physical Read-After-Write (RAW) SHA-256 and TypeScript verifier for ui-clean-worker."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Literal

from pydantic import BaseModel, ConfigDict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

UI_EXTS = {".tsx", ".jsx", ".ts", ".css", ".scss", ".html", ".vue"}
STUB_RE = re.compile(r"alert\(['\"]coming soon|onClick=\{\(\)\s*=>\s*\{\s*\}\}|TODO:\s*implement", re.IGNORECASE)
PURE_BLACK_RE = re.compile(r"(?:color|background(?:-color)?|fill|stroke|shadow|border|--[a-zA-Z0-9_-]+)\s*:[^;\n{}]*?(?:#000000\b|#000(?![0-9a-fA-F])|oklch\(\s*0(?:\.0+)?\s+0(?:\.0+)?\s+0\s*\))")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")


class RAWFileCheck(BaseModel):
    """Per-file Read-After-Write check result."""

    model_config = ConfigDict(extra="forbid")
    file_path: str
    size_bytes: int
    sha256: str
    passed: bool
    issues: List[str]


class RAWVerificationResult(BaseModel):
    """Strict verification payload emitted by ui-clean-worker after disk writes."""

    model_config = ConfigDict(extra="forbid")
    verdict: Literal["[PASS]", "[RAW-VIOLATION]", "[TYPE-ERROR]"]
    files_checked: List[RAWFileCheck]
    tsc_ran: bool
    tsc_passed: bool
    summary: str


def _collect_ui_files(target: Path) -> List[Path]:
    if target.is_file():
        return [target]
    if not target.is_dir():
        return []
    skip = {"node_modules", ".git", "dist", "build", ".next"}
    return [
        p for p in sorted(target.rglob("*"))
        if p.is_file() and p.suffix.lower() in UI_EXTS and not any(s in skip for s in p.parts)
    ][:200]


def _check_single_file(fp: Path, min_bytes: int) -> RAWFileCheck:
    raw = fp.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    issues: List[str] = []
    if len(raw) < min_bytes:
        issues.append(f"[RAW-VIOLATION] Truncated file ({len(raw)} bytes < {min_bytes})")
    text = raw.decode("utf-8", errors="ignore")
    if STUB_RE.search(text):
        issues.append("[STUB] Placeholder alert/empty handler detected")
    if PURE_BLACK_RE.search(text):
        issues.append("[OPTICS] Pure #000000 black violates OLED Dark Mode elevation")
    if EMOJI_RE.search(text):
        issues.append("[ANTI-SLOP] Unicode UI emoji detected")
    return RAWFileCheck(
        file_path=str(fp), size_bytes=len(raw), sha256=digest,
        passed=not issues, issues=issues,
    )


def _maybe_run_tsc(target: Path, run_tsc: bool) -> tuple[bool, bool, str]:
    if not run_tsc:
        return False, True, ""
    project_dir = target if target.is_dir() else target.parent
    while project_dir != project_dir.parent and not (project_dir / "tsconfig.json").is_file():
        project_dir = project_dir.parent
    if not (project_dir / "tsconfig.json").is_file():
        return False, True, ""
    cmd = ["npx.cmd" if sys.platform == "win32" else "npx", "tsc", "--noEmit"]
    proc = subprocess.run(cmd, cwd=str(project_dir), capture_output=True, text=True, timeout=60, encoding="utf-8", errors="replace")
    return True, proc.returncode == 0, (proc.stderr or proc.stdout).strip()[:400]


def verify_raw_frontend(target_path: Path, min_bytes: int = 100, run_tsc: bool = False) -> RAWVerificationResult:
    """Verify physical existence, min bytes, SHA-256, anti-stub hygiene, and optional tsc."""
    if not target_path.exists():
        missing = RAWFileCheck(file_path=str(target_path), size_bytes=0, sha256="", passed=False, issues=["[RAW-VIOLATION] Target path does not exist"])
        return RAWVerificationResult(verdict="[RAW-VIOLATION]", files_checked=[missing], tsc_ran=False, tsc_passed=True, summary="Missing target file")

    files = _collect_ui_files(target_path)
    if not files:
        empty = RAWFileCheck(file_path=str(target_path), size_bytes=0, sha256="", passed=False, issues=["[RAW-VIOLATION] No eligible UI files found"])
        return RAWVerificationResult(verdict="[RAW-VIOLATION]", files_checked=[empty], tsc_ran=False, tsc_passed=True, summary="No eligible UI files")

    checks = [_check_single_file(fp, min_bytes) for fp in files]
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
    parser.add_argument("--target", default=".")
    parser.add_argument("--min-bytes", type=int, default=100)
    parser.add_argument("--run-tsc", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    res = verify_raw_frontend(Path(args.target).resolve(), min_bytes=args.min_bytes, run_tsc=args.run_tsc)
    print(res.model_dump_json(indent=2) if args.json else f"{res.verdict} {res.summary}")
    return 0 if res.verdict == "[PASS]" else 1


if __name__ == "__main__":
    raise SystemExit(main())
