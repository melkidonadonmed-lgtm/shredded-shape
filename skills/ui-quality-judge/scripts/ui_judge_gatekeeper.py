#!/usr/bin/env python3
"""Read-only Actor-Critic UI/UX & WCAG 2.2 OKLCH Gatekeeper (FNR < 0.001)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Literal, Tuple

from pydantic import BaseModel, ConfigDict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

UI_EXTS = {".html", ".css", ".scss", ".tsx", ".jsx", ".ts", ".vue"}
IGNORE_DIRS = {"node_modules", ".git", "dist", "build", ".next"}

PURE_BLACK_RE = re.compile(r"(?:color|background(?:-color)?|fill|stroke|shadow|border|--[a-zA-Z0-9_-]+)\s*:[^;\n{}]*?(?:#000000\b|#000(?![0-9a-fA-F])|oklch\(\s*0(?:\.0+)?\s+0(?:\.0+)?\s+0\s*\))")
NEON_OKLCH_RE = re.compile(r"oklch\(\s*([0-9.]+)\s+([0-9.]+)\s+[0-9.]+")
LIGHT_DARK_OKLCH_RE = re.compile(r"light-dark\(\s*oklch\(\s*([0-9.]+)[^)]+\)\s*,\s*oklch\(\s*([0-9.]+)[^)]+\)")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")
BASE64_BLOAT_RE = re.compile(r"data:image/[a-zA-Z0-9+.-]+;base64,[A-Za-z0-9+/=]{68000,}")
UNSAFE_HTML_RE = re.compile(r"dangerouslySetInnerHTML\s*=")
ROW_REVERSE_RE = re.compile(r"flex-direction\s*:\s*row-reverse|\border\s*:\s*-?\d+\s*;")
OUTLINE_NONE_RE = re.compile(r"outline\s*:\s*(?:none|0)\b")
FLAT_SHADOW_RE = re.compile(r"box-shadow\s*:\s*0\s+\d+px\s+\d+px\s+rgba?\(0\s*,\s*0\s*,\s*0")
HEX_PAIR_RE = re.compile(r"color\s*:\s*(#[0-9a-fA-F]{6})\s*;[^}]*?background(?:-color)?\s*:\s*(#[0-9a-fA-F]{6})")


class JudgeFinding(BaseModel):
    """Single deterministic violation or observation emitted by ui-judge."""

    model_config = ConfigDict(extra="forbid")
    rule_id: str
    severity: Literal["CRITICAL", "WARNING"]
    epistemic_type: Literal["[OBSERVED FACT]", "[TECHNICAL INFERENCE]"]
    file: str
    message: str


class UIJudgeReport(BaseModel):
    """Actor-Critic Gatekeeper output contract."""

    model_config = ConfigDict(extra="forbid")
    verdict: Literal["PASSED", "REJECTED", "UNVERIFIED"]
    wcag_level: Literal["AA", "AAA"]
    min_contrast_required: float
    contrast_ratio_min: float
    files_audited: int
    sha256_hashes: Dict[str, str]
    findings: List[JudgeFinding]


def oklch_to_relative_luminance(l_val: float) -> float:
    """Convert perceptual OKLCH lightness L in [0, 1] to relative CIE Y luminance."""
    clamped = max(0.0, min(1.0, l_val))
    if clamped <= 0.08:
        return (clamped / 0.08) * 0.01
    return ((clamped + 0.16) / 1.16) ** 3


def calculate_oklch_contrast(l_fg: float, l_bg: float) -> float:
    """Compute WCAG 2.2 contrast ratio from two OKLCH lightness values."""
    y1 = oklch_to_relative_luminance(l_fg)
    y2 = oklch_to_relative_luminance(l_bg)
    return round((max(y1, y2) + 0.05) / (min(y1, y2) + 0.05), 2)


def hex_contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    """Compute exact WCAG 2.2 contrast ratio for two #RRGGBB colors."""
    def _lum(hx: str) -> float:
        vals = [int(hx[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
        lin = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in vals]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]

    y1, y2 = _lum(fg_hex), _lum(bg_hex)
    return round((max(y1, y2) + 0.05) / (min(y1, y2) + 0.05), 2)


def _check_contrast(text: str, rel: str, min_cr: float, findings: List[JudgeFinding]) -> float:
    observed_min = 21.0
    for fg_hx, bg_hx in HEX_PAIR_RE.findall(text):
        cr = hex_contrast_ratio(fg_hx, bg_hx)
        observed_min = min(observed_min, cr)
        if cr < min_cr:
            findings.append(JudgeFinding(
                rule_id="WCAG-1.4.3", severity="CRITICAL", epistemic_type="[OBSERVED FACT]",
                file=rel, message=f"Contrast {cr}:1 ({fg_hx} on {bg_hx}) below {min_cr}:1",
            ))
    tokens = {m.group(1): (float(m.group(2)), float(m.group(3))) for m in re.finditer(r"(--(?:ink|text)-primary|--surface-(?:canvas|card)|--bg-(?:canvas|surface-1))\s*:\s*light-dark\(\s*oklch\(\s*([0-9.]+)[^)]+\)\s*,\s*oklch\(\s*([0-9.]+)[^)]+\)", text)}
    ink = tokens.get("--ink-primary") or tokens.get("--text-primary")
    bg = tokens.get("--surface-card") or tokens.get("--surface-canvas") or tokens.get("--bg-canvas")
    if ink and bg:
        for mode, idx in (("light", 0), ("dark", 1)):
            cr = calculate_oklch_contrast(ink[idx], bg[idx])
            observed_min = min(observed_min, cr)
            if cr < min_cr:
                findings.append(JudgeFinding(
                    rule_id="WCAG-1.4.3-OKLCH", severity="CRITICAL", epistemic_type="[OBSERVED FACT]",
                    file=rel, message=f"OKLCH {mode} contrast {cr}:1 below {min_cr}:1",
                ))
    return observed_min


def _check_pattern_rules(text: str, rel: str, findings: List[JudgeFinding]) -> None:
    rules: tuple[tuple[re.Pattern[str], str, Literal["CRITICAL", "WARNING"], Literal["[OBSERVED FACT]", "[TECHNICAL INFERENCE]"], str], ...] = (
        (PURE_BLACK_RE, "OPTICS-NO-BLACK", "CRITICAL", "[OBSERVED FACT]", "Pure #000000 black violates Dark Mode elevation"),
        (EMOJI_RE, "AUDIT-VIS-EMOJI", "CRITICAL", "[OBSERVED FACT]", "Unicode UI emoji detected; use crisp vector SVGs"),
        (BASE64_BLOAT_RE, "AUDIT-VIS-BLOAT", "CRITICAL", "[OBSERVED FACT]", "Base64 inline image exceeds 50KB budget"),
        (ROW_REVERSE_RE, "WCAG-1.3.2", "CRITICAL", "[OBSERVED FACT]", "row-reverse or CSS order breaks DOM == Tab focus sequence"),
        (FLAT_SHADOW_RE, "LOCK-02-SHADOWS", "WARNING", "[OBSERVED FACT]", "Single-pass rgba(0,0,0) shadow detected"),
    )
    for pattern, rule_id, severity, ep_type, msg in rules:
        if pattern.search(text):
            findings.append(JudgeFinding(rule_id=rule_id, severity=severity, epistemic_type=ep_type, file=rel, message=msg))


def _check_static_rules(text: str, rel: str, findings: List[JudgeFinding]) -> None:
    _check_pattern_rules(text, rel, findings)
    for l_s, c_s in NEON_OKLCH_RE.findall(text):
        if float(c_s) > 0.23 and float(l_s) > 0.45:
            findings.append(JudgeFinding(rule_id="OPTICS-NO-NEON", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=rel, message=f"High-chroma neon token oklch(L={l_s}, C={c_s}) exceeds 0.23 cap"))
            break
    if UNSAFE_HTML_RE.search(text) and "DOMPurify" not in text:
        findings.append(JudgeFinding(rule_id="AUDIT-SEC-01", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=rel, message="dangerouslySetInnerHTML used without DOMPurify sanitization"))
    if OUTLINE_NONE_RE.search(text) and ":focus-visible" not in text:
        findings.append(JudgeFinding(rule_id="WCAG-2.4.7", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=rel, message="outline removed without :focus-visible replacement"))
    if ("transition:" in text or "animation:" in text) and "prefers-reduced-motion" not in text:
        findings.append(JudgeFinding(rule_id="WCAG-2.3.3", severity="WARNING", epistemic_type="[TECHNICAL INFERENCE]", file=rel, message="Motion declared without @media (prefers-reduced-motion: reduce)"))


def _collect_files(target: Path) -> List[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() in UI_EXTS else []
    if not target.is_dir():
        return []
    return [
        p for p in sorted(target.rglob("*"))
        if p.is_file() and p.suffix.lower() in UI_EXTS and not any(d in IGNORE_DIRS for d in p.parts)
    ][:200]


def evaluate_ui(target_path: Path, wcag_level: Literal["AA", "AAA"] = "AA") -> UIJudgeReport:
    """Audit UI artifacts read-only and emit PASSED / REJECTED Actor-Critic verdict."""
    min_cr = 7.0 if wcag_level == "AAA" else 4.5
    files = _collect_files(target_path)
    if not files:
        return UIJudgeReport(verdict="UNVERIFIED", wcag_level=wcag_level, min_contrast_required=min_cr, contrast_ratio_min=0.0, files_audited=0, sha256_hashes={}, findings=[])
    base = target_path if target_path.is_dir() else target_path.parent
    hashes: Dict[str, str] = {}
    findings: List[JudgeFinding] = []
    min_obs = 21.0
    for fp in files:
        raw = fp.read_bytes()
        rel = fp.relative_to(base).as_posix() if fp.is_relative_to(base) else fp.name
        hashes[rel] = hashlib.sha256(raw).hexdigest()
        text = raw.decode("utf-8", errors="ignore")
        min_obs = min(min_obs, _check_contrast(text, rel, min_cr, findings))
        _check_static_rules(text, rel, findings)
    has_critical = any(f.severity == "CRITICAL" for f in findings)
    return UIJudgeReport(
        verdict="REJECTED" if has_critical else "PASSED", wcag_level=wcag_level,
        min_contrast_required=min_cr, contrast_ratio_min=min_obs,
        files_audited=len(files), sha256_hashes=hashes, findings=findings,
    )


def _run_self_test() -> int:
    import tempfile
    assert calculate_oklch_contrast(0.20, 0.98) >= 10.0 and hex_contrast_ratio("#ffffff", "#000000") == 21.0
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "bad.css"
        bad.write_text(".x { color: #777777; background: #888888; outline: none; order: 2; }", encoding="utf-8")
        rep = evaluate_ui(bad)
        assert rep.verdict == "REJECTED" and len(rep.findings) >= 3
        good = Path(tmp) / "good.css"
        good.write_text(":root { --ink-primary: light-dark(oklch(0.20 0.02 255), oklch(0.95 0.01 255)); --surface-card: light-dark(oklch(1 0 0), oklch(0.215 0.022 258)); } :focus-visible { outline: 2px solid currentColor; }", encoding="utf-8")
        assert evaluate_ui(good).verdict == "PASSED"
    print(json.dumps({"self_test": "UI_JUDGE_GATEKEEPER_OK"}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-Only WCAG 2.2 & OKLCH UI Quality Judge")
    parser.add_argument("--target", default=".")
    parser.add_argument("--wcag", default="AA", choices=["AA", "AAA"])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    report = evaluate_ui(Path(args.target).resolve(), wcag_level=args.wcag)
    print(report.model_dump_json(indent=2) if args.json else f"{report.verdict} files={report.files_audited} min_cr={report.contrast_ratio_min}:1 findings={len(report.findings)}")
    return 0 if report.verdict == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
