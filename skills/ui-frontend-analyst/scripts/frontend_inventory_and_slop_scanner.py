#!/usr/bin/env python3
"""Forensic frontend inventory, Mermaid navigation map, and AI Slop scanner."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal

from pydantic import BaseModel, ConfigDict, Field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FRONTEND_EXTS = {".html", ".css", ".scss", ".tsx", ".jsx", ".ts", ".vue"}
IGNORE_DIRS = {"node_modules", ".git", "dist", "build", ".next", "__pycache__", ".venv"}

VAR_DECL_RE = re.compile(r"(--[a-zA-Z0-9_-]+)\s*:")
HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
OKLCH_RE = re.compile(r"oklch\([^)]+\)")
LIGHT_DARK_RE = re.compile(r"light-dark\([^)]+\)")
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;}{]+)")
IMPORT_ICON_RE = re.compile(r"from\s+['\"](lucide-react|@heroicons[^'\"]*|phosphor-react|@tabler/icons[^'\"]*|react-icons[^'\"]*)['\"]")
ROUTE_LINK_RE = re.compile(r"""(?:href|to)=['"](/[^'"#?]*|#[a-zA-Z0-9_-]+)['"]""")
OFF_GRID_TW_RE = re.compile(r"\b(?:p|px|py|m|mx|my|gap|w|h)-\[(?:1|3|5|7|9|11|13|15|17|19|21|23)px\]")
IMPORTANT_RE = re.compile(r"!\s*important\b")
PURE_BLACK_RE = re.compile(r"(?:color|background(?:-color)?|fill|stroke|shadow|border|--[a-zA-Z0-9_-]+)\s*:[^;\n{}]*?(?:#000000\b|#000(?![0-9a-fA-F])|oklch\(\s*0(?:\.0+)?\s+0(?:\.0+)?\s+0\s*\))")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")
CONTRACT_RE = re.compile(r"\b(?:interface|type)\s+([A-Z][A-Za-z0-9_]*Props|[A-Z][A-Za-z0-9_]*State)\b")
FLAT_SHADOW_RE = re.compile(r"box-shadow\s*:\s*0\s+\d+px\s+\d+px\s+rgba?\(0\s*,\s*0\s*,\s*0")


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
    detected_stack: List[str]
    tokens_defined_count: int
    tokens_sample: List[str]
    literal_hex_locations: List[str]
    oklch_count: int
    light_dark_count: int
    font_families: List[str]
    imported_icon_libs: List[str]
    inline_svg_count: int
    emoji_hits: int
    spacing_and_style_defects: List[str]
    component_contracts: List[str]
    navigation_targets: List[str]
    navigation_mermaid: str
    before_after_proposals: List[NavigationRefactorProposal]
    ai_slop_score: int = Field(ge=0, le=100)


def _collect_files(target: Path) -> List[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() in FRONTEND_EXTS else []
    if not target.is_dir():
        return []
    files: List[Path] = []
    for item in sorted(target.rglob("*")):
        if item.is_file() and item.suffix.lower() in FRONTEND_EXTS:
            if not any(part in IGNORE_DIRS for part in item.parts):
                files.append(item)
    return files[:250]


def _detect_stack(root: Path, combined_text: str) -> List[str]:
    stack: List[str] = []
    pkg_file = (root if root.is_dir() else root.parent) / "package.json"
    if pkg_file.is_file():
        raw = pkg_file.read_text(encoding="utf-8", errors="ignore")
        for key, label in (("next", "Next.js"), ("react", "React"), ("tailwindcss", "Tailwind CSS"), ("three", "Three.js"), ("framer-motion", "Motion"), ("motion", "Motion"), ("@xyflow/react", "@xyflow/react")):
            if f'"{key}"' in raw and label not in stack:
                stack.append(label)
    if "@theme" in combined_text and "Tailwind v4 @theme" not in stack:
        stack.append("Tailwind v4 @theme")
    if "@layer " in combined_text:
        stack.append("CSS @layer")
    return stack or ["Static HTML/CSS/JS"]


def _build_navigation_artifacts(nav_targets: List[str], files_count: int, raw_text: str) -> tuple[str, List[NavigationRefactorProposal]]:
    unique = sorted(set(nav_targets))[:20]
    lines = ["flowchart LR", '  Root["Entry Shell"]']
    for idx, route in enumerate(unique or ["/main"]):
        safe = re.sub(r"[^a-zA-Z0-9_]", "_", route) or f"route_{idx}"
        lines.append(f'  Root --> N_{idx}_{safe}["{route}"]')
    proposals: List[NavigationRefactorProposal] = []
    if len(unique) > 5 or raw_text.count("<nav") > 3:
        proposals.append(NavigationRefactorProposal(
            issue="Top navigation density exceeds 5 primary slots",
            before_state=f"{len(unique)} routes / {raw_text.count('<nav')} <nav> containers competing horizontally",
            after_proposal="Consolidate into Single-DOM 256px Collapsible Sidebar Rail (>=48em) + 4-item Bottom Bar (<48em)",
            target_pattern="collapsible_sidebar_rail",
        ))
    if files_count == 1 and len(raw_text.splitlines()) > 450:
        proposals.append(NavigationRefactorProposal(
            issue="Monolithic single-page layout risks vertical overload",
            before_state="Single dense file combining multiple domains",
            after_proposal="Split secondary workflows into dedicated child routes with <ol role='list'> breadcrumbs",
            target_pattern="route_split",
        ))
    return "\n".join(lines), proposals


def _scan_line_defects(rel: str, text: str, hex_locs: List[str], defects: List[str]) -> None:
    """Record per-line literal hex locations and spacing/shadow/black anti-patterns."""
    checks = (
        (PURE_BLACK_RE, "pure #000000 black detected"),
        (OFF_GRID_TW_RE, "off-grid spacing"),
        (IMPORTANT_RE, "!important override"),
        (FLAT_SHADOW_RE, "single-pass flat rgba(0,0,0) shadow"),
    )
    for ln, line in enumerate(text.splitlines(), 1):
        hex_hit = HEX_COLOR_RE.search(line)
        if hex_hit:
            hex_locs.append(f"{rel}:{ln} -> {hex_hit.group(0)}")
        for pattern, msg in checks:
            if pattern.search(line):
                defects.append(f"{rel}:{ln} {msg}")


def scan_frontend(target_path: Path) -> FrontendInventoryReport:
    """Scan frontend sources to inventory tokens, colors, fonts, menus, contracts, and AI Slop."""
    files = _collect_files(target_path)
    if not files:
        return FrontendInventoryReport(
            verdict="[UNVERIFIED]", target=str(target_path), files_scanned=0, detected_stack=[],
            tokens_defined_count=0, tokens_sample=[], literal_hex_locations=[], oklch_count=0,
            light_dark_count=0, font_families=[], imported_icon_libs=[], inline_svg_count=0,
            emoji_hits=0, spacing_and_style_defects=[], component_contracts=[], navigation_targets=[],
            navigation_mermaid="flowchart LR", before_after_proposals=[], ai_slop_score=0,
        )
    tokens, hex_locs, fonts, icon_libs, defects, contracts, nav_links = [], [], [], [], [], [], []
    oklch_n = ld_n = svg_n = emoji_n = 0
    chunks: List[str] = []
    base = target_path if target_path.is_dir() else target_path.parent
    for fp in files:
        text = fp.read_text(encoding="utf-8", errors="ignore")
        chunks.append(text)
        rel = fp.relative_to(base).as_posix() if fp.is_relative_to(base) else fp.name
        tokens.extend(VAR_DECL_RE.findall(text))
        oklch_n += len(OKLCH_RE.findall(text))
        ld_n += len(LIGHT_DARK_RE.findall(text))
        svg_n += text.count("<svg")
        emoji_n += len(EMOJI_RE.findall(text))
        fonts.extend(m.strip() for m in FONT_FAMILY_RE.findall(text))
        icon_libs.extend(IMPORT_ICON_RE.findall(text))
        contracts.extend(CONTRACT_RE.findall(text))
        nav_links.extend(ROUTE_LINK_RE.findall(text))
        _scan_line_defects(rel, text, hex_locs, defects)

    slop = min(100, min(30, emoji_n * 15) + min(25, len(defects) * 10) + (15 if oklch_n == 0 and hex_locs else 0))
    verdict: Literal["[PASS]", "[WARN]", "[FAIL]"] = "[PASS]" if slop <= 15 else ("[WARN]" if slop <= 40 else "[FAIL]")
    mermaid, proposals = _build_navigation_artifacts(nav_links, len(files), "\n".join(chunks))
    return FrontendInventoryReport(
        verdict=verdict, target=str(target_path), files_scanned=len(files),
        detected_stack=_detect_stack(target_path, "\n".join(chunks)),
        tokens_defined_count=len(set(tokens)), tokens_sample=sorted(set(tokens))[:30],
        literal_hex_locations=hex_locs[:30], oklch_count=oklch_n, light_dark_count=ld_n,
        font_families=sorted(set(fonts))[:15], imported_icon_libs=sorted(set(icon_libs)),
        inline_svg_count=svg_n, emoji_hits=emoji_n, spacing_and_style_defects=defects[:30],
        component_contracts=sorted(set(contracts))[:25], navigation_targets=sorted(set(nav_links))[:25],
        navigation_mermaid=mermaid, before_after_proposals=proposals, ai_slop_score=slop,
    )


def _run_self_test() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        sample = Path(tmp) / "bad.html"
        sample.write_text('<div class="p-[13px]" style="color:#000000;box-shadow:0 4px 12px rgba(0,0,0,0.4);">🚀</div>', encoding="utf-8")
        rep = scan_frontend(sample)
        assert rep.verdict != "[PASS]" and rep.ai_slop_score >= 40 and rep.emoji_hits == 1
    print(json.dumps({"self_test": "FRONTEND_INVENTORY_ANALYST_OK"}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Forensic Frontend Inventory & AI Slop Scanner")
    parser.add_argument("--target", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _run_self_test()
    report = scan_frontend(Path(args.target).resolve())
    print(report.model_dump_json(indent=2) if args.json else f"{report.verdict} slop={report.ai_slop_score}/100 files={report.files_scanned}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
