#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Shared static craft, AppSec secret/XSS, placeholder, and advisory hygiene guards for v1.6.0."""

from __future__ import annotations

import contextlib
import html
import json
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from typing import Literal, NamedTuple

import _ss_core
import _ss_guards

_FILTER_BLOCK_RE = re.compile(r"<filter\b[^>]*>([\s\S]*?)</filter>", re.IGNORECASE)
_CLIENT_ENV_RE = re.compile(
    r"\b((?:NEXT_PUBLIC|VITE|REACT_APP|NUXT_PUBLIC|EXPO_PUBLIC|PUBLIC)_[A-Z0-9_]{2,})\b"
)
_SECRET_NAME_TOKENS = (
    "SECRET", "PRIVATE_KEY", "PRIVATE", "SERVICE_ROLE", "PASSWORD", "PASSWD",
    "DATABASE_URL", "DB_URL", "ADMIN_KEY", "SIGNING_KEY", "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "STRIPE_SECRET", "JWT_SECRET", "AWS_SECRET",
)
_PUBLIC_ENV_EXEMPT_TOKENS = (
    "PUBLISHABLE", "ANON", "PUBLIC_TOKEN", "SITE_KEY", "CLIENT_ID",
    "MEASUREMENT_ID", "FIREBASE_API_KEY", "POSTHOG_KEY",
)
_LIVE_KEY_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"AIza[0-9A-Za-z_-]{35}"), "GOOGLE_API_KEY"),
    (re.compile(r"sk-(?:live|proj|ant)-[A-Za-z0-9_-]{20,}"), "PROVIDER_SECRET_KEY"),
    (re.compile(r"ghp_[A-Za-z0-9]{36}"), "GITHUB_TOKEN"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "PEM_PRIVATE_KEY"),
)
_PLACEHOLDER_OMISSION_RE = re.compile(
    r"(?:\.\.\.\s*(?:rest\s+of|existing\s+code|remaining\s+(?:code|items|lines|handlers)"
    r"|unchanged|omitted|more\s+here|resto\s+do\s+codigo|codigo\s+existente|inalterado"
    r"|demais\s+(?:itens|linhas))"
    r"|(?:rest\s+of\s+(?:the\s+)?code|resto\s+do\s+codigo|faca\s+o\s+mesmo\s+para\s+os\s+outros"
    r"|existing\s+code\s+\.\.\.))",
    re.IGNORECASE,
)
_DANGEROUS_HTML_RE = re.compile(r"dangerouslySetInnerHTML\s*=")
_TAG_NAME_RE = re.compile(r"^<\s*([a-zA-Z0-9_-]+)")
_DOM_HTML_SINK_RE = re.compile(r"(?:\.innerHTML|\.outerHTML)\s*=|insertAdjacentHTML\s*\(")
_EVAL_SINK_RE = re.compile(r"(?<![.\w$])(?:eval\s*\(|new\s+Function\s*\()")
_CSS_BLOCK_RE = re.compile(r"([^{};]+)\{([^{}]*)\}", re.DOTALL)
_BG_CLIP_TEXT_RE = re.compile(r"(?:-webkit-)?background-clip\s*:\s*text\b", re.IGNORECASE)
_TRANSPARENT_TEXT_RE = re.compile(
    r"(?:color|-webkit-text-fill-color)\s*:\s*transparent\b|gradient\(", re.IGNORECASE
)
_OPEN_TAG_START_RE = re.compile(r"<[a-zA-Z][\w.-]*\b")
_TW_CLIP_RE = re.compile(r"\bbg-clip-text\b")
_TW_GRAD_TEXT_RE = re.compile(r"\btext-transparent\b|\bbg-(?:gradient|linear|radial|conic)-")
_NAV_START_RE = re.compile(r"<nav\b", re.IGNORECASE)
_ARIA_LABEL_RE = re.compile(r"""\baria-label\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)
_REDUNDANT_NAV_WORD_RE = re.compile(r"\b(?:navigation|navegacao)\b", re.IGNORECASE)
_NAV_BLOCK_RE = re.compile(r"<nav\b[^>]*>([\s\S]*?)</nav>", re.IGNORECASE)
_NAV_ITEM_RE = re.compile(r"<(?:a|button)\b[^>]*>([\s\S]*?)</(?:a|button)>", re.IGNORECASE)
_NAV_OL_RE = re.compile(r"<ol\b[^>]*>([\s\S]*?)</ol>", re.IGNORECASE)
_LOCKFILES = ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb")
_CONFLICTING_PKG_PAIRS = (
    ("reactflow", "@xyflow/react"),
    ("bootstrap", "tailwindcss"),
    ("styled-components", "tailwindcss"),
    ("react", "vue"),
    ("react", "@angular/core"),
)


class CraftGuardHit(NamedTuple):
    """Single static craft or security violation detected by _ss_craft_guards."""

    rule_id: str
    severity: Literal["CRITICAL", "WARNING"]
    line: int
    snippet: str
    message: str
    remediation: str


def _normalize_ascii(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in nfkd if unicodedata.category(ch) != "Mn")


def has_gooey_filter_blob(stripped_text: str) -> bool:
    """Return True only when feGaussianBlur and feColorMatrix share the same <filter> block."""
    for m in _FILTER_BLOCK_RE.finditer(stripped_text):
        low = m.group(1).lower()
        if "<fegaussianblur" in low and "<fecolormatrix" in low:
            return True
    return False


def find_client_secret_leaks(path: Path, raw_text: str) -> list[CraftGuardHit]:
    """Detect exposed secret env vars or live keys on UI files without logging secret values."""
    if path.suffix.lower() not in _ss_core.UI_EXTS:
        return []
    hits: list[CraftGuardHit] = []
    flagged_lines: set[int] = set()
    for m in _CLIENT_ENV_RE.finditer(raw_text):
        env_name = m.group(1)
        if any(p in env_name for p in _PUBLIC_ENV_EXEMPT_TOKENS):
            continue
        if any(s in env_name for s in _SECRET_NAME_TOKENS):
            ln = _ss_guards._line_of(raw_text, m.start())
            if ln not in flagged_lines:
                flagged_lines.add(ln)
                redacted = f"{env_name}=[REDACTED]"
                hits.append(CraftGuardHit("AUDIT-SEC-ENV-LEAK", "CRITICAL", ln, redacted, f"Client-exposed secret identifier {redacted}", "Move secrets to server-only env vars without client public prefixes."))
    lines = raw_text.splitlines()
    for pat, label in _LIVE_KEY_PATTERNS:
        for m in pat.finditer(raw_text):
            ln = _ss_guards._line_of(raw_text, m.start())
            if ln in flagged_lines:
                continue
            line_txt = lines[ln - 1] if ln <= len(lines) else ""
            if any(tok in line_txt for tok in ("YOUR_API_KEY", "process.env.", "import.meta.env.")):
                continue
            flagged_lines.add(ln)
            redacted = f"{label}=[REDACTED]"
            hits.append(CraftGuardHit("AUDIT-SEC-ENV-LEAK", "CRITICAL", ln, redacted, f"Hardcoded credential {redacted}", "Remove hardcoded credentials from frontend bundles immediately."))
    return hits


def find_placeholder_omissions(path: Path, raw_text: str) -> list[CraftGuardHit]:
    """Detect AI code-omission placeholders strictly inside comment tokens."""
    if path.suffix.lower() not in _ss_core.UI_EXTS:
        return []
    hits: list[CraftGuardHit] = []
    for m in _ss_core._TOKENIZER_RE.finditer(raw_text):
        cmt = m.group("cmt")
        if cmt is None:
            continue
        if _PLACEHOLDER_OMISSION_RE.search(_normalize_ascii(cmt).lower()):
            ln = _ss_guards._line_of(raw_text, m.start())
            snip = " ".join(cmt.strip().split())[:48]
            hits.append(CraftGuardHit("AUDIT-STUB-PLACEHOLDER", "CRITICAL", ln, snip, f"AI omission placeholder comment detected ({snip})", "Implement complete code with zero omitted sections."))
    return hits


def _is_sanitized_in_scope(stripped: str, pos: int, ident_hint: str = "") -> bool:
    after = stripped[pos : min(len(stripped), pos + 140)]
    if "DOMPurify.sanitize(" in after:
        return True
    if ident_hint:
        pat = re.compile(rf"\b(?:const|let|var)\s+{re.escape(ident_hint)}\s*=\s*[^;\n]*DOMPurify\.sanitize\(")
        return bool(pat.search(stripped))
    return False


def find_unsafe_html_sinks(path: Path, raw_text: str) -> list[CraftGuardHit]:
    """Check HTML/XSS sinks per occurrence so one FOUC theme script or DOMPurify call never hides another."""
    if path.suffix.lower() not in {".html", ".tsx", ".jsx", ".ts", ".js", ".mjs", ".vue"}:
        return []
    stripped = _ss_core.strip_comments(raw_text)
    hits: list[CraftGuardHit] = []
    for m in _DANGEROUS_HTML_RE.finditer(stripped):
        last_lt = stripped.rfind("<", max(0, m.start() - 140), m.start())
        tag_m = _TAG_NAME_RE.match(stripped[last_lt : m.start()]) if last_lt != -1 else None
        is_fouc_tag = tag_m is not None and tag_m.group(1).lower() == "script"
        after = stripped[m.start() : min(len(stripped), m.start() + 360)]
        is_fouc = is_fouc_tag and "data-theme" in after.replace('"', "'")
        ident_m = re.search(r"dangerouslySetInnerHTML\s*=\s*\{\{\s*__html\s*:\s*([A-Za-z_$][\w$]*)\s*\}\}", after[:80])
        if not is_fouc and not _is_sanitized_in_scope(stripped, m.start(), ident_m.group(1) if ident_m else ""):
            ln = _ss_guards._line_of(stripped, m.start())
            hits.append(CraftGuardHit("AUDIT-SEC-01", "CRITICAL", ln, "dangerouslySetInnerHTML", "dangerouslySetInnerHTML used without DOMPurify.sanitize()", "Wrap HTML payload with DOMPurify.sanitize()."))
    for pat, label in ((_DOM_HTML_SINK_RE, "innerHTML/insertAdjacentHTML"), (_EVAL_SINK_RE, "eval/new Function")):
        for m in pat.finditer(stripped):
            stmt = stripped[m.start() : min(len(stripped), m.start() + 200)].split("\n", 1)[0]
            rhs_m = re.search(r"=\s*([A-Za-z_$][\w$]*)\s*(?:;|$)", stmt)
            if pat is _DOM_HTML_SINK_RE and _is_sanitized_in_scope(stripped, m.start(), rhs_m.group(1) if rhs_m else ""):
                continue
            ln = _ss_guards._line_of(stripped, m.start())
            hits.append(CraftGuardHit("AUDIT-SEC-01", "CRITICAL", ln, label, f"Unsanitized dynamic execution/DOM sink ({label})", "Sanitize with DOMPurify.sanitize() or replace dynamic sink with safe DOM APIs."))
    return hits


def find_gradient_text_slop(path: Path, masked_text: str) -> list[CraftGuardHit]:
    """Detect decorative gradient-clipped text in CSS blocks and HTML/JSX tags."""
    if path.suffix.lower() not in {".css", ".scss", ".html", ".tsx", ".jsx", ".vue"}:
        return []
    hits: list[CraftGuardHit] = []
    for blk in _CSS_BLOCK_RE.finditer(masked_text):
        body = blk.group(2)
        if _BG_CLIP_TEXT_RE.search(body) and _TRANSPARENT_TEXT_RE.search(body):
            ln = _ss_guards._line_of(masked_text, blk.start())
            hits.append(CraftGuardHit("ANTI-SLOP-GRADIENT-TEXT", "CRITICAL", ln, "background-clip: text", "Decorative gradient-text clip violates typography contrast discipline", "Use solid OKLCH ink tokens and weight contrast instead of gradient text."))
    if path.suffix.lower() in {".html", ".tsx", ".jsx", ".vue"}:
        for tm in _OPEN_TAG_START_RE.finditer(masked_text):
            tag, _ = _ss_guards._scan_jsx_opening_tag(masked_text, tm.start())
            if _TW_CLIP_RE.search(tag) and _TW_GRAD_TEXT_RE.search(tag):
                ln = _ss_guards._line_of(masked_text, tm.start())
                hits.append(CraftGuardHit("ANTI-SLOP-GRADIENT-TEXT", "CRITICAL", ln, "bg-clip-text", "Tailwind bg-clip-text gradient text detected", "Use crisp solid OKLCH text colors without bg-clip-text."))
    return hits


def find_redundant_nav_aria_labels(path: Path, masked_text: str) -> list[CraftGuardHit]:
    """Warn when <nav aria-label> repeats 'navigation' or 'navegacao'."""
    if path.suffix.lower() not in {".html", ".tsx", ".jsx", ".vue"}:
        return []
    hits: list[CraftGuardHit] = []
    for m in _NAV_START_RE.finditer(masked_text):
        tag, _ = _ss_guards._scan_jsx_opening_tag(masked_text, m.start())
        lbl_m = _ARIA_LABEL_RE.search(tag)
        if not lbl_m:
            continue
        raw_lbl = lbl_m.group(1) or lbl_m.group(2) or ""
        if _REDUNDANT_NAV_WORD_RE.search(_normalize_ascii(raw_lbl)):
            ln = _ss_guards._line_of(masked_text, m.start())
            hits.append(CraftGuardHit("A11Y-NAV-REDUNDANT-LABEL", "WARNING", ln, raw_lbl[:40], f"<nav aria-label='{raw_lbl}'> repeats implicit navigation role", "Name the landmark concisely (e.g., 'Primary' or 'Main') without repeating 'navigation'."))
    return hits


def run_craft_and_sec_guards(
    path: Path, raw_text: str, stripped_text: str, masked_text: str, profile: Literal["analyst", "worker", "judge"]
) -> list[CraftGuardHit]:
    """Unified single-pass dispatcher for v1.6.0 craft and security static guards."""
    del stripped_text
    candidates = (
        find_client_secret_leaks(path, raw_text)
        + find_placeholder_omissions(path, raw_text)
        + find_unsafe_html_sinks(path, raw_text)
        + find_gradient_text_slop(path, masked_text)
    )
    if profile in ("analyst", "judge"):
        candidates.extend(find_redundant_nav_aria_labels(path, masked_text))
    seen: set[tuple[str, int]] = set()
    ordered: list[CraftGuardHit] = []
    for h in candidates:
        if (h.rule_id, h.line) not in seen:
            seen.add((h.rule_id, h.line))
            ordered.append(h)
    return ordered


class _BreadcrumbParser(HTMLParser):
    """Detect raw unhidden '/' or '>' separator text nodes inside breadcrumb lists."""

    def __init__(self) -> None:
        super().__init__()
        self._hidden_depth = 0
        self.raw_separators: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del tag
        amap = {k.lower(): (v or "") for k, v in attrs}
        if self._hidden_depth > 0 or amap.get("aria-hidden", "").lower() == "true":
            self._hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        del tag
        if self._hidden_depth > 0:
            self._hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._hidden_depth == 0 and data.strip() in {"/", ">", "»", "›"}:
            self.raw_separators.append(data.strip())


def _audit_root_dir(target_path: Path, css_text: str) -> list[str]:
    if not target_path.is_dir():
        return []
    root_dir = target_path.parent if (target_path.name.lower() == "src" and (target_path.parent / "package.json").is_file()) else target_path
    warns: list[str] = []
    locks = [lf for lf in _LOCKFILES if (root_dir / lf).is_file()]
    if len(locks) >= 2:
        warns.append(f"Conflicting lockfiles in {root_dir.name}: {', '.join(locks)}")
    tsconfig = root_dir / "tsconfig.json"
    if tsconfig.is_file():
        cleaned = re.sub(r",\s*([}\]])", r"\1", _ss_core.strip_comments(tsconfig.read_text(encoding="utf-8", errors="ignore")))
        try:
            cfg = json.loads(cleaned)
            strict = isinstance(cfg, dict) and (cfg.get("compilerOptions", {}).get("strict") is True or "references" in cfg or "extends" in cfg)
            if not strict:
                warns.append("tsconfig.json lacks strict: true (or references/extends)")
        except ValueError:
            warns.append("tsconfig.json could not be parsed as JSONC")
    pkg = root_dir / "package.json"
    if pkg.is_file():
        with contextlib.suppress(ValueError, OSError):
            pdata = json.loads(pkg.read_text(encoding="utf-8", errors="ignore"))
            deps = set(pdata.get("dependencies", {})) | set(pdata.get("devDependencies", {}))
            for left, right in _CONFLICTING_PKG_PAIRS:
                if left in deps and right in deps:
                    warns.append(f"Mixed frontend stack in package.json: {left} + {right}")
    if any((root_dir / f"tailwind.config.{ext}").is_file() for ext in ("js", "ts", "mjs", "cjs")) and re.search(r"@import\s+[\"']tailwindcss[\"']", css_text):
        warns.append("Mixed Tailwind v3 tailwind.config.* alongside Tailwind v4 @import")
    return warns


def audit_advisory_nav_and_root(
    target_path: Path, loaded_files: list[tuple[Path, str, str]]
) -> tuple[list[str], list[str]]:
    """Return advisory (root_hygiene_warnings, menu_label_audit) without inflating ai_slop_score."""
    css_text = "\n".join(txt for fp, _, txt in loaded_files if fp.suffix.lower() in {".css", ".scss"})
    root_warns = _audit_root_dir(target_path, css_text)
    menu_audit: list[str] = []
    for fp, rel, raw_text in loaded_files:
        if fp.suffix.lower() not in {".html", ".tsx", ".jsx"}:
            continue
        stripped = _ss_core.strip_comments(raw_text)
        for nav_m in _NAV_BLOCK_RE.finditer(stripped):
            nav_html = nav_m.group(1)
            for item_m in _NAV_ITEM_RE.finditer(nav_html):
                txt = re.sub(r"<svg[\s\S]*?</svg>", "", item_m.group(1), flags=re.IGNORECASE)
                txt = re.sub(r"<span[^>]*class=[\"'][^\"']*(?:sr-only|nav-step)[^\"']*[\"'][^>]*>[\s\S]*?</span>", "", txt, flags=re.IGNORECASE)
                txt = re.sub(r"<[^>]*aria-hidden=[\"']true[\"'][^>]*>[\s\S]*?</[^>]+>", "", txt, flags=re.IGNORECASE)
                clean = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", txt)).split())
                if clean and "{" not in clean and "}" not in clean and len(clean) > 26:
                    menu_audit.append(f"{rel}: nav label '{clean[:32]}' exceeds 26 chars ({len(clean)})")
            for ol_m in _NAV_OL_RE.finditer(nav_html):
                bp = _BreadcrumbParser()
                bp.feed(ol_m.group(1))
                if bp.raw_separators:
                    menu_audit.append(f"{rel}: raw breadcrumb separator '{bp.raw_separators[0]}' in HTML; use CSS ::before")
    return root_warns, menu_audit
