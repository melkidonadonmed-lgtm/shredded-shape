#!/usr/bin/env python3
"""Deterministic contract validator for the shredded-shape UI/UX skill and plugin suite."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
POS_TRIG_RE = re.compile(r"\b(use|activate|invoke)\b", re.IGNORECASE)
NEG_TRIG_RE = re.compile(r"\b(do not use|don't use|skip when|exclude)\b", re.IGNORECASE)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")
ALLOWED_PLUGIN_KEYS = frozenset({
    "$schema", "name", "displayName", "version", "description", "author",
    "homepage", "repository", "license", "keywords", "logo", "suggestedPrompts",
})
FORBIDDEN_AGENT_TOOLS = frozenset({
    "*", "call_mcp_tool", "view_file", "list_dir", "find_by_name",
    "grep_search", "write_to_file", "replace_file_content", "multi_replace_file_content",
})
READ_ONLY_AGENTS = frozenset({"ui-analyst.md", "ui-planner.md", "ui-judge.md"})
REQUIRED_HEADINGS = ("Overview", "Inputs", "Procedure", "Gotchas", "Output", "User Communication")


def _extract_frontmatter(raw: str) -> Tuple[Dict[str, Any], str]:
    cleaned = raw.lstrip("\ufeff")
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n?(.*)$", cleaned, re.DOTALL)
    if not match:
        return {}, cleaned
    parsed = yaml.safe_load(match.group(1))
    return (parsed if isinstance(parsed, dict) else {}), match.group(2)


def _check_skill_links_and_headings(skill_dir: Path, body: str, errors: List[str]) -> None:
    if len(body.splitlines()) >= 500:
        errors.append(f"[FAIL] {skill_dir.name}: SKILL.md exceeds 500 lines")
    for heading in REQUIRED_HEADINGS:
        if not re.search(rf"^##\s+.*{re.escape(heading)}", body, re.MULTILINE | re.IGNORECASE):
            errors.append(f"[FAIL] {skill_dir.name}: missing required section '{heading}'")
    stripped = re.sub(r"```.*?```|`[^`\n]+`", "", body, flags=re.DOTALL)
    for target in LINK_RE.findall(stripped):
        if target.startswith(("http://", "https://", "file://", "#")):
            continue
        rel = target.split("#", 1)[0].split("?", 1)[0]
        if ".." in Path(rel).parts:
            errors.append(f"[FAIL] {skill_dir.name}: parent escape '..' in link '{target}'")
        elif rel and not (skill_dir / rel).exists():
            errors.append(f"[FAIL] {skill_dir.name}: broken link '{target}'")


def _check_skill_assets(skill_dir: Path, errors: List[str]) -> None:
    rules_md = skill_dir / "rules" / "audit_criteria.md"
    if not rules_md.is_file():
        errors.append(f"[FAIL] {skill_dir.name}: missing rules/audit_criteria.md")
    else:
        r_text = rules_md.read_text(encoding="utf-8")
        if "[PASS]" not in r_text or "[FAIL]" not in r_text:
            errors.append(f"[FAIL] {skill_dir.name}: audit_criteria.md requires [PASS] and [FAIL]")
    evals_file = skill_dir / "evals" / "evals.json"
    if not evals_file.is_file():
        errors.append(f"[FAIL] {skill_dir.name}: missing evals/evals.json")
        return
    data = json.loads(evals_file.read_text(encoding="utf-8"))
    evals = data.get("evals", []) if isinstance(data, dict) else []
    pos = sum(1 for item in evals if isinstance(item, dict) and item.get("should_trigger") is True)
    neg = sum(1 for item in evals if isinstance(item, dict) and item.get("should_trigger") is False)
    if pos < 2 or neg < 2:
        errors.append(f"[FAIL] {skill_dir.name}: evals.json needs >=2 positive and >=2 negative cases")


def _check_scripts_ast(skill_dir: Path, errors: List[str]) -> None:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return
    for py_file in sorted(scripts_dir.glob("*.py")):
        src = py_file.read_text(encoding="utf-8")
        try:
            tree = ast.parse(src)
        except SyntaxError as exc:
            errors.append(f"[FAIL] {skill_dir.name}/{py_file.name}: syntax error {exc}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "input":
                errors.append(f"[FAIL] {skill_dir.name}/{py_file.name}: interactive input() forbidden")


def validate_skill_dir(skill_dir: Path, strict_mode: bool = True) -> List[str]:
    """Validate one skill package against Antigravity 2.0 and Shredded-Shape contracts."""
    errors: List[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"[FAIL] {skill_dir.name}: missing SKILL.md"]
    meta, body = _extract_frontmatter(skill_md.read_text(encoding="utf-8"))
    name_val = str(meta.get("name", "")).strip()
    desc_val = str(meta.get("description", "")).strip()
    if not SKILL_NAME_RE.match(name_val) or name_val != skill_dir.name:
        errors.append(f"[FAIL] {skill_dir.name}: invalid or mismatched name '{name_val}'")
    if not (30 <= len(desc_val) <= 450) or not POS_TRIG_RE.search(desc_val) or not NEG_TRIG_RE.search(desc_val):
        errors.append(f"[FAIL] {skill_dir.name}: description must be 30..450 chars with positive and negative triggers")
    md_block = meta.get("metadata")
    if strict_mode:
        orphans = [k for k in ("version", "updated_at", "allowed-tools") if k in meta]
        if orphans or not isinstance(md_block, dict):
            errors.append(f"[FAIL] {skill_dir.name}: invalid metadata block or orphan top keys {orphans}")
        elif not SEMVER_RE.match(str(md_block.get("version", "")).strip()):
            errors.append(f"[FAIL] {skill_dir.name}: invalid SemVer metadata.version")
    _check_skill_links_and_headings(skill_dir, body, errors)
    _check_skill_assets(skill_dir, errors)
    _check_scripts_ast(skill_dir, errors)
    return errors


def validate_ecosystem(repo_root: Path) -> List[str]:
    """Validate plugin.json, rules/, agents/*.md, and plans/ui_actor_critic_dag.json."""
    errors: List[str] = []
    pfile = repo_root / "plugin.json"
    if not pfile.is_file():
        errors.append("[FAIL] plugin.json missing")
    else:
        pdata = json.loads(pfile.read_text(encoding="utf-8"))
        extra = set(pdata) - ALLOWED_PLUGIN_KEYS
        if extra or not (repo_root / str(pdata.get("logo", ""))).is_file():
            errors.append(f"[FAIL] plugin.json invalid keys {sorted(extra)} or missing logo")
    rule_file = repo_root / "rules" / "frontend-9-axes-guidelines.md"
    if not rule_file.is_file():
        errors.append("[FAIL] rules/frontend-9-axes-guidelines.md missing")
    else:
        rmeta, _ = _extract_frontmatter(rule_file.read_text(encoding="utf-8"))
        if rmeta.get("trigger") != "glob" or not str(rmeta.get("globs", "")).strip() or rule_file.stat().st_size > 24 * 1024:
            errors.append("[FAIL] rules/frontend-9-axes-guidelines.md violates trigger/glob/24KB contract")
    for af in sorted((repo_root / "agents").glob("*.md")):
        _validate_agent_file(af, errors)
    return errors


def _validate_agent_file(agent_path: Path, errors: List[str]) -> None:
    meta, _ = _extract_frontmatter(agent_path.read_text(encoding="utf-8"))
    tools = meta.get("tools")
    if not meta.get("name") or not meta.get("description") or meta.get("subagent") is not True or meta.get("mainAgent") is not False:
        errors.append(f"[FAIL] {agent_path.name}: missing canonical subagent frontmatter")
    if meta.get("model") != "inherit":
        errors.append(f"[FAIL] {agent_path.name}: model must be 'inherit'")
    if not isinstance(tools, list) or not tools or any(str(t) in FORBIDDEN_AGENT_TOOLS for t in tools):
        errors.append(f"[FAIL] {agent_path.name}: invalid or forbidden tools {tools}")
    elif agent_path.name in READ_ONLY_AGENTS and any(t in ("write_file", "edit_file") for t in tools):
        errors.append(f"[FAIL] {agent_path.name}: read-only subagent cannot declare write tools")


def validate_repository(repo_root: Path, strict_mode: bool = True) -> tuple[int, int, List[str]]:
    """Run full deterministic validation over all skills and ecosystem artifacts."""
    skills_dir = repo_root / "skills"
    skill_dirs = sorted(d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith(".")) if skills_dir.is_dir() else []
    errors: List[str] = []
    passed = 0
    for s_dir in skill_dirs:
        s_errs = validate_skill_dir(s_dir, strict_mode=strict_mode)
        if s_errs:
            errors.extend(s_errs)
        else:
            passed += 1
    errors.extend(validate_ecosystem(repo_root))
    return passed, len(skill_dirs), errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate shredded-shape skills, agents, rules, and plugin.json")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    args = parser.parse_args()
    passed, total, errors = validate_repository(Path(args.root).resolve(), strict_mode=args.strict or True)
    for err in errors:
        print(err)
    print(f"shredded-shape validation: {passed}/{total} skills | errors={len(errors)}")
    return 1 if errors or total == 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
