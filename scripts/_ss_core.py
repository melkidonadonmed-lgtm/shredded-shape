#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Shared pure-stdlib optical, WCAG 2.2 OKLab, and anti-slop kernel for shredded-shape."""

from __future__ import annotations

import colorsys
import math
import re
from pathlib import Path

UI_EXTS = frozenset({".html", ".css", ".scss", ".tsx", ".jsx", ".ts", ".js", ".mjs", ".vue"})
IGNORED_DIRS = frozenset({
    "node_modules", ".git", "dist", "build", ".next", "coverage",
    "__pycache__", ".venv", "venv", ".pytest_cache", ".ruff_cache",
    "playwright-report", ".storybook", "__mocks__",
})
TEST_ONLY_DIRS = frozenset({"__tests__", "tests", "__mocks__"})
_TEST_FILE_RE = re.compile(r"(?:\.test|\.spec|\.stories|\.story)\.[^.]+$", re.IGNORECASE)

CHROMA_WARN = 0.20
CHROMA_CRITICAL = 0.22
CHROMA_DANGER_MAX = 0.24

VALID_SPACING_PX = frozenset({
    0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48,
    56, 64, 72, 80, 96, 112, 128, 240, 256, 260, 280, 320,
})

STYLE_PRESETS: dict[str, dict[str, str]] = {
    "soft": {"radius": "1.35rem", "chroma_cap": "0.12", "menu": "rounded_pill_sidebar", "font": "Plus Jakarta Sans", "spatial": "bento_12_col"},
    "hi-tech": {"radius": "0.375rem", "chroma_cap": "0.14", "menu": "precision_rail_2px", "font": "Space Grotesk", "spatial": "command_center_grid"},
    "tactile": {"radius": "1.0rem", "chroma_cap": "0.16", "menu": "tactile_48px_rail", "font": "Plus Jakarta Sans", "spatial": "workbench_split_view"},
    "elevated": {"radius": "1.10rem", "chroma_cap": "0.15", "menu": "frosted_sticky_header", "font": "Inter", "spatial": "bento_12_col"},
    "retro": {"radius": "0.25rem", "chroma_cap": "0.17", "menu": "geometric_block_tabs", "font": "Space Grotesk", "spatial": "workbench_split_view"},
    "vintage": {"radius": "0.50rem", "chroma_cap": "0.11", "menu": "editorial_toc_65ch", "font": "Instrument Serif", "spatial": "editorial_65ch"},
    "clinical": {"radius": "0.50rem", "chroma_cap": "0.12", "menu": "ehr_3click_sidebar", "font": "IBM Plex Sans", "spatial": "workbench_split_view"},
}

STYLE_SPATIAL_DEFAULTS: dict[str, str] = {k: v["spatial"] for k, v in STYLE_PRESETS.items()}
STYLE_ALIASES: dict[str, str] = {"hitech": "hi-tech"}

_TOKENIZER_RE = re.compile(
    r'(?P<str>"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|`(?:\\.|[^`\\])*`)'
    r"|(?P<cmt>/\*[\s\S]*?\*/|<!--[\s\S]*?-->|(?<!:)//[^\n]*)"
)
_LINK_TAG_RE = re.compile(r"<link\b([^>]*)>", re.IGNORECASE)
_LINK_STYLE_REL_RE = re.compile(r"""\brel\s*=\s*["'][^"']*\bstylesheet\b""", re.IGNORECASE)
_SCRIPT_TAG_RE = re.compile(r"<script\b([^>]*)>", re.IGNORECASE)
_ATTR_REF_RE = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
_EXTERNAL_REF_PREFIXES = ("http://", "https://", "//", "data:", "javascript:", "mailto:", "#")

REFLOW_TRANSITION_RE = re.compile(
    r"transition(?:-property)?\s*:[^;}{]*(?<![a-zA-Z-])"
    r"(all|(?:max-|min-)?(?:width|height)|inline-size|block-size|padding(?:-[a-z-]+)?|margin(?:-[a-z-]+)?|top|left|right|bottom|inset(?:-[a-z-]+)?)"
    r"(?![a-zA-Z-])",
    re.IGNORECASE,
)
COLOR_MIX_OKLCH_WARN_RE = re.compile(r"color-mix\(\s*in\s+oklch\b", re.IGNORECASE)
GRAIN_ABOVE_TEXT_RE = re.compile(
    r"::(?:after|before)[^{};]*\{(?![^}]*z-index\s*:\s*-\d+)[^}]*feTurbulence[^}]*\}",
    re.IGNORECASE | re.DOTALL,
)
SHADOWED_FONT_STACK_RE = re.compile(
    r"font-family\s*:\s*[^;}{]*\b(?:ui-monospace|monospace|sans-serif|serif)\s*,\s*['\"][A-Za-z]",
    re.IGNORECASE,
)
OPAQUE_LIGHT_KEY_RE = re.compile(
    r"--light-key\s*:[^;{}]*light-dark\(\s*oklch\(\s*(?:1(?:\.0+)?|0\.9\d+)\s+[0-9.]+\s+[0-9.]+\s*\)",
    re.IGNORECASE,
)

PURE_BLACK_RE = re.compile(
    r"(?:color|background(?:-color)?|backgroundColor|fill|stroke|border|--[a-zA-Z0-9_-]+)\s*:\s*['\"]?"
    r"(?:#000000\b|#000(?![0-9a-fA-F])|oklch\(\s*0(?:\.0+)?%?\s+0(?:\.0+)?%?\s+[0-9.]+\s*\))"
    r"|(?<![a-zA-Z0-9_-])bg-(?:black|\[#000(?:000)?\])(?![a-zA-Z0-9_-])"
)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\U000026A0-\U000026FF\U00002702-\U00002712\U00002728-\U000027B0]")
ROW_REVERSE_RE = re.compile(
    r"(?<![a-zA-Z0-9_-])(?:flex-direction\s*:\s*row-reverse|flexDirection\s*:\s*['\"]row-reverse['\"]"
    r"|flex-row-reverse|order\s*:\s*-?[1-9]\d*|order-[1-9]\d*)(?![a-zA-Z0-9_-])"
)
FLAT_SHADOW_RE = re.compile(
    r"box-shadow\s*:\s*0(?:px)?\s+\d+px\s+\d+px\s+rgba?\(\s*0\s*,\s*0\s*,\s*0[^,;{}]*\)\s*(?:;|})"
)
NEON_GLOW_RE = re.compile(
    r"(?:box-shadow\s*:[^;{}]*?\b0(?:px)?\s+0(?:px)?\s+(?:1[2-9]|[2-9]\d|\d{3,})px"
    r"(?:\s+(?:0(?:px)?|[1-9]\d*px))?\s+(?:#[0-9a-fA-F]{3,8}|rgba?\([^)]*,\s*(?:1(?:\.0+)?|0\.[3-9]\d*)\)"
    r"|rgb\([^)]+\)|hsl\([^)]+\)|oklch\(\s*[0-9.]+%?\s+0\.(?:2[1-9]|[3-9]\d)[^)]*\)))"
    r"|(?:text-shadow\s*:\s*0(?:px)?\s+0(?:px)?\s+(?:[89]|[1-9]\d+)px)"
    r"|(?:drop-shadow\(\s*0(?:px)?\s+0(?:px)?\s+(?:1[0-9]|[2-9]\d+)px\s+"
    r"(?:#[0-9a-fA-F]{3,8}|rgba?\([^)]*,\s*(?:1(?:\.0+)?|0\.[3-9]\d*)\)|oklch\(\s*[0-9.]+%?\s+0\.(?:2[1-9]|[3-9]\d)))",
    re.IGNORECASE,
)
SLOP_BLOB_RE = re.compile(
    r"(?<!backdrop-)filter\s*:\s*blur\(\s*(?:[4-9]\d|\d{3,})px\s*\)"
    r"|(?<![a-zA-Z0-9_-])(?:animate-blob|blur-3xl)(?![a-zA-Z0-9_-])"
    r"|(?<![a-zA-Z0-9_-])blur-2xl(?![a-zA-Z0-9_-])(?=[^\"'>]*\b(?:rounded-full|bg-gradient-to|pointer-events-none|opacity-))"
    r"|border-radius\s*:\s*\d+%\s+\d+%\s+\d+%\s+\d+%\s*/\s*\d+%"
    r"|<feGaussianBlur[\s\S]{0,240}<feColorMatrix",
    re.IGNORECASE,
)
SLOP_TOKEN_RE = re.compile(
    r"(?<![a-zA-Z0-9_-])from-(?:indigo|purple|violet|fuchsia)-[456]00\b[^\n\"'}]*\b(?:via|to)-(?:indigo|purple|violet|pink|fuchsia)-[456]00(?![a-zA-Z0-9_-])"
    r"|--(?:neon|glow|blob|bloop|cyber|ai-gradient)-[a-z0-9_-]+",
    re.IGNORECASE,
)
DASHED_BOX_SLOP_RE = re.compile(
    r"border(?:-(?:top|bottom|left|right|block|inline))?\s*:\s*[12]px\s+dashed\b"
    r"|(?<![a-zA-Z0-9_-])border-dashed(?![a-zA-Z0-9_-])",
    re.IGNORECASE,
)
_CONFETTI_CSS_RE = re.compile(
    r"\.[a-z0-9_-]*(?:tag|badge|pill|chip)[a-z0-9_-]*\.(warn|warning|danger|error|ok|success|info|cyan|amber|emerald|rose|violet|purple)\b"
    r"|\.(?:tag|badge|pill|chip)-(warn|warning|danger|error|ok|success|info|cyan|amber|emerald|rose|violet|purple)\b",
    re.IGNORECASE,
)
_CONFETTI_TW_RE = re.compile(
    r"(?<![a-zA-Z0-9_-])bg-(amber|yellow|emerald|green|rose|red|sky|cyan|indigo|purple|violet)-500/(?:10|15|20)\b",
    re.IGNORECASE,
)
_OKLCH_VAL_RE = re.compile(r"oklch\(\s*([0-9.]+)(%?)\s+([0-9.]+)(%?)\s+([0-9.]+)")
_HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
_HSL_NEON_RE = re.compile(r"hsl\(\s*\d+\s*,\s*(?:9[5-9]|100)%\s*,\s*(?:4[5-9]|5[0-9]|60)%\s*\)", re.IGNORECASE)
_SVG_BLOCK_RE = re.compile(r"<svg\b([^>]*)>([\s\S]*?)</svg>", re.IGNORECASE)
_SVG_CHILD_RE = re.compile(r"<(?:path|rect|circle|ellipse|line|polyline|polygon|use|g|text|title)\b", re.IGNORECASE)


def is_valid_spacing_px(px: int) -> bool:
    """Return True when px fits the 4px/8px Stitch scale or canonical chrome dimensions."""
    return px in VALID_SPACING_PX or (px >= 16 and px % 4 == 0)


def strip_comments(source: str) -> str:
    """Strip CSS/JS/HTML comments while keeping string literals and exact line numbers."""
    def _repl(match: re.Match[str]) -> str:
        if match.group("str") is not None:
            return match.group(0)
        return re.sub(r"[^\n]", " ", match.group("cmt"))
    return _TOKENIZER_RE.sub(_repl, source)


def resolve_cli_target(pos_target: str | None, flag_target: str | None, default: str = ".") -> Path:
    """Resolve CLI target path with explicit --target/--scope precedence over positional arg."""
    raw = (flag_target or pos_target or default).strip()
    return Path(raw).expanduser().resolve()


def normalize_style_archetype(raw: str) -> str:
    """Normalize style aliases (e.g., hitech -> hi-tech) into canonical StyleArchetype slugs."""
    key = raw.strip().lower()
    return STYLE_ALIASES.get(key, key)


def _is_eligible_ui_file(path: Path, target: Path, include_tests: bool) -> bool:
    if not path.is_file() or path.suffix.lower() not in UI_EXTS:
        return False
    if IGNORED_DIRS.intersection(path.parts):
        return False
    return include_tests or not _is_test_or_story_file(path, target)


def collect_ui_files_scoped(
    target: Path, limit: int = 500, include_tests: bool = False
) -> tuple[list[Path], int, bool]:
    """Collect UI files plus total eligible count and truncation status, excluding test suites by default."""
    if target.is_file():
        if target.suffix.lower() not in UI_EXTS:
            return [], 0, False
        files = _collect_html_linked_files(target) if target.suffix.lower() == ".html" else [target]
        return files[:limit], len(files), len(files) > limit
    if not target.is_dir():
        return [], 0, False
    eligible = [p for p in sorted(target.rglob("*")) if _is_eligible_ui_file(p, target, include_tests)]
    return eligible[:limit], len(eligible), len(eligible) > limit


def _is_test_or_story_file(path: Path, root: Path) -> bool:
    """Return True when file lives inside a test directory under root or uses test/story naming."""
    try:
        rel_parts = path.relative_to(root).parts[:-1]
    except ValueError:
        rel_parts = ()
    return any(part in TEST_ONLY_DIRS for part in rel_parts) or bool(_TEST_FILE_RE.search(path.name))


def _collect_html_linked_files(target: Path) -> list[Path]:
    """Collect a single HTML entrypoint and its safe relative stylesheets/scripts."""
    files = [target]
    cleaned = strip_comments(target.read_text(encoding="utf-8", errors="ignore"))
    root = target.parent.resolve()
    rels = [
        m.group(1) for attrs in _LINK_TAG_RE.findall(cleaned)
        if _LINK_STYLE_REL_RE.search(attrs) and (m := _ATTR_REF_RE.search(attrs))
    ] + [
        m.group(1) for attrs in _SCRIPT_TAG_RE.findall(cleaned)
        if (m := _ATTR_REF_RE.search(attrs))
    ]
    for rel in rels:
        if rel.lower().startswith(_EXTERNAL_REF_PREFIXES):
            continue
        local_rel = rel.split("#", 1)[0].split("?", 1)[0].strip()
        if not local_rel:
            continue
        cand = (root / local_rel).resolve()
        if cand.is_file() and cand.is_relative_to(root) and cand not in files:
            files.append(cand)
    return files


def collect_ui_files(target: Path, limit: int = 250, include_tests: bool = False) -> list[Path]:
    """Collect UI files from a file (with local HTML assets) or directory, skipping test suites and build caches."""
    files, _, _ = collect_ui_files_scoped(target, limit=limit, include_tests=include_tests)
    return files


def oklch_to_relative_luminance(l_val: float, c_val: float = 0.0, h_deg: float = 0.0) -> float:
    """Convert OKLCH (L, C, H) via Bjorn Ottosson OKLab->LMS^3->linear sRGB to CIE 1931 Y."""
    l_clamped = max(0.0, min(1.0, l_val))
    rad = math.radians(h_deg)
    a_ok = c_val * math.cos(rad)
    b_ok = c_val * math.sin(rad)
    l_ = l_clamped + 0.3963377774 * a_ok + 0.2158037573 * b_ok
    m_ = l_clamped - 0.1055613458 * a_ok - 0.0638541728 * b_ok
    s_ = l_clamped - 0.0894841775 * a_ok - 1.2914855480 * b_ok
    l3, m3, s3 = l_ ** 3, m_ ** 3, s_ ** 3
    r_lin = max(0.0, min(1.0, +4.0767416621 * l3 - 3.3077115913 * m3 + 0.2309699292 * s3))
    g_lin = max(0.0, min(1.0, -1.2684380046 * l3 + 2.6097574011 * m3 - 0.3413193965 * s3))
    b_lin = max(0.0, min(1.0, -0.0041960863 * l3 - 0.7034186147 * m3 + 1.7076147010 * s3))
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def calculate_oklch_contrast(
    l_fg: float, l_bg: float, c_fg: float = 0.0, h_fg: float = 0.0, c_bg: float = 0.0, h_bg: float = 0.0
) -> float:
    """Compute WCAG 2.2 contrast ratio from two OKLCH colors."""
    y1 = oklch_to_relative_luminance(l_fg, c_fg, h_fg)
    y2 = oklch_to_relative_luminance(l_bg, c_bg, h_bg)
    return round((max(y1, y2) + 0.05) / (min(y1, y2) + 0.05), 2)


def _srgb_channel_to_linear(val_8bit: int) -> float:
    norm = val_8bit / 255.0
    return norm / 12.92 if norm <= 0.04045 else ((norm + 0.055) / 1.055) ** 2.4


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Parse #RGB or #RRGGBB hex string into 8-bit RGB channels."""
    clean = hex_color.lstrip("#")
    if len(clean) == 3:
        clean = "".join(ch * 2 for ch in clean)
    return int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16)


def hex_contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    """Compute WCAG 2.2 contrast ratio for two #RGB/#RRGGBB colors."""
    def _lum(hx: str) -> float:
        r, g, b = hex_to_rgb(hx)
        return 0.2126 * _srgb_channel_to_linear(r) + 0.7152 * _srgb_channel_to_linear(g) + 0.0722 * _srgb_channel_to_linear(b)
    y1, y2 = _lum(fg_hex), _lum(bg_hex)
    return round((max(y1, y2) + 0.05) / (min(y1, y2) + 0.05), 2)


def srgb_to_oklch(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Convert 8-bit sRGB channels into perceptual OKLCH (L, C, H)."""
    rl, gl, bl = _srgb_channel_to_linear(r), _srgb_channel_to_linear(g), _srgb_channel_to_linear(b)
    l_ = math.cbrt(max(0.0, 0.4122214708 * rl + 0.5363325363 * gl + 0.0514459929 * bl))
    m_ = math.cbrt(max(0.0, 0.2119034982 * rl + 0.6806995451 * gl + 0.1073969566 * bl))
    s_ = math.cbrt(max(0.0, 0.0883024619 * rl + 0.2817188376 * gl + 0.6299787005 * bl))
    l_ok = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a_ok = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b_ok = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    chroma = math.hypot(a_ok, b_ok)
    hue = math.degrees(math.atan2(b_ok, a_ok)) % 360.0
    return l_ok, chroma, hue


def _find_oklch_neons(stripped_text: str) -> list[str]:
    hits: list[str] = []
    for l_s, l_pct, c_s, c_pct, h_s in _OKLCH_VAL_RE.findall(stripped_text):
        l_val = float(l_s) / 100.0 if l_pct else float(l_s)
        c_val = (float(c_s) * 0.4 / 100.0) if c_pct else float(c_s)
        h_val = float(h_s) % 360.0
        cap = CHROMA_DANGER_MAX if 15.0 <= h_val <= 40.0 else CHROMA_CRITICAL
        if c_val > cap and l_val > 0.35:
            hits.append(f"High-chroma neon oklch(L={l_val:.2f}, C={c_val:.2f}, H={h_val:.0f}) > {cap:.2f}")
    return hits


def _is_fluo_hex(r: int, g: int, b: int, s_hsl: float, l_hsl: float) -> bool:
    return s_hsl >= 0.99 and 0.45 <= l_hsl <= 0.65 and min(r, g, b) <= 25 and max(r, g, b) >= 245


def _find_hex_neons(stripped_text: str) -> list[str]:
    hits: list[str] = []
    for hx in _HEX_RE.findall(stripped_text):
        r, g, b = hex_to_rgb(hx)
        _, l_hsl, s_hsl = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        l_ok, c_ok, h_ok = srgb_to_oklch(r, g, b)
        cap = CHROMA_DANGER_MAX if 15.0 <= h_ok <= 40.0 else CHROMA_CRITICAL
        if _is_fluo_hex(r, g, b, s_hsl, l_hsl) or (l_ok > 0.55 and c_ok > cap):
            hits.append(f"High-chroma neon hex {hx} (OKLCH C={c_ok:.2f}, HSL S={s_hsl:.2f})")
    return hits


def find_neon_violations(stripped_text: str) -> list[str]:
    """Detect high-chroma neon oklch(), fluorescent #hex, and saturated hsl() colors."""
    hits = _find_oklch_neons(stripped_text) + _find_hex_neons(stripped_text)
    if _HSL_NEON_RE.search(stripped_text):
        hits.append("Saturated fluorescent hsl() color detected")
    return hits


def _is_exempt_svg_block(attrs: str, body: str) -> bool:
    low_body = body.lower()
    if "<symbol" in low_body or "<defs" in low_body:
        return True
    if re.search(r"\bhidden\b|\bwidth\s*=\s*['\"]0['\"]|role\s*=\s*['\"]img['\"]|data-chart", attrs, re.IGNORECASE):
        return True
    vb_m = re.search(r"viewBox\s*=\s*['\"][^'\"]*\b(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)['\"]", attrs, re.IGNORECASE)
    return bool(vb_m and max(float(vb_m.group(1)), float(vb_m.group(2))) >= 48 and float(vb_m.group(1)) != 960)


def _has_solid_fill(attrs: str) -> bool:
    low = attrs.lower()
    return 'fill="none"' not in low and "fill='none'" not in low


def _is_bloop_circle_cloud(attrs: str, body: str) -> bool:
    circles = re.findall(r"<circle\b([^>]*)/?>", body, re.IGNORECASE)
    if len(circles) < 3 or re.search(r"<(?:path|line|polyline)\b", body, re.IGNORECASE):
        return False
    if _has_solid_fill(attrs):
        return True
    for c in circles:
        if "fill=" in c.lower() and _has_solid_fill(c):
            return True
        r_m = re.search(r"\br\s*=\s*['\"]([0-9.]+)", c)
        if r_m and float(r_m.group(1)) >= 4.0:
            return True
    return False


def _inspect_single_svg(attrs: str, body: str) -> list[str]:
    if _is_exempt_svg_block(attrs, body):
        return []
    issues: list[str] = []
    has_use = bool(re.search(r"<use\b", body, re.IGNORECASE))
    if not has_use and not _SVG_CHILD_RE.search(body) and "{" not in body:
        return ["Empty inline <svg> element with zero vector geometry"]
    if not has_use and not re.search(r"\bviewBox\s*=", attrs, re.IGNORECASE):
        issues.append("Inline UI icon <svg> missing viewBox attribute")
    if re.search(r"<path\b[^>]*\bd\s*=\s*['\"]\s*(?:NaN|undefined)?\s*['\"]", body, re.IGNORECASE):
        issues.append("Corrupted or empty <path d=...> inside inline <svg>")
    if _is_bloop_circle_cloud(attrs, body):
        issues.append("Amateur multi-circle bloop-cloud <svg> detected; use verified Lucide/Material SVG paths")
    return issues


def inspect_inline_svgs(stripped_text: str) -> list[str]:
    """Flag empty inline <svg>, missing viewBox on UI icons, and bloop-cloud circle clusters."""
    issues: list[str] = []
    for attrs, body in _SVG_BLOCK_RE.findall(stripped_text):
        issues.extend(_inspect_single_svg(attrs, body))
    return issues


def has_confetti_badge_slop(stripped_text: str) -> bool:
    """Return True when >=3 distinct multicolored pill/badge tint classes create confetti slop."""
    css_tints = {g.lower() for pair in _CONFETTI_CSS_RE.findall(stripped_text) for g in pair if g}
    tw_tints = {t.lower() for t in _CONFETTI_TW_RE.findall(stripped_text)}
    return len(css_tints) >= 3 or len(tw_tints) >= 3


_TRACKED_TOK_PART = (
    r"--(?:(?:ink|text)-(?:primary|secondary|muted|on-key|on-brand)"
    r"|(?:surface|bg)-(?:canvas|well|sunken|card|card-lit|elevated|key|surface-1|surface-2)"
    r"|brand-(?:primary|fill))"
)
_HUE_PART = r"([0-9.]+|var\(\s*--[a-zA-Z0-9_-]+\s*\))"
_LD_TOK_RE = re.compile(
    rf"({_TRACKED_TOK_PART})\s*:\s*light-dark\(\s*"
    rf"oklch\(\s*([0-9.]+)(%?)\s+([0-9.]+)(%?)\s+{_HUE_PART}[^)]*\)\s*,\s*"
    rf"oklch\(\s*([0-9.]+)(%?)\s+([0-9.]+)(%?)\s+{_HUE_PART}[^)]*\)",
    re.IGNORECASE,
)
_SINGLE_TOK_RE = re.compile(
    rf"({_TRACKED_TOK_PART})\s*:\s*oklch\(\s*([0-9.]+)(%?)\s+([0-9.]+)(%?)\s+{_HUE_PART}[^)]*\)",
    re.IGNORECASE,
)
_BRAND_HUE_NUM_RE = re.compile(r"--brand-hue\s*:\s*([0-9]+(?:\.[0-9]+)?)\b", re.IGNORECASE)
_VAR_ALIAS_RE = re.compile(rf"({_TRACKED_TOK_PART})\s*:\s*var\(\s*(--[a-zA-Z0-9_-]+)", re.IGNORECASE)
_COLOR_SCHEME_RE = re.compile(r"color-scheme\s*:\s*(dark|light)\b", re.IGNORECASE)
_DATA_THEME_SEL_RE = re.compile(r"""\[data-theme\s*=\s*['"]([a-zA-Z0-9_-]+)['"]\]""", re.IGNORECASE)
_MEDIA_SCHEME_RE = re.compile(r"prefers-color-scheme\s*:\s*(dark|light)", re.IGNORECASE)


def _norm_ok(val: str, pct: str, scale: float = 1.0) -> float:
    num = float(val)
    return (num * scale / 100.0) if pct else num


def _parse_hue(raw_hue: str, default_hue: float = 255.0) -> float:
    text = raw_hue.strip()
    if text.lower().startswith("var("):
        return default_hue
    return float(text)


def _iter_css_blocks(stripped: str) -> list[tuple[str, str, str]]:
    """Extract (media_ctx, selector, declarations_body) pairs from HTML/CSS safely."""
    no_scripts = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", " ", stripped, flags=re.IGNORECASE)
    css_text = re.sub(r"</?style\b[^>]*>", "\n", no_scripts, flags=re.IGNORECASE)
    return _scan_css_blocks(css_text)


def _pop_css_block(
    stack: list[tuple[str, list[str]]], buf: list[str], blocks: list[tuple[str, str, str]]
) -> None:
    if len(stack) <= 1:
        return
    if buf:
        stack[-1][1].append("".join(buf))
    hdr, parts = stack.pop()
    ctx = " | ".join(h for h, _ in stack if h.startswith("@"))
    blocks.append((ctx, hdr, "".join(parts)))


def _scan_css_blocks(css_text: str) -> list[tuple[str, str, str]]:
    stack: list[tuple[str, list[str]]] = [("", [])]
    blocks: list[tuple[str, str, str]] = []
    buf: list[str] = []
    for ch in css_text:
        if ch == "{":
            stack.append(("".join(buf).strip(), []))
            buf.clear()
        elif ch == "}":
            _pop_css_block(stack, buf, blocks)
            buf.clear()
        elif ch == ";":
            stack[-1][1].append("".join(buf) + ";")
            buf.clear()
        else:
            buf.append(ch)
    return blocks


def _resolve_var_aliases(vals: dict[str, tuple[float, float, float]], aliases: dict[str, str], locked: set[str] | None = None) -> dict[str, tuple[float, float, float]]:
    out = dict(vals)
    skip = locked or set()
    for _ in range(3):
        for tok, ref in aliases.items():
            if tok not in skip and ref in out:
                out[tok] = out[ref]
    return out


def _classify_theme_scope(media_ctx: str, selector: str) -> str:
    if m := _DATA_THEME_SEL_RE.search(selector):
        return f"theme:{m.group(1).lower()}"
    if re.search(r"(?:^|[\s,])\.dark\b", selector):
        return "theme:dark"
    if re.search(r"(?:^|[\s,])\.light\b", selector):
        return "theme:light"
    if mm := _MEDIA_SCHEME_RE.search(media_ctx):
        return f"media:{mm.group(1).lower()}"
    if re.match(r"^(?:@theme|:root|html|body|:host)\b", selector.strip(), re.IGNORECASE):
        return "root"
    return "other"


def _infer_polarity(bucket_name: str, body_scheme: str | None, vals: dict[str, tuple[float, float, float]]) -> str:
    if body_scheme in {"dark", "light"}:
        return body_scheme
    low = bucket_name.lower()
    if re.search(r"dark|night|obsidian|matte", low):
        return "dark"
    if "light" in low or "day" in low:
        return "light"
    for surf in ("--bg-canvas", "--surface-canvas", "--bg-card", "--surface-card"):
        if surf in vals:
            return "dark" if vals[surf][0] < 0.50 else "light"
    return "light"


def _resolve_root_maps(
    root_light: dict[str, tuple[float, float, float]],
    root_dark: dict[str, tuple[float, float, float]],
    root_single: dict[str, tuple[float, float, float]],
    root_aliases: dict[str, str],
    root_scheme: str | None,
) -> tuple[dict[str, tuple[float, float, float]], dict[str, tuple[float, float, float]]]:
    if root_single:
        pol = _infer_polarity("root", root_scheme, root_single)
        target_root = root_dark if pol == "dark" else root_light
        for k, v in root_single.items():
            target_root.setdefault(k, v)
    resolved_light = _resolve_var_aliases(root_light, root_aliases) if root_light else {}
    resolved_dark = _resolve_var_aliases(root_dark, root_aliases) if root_dark else {}
    return resolved_light, resolved_dark


def _merge_extracted_themes(
    root_light: dict[str, tuple[float, float, float]],
    root_dark: dict[str, tuple[float, float, float]],
    root_single: dict[str, tuple[float, float, float]],
    root_aliases: dict[str, str],
    root_scheme: str | None,
    themes: dict[str, dict[str, object]],
) -> dict[str, dict[str, tuple[float, float, float]]]:
    resolved_light, resolved_dark = _resolve_root_maps(root_light, root_dark, root_single, root_aliases, root_scheme)
    maps: dict[str, dict[str, tuple[float, float, float]]] = {}
    if resolved_light:
        maps["root:light"] = resolved_light
    if resolved_dark:
        maps["root:dark"] = resolved_dark
    for scope, data in themes.items():
        vals: dict[str, tuple[float, float, float]] = data["vals"]  # type: ignore[assignment]
        t_aliases: dict[str, str] = data["aliases"]  # type: ignore[assignment]
        if not vals and not t_aliases:
            continue
        pol = _infer_polarity(scope, data["scheme"], vals)  # type: ignore[arg-type]
        base = resolved_dark if pol == "dark" else resolved_light
        maps[f"{scope}:{pol}"] = _resolve_var_aliases({**base, **vals}, {**root_aliases, **t_aliases}, locked=set(vals))
    return maps


def _extract_block_oklch_tokens(
    body: str, blk_hue: float, root_light: dict[str, tuple[float, float, float]], root_dark: dict[str, tuple[float, float, float]]
) -> tuple[dict[str, tuple[float, float, float]], dict[str, str]]:
    ld_keys: set[str] = set()
    for m in _LD_TOK_RE.finditer(body):
        tok = m.group(1).lower()
        ld_keys.add(tok)
        root_light[tok] = (_norm_ok(m.group(2), m.group(3)), _norm_ok(m.group(4), m.group(5), 0.4), _parse_hue(m.group(6), blk_hue))
        root_dark[tok] = (_norm_ok(m.group(7), m.group(8)), _norm_ok(m.group(9), m.group(10), 0.4), _parse_hue(m.group(11), blk_hue))
    singles = {
        m.group(1).lower(): (_norm_ok(m.group(2), m.group(3)), _norm_ok(m.group(4), m.group(5), 0.4), _parse_hue(m.group(6), blk_hue))
        for m in _SINGLE_TOK_RE.finditer(body)
        if m.group(1).lower() not in ld_keys
    }
    aliases = {m.group(1).lower(): m.group(2).lower() for m in _VAR_ALIAS_RE.finditer(body)}
    return singles, aliases


def _record_scoped_tokens(
    scope: str,
    body: str,
    singles: dict[str, tuple[float, float, float]],
    aliases: dict[str, str],
    root_single: dict[str, tuple[float, float, float]],
    root_aliases: dict[str, str],
    themes: dict[str, dict[str, object]],
    root_scheme: str | None,
) -> str | None:
    scheme_m = _COLOR_SCHEME_RE.search(body)
    scheme_val = scheme_m.group(1).lower() if scheme_m else None
    if scope == "root":
        root_single.update(singles)
        root_aliases.update(aliases)
        return scheme_val if scheme_val in {"dark", "light"} and "light dark" not in body.lower() else root_scheme
    bucket = themes.setdefault(scope, {"vals": {}, "aliases": {}, "scheme": None})
    bucket["vals"].update(singles)  # type: ignore[union-attr]
    bucket["aliases"].update(aliases)  # type: ignore[union-attr]
    if scheme_val:
        bucket["scheme"] = scheme_val
    return root_scheme


def extract_theme_oklch_maps(stripped: str) -> dict[str, dict[str, tuple[float, float, float]]]:
    """Extract polarity-isolated OKLCH token maps from light-dark(), :root, @media, and [data-theme]."""
    hue_m = _BRAND_HUE_NUM_RE.search(stripped)
    default_hue = float(hue_m.group(1)) if hue_m else 255.0
    root_light: dict[str, tuple[float, float, float]] = {}
    root_dark: dict[str, tuple[float, float, float]] = {}
    root_single: dict[str, tuple[float, float, float]] = {}
    root_aliases: dict[str, str] = {}
    root_scheme: str | None = None
    themes: dict[str, dict[str, object]] = {}

    for media_ctx, selector, body in _iter_css_blocks(stripped):
        scope = _classify_theme_scope(media_ctx, selector)
        if scope == "other":
            continue
        b_hue_m = _BRAND_HUE_NUM_RE.search(body)
        blk_hue = float(b_hue_m.group(1)) if b_hue_m else default_hue
        singles, aliases = _extract_block_oklch_tokens(body, blk_hue, root_light, root_dark)
        root_scheme = _record_scoped_tokens(scope, body, singles, aliases, root_single, root_aliases, themes, root_scheme)

    return _merge_extracted_themes(root_light, root_dark, root_single, root_aliases, root_scheme, themes)
