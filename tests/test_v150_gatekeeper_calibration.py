"""Calibration tests for shredded-shape v1.5.0 ([GAP-01..06] & gatekeeper accuracy)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from scripts import _ss_core, _ss_guards, sync_shredded_shape, validate_shredded_shape

ROOT = Path(__file__).resolve().parent.parent


def _load_mod(rel_path: str, mod_name: str):
    spec = importlib.util.spec_from_file_location(mod_name, ROOT / rel_path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


ANALYST = _load_mod("skills/ui-frontend-analyst/scripts/frontend_inventory_and_slop_scanner.py", "ss_analyst_v150")
JUDGE = _load_mod("skills/ui-quality-judge/scripts/ui_judge_gatekeeper.py", "ss_judge_v150")
UX_AUD = _load_mod("skills/ui-quality-judge/scripts/ui_ux_frontend_auditor.py", "ss_ux_v150")
CZ_AUD = _load_mod("skills/complex-zero/scripts/complex_zero_ast_auditor.py", "ss_cz_v150")


def test_scoped_file_collection_skips_tests_and_flags_truncation(tmp_path: Path) -> None:
    src = tmp_path / "src"
    (src / "__tests__").mkdir(parents=True)
    (src / "components").mkdir(parents=True)
    (src / "__tests__" / "App.test.tsx").write_text("export const t = 1;", encoding="utf-8")
    (src / "components" / "Story.stories.tsx").write_text("export default {};", encoding="utf-8")
    (src / "components" / "App.tsx").write_text("export function App() { return <main />; }\n", encoding="utf-8")
    (src / "components" / "Card.tsx").write_text("export function Card() { return <article />; }\n", encoding="utf-8")

    files, total, truncated = _ss_core.collect_ui_files_scoped(src, limit=500)
    assert total == 2 and not truncated
    assert [f.name for f in files] == ["App.tsx", "Card.tsx"]

    limited, total_lim, trunc_lim = _ss_core.collect_ui_files_scoped(src, limit=1)
    assert len(limited) == 1 and total_lim == 2 and trunc_lim


def test_pseudo_icon_hits_and_emoji_hard_blocker(tmp_path: Path) -> None:
    emoji_only = tmp_path / "EmojiOnly.tsx"
    emoji_only.write_text("export function E() { return <button type='button'>🚀</button>; }\n", encoding="utf-8")
    rep = ANALYST.scan_frontend(emoji_only)
    assert rep.verdict == "[FAIL]" and rep.ai_slop_score >= 45 and rep.emoji_hits == 1

    pseudo = tmp_path / "Pseudo.tsx"
    pseudo_src = "export function P() { return <button type='button' onClick={() => close()}>+</button>; }\n"
    pseudo.write_text(pseudo_src, encoding="utf-8")
    hits = _ss_guards.find_pseudo_icon_hits(pseudo, pseudo_src)
    assert hits and hits[0][0] == 1

    clean_src = "export function C() { return <button type='button'>Ctrl+S<svg viewBox='0 0 24 24'><path d='M5 12h14'/></svg></button>; }\n"
    assert _ss_guards.find_pseudo_icon_hits(pseudo, clean_src) == []


def test_target_size_overrides_ignore_border_width_and_inner_svg(tmp_path: Path) -> None:
    css = tmp_path / "app.css"
    css_bad = "button.close-btn { width: 28px; height: 28px; }\n.card { border-width: 2px; line-height: 16px; }\n"
    hits = _ss_guards.find_target_size_overrides(css, css_bad)
    assert len(hits) == 1 and hits[0][0] == 1

    tsx = tmp_path / "IconButton.tsx"
    tsx_bad = "export function B() { return <button type='button' className='h-8 w-8' onClick={() => go()}>X</button>; }\n"
    assert len(_ss_guards.find_target_size_overrides(tsx, tsx_bad)) == 1

    tsx_good = "export function G() { return <button type='button' className='min-h-11 min-w-11'><svg className='w-4 h-4' /></button>; }\n"
    assert _ss_guards.find_target_size_overrides(tsx, tsx_good) == []


def test_print_isolation_and_print_shadow_leak(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text("<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'></head></html>", encoding="utf-8")
    src = tmp_path / "src"
    (src / "data").mkdir(parents=True)
    (src / "styles").mkdir(parents=True)
    (src / "data" / "susDocumentsCatalog.ts").write_text(
        "export const tpl = `<!DOCTYPE html><html><style>.row{width:3px;font-size:9px;box-shadow:none;}</style><body>A4</body></html>`;\n",
        encoding="utf-8",
    )
    (src / "styles" / "globals.css").write_text(
        ":root { --bg-well: oklch(0.94 0.01 250); --bg-canvas: oklch(0.97 0.01 250); --bg-card: oklch(0.99 0 0); --bg-card-lit: oklch(1 0 0); --ink-primary: oklch(0.18 0.02 255); --catch-light: inset 0 1px 0 0 oklch(1 0 0 / 0.8); --shadow-elevation-1: 0 2px 4px oklch(0 0 0 / 0.1), 0 4px 10px -2px oklch(0 0 0 / 0.08); }\n"
        "body { -webkit-font-smoothing: antialiased; font-optical-sizing: auto; }\n"
        ".btn:focus-visible { outline: 2px solid currentColor; }\n"
        "@media (prefers-reduced-motion: reduce) { * { transition: none; } }\n"
        "@media print { .sheet { box-shadow: none !important; } }\n",
        encoding="utf-8",
    )
    ux_clean = UX_AUD.evaluate_target(src)
    assert not any("<html" in r or "9px" in r or "3px" in r for r in ux_clean.recommendations)

    (src / "styles" / "globals.css").write_text(
        (src / "styles" / "globals.css").read_text(encoding="utf-8") + "\n.micro { font-size: 11px; }\n@media print { .leak { box-shadow: 0 4px 12px rgba(0,0,0,0.2); } }\n",
        encoding="utf-8",
    )
    ux_micro = UX_AUD.evaluate_target(src)
    assert any("11px" in r for r in ux_micro.recommendations)
    rep = JUDGE.evaluate_ui(src)
    assert any(f.rule_id == "CLINICAL-PRINT-SHADOW" for f in rep.findings)


def test_balanced_div_onclick_exempts_backdrop_and_catches_real_line(tmp_path: Path) -> None:
    comp = tmp_path / "SearchBar.tsx"
    src = (
        "export function SearchBar({ onClose, handleSelect }: any) {\n"
        "  return (\n"
        "    <div className='fixed inset-0 bg-black/50' aria-hidden='true' onClick={onClose}>\n"
        "      <div className='modal-panel' onClick={(e) => { e.stopPropagation(); }}>\n"
        "        <div key='a' onClick={() => handleSelect('a')} className='row'>Select A</div>\n"
        "      </div>\n"
        "    </div>\n"
        "  );\n"
        "}\n"
    )
    comp.write_text(src, encoding="utf-8")
    hits = _ss_guards.find_unsemantic_div_clicks(comp, src)
    assert len(hits) == 1 and hits[0][0] == 5

    rep = JUDGE.evaluate_ui(comp)
    click_findings = [f for f in rep.findings if f.rule_id == "AUDIT-A11Y-CLICK-DIV"]
    assert len(click_findings) == 1 and click_findings[0].file.endswith(":5")

    cz = CZ_AUD.audit_source_bundle({"SearchBar.tsx": src})
    assert any(f.get("rule") == "SEMANTIC_BUTTON" for f in cz["findings"])


def test_fail_closed_unverified_on_narrowed_styles_or_truncation(tmp_path: Path) -> None:
    (tmp_path / "styles").mkdir()
    (tmp_path / "components").mkdir()
    (tmp_path / "components" / "App.tsx").write_text("export function App() { return <main />; }\n", encoding="utf-8")
    (tmp_path / "styles" / "globals.css").write_text(
        ":root { --bg-well: oklch(0.94 0.01 250); --bg-canvas: oklch(0.97 0.01 250); --bg-card: oklch(1 0 0); --bg-card-lit: oklch(1 0 0); --ink-primary: oklch(0.18 0.02 255); }\n",
        encoding="utf-8",
    )
    rep = JUDGE.evaluate_ui(tmp_path / "styles")
    assert rep.verdict == "UNVERIFIED" and rep.scope_narrowed is True


def test_isolated_tsx_component_skips_global_css_false_positives(tmp_path: Path) -> None:
    comp = tmp_path / "AppShell.tsx"
    comp.write_text(
        "export function AppShell() {\n"
        "  return (\n"
        "    <header className='p-4'>\n"
        "      <nav aria-label='Main' className='flex gap-4'><a href='/'>Home</a></nav>\n"
        "      <main className='p-6 border shadow-sm'><svg width='20' height='20' viewBox='0 0 24 24'><path d='M4 12h16'/></svg><h1>Dash</h1></main>\n"
        "    </header>\n"
        "  );\n"
        "}\n",
        encoding="utf-8",
    )
    rep = UX_AUD.evaluate_target(comp)
    assert rep.verdict == "PASS" and rep.final_score >= 85.0


def test_sync_vendors_guards_and_strict_validator_passes(tmp_path: Path) -> None:
    res = sync_shredded_shape.sync_shredded_shape(repo_root=ROOT, gemini_root=tmp_path, sync_local_workspace=False)
    assert "triad_mirrored" not in res
    assert (tmp_path / "config" / "plugins" / "shredded-shape" / "skills" / "ui-quality-judge" / "scripts" / "_ss_guards.py").is_file()
    passed, total, errors = validate_shredded_shape.validate_repository(ROOT, strict_mode=True)
    assert errors == [] and passed == total and total == 6
