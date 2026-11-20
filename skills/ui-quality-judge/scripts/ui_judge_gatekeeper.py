#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.7.0"]
# ///
"""Read-only Actor-Critic UI/UX & WCAG 2.2 OKLab Gatekeeper (FNR < 0.001)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_HERE = Path(__file__).resolve().parent
for _cand in (*(p / "scripts" for p in _HERE.parents if (p / "pyproject.toml").is_file()), _HERE, *(p / "scripts" for p in _HERE.parents)):
    if (_cand / "_ss_core.py").is_file() and str(_cand) not in sys.path:
        sys.path.insert(0, str(_cand))
        break

import _ss_core
import _ss_craft_guards
import _ss_guards

BASE64_BLOAT_RE = re.compile(r"data:image/[a-zA-Z0-9+.-]+;base64,[A-Za-z0-9+/=]{68000,}")
OUTLINE_NONE_RE = re.compile(r"outline\s*:\s*(?:none|0)\b")
COLOR_DECL_RE = re.compile(r"(?<![a-zA-Z0-9_-])color\s*:\s*(#[0-9a-fA-F]{3,6})\b", re.IGNORECASE)
BG_DECL_RE = re.compile(r"background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6})\b", re.IGNORECASE)
CSS_BLOCK_RE = re.compile(r"([^{};]+)\{([^{}]*)\}", re.DOTALL)
BAD_SPAN_PRESSED_RE = re.compile(r"<span\b(?![^>]*\brole\s*=\s*['\"]button['\"])[^>]*\baria-pressed\s*=", re.IGNORECASE)
BAD_LISTBOX_BTN_RE = re.compile(r'role\s*=\s*["\']listbox["\'][\s\S]{0,1200}<button\b(?![^>]*\brole\s*=\s*["\']option["\'])[^>]*\baria-selected\s*=', re.IGNORECASE)
_SPA_ROUTE_RE = re.compile(r"""(?:<Route\b[^>]*path=|activeTab\s*===|currentView\s*===)\s*['"]([a-zA-Z0-9_/-]+)['"]""")
_COMPONENT_SIBLING_EXTS = frozenset({".tsx", ".jsx", ".html"})


class JudgeFinding(BaseModel):
    """Single deterministic violation or observation emitted by ui-judge."""

    model_config = ConfigDict(extra="forbid")
    rule_id: str
    severity: Literal["CRITICAL", "WARNING"]
    epistemic_type: Literal["[OBSERVED FACT]", "[TECHNICAL INFERENCE]"]
    file: str
    message: str
    remediation: str = ""


class UIJudgeReport(BaseModel):
    """Actor-Critic Gatekeeper output contract."""

    model_config = ConfigDict(extra="forbid")
    verdict: Literal["PASSED", "REJECTED", "UNVERIFIED"]
    wcag_level: Literal["AA", "AAA"]
    min_contrast_required: float
    contrast_ratio_min: float
    files_audited: int
    scope_path: str = ""
    files_total_eligible: int = 0
    truncated: bool = False
    scope_narrowed: bool = False
    unverified_routes: list[str] = Field(default_factory=list)
    sha256_hashes: dict[str, str]
    findings: list[JudgeFinding]


JudgeFinding.model_rebuild()
UIJudgeReport.model_rebuild()


oklch_to_relative_luminance = _ss_core.oklch_to_relative_luminance
calculate_oklch_contrast = _ss_core.calculate_oklch_contrast
hex_contrast_ratio = _ss_core.hex_contrast_ratio


def _first_line(text: str, pattern: re.Pattern[str]) -> int:
    for ln, line in enumerate(text.splitlines(), 1):
        if pattern.search(line):
            return ln
    return 1


def _check_block_hex_pairs(stripped: str, rel: str, min_cr: float, findings: list[JudgeFinding]) -> float:
    observed = 21.0
    for block in CSS_BLOCK_RE.finditer(stripped):
        body = block.group(2)
        fg_m, bg_m = COLOR_DECL_RE.search(body), BG_DECL_RE.search(body)
        if not (fg_m and bg_m):
            continue
        cr = hex_contrast_ratio(fg_m.group(1), bg_m.group(1))
        observed = min(observed, cr)
        if cr < min_cr:
            ln = stripped[: block.start()].count("\n") + 1
            findings.append(JudgeFinding(
                rule_id="WCAG-1.4.3", severity="CRITICAL", epistemic_type="[OBSERVED FACT]",
                file=f"{rel}:{ln}", message=f"Contrast {cr}:1 ({fg_m.group(1)} on {bg_m.group(1)}) below {min_cr}:1",
                remediation="Increase perceptual lightness delta between foreground and background tokens.",
            ))
    return observed


def _check_dark_surface_order(
    theme_name: str,
    tokens: dict[str, tuple[float, float, float]],
    card: tuple[float, float, float] | None,
    canvas: tuple[float, float, float] | None,
    findings: list[JudgeFinding],
) -> None:
    if not theme_name.endswith(":dark"):
        return
    well = tokens.get("--bg-well") or tokens.get("--surface-well") or tokens.get("--surface-sunken") or tokens.get("--bg-sunken")
    lit = tokens.get("--bg-card-lit") or tokens.get("--surface-elevated")
    checks = (
        (card and canvas and card[0] <= canvas[0], f"Dark Mode card L={card[0] if card else 0} must exceed canvas L={canvas[0] if canvas else 0}", "Elevate Dark Mode surface lightness progressively (well < canvas < card < card-lit)."),
        (well and canvas and well[0] >= canvas[0], f"Dark Mode well L={well[0] if well else 0} must sit below canvas L={canvas[0] if canvas else 0}", "Keep carved --bg-well darker than --bg-canvas in Dark Mode."),
        (lit and card and lit[0] <= card[0], f"Dark Mode card-lit L={lit[0] if lit else 0} must exceed card L={card[0] if card else 0}", "Step hover/selected --bg-card-lit above --bg-card in Dark Mode."),
    )
    for failed, msg, rem in checks:
        if failed:
            findings.append(JudgeFinding(
                rule_id="OPTICS-DARK-ELEVATION", severity="CRITICAL",
                epistemic_type="[OBSERVED FACT]", file=f"bundle:{theme_name}", message=msg, remediation=rem,
            ))


def _audit_single_theme_tokens(
    theme_name: str,
    tokens: dict[str, tuple[float, float, float]],
    min_cr: float,
    findings: list[JudgeFinding],
) -> float:
    observed_primary = 21.0
    ink_pri = tokens.get("--ink-primary") or tokens.get("--text-primary")
    card = tokens.get("--bg-card") or tokens.get("--surface-card") or tokens.get("--bg-surface-1")
    canvas = tokens.get("--bg-canvas") or tokens.get("--surface-canvas")
    if ink_pri:
        for surf_label, surf in (("card", card), ("canvas", canvas)):
            if not surf:
                continue
            cr = calculate_oklch_contrast(ink_pri[0], surf[0], ink_pri[1], ink_pri[2], surf[1], surf[2])
            observed_primary = min(observed_primary, cr)
            if cr < min_cr:
                findings.append(JudgeFinding(
                    rule_id="WCAG-1.4.3-OKLCH", severity="CRITICAL", epistemic_type="[OBSERVED FACT]",
                    file=f"bundle:{theme_name}", message=f"{theme_name} primary on {surf_label} contrast {cr}:1 below {min_cr}:1",
                    remediation="Adjust OKLCH L values to achieve >= 4.5:1 (AA) or >= 7.0:1 (AAA).",
                ))
    ref_bg = canvas or card
    for ink_key in ("--ink-secondary", "--text-secondary", "--ink-muted", "--text-muted"):
        if (ink_tok := tokens.get(ink_key)) and ref_bg:
            cr_sub = calculate_oklch_contrast(ink_tok[0], ref_bg[0], ink_tok[1], ink_tok[2], ref_bg[1], ref_bg[2])
            if cr_sub < 4.5:
                findings.append(JudgeFinding(
                    rule_id="WCAG-1.4.3-OKLCH", severity="CRITICAL", epistemic_type="[OBSERVED FACT]",
                    file=f"bundle:{theme_name}", message=f"{theme_name} {ink_key} contrast {cr_sub}:1 below 4.5:1 AA",
                    remediation=f"Adjust {ink_key} OKLCH lightness against canvas/card.",
                ))
    if (ink_key := tokens.get("--ink-on-key") or tokens.get("--text-on-key")) and (key_bg := tokens.get("--bg-key") or tokens.get("--surface-key")):
        cr_key = calculate_oklch_contrast(ink_key[0], key_bg[0], ink_key[1], ink_key[2], key_bg[1], key_bg[2])
        if cr_key < 4.5:
            findings.append(JudgeFinding(
                rule_id="WCAG-1.4.3-OKLCH", severity="CRITICAL", epistemic_type="[OBSERVED FACT]",
                file=f"bundle:{theme_name}", message=f"{theme_name} --ink-on-key on --bg-key contrast {cr_key}:1 below 4.5:1",
                remediation="Increase contrast between --ink-on-key and --bg-key.",
            ))
    if (ink_brand := tokens.get("--ink-on-brand") or tokens.get("--text-on-brand")) and (brand_bg := tokens.get("--brand-fill") or tokens.get("--brand-primary")):
        cr_brand = calculate_oklch_contrast(ink_brand[0], brand_bg[0], ink_brand[1], ink_brand[2], brand_bg[1], brand_bg[2])
        if cr_brand < 4.5:
            findings.append(JudgeFinding(
                rule_id="WCAG-1.4.3-OKLCH", severity="CRITICAL", epistemic_type="[OBSERVED FACT]",
                file=f"bundle:{theme_name}", message=f"{theme_name} --ink-on-brand on --brand-fill contrast {cr_brand}:1 below 4.5:1",
                remediation="Separate --brand-fill/--ink-on-brand lightness per polarity to guarantee >= 4.5:1 contrast.",
            ))
    _check_dark_surface_order(theme_name, tokens, card, canvas, findings)
    return observed_primary


def _check_bundle_theme_maps(
    bundle_stripped: str, min_cr: float, findings: list[JudgeFinding], maps: dict[str, dict[str, tuple[float, float, float]]] | None = None
) -> float:
    resolved_maps = _ss_core.extract_theme_oklch_maps(bundle_stripped) if maps is None else maps
    if not resolved_maps:
        return 21.0
    observed = 21.0
    for theme_name, tokens in resolved_maps.items():
        observed = min(observed, _audit_single_theme_tokens(theme_name, tokens, min_cr, findings))
    return observed


def _check_sheen_and_brand_fill(stripped: str, rel: str, maps: dict[str, dict[str, tuple[float, float, float]]], findings: list[JudgeFinding]) -> None:
    if m_grain := _ss_core.GRAIN_ABOVE_TEXT_RE.search(stripped):
        findings.append(JudgeFinding(
            rule_id="OPTICS-GRAIN-ABOVE-TEXT", severity="CRITICAL", epistemic_type="[OBSERVED FACT]",
            file=f"{rel}:{stripped[: m_grain.start()].count('\n') + 1}",
            message="SVG feTurbulence ::after/::before overlay lacks z-index: -1 and paints noise over text",
            remediation="Add z-index: -1 to grain pseudo-element inside isolation: isolate.",
        ))
    if any(t.endswith(":dark") and (bp := toks.get("--brand-primary")) and bp[0] >= 0.60 for t, toks in maps.items()):
        for blk in CSS_BLOCK_RE.finditer(stripped):
            body = blk.group(2)
            if re.search(r"background(?:-color)?\s*:\s*var\(\s*--brand-primary\s*\)", body, re.IGNORECASE) and re.search(r"(?<![a-zA-Z0-9_-])color\s*:\s*oklch\(\s*0\.9\d*", body, re.IGNORECASE):
                findings.append(JudgeFinding(
                    rule_id="WCAG-1.4.3-BRAND-FILL", severity="CRITICAL", epistemic_type="[OBSERVED FACT]",
                    file=f"{rel}:{stripped[: blk.start()].count('\n') + 1}",
                    message="Hardcoded near-white ink on var(--brand-primary) fails contrast in Dark Mode (L >= 0.60)",
                    remediation="Use --brand-fill and --ink-on-brand polarity tokens instead of oklch(0.99 ...) on --brand-primary.",
                ))
    if _ss_core.OPAQUE_LIGHT_KEY_RE.search(stripped) and any(
        t.endswith(":light") and (bk := toks.get("--bg-key") or toks.get("--surface-key")) and (ik := toks.get("--ink-on-key")) and bk[0] < 0.50 and ik[0] > 0.85
        for t, toks in maps.items()
    ):
        findings.append(JudgeFinding(
            rule_id="OPTICS-OPAQUE-KEY-SHEEN", severity="CRITICAL", epistemic_type="[OBSERVED FACT]",
            file=f"{rel}:{_first_line(stripped, _ss_core.OPAQUE_LIGHT_KEY_RE)}",
            message="Opaque light-mode --light-key white gradient masks dark --bg-key surfaces behind light --ink-on-key",
            remediation="Make --light-key translucent or raise --bg-key with dark --ink-on-key.",
        ))


def _check_guard_findings(
    target_fp: Path, raw: str, stripped: str, masked: str, rel: str, findings: list[JudgeFinding]
) -> None:
    for hit in _ss_craft_guards.run_craft_and_sec_guards(target_fp, raw, stripped, masked, profile="judge"):
        findings.append(JudgeFinding(rule_id=hit.rule_id, severity=hit.severity, epistemic_type="[OBSERVED FACT]", file=f"{rel}:{hit.line}", message=hit.message, remediation=hit.remediation))
    for ln, snippet, rem in _ss_guards.find_print_shadow_leaks(target_fp, raw):
        findings.append(JudgeFinding(rule_id="CLINICAL-PRINT-SHADOW", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=f"{rel}:{ln}", message=f"Non-none box-shadow inside @media print ({snippet})", remediation=rem))
    for ln, snippet, rem in _ss_guards.find_unsemantic_div_clicks(target_fp, raw):
        findings.append(JudgeFinding(rule_id="AUDIT-A11Y-CLICK-DIV", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=f"{rel}:{ln}", message=f"Clickable <div onClick> without semantic button/role ({snippet[:48]})", remediation=rem))
    for ln, snippet, rem in _ss_guards.find_pseudo_icon_hits(target_fp, raw):
        findings.append(JudgeFinding(rule_id="AUDIT-VIS-PSEUDO-ICON", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=f"{rel}:{ln}", message=f"Unicode/ASCII pseudo-icon '{snippet}' detected; use crisp SVG", remediation=rem))
    for ln, snippet, rem in _ss_guards.find_target_size_overrides(target_fp, raw):
        findings.append(JudgeFinding(rule_id="FITTS-TARGET-SIZE", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=f"{rel}:{ln}", message=f"Interactive hit target < 40px ({snippet})", remediation=rem))


def _check_static_rules(raw: str, stripped: str, rel: str, bundle_stripped: str, findings: list[JudgeFinding], fp: Path | None = None) -> None:
    target_fp = fp if fp is not None else Path(rel)
    masked = _ss_guards.strip_print_sheet_contexts(target_fp, stripped)
    rules: tuple[tuple[re.Pattern[str], str, Literal["CRITICAL", "WARNING"], Literal["[OBSERVED FACT]", "[TECHNICAL INFERENCE]"], str, str], ...] = (
        (_ss_core.PURE_BLACK_RE, "OPTICS-NO-BLACK", "CRITICAL", "[OBSERVED FACT]", "Pure #000000 black violates Dark Mode elevation", "Replace #000000 with oklch(0.16 0.02 258)."),
        (_ss_core.EMOJI_RE, "AUDIT-VIS-EMOJI", "CRITICAL", "[OBSERVED FACT]", "Unicode UI emoji detected; use crisp vector SVGs", "Replace emoji with 16/20/24px Lucide/Material SVG."),
        (BASE64_BLOAT_RE, "AUDIT-VIS-BLOAT", "CRITICAL", "[OBSERVED FACT]", "Base64 inline image exceeds 50KB budget", "Move image to external asset file or vector SVG."),
        (_ss_core.ROW_REVERSE_RE, "WCAG-1.3.2", "CRITICAL", "[OBSERVED FACT]", "row-reverse, CSS order, or grid-auto-flow: dense breaks DOM == Tab focus sequence", "Reorder DOM nodes directly instead of visual CSS reversal."),
        (_ss_core.FLAT_SHADOW_RE, "LOCK-02-SHADOWS", "WARNING", "[OBSERVED FACT]", "Single-pass rgba(0,0,0) shadow detected", "Use 3-layer optical shadow (Umbra + negative Penumbra + Catch-Light)."),
        (_ss_core.NEON_GLOW_RE, "OPTICS-NEON-GLOW", "CRITICAL", "[OBSERVED FACT]", "Omnidirectional neon shadow/glow violates optical discipline", "Use subtle directional dark halo (spread < 0, alpha <= 0.16)."),
        (_ss_core.SLOP_BLOB_RE, "ANTI-SLOP-BLOB", "CRITICAL", "[OBSERVED FACT]", "Decorative blur blob, organic bloop, or gooey SVG detected", "Remove decorative blur blobs; use sharp geometry and 3-layer elevation."),
        (_ss_core.SLOP_TOKEN_RE, "ANTI-SLOP-TOKEN", "CRITICAL", "[OBSERVED FACT]", "Cosmetic neon/violet AI-slop token or gradient detected", "Use calibrated 3-layer OKLCH semantic tokens."),
        (_ss_core.DASHED_BOX_SLOP_RE, "ANTI-SLOP-WIREFRAME", "CRITICAL", "[OBSERVED FACT]", "Dashed wireframe layout border detected", "Use recessed wells (--bg-well) or 1px hairline separation (--border-side) instead of dashed boxes."),
        (BAD_SPAN_PRESSED_RE, "AUDIT-A11Y-ARIA-ATTR", "CRITICAL", "[OBSERVED FACT]", "aria-pressed used on non-interactive <span> without role='button'", "Use native <button type='button' aria-pressed='...'>."),
        (BAD_LISTBOX_BTN_RE, "AUDIT-A11Y-ARIA-ATTR", "CRITICAL", "[OBSERVED FACT]", "role='listbox' wraps <button aria-selected> without role='option'", "Use role='group' with <button aria-pressed> or proper role='option'."),
        (_ss_core.REFLOW_TRANSITION_RE, "PERF-REFLOW", "CRITICAL", "[OBSERVED FACT]", "Layout-thrashing transition property (all/width/height/margin/padding)", "Animate GPU transform and opacity only."),
    )
    for pattern, rule_id, severity, ep_type, msg, rem in rules:
        if pattern.search(masked):
            findings.append(JudgeFinding(rule_id=rule_id, severity=severity, epistemic_type=ep_type, file=f"{rel}:{_first_line(masked, pattern)}", message=msg, remediation=rem))
    _check_guard_findings(target_fp, raw, stripped, masked, rel, findings)
    if len(raw.splitlines()) > 600:
        findings.append(JudgeFinding(rule_id="CAP-600L", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=f"{rel}:601", message=f"File exceeds 600-line ceiling ({len(raw.splitlines())} lines)", remediation="Split module by domain concern (<= 600 lines/file)."))
    if re.search(r"//.*?\bidle\b.*?\bloading\b.*?\berror\b", raw, re.IGNORECASE):
        findings.append(JudgeFinding(rule_id="AUDIT-STATE-GAMING", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=f"{rel}:1", message="Comment-gamed FSM state strings detected", remediation="Implement executable FSM transitions instead of comments."))
    for msg in _ss_core.find_neon_violations(masked):
        findings.append(JudgeFinding(rule_id="OPTICS-NO-NEON", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=f"{rel}:1", message=msg, remediation="Clamp OKLCH chroma C <= 0.20 (hard max 0.22)."))
    for msg in _ss_core.inspect_inline_svgs(stripped):
        findings.append(JudgeFinding(rule_id="AUDIT-VIS-BAD-SVG", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=f"{rel}:1", message=msg, remediation="Use verified Lucide/Material 24x24 vector SVG paths."))
    if _ss_core.has_confetti_badge_slop(masked):
        findings.append(JudgeFinding(rule_id="ANTI-SLOP-CONFETTI", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=f"{rel}:1", message=">=3 multicolored pill/badge variants create AI confetti slop", remediation="Use neutral recessed .engraved-pill wells paired with a 6px .lum-bead status dot."))
    if OUTLINE_NONE_RE.search(masked) and ":focus-visible" not in bundle_stripped:
        findings.append(JudgeFinding(rule_id="WCAG-2.4.7", severity="CRITICAL", epistemic_type="[OBSERVED FACT]", file=f"{rel}:{_first_line(masked, OUTLINE_NONE_RE)}", message="outline removed without :focus-visible replacement", remediation="Provide explicit :focus-visible outline (>= 2px solid)."))
    if ("transition:" in masked or "animation:" in masked) and "prefers-reduced-motion" not in bundle_stripped:
        findings.append(JudgeFinding(rule_id="WCAG-2.3.3", severity="WARNING", epistemic_type="[TECHNICAL INFERENCE]", file=f"{rel}:1", message="Motion declared without @media (prefers-reduced-motion: reduce)", remediation="Add @media (prefers-reduced-motion: reduce) fallback."))
    if _ss_core.COLOR_MIX_OKLCH_WARN_RE.search(masked):
        findings.append(JudgeFinding(rule_id="OPTICS-COLOR-MIX-OKLAB", severity="WARNING", epistemic_type="[TECHNICAL INFERENCE]", file=f"{rel}:{_first_line(masked, _ss_core.COLOR_MIX_OKLCH_WARN_RE)}", message="color-mix(in oklch, ...) risks Chromium hue-arc artifacts; prefer color-mix(in oklab, ...)", remediation="Switch UI state color mixing to color-mix(in oklab, ...)."))


def _detect_scope_narrowed(target_path: Path) -> bool:
    if not target_path.is_dir() or target_path.name.lower() not in {"styles", "css"}:
        return False
    parent = target_path.parent
    for sib in parent.rglob("*"):
        if not sib.is_file() or sib.is_relative_to(target_path):
            continue
        if any(part in _ss_core.IGNORED_DIRS for part in sib.parts):
            continue
        if sib.suffix.lower() in _COMPONENT_SIBLING_EXTS:
            return True
    return False


def evaluate_ui(target_path: Path, wcag_level: Literal["AA", "AAA"] = "AA") -> UIJudgeReport:
    """Audit UI artifacts read-only and emit PASSED / REJECTED / UNVERIFIED Actor-Critic verdict."""
    files, total_eligible, truncated = _ss_core.collect_ui_files_scoped(target_path, limit=500)
    narrowed = _detect_scope_narrowed(target_path)
    min_req = 7.0 if wcag_level == "AAA" else 4.5
    if not files:
        return UIJudgeReport(
            verdict="UNVERIFIED", wcag_level=wcag_level, min_contrast_required=min_req, contrast_ratio_min=0.0,
            files_audited=0, scope_path=str(target_path), files_total_eligible=0, truncated=False, scope_narrowed=narrowed,
            unverified_routes=[], sha256_hashes={}, findings=[],
        )

    base = target_path if target_path.is_dir() else target_path.parent
    loaded: list[tuple[Path, str, str, str, str]] = []
    hashes: dict[str, str] = {}
    spa_routes: set[str] = set()
    for fp in files:
        raw_bytes = fp.read_bytes()
        rel = fp.relative_to(base).as_posix() if fp.is_relative_to(base) else fp.name
        hashes[rel] = hashlib.sha256(raw_bytes).hexdigest()
        raw_text = raw_bytes.decode("utf-8", errors="ignore")
        stripped = _ss_core.strip_comments(raw_text)
        masked = _ss_guards.strip_print_sheet_contexts(fp, stripped)
        spa_routes.update(_SPA_ROUTE_RE.findall(stripped))
        loaded.append((fp, rel, raw_text, stripped, masked))

    unmasked_bundle = "\n".join(item[3] for item in loaded)
    bundle_stripped = "\n".join(item[4] for item in loaded)
    maps = _ss_core.extract_theme_oklch_maps(bundle_stripped)
    is_clinical = any(k in unmasked_bundle for k in ("clinical-day", "clinical-night", ".sus-grid"))
    eff_level: Literal["AA", "AAA"] = "AAA" if is_clinical else wcag_level
    min_cr = 7.0 if eff_level == "AAA" else 4.5
    findings: list[JudgeFinding] = []
    min_obs = 21.0
    for fp, rel, raw_text, stripped, masked in loaded:
        min_obs = min(min_obs, _check_block_hex_pairs(masked, rel, min_cr, findings))
        _check_static_rules(raw_text, stripped, rel, bundle_stripped, findings, fp=fp)
        _check_sheen_and_brand_fill(masked, rel, maps, findings)
    min_obs = min(min_obs, _check_bundle_theme_maps(bundle_stripped, min_cr, findings, maps=maps))
    if truncated or narrowed:
        reason = f"Scope narrowed to {target_path.name}/ while parent has component siblings" if narrowed else f"Audit truncated ({len(files)}/{total_eligible} files)"
        findings.append(JudgeFinding(rule_id="SCOPE-UNVERIFIED", severity="WARNING", epistemic_type="[OBSERVED FACT]", file=str(target_path), message=reason, remediation="Audit project src/ root without artificial CSS-only narrowing or exceeds-limit truncation."))
    has_critical = any(f.severity == "CRITICAL" for f in findings)
    verdict: Literal["PASSED", "REJECTED", "UNVERIFIED"] = "UNVERIFIED" if (truncated or narrowed) else ("REJECTED" if has_critical else "PASSED")
    return UIJudgeReport(
        verdict=verdict, wcag_level=eff_level, min_contrast_required=min_cr, contrast_ratio_min=min_obs,
        files_audited=len(files), scope_path=str(target_path), files_total_eligible=total_eligible,
        truncated=truncated, scope_narrowed=narrowed, unverified_routes=sorted(spa_routes)[:30],
        sha256_hashes=hashes, findings=findings,
    )


def _run_composite(target_path: Path, wcag_level: Literal["AA", "AAA"]) -> dict[str, object]:
    from dataclasses import asdict

    import audit_tactile_ui
    import ui_ux_frontend_auditor

    gate = evaluate_ui(target_path, wcag_level=wcag_level)
    tactile = audit_tactile_ui.run_audit(target_path)
    ux_rep = ui_ux_frontend_auditor.evaluate_target(target_path)
    ux_ok = (ux_rep.total_tags == 0) or (ux_rep.verdict == "PASS")
    overall = "UNVERIFIED" if gate.verdict == "UNVERIFIED" else ("PASSED" if (gate.verdict == "PASSED" and tactile.get("verdict") == "PASS" and ux_ok) else "REJECTED")
    return {
        "overall_verdict": overall,
        "gatekeeper": gate.model_dump(),
        "tactile_readiness": tactile,
        "ui_ux_6dim": asdict(ux_rep) if ux_rep.total_tags > 0 else None,
    }


def _run_self_test() -> int:
    import tempfile
    assert oklch_to_relative_luminance(0.50) == 0.125
    assert calculate_oklch_contrast(0.20, 0.98) >= 10.0 and hex_contrast_ratio("#ffffff", "#000000") == 21.0
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "bad.css"
        bad.write_text(".x { background: #888888; color: #777777; outline: none; order: 2; }", encoding="utf-8")
        rep = evaluate_ui(bad)
        assert rep.verdict == "REJECTED" and len(rep.findings) >= 3
        good = Path(tmp) / "good.css"
        good.write_text(
            ":root { --ink-primary: light-dark(oklch(0.20 0.02 255), oklch(0.95 0.01 255)); "
            "--surface-card: light-dark(oklch(1 0 0), oklch(0.215 0.022 258)); } "
            ":focus-visible { outline: 2px solid currentColor; }",
            encoding="utf-8",
        )
        assert evaluate_ui(good).verdict == "PASSED"
    print(json.dumps({"self_test": "UI_JUDGE_GATEKEEPER_OK"}, ensure_ascii=False))
    return 0


def _dispatch_non_code_axis(
    target: Path, axis: str, workspace_raw: str, emit_json: bool
) -> int | None:
    resolved_axis = axis
    if resolved_axis == "auto" and target.is_file() and target.suffix.lower() in {".md", ".json"}:
        low = target.name.lower()
        resolved_axis = "technical_audit" if ("clareza" in low or "inventory" in low or "audit" in low) else "execution_plan"
    if resolved_axis not in {"execution_plan", "technical_audit"}:
        return None
    if str(_HERE) not in sys.path:
        sys.path.insert(0, str(_HERE))
    import artifact_axis_judge

    ws = Path(workspace_raw).expanduser().resolve() if workspace_raw.strip() else None
    rep = artifact_axis_judge.evaluate_execution_plan(target) if resolved_axis == "execution_plan" else artifact_axis_judge.evaluate_technical_audit(target, workspace=ws)
    print(rep.model_dump_json(indent=2) if emit_json else f"{rep.verdict} axis={rep.axis} checks={rep.checks_passed} findings={len(rep.findings)}")
    return 0 if rep.verdict == "PASSED" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-Only WCAG 2.2 & OKLab UI Quality Judge")
    parser.add_argument("target", nargs="?", default=None, help="Target frontend file or directory")
    parser.add_argument("--target", dest="target_flag", default=None, help="Explicit --target path")
    parser.add_argument("--wcag", default="AA", choices=["AA", "AAA"])
    parser.add_argument("--axis", default="auto", choices=["auto", "ui_code", "execution_plan", "technical_audit"])
    parser.add_argument("--workspace", default="", help="Optional workspace root for Axis-3 file:line verification")
    parser.add_argument("--composite", action="store_true", help="Run all 3 Stage-3 engines in a single pass")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    target = _ss_core.resolve_cli_target(args.target, args.target_flag)
    if (axis_exit := _dispatch_non_code_axis(target, args.axis, args.workspace, args.json)) is not None:
        return axis_exit
    if args.composite:
        payload = _run_composite(target, args.wcag)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0 if payload["overall_verdict"] == "PASSED" else 1
    report = evaluate_ui(target, wcag_level=args.wcag)
    print(report.model_dump_json(indent=2) if args.json else f"{report.verdict} files={report.files_audited} min_cr={report.contrast_ratio_min}:1 findings={len(report.findings)}")
    return 0 if report.verdict == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
