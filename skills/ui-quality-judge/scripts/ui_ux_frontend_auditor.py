#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Deterministic 6-Dimension UI/UX mathematical auditor for ui-quality-judge."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_HERE = Path(__file__).resolve().parent
for _cand in (*(p / "scripts" for p in _HERE.parents if (p / "pyproject.toml").is_file()), _HERE, *(p / "scripts" for p in _HERE.parents)):
    if (_cand / "_ss_core.py").is_file() and str(_cand) not in sys.path:
        sys.path.insert(0, str(_cand))
        break

import _ss_core

VOID_ELEMENTS: set[str] = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
SEMANTIC_TAGS: set[str] = {"main", "header", "nav", "aside", "section", "article", "footer"}
STANDARD_ICON_PX: set[int] = {16, 20, 24, 32}

TW_ARBITRARY_PX_RE = re.compile(
    r"(?<![a-zA-Z0-9_-])(?:p|px|py|pt|pr|pb|pl|m|mx|my|mt|mr|mb|ml|gap|gap-x|gap-y|w|h|top|left|right|bottom)-\[(\d+)px\](?![a-zA-Z0-9_-])"
)
CSS_SPACING_PX_RE = re.compile(
    r"(?:padding(?:-(?:top|right|bottom|left|inline|block|inline-start|inline-end|block-start|block-end))?|margin(?:-(?:top|right|bottom|left|inline|block|inline-start|inline-end|block-start|block-end))?|(?:row-|column-)?gap)\s*:\s*([^;}{]+)",
    re.IGNORECASE,
)
PX_VAL_RE = re.compile(r"(\d+)\s*px", re.IGNORECASE)
FONT_SIZE_PX_RE = re.compile(r"font-size\s*:\s*(\d+)\s*px", re.IGNORECASE)
COLOR_PAIR_RE = re.compile(
    r"\{[^{}]*?(?:(?<![a-zA-Z0-9_-])color\s*:\s*(#[0-9a-fA-F]{3,6}))[^{}]*?(?:background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6}))"
    r"|\{[^{}]*?(?:background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6}))[^{}]*?(?:(?<![a-zA-Z0-9_-])color\s*:\s*(#[0-9a-fA-F]{3,6}))",
    re.IGNORECASE | re.DOTALL,
)
SHORTHAND_ALLOW_DISCRETE_RE = re.compile(r"transition\s*:[^;}{]*\ballow-discrete\b", re.IGNORECASE)
BOX_SHADOW_RE = re.compile(r"box-shadow\s*:\s*([^;}{]+)", re.IGNORECASE)
TW_ICON_CLASS_RE = re.compile(r"(?<![a-zA-Z0-9_-])w-(4|5|6)(?![a-zA-Z0-9_-])(?=[^\"']*?\bh-\1\b)|(?<![a-zA-Z0-9_-])h-(4|5|6)(?![a-zA-Z0-9_-])(?=[^\"']*?\bw-\2\b)")
TS_GENERIC_CALL_RE = re.compile(r"\b([A-Za-z_$][\w$.]*)\s*<(?!/)(?:[^<>()\n]|\{[^{}\n]*\}|<[^<>\n]*>)+>(?=\s*\()")
TS_GENERIC_TYPE_RE = re.compile(
    r"\b(?:Promise|Array|Record|Readonly|Partial|Pick|Omit|Map|Set|Required|Extract|Exclude|ReturnType|Parameters|React\.FC|FC|MouseEvent|KeyboardEvent|PointerEvent|ChangeEvent|FormEvent)"
    r"\s*<(?:[^<>]|\{[^{}]*\}|<[^<>]*>)+>"
)
TS_DECL_GENERIC_RE = re.compile(r"\b((?:interface|type)\s+[A-Za-z_$][\w$]*)\s*<[^<>\n{}]+>")

ELEVATION_TOKENS = (
    "--shadow-elevation-1", "--shadow-elevation-2", "--shadow-elevation-3",
    "--shadow-elevation-low", "--shadow-elevation-medium", "--shadow-elevation-high",
    "--shadow-layer-sm", "--shadow-layer-md", "--shadow-layer-lg",
    "--shadow-inset", "--shadow-inset-sunken", "--shadow-clean-card",
    "--shadow-well", "--shadow-key", "--light-zenith", "--rim-top",
    "--elevation-1", "--elevation-2", "--elevation-3", "--elevation-low",
    "--elevation-medium", "--elevation-high", "--elevation-pressed",
    "--elevation-pressed-inset", "tactile-low", "tactile-md", "tactile-lg",
    "tactile-pressed", "shadow-elevation-low", "shadow-elevation-medium",
    "shadow-elevation-high", "shadow-lg", "shadow-xl", "shadow-2xl",
)


@dataclass
class UIUXAuditReport:
    """Consolidated 6-Dimension UI/UX mathematical audit output."""

    target_name: str
    final_score: float
    grade: str
    verdict: str
    total_tags: int
    max_dom_depth: int
    divsoup_ratio: float
    icons_count: int
    standard_icon_sizes: bool
    token_adherence_pct: float
    arbitrary_values: list[str] = field(default_factory=list)
    contrast_violations: list[str] = field(default_factory=list)
    min_contrast_ratio: float = 21.0
    light_physics_135: bool = False
    elevation_shadows: bool = False
    zero_reflow_motion: bool = True
    reduced_motion_support: bool = False
    dimension_scores: dict[str, float] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)


class DOMStructureParser(HTMLParser):
    """Parse HTML/JSX structure for DOM depth, divsoup ratio, viewport, and SVG icons."""

    def __init__(self) -> None:
        super().__init__()
        self.total_tags = self.div_count = self.semantic_count = 0
        self.current_depth = self.max_depth = 0
        self.viewport_present = self.aria_current_present = False
        self.icons_count = self.asymmetric_or_nonstd_icons = self._hidden_svg_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        t = tag.lower()
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        self.total_tags += 1
        if t == "div":
            self.div_count += 1
        elif t in SEMANTIC_TAGS:
            self.semantic_count += 1
        if t == "meta" and attr_map.get("name", "").lower() == "viewport" and "width=device-width" in attr_map.get("content", "").lower():
            self.viewport_present = True
        if attr_map.get("aria-current") == "page":
            self.aria_current_present = True
        if t == "svg":
            if "hidden" in attr_map or attr_map.get("width") == "0":
                self._hidden_svg_depth += 1
            elif self._hidden_svg_depth == 0:
                self._inspect_svg_icon(attr_map)
        elif t in ("symbol", "defs") and self._hidden_svg_depth > 0:
            self._hidden_svg_depth += 1
        if t not in VOID_ELEMENTS:
            self.current_depth += 1
            self.max_depth = max(self.max_depth, self.current_depth)

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t in ("svg", "symbol", "defs") and self._hidden_svg_depth > 0:
            self._hidden_svg_depth -= 1
        if t not in VOID_ELEMENTS and self.current_depth > 0:
            self.current_depth -= 1

    def _inspect_svg_icon(self, attr_map: dict[str, str]) -> None:
        if attr_map.get("role") == "img" or "data-chart" in attr_map:
            return
        self.icons_count += 1
        w_str = re.sub(r"[^0-9]", "", attr_map.get("width", ""))
        h_str = re.sub(r"[^0-9]", "", attr_map.get("height", ""))
        vb = attr_map.get("viewbox", "")
        if w_str and h_str:
            w_px, h_px = int(w_str), int(h_str)
            if max(w_px, h_px) >= 48:
                return
            if w_px != h_px or w_px not in STANDARD_ICON_PX:
                self.asymmetric_or_nonstd_icons += 1
            return
        if not TW_ICON_CLASS_RE.search(attr_map.get("class", "")):
            parts = vb.split()
            try:
                if len(parts) == 4 and parts[2] == parts[3] and int(float(parts[2])) in STANDARD_ICON_PX:
                    return
            except ValueError:
                pass
            self.asymmetric_or_nonstd_icons += 1


wcag_contrast_ratio = _ss_core.hex_contrast_ratio


def audit_color_contrast_pairs(source: str) -> tuple[list[str], float]:
    """Extract explicit CSS hex color/background pairs and enforce CR >= 4.5:1."""
    violations: list[str] = []
    min_cr = 21.0
    for match in COLOR_PAIR_RE.finditer(source):
        fg = match.group(1) or match.group(4)
        bg = match.group(2) or match.group(3)
        if not fg or not bg:
            continue
        cr = wcag_contrast_ratio(fg, bg)
        min_cr = min(min_cr, cr)
        if cr < 4.5:
            violations.append(f"{fg} on {bg} (CR={cr}:1 < 4.5:1)")
    return violations, min_cr


def audit_design_tokens_8px(source: str, recs: list[str]) -> tuple[float, float, list[str]]:
    """Audit 4px/8px grid alignment, arbitrary px literals, and anti-slop token hygiene."""
    arbitrary: list[str] = []
    total_checks = valid_checks = 0
    for m in TW_ARBITRARY_PX_RE.finditer(source):
        total_checks += 1
        if _ss_core.is_valid_spacing_px(int(m.group(1))):
            valid_checks += 1
        else:
            arbitrary.append(m.group(0))
    for decl in CSS_SPACING_PX_RE.finditer(source):
        for px_m in PX_VAL_RE.finditer(decl.group(1)):
            total_checks += 1
            if _ss_core.is_valid_spacing_px(int(px_m.group(1))):
                valid_checks += 1
            else:
                arbitrary.append(f"{px_m.group(1)}px")
    token_vars = set(re.findall(r"var\(--[a-zA-Z0-9_-]+\)", source))
    total_checks += max(len(token_vars), 3)
    valid_checks += len(token_vars)
    adherence = round((valid_checks / max(total_checks, 1)) * 100.0, 1)
    slop_pen = 25.0 if _ss_core.SLOP_TOKEN_RE.search(source) else 0.0
    score = max(0.0, min(100.0, adherence - (len(arbitrary) * 8.0) + (10.0 if token_vars else -15.0) - slop_pen))
    if arbitrary:
        recs.append(f"Replace {len(arbitrary)} arbitrary px values ({', '.join(arbitrary[:4])}) with 4px/8px tokens.")
    if slop_pen:
        recs.append("Remove cosmetic neon/violet slop tokens and use calibrated 3-layer OKLCH variables.")
    if not token_vars:
        recs.append("Adopt semantic CSS variables (e.g., var(--surface-card), var(--border-subtle)) per DESIGN.md.")
    return round(score, 1), adherence, arbitrary


def audit_typography_and_wcag(source: str, parser: DOMStructureParser, recs: list[str]) -> tuple[float, list[str], float]:
    """Audit typography crispness, viewport metadata, >=12px scale, and WCAG contrast."""
    score = 100.0
    low = source.lower()
    if not parser.viewport_present and "<html" in low:
        score -= 25.0
        recs.append("Set <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">.")
    if "antialiased" not in low:
        score -= 15.0
        recs.append("Enable subpixel smoothing (-webkit-font-smoothing: antialiased).")
    if not any(k in low for k in ("font-optical-sizing", "font-synthesis", "optimizelegibility")):
        score -= 10.0
        recs.append("Add font-optical-sizing: auto and font-synthesis: none for crisp type.")
    tiny_fonts = [int(m.group(1)) for m in FONT_SIZE_PX_RE.finditer(source) if int(m.group(1)) < 12]
    if tiny_fonts:
        score -= 20.0
        recs.append(f"Remove sub-12px micro-fonts ({tiny_fonts[0]}px detected).")
    violations, min_cr = audit_color_contrast_pairs(source)
    if violations:
        score -= min(40.0, len(violations) * 20.0)
        recs.append(f"Fix {len(violations)} WCAG contrast violation(s): {violations[0]}.")
    return max(0.0, round(score, 1)), violations, min_cr


def audit_dom_and_navigation(source: str, parser: DOMStructureParser, recs: list[str]) -> tuple[float, float]:
    """Audit DOM depth <= 12, divsoup ratio <= 0.45, landmarks, and :focus-visible."""
    score = 100.0
    divsoup = round(parser.div_count / max(parser.total_tags, 1), 2)
    if parser.max_depth > 12:
        score -= min(40.0, (parser.max_depth - 12) * 8.0)
        recs.append(f"Reduce DOM nesting depth ({parser.max_depth}) to <= 12.")
    if divsoup > 0.45:
        score -= min(35.0, (divsoup - 0.45) * 100.0)
        recs.append(f"Reduce divsoup ratio ({divsoup}) to <= 0.45 via HTML5 landmarks.")
    if parser.total_tags > 0 and parser.semantic_count == 0:
        score -= 20.0
        recs.append("Add semantic HTML5 landmarks (<header>, <nav>, <main>, <section>).")
    if "focus-visible" not in source.lower():
        score -= 15.0
        recs.append("Declare accessible keyboard focus rings via :focus-visible.")
    return max(0.0, round(score, 1)), divsoup


def _evaluate_lighting_score(source: str, low: str, recs: list[str]) -> tuple[float, bool, bool]:
    has_zenith = bool(
        re.search(r"border-top\s*:\s*1px\s+solid\s+(?:rgba\(\s*255\s*,\s*255\s*,\s*255|oklch\(\s*1\s+0\s+0)", low)
        or re.search(r"inset\s+0(?:px)?\s+1px\s+0(?:px)?(?:\s+0(?:px)?)?\s+(?:rgba\(\s*255\s*,\s*255\s*,\s*255|oklch\(\s*1\s+0\s+0|light-dark\()", low)
        or any(k in low for k in ("--specular-rim", "--catch-light", "--shadow-inset", "--light-zenith", "--rim-top"))
        or ("border-t" in low and "white/" in low)
    )
    shadows = [m.group(1) for m in BOX_SHADOW_RE.finditer(source) if not _ss_core.NEON_GLOW_RE.search(f"box-shadow:{m.group(1)}")]
    has_layered = any("," in s for s in shadows) or any(tok in low for tok in ELEVATION_TOKENS)
    score = (55.0 if has_zenith else 20.0) + (45.0 if has_layered else 15.0)
    if _ss_core.NEON_GLOW_RE.search(source):
        score = max(0.0, score - 35.0)
        recs.append("Replace omnidirectional neon glow with directional dark halo or 3-layer shadows.")
    if _ss_core.SLOP_BLOB_RE.search(source):
        score = max(0.0, score - 25.0)
        recs.append("Remove decorative blur blobs or organic bloops.")
    if not has_zenith:
        recs.append("Add zenithal specular catch-light (--catch-light: inset 0 1px 0 0 ...).")
    if not has_layered:
        recs.append("Use 3-layer optical shadows (--shadow-elevation-1..3).")
    return round(score, 1), has_zenith, has_layered


def audit_light_and_motion(source: str, recs: list[str]) -> tuple[float, bool, bool, float, bool, bool]:
    """Audit zenithal lighting, multi-layer non-neon shadows, zero-reflow GPU motion, and reduced motion."""
    low = source.lower()
    light_score, has_zenith, has_layered = _evaluate_lighting_score(source, low, recs)
    reflow_hits = [m.group(1) for m in _ss_core.REFLOW_TRANSITION_RE.finditer(source)]
    zero_reflow = len(reflow_hits) == 0
    has_rm = "prefers-reduced-motion" in low or "motion-reduce:" in low
    motion_score = 100.0
    if not zero_reflow:
        motion_score -= 45.0
        recs.append(f"Avoid reflow animation properties ({', '.join(set(reflow_hits))}); animate transform/opacity.")
    if SHORTHAND_ALLOW_DISCRETE_RE.search(source):
        motion_score -= 10.0
        recs.append("Declare transition-behavior: allow-discrete as a standalone property after transition.")
    if not has_rm:
        motion_score -= 25.0
        recs.append("Include @media (prefers-reduced-motion: reduce) fallback.")
    return light_score, has_zenith, has_layered, max(0.0, round(motion_score, 1)), zero_reflow, has_rm


_MARKUP_EXTS = frozenset({".html", ".htm", ".tsx", ".jsx", ".vue"})


def _strip_ts_generics(text: str) -> str:
    cleaned = TS_DECL_GENERIC_RE.sub(r"\1", text)
    cleaned = TS_GENERIC_TYPE_RE.sub("", cleaned)
    return TS_GENERIC_CALL_RE.sub(r"\1", cleaned)


def _score_bundle(
    stripped: str,
    parser: DOMStructureParser,
    target_name: str,
    markup_source: str | None = None,
) -> UIUXAuditReport:
    recs: list[str] = []
    s_tokens, adherence, arbitrary = audit_design_tokens_8px(stripped, recs)
    s_typo, contrast_violations, min_cr = audit_typography_and_wcag(stripped, parser, recs)
    s_dom, divsoup = audit_dom_and_navigation(stripped, parser, recs)
    svg_issues = _ss_core.inspect_inline_svgs(markup_source if markup_source is not None else stripped)
    bad_icons = parser.asymmetric_or_nonstd_icons + len(svg_issues)
    std_icons = bad_icons == 0
    s_icons = 100.0 if std_icons else max(0.0, 100.0 - bad_icons * 35.0)
    if not std_icons:
        recs.append("Standardize 1:1 16/20/24px vector icons with non-empty verified geometry.")
    s_light, has_135, has_shadows, s_motion, zero_reflow, has_rm = audit_light_and_motion(stripped, recs)
    final_score = round(0.20 * s_tokens + 0.20 * s_typo + 0.15 * s_dom + 0.15 * s_icons + 0.15 * s_light + 0.15 * s_motion, 1)
    grade = "A+ (Elite)" if final_score >= 92.0 else ("A (Pass)" if final_score >= 85.0 else ("B (Needs Refinement)" if final_score >= 70.0 else "C/F (Fail)"))
    verdict = "PASS" if final_score >= 85.0 and not contrast_violations and zero_reflow else "FAIL"
    return UIUXAuditReport(
        target_name=target_name, final_score=final_score, grade=grade, verdict=verdict,
        total_tags=parser.total_tags, max_dom_depth=parser.max_depth, divsoup_ratio=divsoup,
        icons_count=parser.icons_count, standard_icon_sizes=std_icons, token_adherence_pct=adherence,
        arbitrary_values=arbitrary, contrast_violations=contrast_violations, min_contrast_ratio=min_cr,
        light_physics_135=has_135, elevation_shadows=has_shadows, zero_reflow_motion=zero_reflow,
        reduced_motion_support=has_rm,
        dimension_scores={
            "design_tokens": s_tokens, "typography_mobile": s_typo, "structure_semantics": s_dom,
            "iconography": s_icons, "light_elevation": s_light, "motion_transitions": s_motion,
        },
        recommendations=recs,
    )


def evaluate_source(source: str, target_name: str = "Component") -> UIUXAuditReport:
    """Execute deterministic 6-Dimension mathematical UI/UX audit on frontend source."""
    stripped = _ss_core.strip_comments(source)
    parser = DOMStructureParser()
    parser.feed(_strip_ts_generics(stripped))
    return _score_bundle(stripped, parser, target_name)


def evaluate_target(target_path: Path) -> UIUXAuditReport:
    """Audit a file or bundle path, isolating DOM and SVG parsing per markup file (.html/.tsx/.jsx/.vue)."""
    files = _ss_core.collect_ui_files(target_path, limit=250)
    if not files:
        return evaluate_source("", target_path.name)
    stripped_parts: list[str] = []
    markup_parts: list[str] = []
    parser = DOMStructureParser()
    for fp in files:
        stripped_text = _ss_core.strip_comments(fp.read_text(encoding="utf-8", errors="replace"))
        stripped_parts.append(stripped_text)
        if fp.suffix.lower() in _MARKUP_EXTS:
            markup_parts.append(stripped_text)
            parser.current_depth = 0
            parser._hidden_svg_depth = 0
            feed_src = _strip_ts_generics(stripped_text) if fp.suffix.lower() in {".ts", ".tsx", ".jsx"} else stripped_text
            parser.feed(feed_src)
    return _score_bundle("\n".join(stripped_parts), parser, target_path.name, markup_source="\n".join(markup_parts))


def format_cli_report(report: UIUXAuditReport) -> str:
    """Format 6-Dimension UI/UX report for CLI output."""
    lines = [
        "=" * 65,
        f"UI/UX AUDIT REPORT: {report.target_name}",
        f"SCORE: {report.final_score}/100 | GRADE: {report.grade} | [{report.verdict}]",
        f"Tags: {report.total_tags} | DOM Depth: {report.max_dom_depth} | Divsoup: {report.divsoup_ratio}",
        f"Icons: {report.icons_count} (std={report.standard_icon_sizes}) | Tokens: {report.token_adherence_pct}%",
        f"Zenith Light: {report.light_physics_135} | Shadows: {report.elevation_shadows} | Zero-Reflow: {report.zero_reflow_motion}",
    ]
    for rec in report.recommendations:
        lines.append(f"  - {rec}")
    return "\n".join(lines + ["=" * 65])


def _run_self_test() -> int:
    demo_html = """<!DOCTYPE html><html lang="en"><head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      body { -webkit-font-smoothing: antialiased; font-optical-sizing: auto; color: #f8fafc; background-color: #0f172a; padding: 16px; margin: 8px; }
      .card { border: 1px solid var(--border-muted); border-top: 1px solid rgba(255,255,255,0.15); box-shadow: 0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2); padding: 24px; gap: 16px; transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1), opacity 200ms ease; }
      .btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
      @media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition-duration: 0.01ms !important; } }
    </style></head><body><header><nav><a href="/" aria-current="page" class="btn">Home</a></nav></header>
    <main><section class="card"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"><path d="M4 12h16"/></svg><h1>Dashboard</h1></section></main></body></html>"""
    rep = evaluate_source(demo_html, "DashboardDemo.html")
    assert rep.final_score >= 92.0 and rep.verdict == "PASS", f"Self-test failed: {rep}"
    print(format_cli_report(rep))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic 6-Dimension UI/UX Frontend Auditor")
    parser.add_argument("target", nargs="?", default=None, help="Target frontend file or directory")
    parser.add_argument("--target", dest="target_flag", default=None, help="Explicit --target frontend path")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--self-test", action="store_true", help="Run built-in deterministic self-test")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    target_path = _ss_core.resolve_cli_target(args.target, args.target_flag)
    if not target_path.exists():
        print(f"[FAIL] Target not found: {target_path}", file=sys.stderr)
        return 1
    report = evaluate_target(target_path)
    print(json.dumps(asdict(report), indent=2, ensure_ascii=False) if args.json else format_cli_report(report))
    return 0 if report.verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
