#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Shared visual hierarchy, menu decompression, tab governance, and CDP probe for complex-zero."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

INLINE_FONT_SIZE_PX_RE = re.compile(r"style\s*=\s*['\"][^'\"]*?\bfont-size\s*:\s*(\d+(?:\.\d+)?)\s*px", re.IGNORECASE)
CSS_BLOCK_RE = re.compile(r"([^{};]+)\{([^{}]*)\}", re.DOTALL)
FONT_SIZE_DECL_RE = re.compile(r"\bfont-size\s*:\s*(\d+(?:\.\d+)?)\s*px\b", re.IGNORECASE)
GAP_DECL_RE = re.compile(r"\bgap\s*:\s*(\d+(?:\.\d+)?)\s*px\b", re.IGNORECASE)
MIN_BLOCK_DECL_RE = re.compile(r"\b(?:min-block-size|min-height)\s*:\s*(\d+(?:\.\d+)?)\s*px\b", re.IGNORECASE)
PADDING_COMPACT_RE = re.compile(r"<button\b[^>]*?style\s*=\s*['\"][^'\"]*?\bpadding\s*:\s*([0-5])px\s+([0-9])px\b", re.IGNORECASE)
NAV_TAG_RE = re.compile(r"<nav\b[^>]*>", re.IGNORECASE)
ROLE_TAB_RE = re.compile(r"\brole\s*=\s*['\"]tab['\"]", re.IGNORECASE)
TAB_LABEL_EXTRACT_RE = re.compile(r"<[^>]*\brole\s*=\s*['\"]tab['\"][^>]*>([^<]+)<", re.IGNORECASE)
BACKEND_TAB_NAME_RE = re.compile(r"\b(?:sql_raw|db_pool|worker_queue|cron_daemon|grpc_stub|env_vars|raw_payload|redis_keys|sqlite_wal)\b", re.IGNORECASE)
SUBTAB_CALL_RE = re.compile(r"\b(?:switchNodesSubview|setCatalogTreeMode|setCatalogCategoryFilter|switchSubTab)\s*\(", re.IGNORECASE)
PRIMARY_TAB_CALL_RE = re.compile(r"\b(?:switchCanvasTab|switchTab|setActiveTab)\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", re.IGNORECASE)
TEXT_INPUT_RE = re.compile(r"<(?:textarea\b|input\b[^>]*?\btype\s*=\s*['\"](?:text|search)['\"])", re.IGNORECASE)
HARDCODED_NODE_PASS_RE = re.compile(r"(?:tag\s*\+\s*['\"]\s*\[PASS\]['\"]|\[(?:DIR|FILE|IMG|MD)\]\s*\[PASS\])")
METRIC_BADGE_OCCURRENCE_RE = re.compile(r"class\s*=\s*['\"][^'\"]*\bmetric-badge\b", re.IGNORECASE)

MENU_SELECTOR_TOKENS = (
    ".mode-switcher", ".mode-btn", ".chip-btn", ".canvas-tabs", ".canvas-tab",
    ".nav-", "nav ", '[role="tab"]', '[role="tablist"]', ".toolbar", ".tab-",
)

CHROME_DEVTOOLS_EVALUATE_SCRIPT = """() => {
  const getPx = (el, prop) => parseFloat(window.getComputedStyle(el)[prop] || '0') || 0;
  const isVis = (el) => {
    const r = el.getBoundingClientRect();
    const s = window.getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity || '1') > 0;
  };
  const h1 = document.querySelector('h1'), h2 = document.querySelector('h2'), h3 = document.querySelector('h3');
  const h1Px = h1 ? getPx(h1, 'fontSize') : 0;
  const h2Px = h2 ? getPx(h2, 'fontSize') : 0;
  const h3Px = h3 ? getPx(h3, 'fontSize') : 0;
  const bodyPx = getPx(document.body, 'fontSize');
  const hierarchyMonotonic = (!h1 || !h2 || h1Px > h2Px) && (!h2 || bodyPx <= h2Px);

  const crampedMenus = [];
  document.querySelectorAll('nav, [role="tablist"], .mode-switcher, .canvas-tabs').forEach((navEl, idx) => {
    if (!isVis(navEl)) return;
    const gapPx = getPx(navEl, 'gap') || getPx(navEl, 'columnGap');
    const items = Array.from(navEl.querySelectorAll('button, a, [role="tab"]')).filter(isVis);
    if (gapPx > 0 && gapPx < 8) crampedMenus.push(`nav#${navEl.id || idx}: gap=${gapPx}px (< 8px)`);
    if (items.length > 6) crampedMenus.push(`nav#${navEl.id || idx}: ${items.length} stacked items (> 6)`);
    items.forEach((btn) => {
      const fz = getPx(btn, 'fontSize');
      const r = btn.getBoundingClientRect();
      if (fz < 13) crampedMenus.push(`${btn.tagName.toLowerCase()}#${btn.id || btn.textContent.trim().slice(0, 18)}: fontSize=${fz}px (< 13px)`);
      if (btn.scrollWidth > btn.clientWidth + 2) crampedMenus.push(`${btn.tagName.toLowerCase()}#${btn.id || btn.textContent.trim().slice(0, 18)}: overflow`);
      if (r.height < 44) crampedMenus.push(`${btn.tagName.toLowerCase()}#${btn.id || btn.textContent.trim().slice(0, 18)}: height=${Math.round(r.height)}px (< 44px)`);
    });
  });

  const visibleNavs = Array.from(document.querySelectorAll('nav')).filter(isVis).length;
  const tabEls = Array.from(document.querySelectorAll('[role="tab"]'));
  const normLabels = tabEls.map((t) => (t.textContent || '').trim().toLowerCase()).filter(Boolean);
  const duplicateTabLabels = normLabels.filter((lbl, idx) => normLabels.indexOf(lbl) !== idx);
  const visibleInputs = Array.from(document.querySelectorAll('textarea, input[type="text"], input[type="search"], input:not([type])')).filter(isVis).length;

  return {
    pageMetadata: {
      title: document.title,
      hasViewportMeta: Boolean(document.querySelector('meta[name="viewport"]')),
      hasDescriptionMeta: Boolean(document.querySelector('meta[name="description"]')),
      theme: document.documentElement.getAttribute('data-theme') || 'default',
    },
    visualHierarchy: { h1Px, h2Px, h3Px, bodyPx, hierarchyMonotonic },
    organizationSprawl: { visibleNavs, allTabs: tabEls.length, duplicateTabLabels, visibleInputs },
    crampedMenus,
    passed: hierarchyMonotonic && crampedMenus.length === 0 && visibleNavs <= 3 && tabEls.length <= 6 && duplicateTabLabels.length === 0 && visibleInputs <= 3,
  };
}"""


@dataclass
class UnifiedVisualOrgReport:
    """Consolidated report for visual hierarchy, menu ergonomics, and tab governance."""

    nav_landmarks_count: int = 0
    primary_tabs_count: int = 0
    nested_subtab_calls: int = 0
    concurrent_text_inputs: int = 0
    inline_micro_font_count: int = 0
    tiny_font_declarations: list[str] = field(default_factory=list)
    cramped_menu_violations: list[str] = field(default_factory=list)
    sprawl_and_org_violations: list[str] = field(default_factory=list)
    hierarchy_violations: list[str] = field(default_factory=list)
    graph_node_violations: list[str] = field(default_factory=list)
    org_penalty_points: int = 0
    hierarchy_menu_penalty_points: int = 0
    graph_penalty_points: int = 0


def _inspect_css_blocks_for_menus_and_fonts(combined: str, tiny_fonts: list[str], cramped_menus: list[str]) -> None:
    for match in CSS_BLOCK_RE.finditer(combined):
        selector = " ".join(match.group(1).strip().split())
        body = match.group(2)
        if not selector or selector.startswith("@"):
            continue
        is_menu_sel = any(tok in selector.lower() for tok in MENU_SELECTOR_TOKENS)
        for fz_m in FONT_SIZE_DECL_RE.finditer(body):
            px_val = float(fz_m.group(1))
            if px_val < 12.0:
                tiny_fonts.append(f"{selector} {{ font-size: {px_val:g}px (< 12px) }}")
            elif is_menu_sel and px_val < 13.0:
                cramped_menus.append(f"Cramped menu font in '{selector}': {px_val:g}px (< 13px)")
        if is_menu_sel:
            for gap_m in GAP_DECL_RE.finditer(body):
                gap_val = float(gap_m.group(1))
                if gap_val < 6.0:
                    cramped_menus.append(f"Cramped menu gap in '{selector}': {gap_val:g}px (< 6px)")


def _inspect_inline_styles_and_templates(combined: str, report: UnifiedVisualOrgReport) -> None:
    micro_inline = [float(m.group(1)) for m in INLINE_FONT_SIZE_PX_RE.finditer(combined) if float(m.group(1)) <= 13.0]
    report.inline_micro_font_count = len(micro_inline)
    if len(micro_inline) > 4:
        report.hierarchy_violations.append(f"Inline micro-font clutter: {len(micro_inline)} elements <= 13px flattening hierarchy")
    for min_m in MIN_BLOCK_DECL_RE.finditer(combined):
        val = float(min_m.group(1))
        if val < 40.0:
            report.cramped_menu_violations.append(f"Undersized target min-block-size/min-height: {val:g}px (< 40px)")
    for pad_m in PADDING_COMPACT_RE.finditer(combined):
        report.cramped_menu_violations.append(f"Cramped inline button padding: {pad_m.group(1)}px {pad_m.group(2)}px")
    for nav_tag in NAV_TAG_RE.findall(combined):
        if (gap_m := GAP_DECL_RE.search(nav_tag)) and float(gap_m.group(1)) < 6.0:
            report.cramped_menu_violations.append(f"<nav> inline gap < 6px ({gap_m.group(1)}px)")


def _inspect_sprawl_and_graph_nodes(combined: str, report: UnifiedVisualOrgReport) -> None:
    report.nav_landmarks_count = len(NAV_TAG_RE.findall(combined))
    report.primary_tabs_count = max(len(ROLE_TAB_RE.findall(combined)), len(set(PRIMARY_TAB_CALL_RE.findall(combined))))
    report.nested_subtab_calls = len(SUBTAB_CALL_RE.findall(combined))
    report.concurrent_text_inputs = len(TEXT_INPUT_RE.findall(combined))
    if report.nav_landmarks_count > 3:
        report.sprawl_and_org_violations.append(f"Excess <nav> containers ({report.nav_landmarks_count} > 3 layers)")
    tab_labels = [lbl.strip().lower() for lbl in TAB_LABEL_EXTRACT_RE.findall(combined) if lbl.strip()]
    if dup_labels := sorted({lbl for lbl in tab_labels if tab_labels.count(lbl) > 1}):
        report.sprawl_and_org_violations.append(f"Duplicate tab labels ({', '.join(dup_labels)})")
    if backend_tabs := [lbl for lbl in tab_labels + list(PRIMARY_TAB_CALL_RE.findall(combined)) if BACKEND_TAB_NAME_RE.search(lbl)]:
        report.sprawl_and_org_violations.append(f"Exposed backend plumbing tabs ({', '.join(sorted(set(backend_tabs)))})")
    if report.primary_tabs_count > 6:
        report.sprawl_and_org_violations.append(f"Excess primary tabs ({report.primary_tabs_count} > 6)")
    if report.primary_tabs_count > 0 and report.nested_subtab_calls > 0:
        report.sprawl_and_org_violations.append(f"Nested sub-tab calls inside tabs ({report.nested_subtab_calls})")
    if report.concurrent_text_inputs > 3:
        report.sprawl_and_org_violations.append(f"Multiple competing text inputs ({report.concurrent_text_inputs} > 3)")
    if HARDCODED_NODE_PASS_RE.search(combined):
        report.graph_node_violations.append("Hardcoded '[PASS]' node badge detected (visual placebo)")
    if (badge_count := len(METRIC_BADGE_OCCURRENCE_RE.findall(combined))) >= 3 and "fs-node-box" in combined:
        report.graph_node_violations.append(f"Node badge overstuffing ({badge_count} metric-badges inside node card)")


def analyze_visual_hierarchy_and_organization(combined_source: str) -> UnifiedVisualOrgReport:
    """Run static structural, typographic hierarchy, menu, and graph-node audit."""
    report = UnifiedVisualOrgReport()
    _inspect_css_blocks_for_menus_and_fonts(combined_source, report.tiny_font_declarations, report.cramped_menu_violations)
    _inspect_inline_styles_and_templates(combined_source, report)
    _inspect_sprawl_and_graph_nodes(combined_source, report)
    if report.tiny_font_declarations:
        report.hierarchy_violations.extend(report.tiny_font_declarations[:5])
    if report.sprawl_and_org_violations:
        report.org_penalty_points = min(20, len(report.sprawl_and_org_violations) * 7)
    if report.cramped_menu_violations or report.hierarchy_violations:
        report.hierarchy_menu_penalty_points = min(20, (len(report.cramped_menu_violations) + len(report.hierarchy_violations)) * 6)
    if report.graph_node_violations:
        report.graph_penalty_points = min(15, len(report.graph_node_violations) * 8)
    return report


def probe_live_url_metadata(live_url: str, timeout_sec: float = 5.0) -> dict[str, Any]:
    """Fetch live HTML/CSS metadata and run static hierarchy/menu checks."""
    parsed = urllib.parse.urlparse(live_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return {"reachable": False, "error": "URL must start with http:// or https://"}
    try:
        req = urllib.request.Request(live_url, headers={"User-Agent": "ComplexZero-Probe/1.6.0"})
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:  # nosec B310
            html = resp.read().decode("utf-8", errors="replace")
            status_code = resp.status
    except Exception as exc:  # noqa: BLE001
        return {"reachable": False, "url": live_url, "error": str(exc)}
    org_rep = analyze_visual_hierarchy_and_organization(html)
    return {
        "reachable": True, "url": live_url, "http_status": status_code,
        "has_title": bool(re.search(r"<title>[^<]+</title>", html, re.IGNORECASE)),
        "has_viewport_meta": bool(re.search(r"<meta[^>]+name=['\"]viewport['\"]", html, re.IGNORECASE)),
        "live_dom_analysis": asdict(org_rep),
    }


def main() -> int:
    """CLI helper to dump Chrome DevTools evaluate_script payload or probe a live URL."""
    parser = argparse.ArgumentParser(description="Visual Hierarchy & CDP Probe (complex-zero)")
    parser.add_argument("--dump-cdp-script", action="store_true")
    parser.add_argument("--live-url", type=str, default="")
    args = parser.parse_args()
    if args.dump_cdp_script:
        print(CHROME_DEVTOOLS_EVALUATE_SCRIPT)
    elif args.live_url:
        print(json.dumps(probe_live_url_metadata(args.live_url), indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"status": "READY", "module": "visual_hierarchy_and_cdp_probe"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
