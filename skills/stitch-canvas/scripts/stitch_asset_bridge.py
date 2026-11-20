#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.7.0"]
# ///
"""Cross-platform Google Stitch Canvas asset bridge (SSRF-safe download, =w{width}, RAW SHA-256)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ALLOWED_ASSET_HOSTS = ("googleusercontent.com", "storage.googleapis.com", "stitch.googleapis.com")
SCREENSHOT_WIDTH_RE = re.compile(r"=w\d+(?:-[A-Za-z0-9_-]+)?$")


class ScreenInstanceRef(BaseModel):
    """Minimal screen instance selector accepted by Stitch apply_design_system."""

    model_config = ConfigDict(extra="forbid")
    id: str = Field(min_length=1)
    sourceScreen: str = Field(min_length=1)


class StitchAssetCheck(BaseModel):
    """Read-After-Write checksum record for one downloaded Stitch artifact."""

    model_config = ConfigDict(extra="forbid")
    path: str
    bytes_written: int
    sha256: str


class StitchBridgeReport(BaseModel):
    """Structured report emitted by stitch_asset_bridge.py."""

    model_config = ConfigDict(extra="forbid")
    verdict: str
    action: str
    selected_instances: list[ScreenInstanceRef] = Field(default_factory=list)
    normalized_screenshot_url: str | None = None
    files: list[StitchAssetCheck] = Field(default_factory=list)


def validate_stitch_asset_url(url: str) -> str:
    """Validate HTTPS scheme and allowlisted Google Stitch asset hostnames."""
    parsed = urllib.parse.urlparse(url.strip())
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not host:
        raise ValueError(f"Unsafe URL scheme or empty host: {url!r}")
    if not any(host == allowed or host.endswith(f".{allowed}") for allowed in ALLOWED_ASSET_HOSTS):
        raise ValueError(f"Host '{host}' outside Stitch asset allowlist")
    return url.strip()


def normalize_screenshot_url(url: str, width: int) -> str:
    """Ensure full-resolution =w{width} suffix on Stitch Google CDN screenshot URLs."""
    clean = validate_stitch_asset_url(url)
    if width <= 0:
        raise ValueError(f"width must be > 0, got {width}")
    if SCREENSHOT_WIDTH_RE.search(clean):
        return SCREENSHOT_WIDTH_RE.sub(f"=w{width}", clean)
    return f"{clean}=w{width}"


def filter_screen_instances(project_payload: dict[str, Any]) -> list[ScreenInstanceRef]:
    """Extract only real screen instances ({id, sourceScreen}) excluding DESIGN_SYSTEM_INSTANCE."""
    raw_items = project_payload.get("screenInstances")
    if raw_items is None and isinstance(project_payload.get("data"), dict):
        raw_items = project_payload["data"].get("screenInstances")
    if not isinstance(raw_items, list):
        return []
    kept: list[ScreenInstanceRef] = []
    for item in raw_items:
        if not isinstance(item, dict) or item.get("type") == "DESIGN_SYSTEM_INSTANCE":
            continue
        iid = str(item.get("id", "")).strip()
        src = str(item.get("sourceScreen", "")).strip()
        if iid and src:
            kept.append(ScreenInstanceRef(id=iid, sourceScreen=src))
    return kept


def download_verified_asset(url: str, dest: Path) -> StitchAssetCheck:
    """Download an allowlisted HTTPS Stitch asset and return SHA-256 Read-After-Write proof."""
    safe_url = validate_stitch_asset_url(url)
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(safe_url, headers={"User-Agent": "shredded-shape-stitch-bridge/1.6.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    dest.write_bytes(data)
    written = dest.read_bytes()
    return StitchAssetCheck(
        path=str(dest),
        bytes_written=len(written),
        sha256=hashlib.sha256(written).hexdigest(),
    )


def _run_self_test() -> int:
    """Verify URL allowlist, =w{width} normalization, and screenInstances filtering."""
    sample_project = {
        "screenInstances": [
            {"id": "ds-1", "sourceScreen": "projects/1/screens/ds", "type": "DESIGN_SYSTEM_INSTANCE"},
            {"id": "scr-1", "sourceScreen": "projects/1/screens/1", "x": 10, "y": 20, "width": 1280, "height": 800},
        ]
    }
    filtered = filter_screen_instances(sample_project)
    assert len(filtered) == 1 and filtered[0].model_dump() == {"id": "scr-1", "sourceScreen": "projects/1/screens/1"}
    norm = normalize_screenshot_url("https://lh3.googleusercontent.com/aida/example-token", 1280)
    assert norm.endswith("=w1280")
    assert normalize_screenshot_url(norm, 1440).endswith("=w1440")
    try:
        validate_stitch_asset_url("http://169.254.169.254/latest/meta-data")
    except ValueError:
        return 0
    return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cross-platform Stitch Canvas bridge utilities")
    parser.add_argument("action", nargs="?", choices=["filter-instances", "normalize-url", "download-screen"])
    parser.add_argument("--project-json", help="Path to get_project JSON output")
    parser.add_argument("--url", help="Asset URL for normalize-url")
    parser.add_argument("--html-url", help="Stitch htmlCode.downloadUrl")
    parser.add_argument("--screenshot-url", help="Stitch screenshot.downloadUrl")
    parser.add_argument("--width", type=int, default=1280, help="Target screenshot width (=w{width})")
    parser.add_argument("--out-dir", default=".stitch/designs", help="Output directory for downloaded assets")
    parser.add_argument("--page", default="screen", help="Slug filename for downloaded artifacts")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON output")
    parser.add_argument("--self-test", action="store_true", help="Run built-in deterministic assertions")
    return parser


def _dispatch_action(args: argparse.Namespace) -> StitchBridgeReport:
    if args.action == "filter-instances":
        if not args.project_json:
            raise ValueError("--project-json is required for filter-instances")
        payload = json.loads(Path(args.project_json).read_text(encoding="utf-8"))
        return StitchBridgeReport(verdict="[PASS]", action="filter-instances", selected_instances=filter_screen_instances(payload))
    if args.action == "normalize-url":
        if not args.url:
            raise ValueError("--url is required for normalize-url")
        return StitchBridgeReport(verdict="[PASS]", action="normalize-url", normalized_screenshot_url=normalize_screenshot_url(args.url, args.width))
    if args.action == "download-screen":
        checks: list[StitchAssetCheck] = []
        out_dir = Path(args.out_dir)
        if args.html_url:
            checks.append(download_verified_asset(args.html_url, out_dir / f"{args.page}.html"))
        if args.screenshot_url:
            full_png = normalize_screenshot_url(args.screenshot_url, args.width)
            checks.append(download_verified_asset(full_png, out_dir / f"{args.page}.png"))
        if not checks:
            raise ValueError("Provide --html-url and/or --screenshot-url for download-screen")
        return StitchBridgeReport(verdict="[PASS]", action="download-screen", files=checks)
    raise ValueError("Specify an action or --self-test")


def main() -> int:
    """CLI entrypoint for Stitch asset normalization, filtering, and verified downloads."""
    args = _build_parser().parse_args()
    if args.self_test:
        rc = _run_self_test()
        if args.json:
            print(json.dumps({"verdict": "[PASS]" if rc == 0 else "[FAIL]", "self_test": rc == 0}))
        return rc
    report = _dispatch_action(args)
    print(report.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
