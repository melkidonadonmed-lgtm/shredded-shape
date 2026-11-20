#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Shared static AST/CSS/JSX structural guards for shredded-shape v1.6.0."""

from __future__ import annotations

import re
from pathlib import Path

from _ss_core import strip_comments

PSEUDO_ICON_SYMBOL_RE = re.compile(r"[✕✖✗✘≡⋮⋯▾▸▴◂▼▲▶◀☰⚙★☆🗑✎✏]")
_PSEUDO_INNER_GLYPH_RE = re.compile(
    r"^\s*(?:\{[^}]*[\"'][+\u00d7\u2715\u25b8\u25be\u2190\u2192\u2191\u2193\u2713\u2714][\"'][^}]*\}|[+\u00d7\u2190\u2192\u2191\u2193\u2713\u2714])\s*</(?:button|a|summary)>",
    re.IGNORECASE,
)
_PSEUDO_TERNARY_CHAR_RE = re.compile(r"[\"'](?:▾|▸|▴|◂|✕|✖|≡|⋮|⋯|▼|▲|▶|◀)[\"']")
_PRINT_HEADER_RE = re.compile(r"@media\s+print\b|@page\b|\.(?:sus-grid|print-sheet|a4-sheet)\b", re.IGNORECASE)
_PRINT_HINT_RE = re.compile(r"@media\s+print|@page|\b210mm\b|\b297mm\b|\.sus-grid\b|<!doctype html|<html\b", re.IGNORECASE)
_BACKTICK_TEMPLATE_RE = re.compile(r"`[^`]{80,}`", re.DOTALL)
_BOX_SHADOW_VALUE_RE = re.compile(r"box-shadow\s*:\s*([^;}{]+)", re.IGNORECASE)
_INTERACTIVE_CSS_RULE_RE = re.compile(
    r"(?:^|[},;\s])((?:button|summary|select|a\.btn|\.btn(?:-[a-z0-9_-]+)?|\.icon-btn|\.close-btn|\.nav-item|\.tab-btn|input:(?!\[type=[\"']?(?:checkbox|radio)\]))[^{};]*)\{([^}]+)\}",
    re.IGNORECASE,
)
_CSS_SMALL_DIM_RE = re.compile(r"(?:^|[;\s])(?:min-)?(?:width|height)\s*:\s*([0-9]+(?:\.[0-9]+)?)px", re.IGNORECASE)
_INTERACTIVE_JSX_START_RE = re.compile(r"<(button|a|summary)\b", re.IGNORECASE)
_TW_TINY_SIZE_RE = re.compile(r"\b(?:h|w|min-h|min-w|size)-(?:6|7|8|9|\[(?:24|28|30|32|34|36|38)px\])\b")
_TW_SAFE_MIN_RE = re.compile(r"\b(?:min-h-11|min-h-12|min-h-\[(?:44|48)px\]|min-w-11|min-w-12)\b")
_DIV_OPEN_RE = re.compile(r"<div\b", re.IGNORECASE)
_ONCLICK_RE = re.compile(r"\bonClick\s*=", re.IGNORECASE)
_ROLE_OR_BUTTON_RE = re.compile(r"\brole\s*=", re.IGNORECASE)
_ARIA_HIDDEN_TRUE_RE = re.compile(r"""\baria-hidden\s*=\s*(?:\{true\}|["']true["'])""", re.IGNORECASE)
_STOP_PROPAGATION_ONLY_RE = re.compile(
    r"\bonClick\s*=\s*\{\s*(?:\([^)]*\)|[a-z_]\w*)\s*=>\s*\{?\s*[a-z_]\w*\.stopPropagation\(\)\s*;?\s*\}?\s*\}",
    re.IGNORECASE | re.DOTALL,
)
_BACKDROP_HINT_RE = re.compile(r"\b(?:backdrop|overlay|scrim|inset-0)\b|bg-black/|bg-slate-\d+/|bg-stone-\d+/", re.IGNORECASE)
_CLOSE_HANDLER_RE = re.compile(r"\bon(?:Close|Dismiss|Cancel)\b|setIs\w*Open\(\s*false\s*\)|closeModal|handleClose", re.IGNORECASE)


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _blank_preserving_newlines(snippet: str) -> str:
    return re.sub(r"[^\n]", " ", snippet)


def strip_print_sheet_contexts(path: Path, text: str) -> str:
    """Mask @media print / .sus-grid blocks and .ts print-HTML templates while preserving exact line numbers."""
    suffix = path.suffix.lower()
    out = text
    if suffix in {".ts", ".tsx", ".js", ".jsx"}:
        def _blank_ts_print_template(m: re.Match[str]) -> str:
            block = m.group(0)
            if _PRINT_HINT_RE.search(block) or "print" in path.stem.lower() or "sus" in path.stem.lower():
                return _blank_preserving_newlines(block)
            return block
        out = _BACKTICK_TEMPLATE_RE.sub(_blank_ts_print_template, out)
    if suffix in {".css", ".scss", ".html"}:
        out = _mask_balanced_blocks(out, _PRINT_HEADER_RE)
    return out


def _mask_balanced_blocks(text: str, header_re: re.Pattern[str]) -> str:
    """Blank CSS blocks whose selector/at-rule header matches header_re without breaking line numbers."""
    chars = list(text)
    for m in header_re.finditer(text):
        brace_idx = text.find("{", m.end())
        if brace_idx < 0 or text[m.end():brace_idx].count(";") > 0:
            continue
        depth = 0
        end_idx = brace_idx
        while end_idx < len(text):
            ch = text[end_idx]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end_idx += 1
                    break
            end_idx += 1
        for i in range(m.start(), min(end_idx, len(chars))):
            if chars[i] != "\n":
                chars[i] = " "
    return "".join(chars)


def find_print_shadow_leaks(path: Path, text: str) -> list[tuple[int, str, str]]:
    """Flag non-none box-shadow declarations left active inside @media print blocks."""
    if path.suffix.lower() not in {".css", ".scss", ".html"}:
        return []
    cleaned = strip_comments(text)
    hits: list[tuple[int, str, str]] = []
    for m in re.finditer(r"@media\s+print\b", cleaned, re.IGNORECASE):
        brace_idx = cleaned.find("{", m.end())
        if brace_idx < 0:
            continue
        block_end = _find_matching_brace(cleaned, brace_idx)
        block = cleaned[brace_idx:block_end]
        for sm in _BOX_SHADOW_VALUE_RE.finditer(block):
            val = sm.group(1).strip().lower()
            if not val.startswith("none"):
                line = _line_of(text, brace_idx + sm.start())
                hits.append((line, f"box-shadow: {sm.group(1).strip()[:48]}", "Add box-shadow: none !important; inside @media print."))
    return hits


def _find_matching_brace(text: str, open_idx: int) -> int:
    depth = 0
    for idx in range(open_idx, len(text)):
        if text[idx] == "{":
            depth += 1
        elif text[idx] == "}":
            depth -= 1
            if depth == 0:
                return idx + 1
    return len(text)


def find_pseudo_icon_hits(path: Path, text: str) -> list[tuple[int, str, str]]:
    """Detect non-SVG ASCII/Unicode glyph icons inside UI files and interactive JSX buttons."""
    cleaned = strip_print_sheet_contexts(path, strip_comments(text))
    hits: list[tuple[int, str, str]] = []
    seen_lines: set[int] = set()
    for pat in (PSEUDO_ICON_SYMBOL_RE, _PSEUDO_TERNARY_CHAR_RE):
        for m in pat.finditer(cleaned):
            line = _line_of(cleaned, m.start())
            if line in seen_lines:
                continue
            seen_lines.add(line)
            snippet = m.group(0).strip().replace("\n", " ")[:48]
            hits.append((line, snippet, "Replace ASCII/Unicode pseudo-icon with a crisp 24x24 stroke SVG (Lucide or Material)."))
    for jm in _INTERACTIVE_JSX_START_RE.finditer(cleaned):
        _, end_pos = _scan_jsx_opening_tag(cleaned, jm.start())
        tail = cleaned[end_pos : end_pos + 160]
        if inner := _PSEUDO_INNER_GLYPH_RE.match(tail):
            line = _line_of(cleaned, jm.start())
            if line not in seen_lines:
                seen_lines.add(line)
                hits.append((line, inner.group(0).strip()[:48], "Replace ASCII/Unicode pseudo-icon with a crisp 24x24 stroke SVG (Lucide or Material)."))
    return hits


def find_target_size_overrides(path: Path, text: str) -> list[tuple[int, str, str]]:
    """Detect explicit CSS/Tailwind dimensions < 40px on interactive controls (ignoring inner <svg> icons)."""
    cleaned = strip_print_sheet_contexts(path, strip_comments(text))
    hits: list[tuple[int, str, str]] = []
    if path.suffix.lower() in {".css", ".scss", ".html"}:
        for rm in _INTERACTIVE_CSS_RULE_RE.finditer(cleaned):
            body = rm.group(2)
            for dm in _CSS_SMALL_DIM_RE.finditer(body):
                px = float(dm.group(1))
                if 12 <= px < 40:
                    line = _line_of(cleaned, rm.start() + dm.start())
                    hits.append((line, f"{rm.group(1).strip()[:32]} ({px:g}px)", "Enforce >= 44px-48px interactive hit target (or 44px ::after target apron)."))
                    break
    if path.suffix.lower() in {".tsx", ".jsx", ".html"}:
        for jm in _INTERACTIVE_JSX_START_RE.finditer(cleaned):
            tag, _ = _scan_jsx_opening_tag(cleaned, jm.start())
            if _TW_TINY_SIZE_RE.search(tag) and not _TW_SAFE_MIN_RE.search(tag):
                line = _line_of(cleaned, jm.start())
                hits.append((line, tag.replace("\n", " ")[:56], "Ensure button/link hit target reaches >= 44px (min-h-11/min-w-11 or 44px touch target)."))
    return hits


def _scan_jsx_opening_tag(text: str, start_idx: int) -> tuple[str, int]:
    """Read a JSX/HTML opening tag cleanly across `{...}` expressions containing `=>` or `>`."""
    idx = start_idx
    brace_depth = 0
    quote: str | None = None
    while idx < len(text):
        ch = text[idx]
        if quote:
            if ch == "\\" and idx + 1 < len(text):
                idx += 2
                continue
            if ch == quote:
                quote = None
        elif ch in ("'", '"', "`"):
            quote = ch
        elif ch == "{":
            brace_depth += 1
        elif ch == "}" and brace_depth > 0:
            brace_depth -= 1
        elif ch == ">" and brace_depth == 0:
            return text[start_idx : idx + 1], idx + 1
        idx += 1
    return text[start_idx:], len(text)


def find_unsemantic_div_clicks(path: Path, text: str) -> list[tuple[int, str, str]]:
    """Find interactive <div onClick> elements without role=, exempting stopPropagation shields and dismiss backdrops."""
    if path.suffix.lower() not in {".tsx", ".jsx", ".html"}:
        return []
    hits: list[tuple[int, str, str]] = []
    for m in _DIV_OPEN_RE.finditer(text):
        tag, _ = _scan_jsx_opening_tag(text, m.start())
        if not _ONCLICK_RE.search(tag) or _ROLE_OR_BUTTON_RE.search(tag):
            continue
        if _STOP_PROPAGATION_ONLY_RE.search(tag):
            continue
        if _ARIA_HIDDEN_TRUE_RE.search(tag) or (_BACKDROP_HINT_RE.search(tag) and _CLOSE_HANDLER_RE.search(tag)):
            continue
        line = _line_of(text, m.start())
        hits.append((line, tag.replace("\n", " ")[:72], "Use semantic <button type='button'> or add role='button' tabIndex={0} onKeyDown."))
    return hits
