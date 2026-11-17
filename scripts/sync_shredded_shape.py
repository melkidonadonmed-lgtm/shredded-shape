#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Synchronize shredded-shape plugin bundle, vendored _ss_core, and agent mirrors."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_GEMINI_ROOT = Path(r"C:\Users\melki\.gemini")


def _write_lf(src: Path, dst: Path) -> None:
    """Copy a UTF-8 text file normalized to LF line endings."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text(encoding="utf-8").replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def _copy_tree(src: Path, dst: Path) -> int:
    if not src.exists():
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in sorted(src.rglob("*")):
        if "__pycache__" in item.parts or item.suffix == ".pyc":
            continue
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            count += 1
    return count


def _vendor_core_into_skills(core_src: Path, skills_root: Path) -> int:
    if not core_src.is_file() or not skills_root.is_dir():
        return 0
    vendored = 0
    for s_dir in sorted(d for d in skills_root.iterdir() if d.is_dir() and not d.name.startswith(".")):
        scripts_dir = s_dir / "scripts"
        if scripts_dir.is_dir():
            _write_lf(core_src, scripts_dir / "_ss_core.py")
            vendored += 1
    return vendored


def _sync_local_workspace_mirrors(repo_root: Path, core_src: Path, agents_src: Path) -> tuple[int, int]:
    """Clean legacy root triad files, vendor _ss_core locally, and sync .agents/agents."""
    triad_cleaned = 0
    for legacy_name in ("CONTEXT.md", "SPEC.md"):
        legacy_path = repo_root / legacy_name
        if legacy_path.is_file() and (repo_root / ".context" / legacy_name.lower()).is_file():
            legacy_path.unlink(missing_ok=True)
            triad_cleaned += 1
    local_vendored = _vendor_core_into_skills(core_src, repo_root / "skills")
    if not agents_src.is_dir():
        return triad_cleaned, local_vendored
    local_agents_dst = repo_root / ".agents" / "agents"
    local_agents_dst.mkdir(parents=True, exist_ok=True)
    allowed_names = {af.name for af in agents_src.glob("*.md")}
    for existing in list(local_agents_dst.glob("*.md")):
        if existing.name not in allowed_names:
            existing.unlink(missing_ok=True)
    for af in sorted(agents_src.glob("*.md")):
        _write_lf(af, local_agents_dst / af.name)
    return triad_cleaned, local_vendored


def _sync_global_gemini_agents(agents_src: Path, gemini_root: Path) -> None:
    """Sync UI subagents to gemini_root/agents and remove stale copies in gemini_root/config/agents."""
    if not agents_src.is_dir():
        return
    dst_dir = gemini_root / "agents"
    dst_dir.mkdir(parents=True, exist_ok=True)
    cfg_agents_dir = gemini_root / "config" / "agents"
    for af in sorted(agents_src.glob("*.md")):
        _write_lf(af, dst_dir / af.name)
        if cfg_agents_dir.is_dir():
            (cfg_agents_dir / af.name).unlink(missing_ok=True)


def sync_shredded_shape(
    repo_root: Path = ROOT_DIR,
    gemini_root: Path = DEFAULT_GEMINI_ROOT,
    sync_local_workspace: bool | None = None,
    local_only: bool = False,
) -> dict[str, Any]:
    """Deploy shredded-shape plugin bundle and update local workspace mirrors when authorized."""
    do_local = (gemini_root.resolve() == DEFAULT_GEMINI_ROOT.resolve()) if sync_local_workspace is None else sync_local_workspace
    core_src = repo_root / "scripts" / "_ss_core.py"
    agents_src = repo_root / "agents"
    agents_copied = len(list(agents_src.glob("*.md"))) if agents_src.is_dir() else 0
    triad_cleaned, local_vendored = (
        _sync_local_workspace_mirrors(repo_root, core_src, agents_src) if (do_local or local_only) else (0, 0)
    )
    if local_only:
        return {
            "status": "LOCAL_SYNCHRONIZED",
            "plugin": "shredded-shape",
            "triad_mirrored": 0,
            "legacy_mirrors_cleaned": triad_cleaned,
            "vendored_core_targets": local_vendored,
            "agents_synced": agents_copied,
        }

    plugin_dst = gemini_root / "config" / "plugins" / "shredded-shape"
    if plugin_dst.exists():
        shutil.rmtree(plugin_dst)
    plugin_dst.mkdir(parents=True, exist_ok=True)

    copied = sum(_copy_tree(repo_root / folder, plugin_dst / folder) for folder in ("skills", "rules", "plans", "assets", "agents"))
    for root_file in ("plugin.json", "README.md"):
        rf = repo_root / root_file
        if rf.is_file():
            shutil.copy2(rf, plugin_dst / root_file)
            copied += 1
    vendored_count = _vendor_core_into_skills(core_src, plugin_dst / "skills")
    _sync_global_gemini_agents(agents_src, gemini_root)

    return {
        "status": "SYNCHRONIZED",
        "plugin": "shredded-shape",
        "plugin_dst": str(plugin_dst),
        "triad_mirrored": 0,
        "legacy_mirrors_cleaned": triad_cleaned,
        "plugin_files_copied": copied,
        "vendored_core_targets": vendored_count,
        "agents_synced": agents_copied,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize shredded-shape plugin bundle and local mirrors")
    parser.add_argument("--local-only", action="store_true", help="Sync only repo vendored _ss_core and .agents/agents")
    args = parser.parse_args()
    summary = sync_shredded_shape(local_only=bool(args.local_only))
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
