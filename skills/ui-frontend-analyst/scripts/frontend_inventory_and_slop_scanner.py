#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.7.0"]
# ///
"""Forensic frontend inventory, Mermaid navigation map, and AI Slop scanner."""

from __future__ import annotations

import argparse
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

VAR_DECL_RE = re.compile(r"(--[a-zA-Z0-9_-]+)\s*:")
HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|(?:rgba?|hsla?)\([^)]+\)")
OKLCH_RE = re.compile(r"oklch\([^)]+\)")
LIGHT_DARK_RE = re.compile(r"light-dark\([^)]+\)")
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;}{]+)")
IMPORT_ICON_RE = re.compile(
    r"from\s+['\"](lucide-react|@phosphor-icons/react|phosphor-react|@fluentui/react-icons"
    r"|@material-symbols/svg-[a-z0-9-]+|@heroicons[^'\"]*|@tabler/icons[^'\"]*|@radix-ui/react-icons|react-icons[^'\"]*)['\"]"
)
ROUTE_LINK_RE = re.compile(r"""(?:href|to)=['"](/[^'"#?]*|#[a-zA-Z0-9_-]+)['"]""")
OFF_GRID_TW_RE = re.compile(r"(?<![a-zA-Z0-9_-])(?:p|px|py|m|mx|my|gap|w|h)-\[(?:1|3|5|7|9|11|13|15|17|19|21|23)px\](?![a-zA-Z0-9_-])")
IMPORTANT_RE = re.compile(r"!\s*important\b")
CONTRACT_RE = re.compile(r"\b(?:interface|type)\s+([A-Z][A-Za-z0-9_]*Props|[A-Z][A-Za-z0-9_]*State)\b")
CLICHE_COPY_RE = re.compile(
    r"\b(?:unlock the power|next-gen seamless|10,000\+\s+teams|revolutionize your workflow|seamless integration)\b",
    re.IGNORECASE,
)


class NavigationRefactorProposal(BaseModel):
    """Structured Before vs. After UX navigation mutation proposal."""

    model_config = ConfigDict(extra="forbid")
    issue: str
    before_state: str
    after_proposal: str
    target_pattern: Literal["collapsible_sidebar_rail", "route_split", "bottom_bar_adaptive", "inspector_drawer"]


class FrontendInventoryReport(BaseModel):
    """Strict inventory and AI Slop diagnostic output."""

    model_config = ConfigDict(extra="forbid")
    verdict: Literal["[PASS]", "[WARN]", "[FAIL]", "[UNVERIFIED]"]
    target: str
    files_scanned: int
    detected_stack: list[str]
    tokens_defined_count: int
    tokens_sample: list[str]
    literal_hex_locations: list[str]
    oklch_count: int
    light_dark_count: int
    font_families: list[str]
    imported_icon_libs: list[str]
    inline_svg_count: int
    emoji_hits: int
    spacing_and_style_defects: list[str]
    component_contracts: list[str]
    navigation_targets: list[str]
    navigation_mermaid: str
    before_after_proposals: list[NavigationRefactorProposal]
    ai_slop_score: int = Field(ge=0, le=100)


def _detect_stack(root: Path, combined_text: str) -> list[str]:
    stack: list[str] = []
    pkg_file = (root if root.is_dir() else root.parent) / "package.json"
    if pkg_file.is_file():
        raw = pkg_file.read_text(encoding="utf-8", errors="ignore")
        pairs = (("next", "Next.js"), ("react", "React"), ("tailwindcss", "Tailwind CSS"), ("three", "Three.js"), ("framer-motion", "Motion"), ("motion", "Motion"), ("@xyflow/react", "@xyflow/react"))
        for key, label in pairs:
            if f'"{key}"' in raw and label not in stack:
                stack.append(label)
    if "@theme" in combined_text and "Tailwind v4 @theme" not in stack:
        stack.append("Tailwind v4 @theme")
    if "@layer " in combined_text:
        stack.append("CSS @layer")
    return stack or ["Static HTML/CSS/JS"]


def _build_navigation_artifacts(nav_targets: list[str], oversized_files: list[str], raw_text: str) -> tuple[str, list[NavigationRefactorProposal]]:
    unique = sorted(set(nav_targets))[:20]
    lines = ["flowchart LR", '  Root["Entry Shell"]']
    for idx, route in enumerate(unique or ["/main"]):
        safe = re.sub(r"[^a-zA-Z0-9_]", "_", route) or f"route_{idx}"
        lines.append(f'  Root --> N_{idx}_{safe}["{route}"]')
    proposals: list[NavigationRefactorProposal] = []
    if len(unique) > 5 or raw_text.count("<nav") > 3:
        proposals.append(NavigationRefactorProposal(
            issue="Top navigation density exceeds 5 primary slots",
            before_state=f"{len(unique)} routes / {raw_text.count('<nav')} <nav> containers competing horizontally",
            after_proposal="Consolidate into Single-DOM 256px Collapsible Sidebar Rail (>=48em) + 4-item Bottom Bar (<48em)",
            target_pattern="collapsible_sidebar_rail",
        ))
    if oversized_files:
        proposals.append(NavigationRefactorProposal(
            issue=f"UI module(s) exceed 600-line maintainability ceiling: {', '.join(oversized_files[:3])}",
            before_state=f"{len(oversized_files)} file(s) combining multiple concerns (>600 lines)",
            after_proposal="Decompose into cohesive <=600-line modules or child routes with <ol role='list'> breadcrumbs",
            target_pattern="route_split",
        ))
    return "\n".join(lines), proposals


def _scan_line_defects(rel: str, stripped: str, hex_locs: list[str], defects: list[str]) -> None:
    checks = (
        (_ss_core.PURE_BLACK_RE, "[OPTICS-NO-BLACK] pure #000000 black detected"),
        (OFF_GRID_TW_RE, "off-grid spacing"),
        (IMPORTANT_RE, "!important override"),
        (_ss_core.FLAT_SHADOW_RE, "single-pass flat rgba(0,0,0) shadow"),
        (CLICHE_COPY_RE, "generic AI SaaS copy cliché"),
        (_ss_core.NEON_GLOW_RE, "[OPTICS-NEON-GLOW] omnidirectional neon shadow/glow"),
        (_ss_core.SLOP_BLOB_RE, "[ANTI-SLOP-BLOB] decorative blur orb or organic bloop"),
        (_ss_core.SLOP_TOKEN_RE, "[ANTI-SLOP-TOKEN] cosmetic neon/gradient slop token"),
        (_ss_core.DASHED_BOX_SLOP_RE, "[ANTI-SLOP-WIREFRAME] dashed wireframe border detected"),
        (_ss_core.SHADOWED_FONT_STACK_RE, "[TYP-DEAD-FONT-FALLBACK] named font placed after generic family is unreachable"),
    )
    for ln, line in enumerate(stripped.splitlines(), 1):
        if hex_hit := HEX_COLOR_RE.search(line):
            hex_locs.append(f"{rel}:{ln} -> {hex_hit.group(0)}")
        for pattern, msg in checks:
            if pattern.search(line):
                defects.append(f"{rel}:{ln} {msg}")
    for m_grain in _ss_core.GRAIN_ABOVE_TEXT_RE.finditer(stripped):
        ln = stripped[: m_grain.start()].count("\n") + 1
        defects.append(f"{rel}:{ln} [OPTICS-GRAIN-ABOVE-TEXT] feTurbulence overlay missing z-index: -1")
    for msg in _ss_core.find_neon_violations(stripped):
        defects.append(f"{rel}:1 [OPTICS-NO-NEON] {msg}")
    for msg in _ss_core.inspect_inline_svgs(stripped):
        defects.append(f"{rel}:1 [AUDIT-VIS-BAD-SVG] {msg}")
    if "<feGaussianBlur" in stripped and "<feColorMatrix" in stripped and not any("ANTI-SLOP-BLOB" in d for d in defects):
        defects.append(f"{rel}:1 [ANTI-SLOP-BLOB] SVG gooey filter detected")


def _unverified_report(target_path: Path) -> FrontendInventoryReport:
    return FrontendInventoryReport(
        verdict="[UNVERIFIED]", target=str(target_path), files_scanned=0, detected_stack=[],
        tokens_defined_count=0, tokens_sample=[], literal_hex_locations=[], oklch_count=0,
        light_dark_count=0, font_families=[], imported_icon_libs=[], inline_svg_count=0,
        emoji_hits=0, spacing_and_style_defects=[], component_contracts=[], navigation_targets=[],
        navigation_mermaid="flowchart LR", before_after_proposals=[], ai_slop_score=0,
    )


def scan_frontend(target_path: Path) -> FrontendInventoryReport:
    """Scan frontend sources to inventory tokens, colors, fonts, menus, contracts, and AI Slop."""
    files = _ss_core.collect_ui_files(target_path)
    if not files:
        return _unverified_report(target_path)
    tokens, hex_locs, fonts, icon_libs, defects, contracts, nav_links = [], [], [], [], [], [], []
    oklch_n = ld_n = svg_n = emoji_n = 0
    chunks: list[str] = []
    stripped_chunks: list[str] = []
    oversized_files: list[str] = []
    base = target_path if target_path.is_dir() else target_path.parent
    for fp in files:
        text = fp.read_text(encoding="utf-8", errors="ignore")
        stripped = _ss_core.strip_comments(text)
        chunks.append(text)
        stripped_chunks.append(stripped)
        rel = fp.relative_to(base).as_posix() if fp.is_relative_to(base) else fp.name
        if len(text.splitlines()) > 600:
            oversized_files.append(rel)
        tokens.extend(VAR_DECL_RE.findall(stripped))
        oklch_n += len(OKLCH_RE.findall(stripped))
        ld_n += len(LIGHT_DARK_RE.findall(stripped))
        svg_n += stripped.count("<svg")
        emoji_n += len(_ss_core.EMOJI_RE.findall(stripped))
        fonts.extend(m.strip() for m in FONT_FAMILY_RE.findall(stripped))
        icon_libs.extend(IMPORT_ICON_RE.findall(stripped))
        contracts.extend(CONTRACT_RE.findall(stripped))
        no_use = re.sub(r"<use\b[^>]*>", "", stripped, flags=re.IGNORECASE)
        nav_links.extend(ROUTE_LINK_RE.findall(no_use))
        _scan_line_defects(rel, stripped, hex_locs, defects)

    unique_libs = sorted(set(icon_libs))
    if len(unique_libs) > 1:
        defects.append(f"global:1 mixed icon libraries ({', '.join(unique_libs)})")
    if _ss_core.has_confetti_badge_slop("\n".join(stripped_chunks)):
        defects.append("global:1 [ANTI-SLOP-CONFETTI] >=3 multicolored pill/badge variants; use neutral engraved-pill wells + 6px lum-bead")
    slop = min(100, min(30, emoji_n * 15) + min(55, len(defects) * 12) + (15 if oklch_n == 0 and hex_locs else 0))
    verdict: Literal["[PASS]", "[WARN]", "[FAIL]"] = "[PASS]" if slop <= 15 else ("[WARN]" if slop <= 40 else "[FAIL]")
    mermaid, proposals = _build_navigation_artifacts(nav_links, oversized_files, "\n".join(chunks))
    return FrontendInventoryReport(
        verdict=verdict, target=str(target_path), files_scanned=len(files),
        detected_stack=_detect_stack(target_path, "\n".join(chunks)),
        tokens_defined_count=len(set(tokens)), tokens_sample=sorted(set(tokens))[:30],
        literal_hex_locations=hex_locs[:30], oklch_count=oklch_n, light_dark_count=ld_n,
        font_families=sorted(set(fonts))[:15], imported_icon_libs=unique_libs,
        inline_svg_count=svg_n, emoji_hits=emoji_n, spacing_and_style_defects=defects[:30],
        component_contracts=sorted(set(contracts))[:25], navigation_targets=sorted(set(nav_links))[:25],
        navigation_mermaid=mermaid, before_after_proposals=proposals, ai_slop_score=slop,
    )


def _run_self_test() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        sample = Path(tmp) / "bad.html"
        sample.write_text(
            '<div class="p-[13px] blur-3xl" style="color:#000000;box-shadow:0 0 18px #00ffff;">🚀</div>',
            encoding="utf-8",
        )
        rep = scan_frontend(sample)
        assert rep.verdict == "[FAIL]" and rep.ai_slop_score >= 45 and rep.emoji_hits == 1
    print(json.dumps({"self_test": "FRONTEND_INVENTORY_ANALYST_OK"}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Forensic Frontend Inventory & AI Slop Scanner")
    parser.add_argument("target", nargs="?", default=None, help="Target frontend file or directory")
    parser.add_argument("--target", dest="target_flag", default=None, help="Explicit --target path")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    report = scan_frontend(_ss_core.resolve_cli_target(args.target, args.target_flag))
    print(report.model_dump_json(indent=2) if args.json else f"{report.verdict} slop={report.ai_slop_score}/100 files={report.files_scanned}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
