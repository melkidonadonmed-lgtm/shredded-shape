#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0.0"]
# ///
"""Deterministic contract validator for the shredded-shape UI/UX skill and plugin suite."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

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
    "homepage", "repository", "license", "keywords", "logo", "suggestedPrompts", "disabled",
})
FORBIDDEN_AGENT_TOOLS = frozenset({
    "*", "call_mcp_tool", "view_file", "list_dir", "find_by_name",
    "grep_search", "write_to_file", "replace_file_content", "multi_replace_file_content",
})
READ_ONLY_AGENTS = frozenset({"ui-analyst.md", "ui-planner.md", "ui-judge.md"})
REQUIRED_HEADINGS = ("Overview", "Inputs", "Procedure", "Gotchas", "Output", "User Communication")
CODE_CAP_EXTS = frozenset({".py", ".js", ".mjs", ".html", ".css"})
MAX_DESC_RECOMMENDED = 420


def _extract_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    cleaned = raw.lstrip("\ufeff")
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n?(.*)$", cleaned, re.DOTALL)
    if not match:
        return {}, cleaned
    parsed = yaml.safe_load(match.group(1))
    return (parsed if isinstance(parsed, dict) else {}), match.group(2)


def _check_relative_links(skill_dir: Path, md_file: Path, text: str, errors: list[str]) -> None:
    stripped = re.sub(r"```.*?```|`[^`\n]+`", "", text, flags=re.DOTALL)
    for target in LINK_RE.findall(stripped):
        if target.startswith(("http://", "https://", "file://", "#")):
            continue
        rel = target.split("#", 1)[0].split("?", 1)[0]
        if ".." in Path(rel).parts:
            errors.append(f"[FAIL] {skill_dir.name}/{md_file.name}: parent escape '..' in link '{target}'")
        elif rel and not ((md_file.parent / rel).exists() or (skill_dir / rel).exists()):
            errors.append(f"[FAIL] {skill_dir.name}/{md_file.name}: broken link '{target}'")


def _check_skill_markdown(skill_dir: Path, raw: str, body: str, errors: list[str]) -> None:
    if len(raw.splitlines()) > 500 or len(body.splitlines()) >= 500:
        errors.append(f"[FAIL] {skill_dir.name}: SKILL.md exceeds 500 lines")
    for heading in REQUIRED_HEADINGS:
        if not re.search(rf"^##\s+.*{re.escape(heading)}", body, re.MULTILINE | re.IGNORECASE):
            errors.append(f"[FAIL] {skill_dir.name}: missing required section '{heading}'")
    _check_relative_links(skill_dir, skill_dir / "SKILL.md", body, errors)


_EVAL_CASE_KEYS = frozenset({"id", "prompt", "should_trigger", "assertions"})


def _is_valid_eval_item(item: Any, seen_ids: set[str]) -> bool:
    if not isinstance(item, dict) or set(item.keys()) != _EVAL_CASE_KEYS:
        return False
    eid = str(item["id"]).strip()
    if not eid or eid in seen_ids or not str(item["prompt"]).strip():
        return False
    if not isinstance(item["should_trigger"], bool) or not item["assertions"]:
        return False
    seen_ids.add(eid)
    return True


def _check_evals_json(skill_dir: Path, evals_file: Path, strict_mode: bool, errors: list[str]) -> None:
    if not evals_file.is_file():
        errors.append(f"[FAIL] {skill_dir.name}: missing evals/evals.json")
        return
    data = json.loads(evals_file.read_text(encoding="utf-8"))
    is_valid_root = isinstance(data, dict) and set(data.keys()) == {"skill_name", "evals"} and data.get("skill_name") == skill_dir.name
    if strict_mode and not is_valid_root:
        errors.append(f"[FAIL] {skill_dir.name}: evals.json must use canonical {{skill_name, evals}} keys")
        return
    evals = data.get("evals", []) if isinstance(data, dict) else []
    pos = sum(1 for item in evals if isinstance(item, dict) and item.get("should_trigger") is True)
    neg = sum(1 for item in evals if isinstance(item, dict) and item.get("should_trigger") is False)
    if min(pos, neg) < 2:
        errors.append(f"[FAIL] {skill_dir.name}: evals.json needs >=2 positive and >=2 negative cases")
    seen_ids: set[str] = set()
    for idx, item in enumerate(evals):
        if not _is_valid_eval_item(item, seen_ids):
            errors.append(f"[FAIL] {skill_dir.name}: eval #{idx} has invalid or duplicate id/prompt/assertions")


def _check_skill_assets(skill_dir: Path, strict_mode: bool, errors: list[str]) -> None:
    rules_md = skill_dir / "rules" / "audit_criteria.md"
    if not rules_md.is_file():
        errors.append(f"[FAIL] {skill_dir.name}: missing rules/audit_criteria.md")
    else:
        r_text = rules_md.read_text(encoding="utf-8")
        if "[PASS]" not in r_text or "[FAIL]" not in r_text:
            errors.append(f"[FAIL] {skill_dir.name}: audit_criteria.md requires [PASS] and [FAIL]")
        _check_relative_links(skill_dir, rules_md, r_text, errors)
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        for ref_md in sorted(refs_dir.glob("*.md")):
            r_raw = ref_md.read_text(encoding="utf-8")
            if len(r_raw.splitlines()) > 150:
                errors.append(f"[FAIL] {skill_dir.name}/references/{ref_md.name}: exceeds 150 lines ({len(r_raw.splitlines())})")
            _check_relative_links(skill_dir, ref_md, r_raw, errors)
    _check_evals_json(skill_dir, skill_dir / "evals" / "evals.json", strict_mode, errors)


def _check_single_script_ast(skill_name: str, item: Path, src: str, errors: list[str]) -> None:
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        errors.append(f"[FAIL] {skill_name}/{item.name}: syntax error {exc}")
        return
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "input":
            errors.append(f"[FAIL] {skill_name}/{item.name}: interactive input() forbidden")


def _check_scripts_ast(skill_dir: Path, errors: list[str]) -> None:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return
    for item in sorted(scripts_dir.iterdir()):
        if not item.is_file() or item.suffix.lower() not in CODE_CAP_EXTS:
            continue
        src = item.read_text(encoding="utf-8", errors="ignore")
        if len(src.splitlines()) > 600:
            errors.append(f"[FAIL] {skill_dir.name}/{item.name}: exceeds 600 lines")
        if item.suffix.lower() == ".py":
            _check_single_script_ast(skill_dir.name, item, src, errors)


def _check_strict_skill_metadata(skill_name: str, meta: dict[str, Any], errors: list[str]) -> None:
    orphans = [k for k in ("version", "updated_at", "allowed-tools") if k in meta]
    md_block = meta.get("metadata")
    if orphans or not isinstance(md_block, dict):
        errors.append(f"[FAIL] {skill_name}: invalid metadata block or orphan top keys {orphans}")
        return
    if not SEMVER_RE.match(str(md_block.get("version", "")).strip()):
        errors.append(f"[FAIL] {skill_name}: invalid SemVer metadata.version")
    elif not (str(meta.get("compatibility", "")).strip() and str(md_block.get("category", "")).strip() and md_block.get("tags")):
        errors.append(f"[FAIL] {skill_name}: missing compatibility, metadata.category, or metadata.tags")


def validate_skill_dir(skill_dir: Path, strict_mode: bool = True) -> list[str]:
    """Validate one skill package against Antigravity 2.0 and Shredded-Shape contracts."""
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"[FAIL] {skill_dir.name}: missing SKILL.md"]
    raw = skill_md.read_text(encoding="utf-8")
    meta, body = _extract_frontmatter(raw)
    name_val = str(meta.get("name", "")).strip()
    desc_val = str(meta.get("description", "")).strip()
    if not SKILL_NAME_RE.match(name_val) or name_val != skill_dir.name:
        errors.append(f"[FAIL] {skill_dir.name}: invalid or mismatched name '{name_val}'")
    pos_clause = NEG_TRIG_RE.split(desc_val, maxsplit=1)[0]
    if not (30 <= len(desc_val) <= MAX_DESC_RECOMMENDED) or not POS_TRIG_RE.search(pos_clause) or not NEG_TRIG_RE.search(desc_val):
        errors.append(f"[FAIL] {skill_dir.name}: description must be 30..{MAX_DESC_RECOMMENDED} chars with positive before negative triggers")
    if strict_mode:
        _check_strict_skill_metadata(skill_dir.name, meta, errors)
    _check_skill_markdown(skill_dir, raw, body, errors)
    _check_skill_assets(skill_dir, strict_mode, errors)
    _check_scripts_ast(skill_dir, errors)
    return errors


def check_jaccard_overlaps(skill_dirs: list[Path], threshold: float = 0.80) -> list[str]:
    """Detect semantic L1 positive description overlap >= threshold across sibling skills."""
    stop = {"use", "when", "this", "skill", "the", "and", "for", "with", "from", "via", "or", "to", "in", "of", "on"}
    tokens_by_name: dict[str, set[str]] = {}
    for s_dir in skill_dirs:
        sm = s_dir / "SKILL.md"
        if not sm.is_file():
            continue
        meta, _ = _extract_frontmatter(sm.read_text(encoding="utf-8"))
        pos_desc = NEG_TRIG_RE.split(str(meta.get("description", "")), maxsplit=1)[0].lower()
        tokens_by_name[s_dir.name] = {w for w in re.findall(r"[a-z0-9_-]{3,}", pos_desc) if w not in stop}
    names = sorted(tokens_by_name)
    return [
        f"[FAIL] L1 Jaccard overlap >= {threshold}: '{left}' vs '{right}'"
        for idx, left in enumerate(names)
        for right in names[idx + 1:]
        if tokens_by_name[left] and tokens_by_name[right]
        and (len(tokens_by_name[left] & tokens_by_name[right]) / len(tokens_by_name[left] | tokens_by_name[right])) >= threshold
    ]


def _check_agent_tools(agent_name: str, policy: str, tools: Any, errors: list[str]) -> None:
    if not isinstance(tools, list) or not tools:
        errors.append(f"[FAIL] {agent_name}: invalid or empty tools {tools}")
        return
    str_tools = [str(t) for t in tools]
    if any(t in FORBIDDEN_AGENT_TOOLS for t in str_tools) or "send_message" not in str_tools:
        errors.append(f"[FAIL] {agent_name}: forbidden tools or missing 'send_message' in {str_tools}")
    if agent_name in READ_ONLY_AGENTS and (any(t in ("write_file", "edit_file") for t in str_tools) or policy != "sandbox"):
        errors.append(f"[FAIL] {agent_name}: read-only subagent requires sandbox policy and zero write tools")


def _validate_agent_file(agent_path: Path, errors: list[str]) -> None:
    raw = agent_path.read_text(encoding="utf-8")
    meta, body = _extract_frontmatter(raw)
    desc_val = str(meta.get("description", "")).strip()
    if not meta.get("name") or not desc_val or meta.get("subagent") is not True or meta.get("mainAgent") is not False:
        errors.append(f"[FAIL] {agent_path.name}: missing canonical subagent frontmatter")
    elif not (30 <= len(desc_val) <= MAX_DESC_RECOMMENDED) or not NEG_TRIG_RE.search(desc_val):
        errors.append(f"[FAIL] {agent_path.name}: description must be 30..{MAX_DESC_RECOMMENDED} chars with 'Do NOT use' boundary")
    if meta.get("model") != "inherit":
        errors.append(f"[FAIL] {agent_path.name}: model must be 'inherit'")
    policy = str(meta.get("commandExecutionPolicy", "sandbox"))
    if policy not in {"auto", "sandbox", "off"}:
        errors.append(f"[FAIL] {agent_path.name}: invalid commandExecutionPolicy")
    _check_agent_tools(agent_path.name, policy, meta.get("tools"), errors)
    if "pt-BR" not in body:
        errors.append(f"[FAIL] {agent_path.name}: subagent body must preserve [LOCK-04] 'pt-BR' communication rule")


def _check_folder_line_caps(repo_root: Path, folder: str, errors: list[str]) -> None:
    d = repo_root / folder
    if not d.is_dir():
        return
    for f in sorted(d.rglob("*")):
        if f.is_file() and f.suffix.lower() in CODE_CAP_EXTS and len(f.read_text("utf-8", errors="ignore").splitlines()) > 600:
            errors.append(f"[FAIL] {f.relative_to(repo_root)} exceeds 600 lines")


def _check_parity_and_line_caps(repo_root: Path, errors: list[str]) -> None:
    agents_dir = repo_root / "agents"
    mirror_dir = repo_root / ".agents" / "agents"
    if agents_dir.is_dir() and mirror_dir.is_dir():
        src_files = {p.name: p for p in agents_dir.glob("*.md")}
        dst_files = {p.name: p for p in mirror_dir.glob("*.md")}
        if set(src_files) != set(dst_files):
            errors.append("[FAIL] .agents/agents filename mismatch with agents/")
        for name, src in src_files.items():
            if name in dst_files and src.read_text("utf-8").replace("\r\n", "\n") != dst_files[name].read_text("utf-8").replace("\r\n", "\n"):
                errors.append(f"[FAIL] .agents/agents/{name} drifted from agents/{name}")
    for shared_src in sorted((repo_root / "scripts").glob("_ss_*.py")):
        if not (repo_root / "skills").is_dir():
            break
        shared_norm = shared_src.read_text("utf-8").replace("\r\n", "\n")
        for s_dir in sorted(d for d in (repo_root / "skills").iterdir() if d.is_dir() and not d.name.startswith(".")):
            scripts_dir = s_dir / "scripts"
            if not scripts_dir.is_dir():
                continue
            vendored = scripts_dir / shared_src.name
            if not vendored.is_file():
                errors.append(f"[FAIL] Missing vendored {vendored.relative_to(repo_root)}")
            elif vendored.read_text("utf-8").replace("\r\n", "\n") != shared_norm:
                errors.append(f"[FAIL] Vendored {vendored.relative_to(repo_root)} drifted from scripts/{shared_src.name}")
    for folder in ("scripts", "assets", "tests"):
        _check_folder_line_caps(repo_root, folder, errors)


def _validate_dag_against_agents(repo_root: Path, tasks: list[Any], errors: list[str]) -> None:
    if len(tasks) != 4:
        errors.append("[FAIL] plans/ui_actor_critic_dag.json must contain 4 stage tasks")
        return
    for task in tasks:
        payload = task.get("payload", {}) if isinstance(task, dict) else {}
        agent_rel = str(payload.get("agent_spec", ""))
        agent_file = repo_root / agent_rel
        if not agent_rel or not agent_file.is_file():
            errors.append(f"[FAIL] DAG task missing valid agent_spec: '{agent_rel}'")
            continue
        ameta, _ = _extract_frontmatter(agent_file.read_text(encoding="utf-8"))
        if payload.get("max_steps") != ameta.get("max_steps") or payload.get("stop_condition") != ameta.get("stop_condition"):
            errors.append(f"[FAIL] {agent_file.name} max_steps/stop_condition drifted from ui_actor_critic_dag.json")
        if payload.get("reasoning_pattern") not in {"CoT", "ToT", "ReAct", "Self-Refine"}:
            errors.append(f"[FAIL] {agent_file.name}: invalid reasoning_pattern in ui_actor_critic_dag.json")


def _validate_9_axes_rule(rule_file: Path, errors: list[str]) -> None:
    if not rule_file.is_file():
        errors.append("[FAIL] rules/frontend-9-axes-guidelines.md missing")
        return
    raw = rule_file.read_text(encoding="utf-8")
    rmeta, rbody = _extract_frontmatter(raw)
    if rmeta.get("trigger") != "glob" or not str(rmeta.get("globs", "")).strip() or rule_file.stat().st_size > 24 * 1024:
        errors.append("[FAIL] rules/frontend-9-axes-guidelines.md violates trigger/glob/24KB contract")
    missing_axes = [idx for idx in range(1, 10) if f"Axis {idx}" not in rbody]
    if missing_axes:
        errors.append(f"[FAIL] rules/frontend-9-axes-guidelines.md missing explicit headings for Axis {missing_axes}")


def validate_ecosystem(repo_root: Path) -> list[str]:
    """Validate plugin.json, rules/, plans/, agents/*.md, mirror parity, and <=600 file caps."""
    errors: list[str] = []
    pfile = repo_root / "plugin.json"
    if not pfile.is_file():
        errors.append("[FAIL] plugin.json missing")
    else:
        pdata = json.loads(pfile.read_text(encoding="utf-8"))
        extra = set(pdata) - ALLOWED_PLUGIN_KEYS
        if extra or not (repo_root / str(pdata.get("logo", ""))).is_file():
            errors.append(f"[FAIL] plugin.json invalid keys {sorted(extra)} or missing logo")
    _validate_9_axes_rule(repo_root / "rules" / "frontend-9-axes-guidelines.md", errors)
    dag_file = repo_root / "plans" / "ui_actor_critic_dag.json"
    if not dag_file.is_file():
        errors.append("[FAIL] plans/ui_actor_critic_dag.json missing")
    else:
        dag_data = json.loads(dag_file.read_text(encoding="utf-8"))
        _validate_dag_against_agents(repo_root, dag_data.get("tasks", []), errors)
    for af in sorted((repo_root / "agents").glob("*.md")):
        _validate_agent_file(af, errors)
    _check_parity_and_line_caps(repo_root, errors)
    return errors


def _check_single_skill_release_parity(s_dir: Path, exp_ver: str, exp_lic: str, errors: list[str]) -> None:
    sm = s_dir / "SKILL.md"
    if not sm.is_file():
        return
    meta, _ = _extract_frontmatter(sm.read_text(encoding="utf-8"))
    md_ver = str((meta.get("metadata") or {}).get("version", "")).strip()
    sk_lic = str(meta.get("license", "")).strip()
    if md_ver != exp_ver or sk_lic != exp_lic:
        errors.append(f"[FAIL] {s_dir.name}: version/license ({md_ver}/{sk_lic}) drifted from plugin.json ({exp_ver}/{exp_lic})")


def _check_release_parity(repo_root: Path, skill_dirs: list[Path], errors: list[str]) -> None:
    pfile = repo_root / "plugin.json"
    pyproj = repo_root / "pyproject.toml"
    if not (skill_dirs and pfile.is_file() and pyproj.is_file()):
        return
    pdata = json.loads(pfile.read_text(encoding="utf-8"))
    proj_meta = tomllib.loads(pyproj.read_text(encoding="utf-8")).get("project", {})
    raw_lic = proj_meta.get("license", "")
    proj_lic = raw_lic.get("text", "") if isinstance(raw_lic, dict) else str(raw_lic)
    exp_ver = str(pdata.get("version", "")).strip()
    exp_lic = str(pdata.get("license", "")).strip()
    if str(proj_meta.get("version", "")).strip() != exp_ver or proj_lic.strip() != exp_lic:
        errors.append(f"[FAIL] pyproject.toml version/license drifted from plugin.json ({exp_ver} / {exp_lic})")
    for s_dir in skill_dirs:
        _check_single_skill_release_parity(s_dir, exp_ver, exp_lic, errors)


def validate_repository(repo_root: Path, strict_mode: bool = True) -> tuple[int, int, list[str]]:
    """Run full deterministic validation over all skills and ecosystem artifacts."""
    skills_dir = repo_root / "skills"
    skill_dirs = sorted(d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith(".")) if skills_dir.is_dir() else []
    errors: list[str] = []
    passed = 0
    for s_dir in skill_dirs:
        s_errs = validate_skill_dir(s_dir, strict_mode=strict_mode)
        if s_errs:
            errors.extend(s_errs)
        else:
            passed += 1
    errors.extend(check_jaccard_overlaps(skill_dirs))
    errors.extend(validate_ecosystem(repo_root))
    if strict_mode:
        _check_release_parity(repo_root, skill_dirs, errors)
    return passed, len(skill_dirs), errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate shredded-shape skills, agents, rules, and plugin.json")
    parser.add_argument("--strict", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    args = parser.parse_args()
    root_dir = Path(args.root).resolve()
    passed, total, errors = validate_repository(root_dir, strict_mode=bool(args.strict))
    agent_files = sorted((root_dir / "agents").glob("*.md")) if (root_dir / "agents").is_dir() else []
    agent_errors = sum(1 for e in errors if any(af.name in e for af in agent_files))
    agent_ok = max(0, len(agent_files) - agent_errors)
    for err in errors:
        print(err)
    print(f"shredded-shape validation: {passed}/{total} skills | {agent_ok}/{len(agent_files)} subagents | errors={len(errors)}")
    return 1 if errors or total == 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
