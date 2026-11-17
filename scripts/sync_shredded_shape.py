#!/usr/bin/env python3
"""Synchronize shredded-shape into ~/.gemini/config/plugins/shredded-shape and mirror Triad v2.1."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_GEMINI_ROOT = Path(r"C:\Users\melki\.gemini")


def _copy_tree(src: Path, dst: Path) -> int:
    if not src.exists():
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in src.rglob("*"):
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


def sync_shredded_shape(repo_root: Path = ROOT_DIR, gemini_root: Path = DEFAULT_GEMINI_ROOT) -> Dict[str, Any]:
    """Maintain canonical .context/{context,spec}.md without root mirrors and deploy plugin bundle."""
    triad_cleaned = 0
    for legacy_name in ("CONTEXT.md", "SPEC.md"):
        legacy_path = repo_root / legacy_name
        ctx_path = repo_root / ".context" / legacy_name.lower()
        if legacy_path.is_file() and ctx_path.is_file():
            legacy_path.unlink(missing_ok=True)
            triad_cleaned += 1

    plugin_dst = gemini_root / "config" / "plugins" / "shredded-shape"
    if plugin_dst.exists():
        shutil.rmtree(plugin_dst)
    plugin_dst.mkdir(parents=True, exist_ok=True)

    copied = 0
    for folder in ("skills", "rules", "plans", "assets"):
        copied += _copy_tree(repo_root / folder, plugin_dst / folder)
    for root_file in ("plugin.json", "README.md"):
        rf = repo_root / root_file
        if rf.is_file():
            shutil.copy2(rf, plugin_dst / root_file)
            copied += 1

    agents_copied = 0
    agents_src = repo_root / "agents"
    if agents_src.is_dir():
        (gemini_root / "agents").mkdir(parents=True, exist_ok=True)
        for af in sorted(agents_src.glob("*.md")):
            shutil.copy2(af, gemini_root / "agents" / af.name)
            agents_copied += 1

    return {
        "status": "SYNCHRONIZED",
        "plugin": "shredded-shape",
        "plugin_dst": str(plugin_dst),
        "triad_mirrored": 0,
        "legacy_mirrors_cleaned": triad_cleaned,
        "plugin_files_copied": copied,
        "agents_synced": agents_copied,
    }


def main() -> int:
    summary = sync_shredded_shape()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
