# project-path: kanda_reasoner_app/project_structure_visualizer/web_assets.py
"""Local HTML asset assembly for Project Structure 3D."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

__all__ = ["asset_root", "build_visualizer_html", "vendor_manifest"]

_VENDOR_VERSION = "1.80.0"
_VENDOR_ASSET = "vendor/3d-force-graph-1.80.0.min.js"
_VENDOR_MANIFEST = "vendor/VENDOR_MANIFEST.json"


def asset_root() -> Path:
    """Return the package-owned local visualizer asset folder."""
    return Path(__file__).resolve().with_name("web")


def _read_asset(filename: str) -> str:
    """Read one UTF-8 local asset with strict decoding."""
    return (asset_root() / filename).read_text(
        encoding="utf-8",
        errors="strict",
    )


def _sha256(path: Path) -> str:
    """Return one lowercase SHA-256 digest."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def vendor_manifest() -> dict[str, Any]:
    """Load and verify the pinned local renderer manifest."""
    manifest_path = asset_root() / _VENDOR_MANIFEST
    loaded = json.loads(manifest_path.read_text(encoding="utf-8", errors="strict"))
    if not isinstance(loaded, dict):
        raise RuntimeError("3d-force-graph vendor manifest root must be an object")
    if loaded.get("package_name") != "3d-force-graph":
        raise RuntimeError("unexpected local renderer package name")
    if loaded.get("package_version") != _VENDOR_VERSION:
        raise RuntimeError("unexpected local renderer package version")
    if loaded.get("license") != "MIT":
        raise RuntimeError("unexpected local renderer license")
    asset_path = asset_root() / _VENDOR_ASSET
    if not asset_path.is_file():
        raise RuntimeError("pinned local 3d-force-graph asset is missing")
    expected_hash = str(loaded.get("asset_sha256", "")).lower()
    if len(expected_hash) != 64 or _sha256(asset_path) != expected_hash:
        raise RuntimeError("pinned local 3d-force-graph SHA-256 mismatch")
    if asset_path.stat().st_size != int(loaded.get("asset_size_bytes", -1)):
        raise RuntimeError("pinned local 3d-force-graph size mismatch")
    license_path = asset_root() / "vendor/LICENSE-3d-force-graph.txt"
    if not license_path.is_file() or "MIT License" not in license_path.read_text(
        encoding="utf-8", errors="strict"
    ):
        raise RuntimeError("local 3d-force-graph MIT license text is missing")
    return loaded


def build_visualizer_html(
    graph_json: str,
    generation_id: str,
    *,
    embedded: bool,
) -> str:
    """Build one self-contained local WebGL renderer document."""
    template = _read_asset("index_template.html")
    manifest = vendor_manifest()
    qwebchannel_script = (
        '<script src="qrc:///qtwebchannel/qwebchannel.js"></script>'
        if embedded
        else ""
    )
    replacements = {
        "{{KANDA_STYLE}}": _read_asset("graph_theme.css"),
        "{{KANDA_QWEBCHANNEL_SCRIPT}}": qwebchannel_script,
        "{{KANDA_VENDOR_MANIFEST_JSON}}": json.dumps(
            manifest, ensure_ascii=True, separators=(",", ":")
        ),
        "{{KANDA_VENDOR_SCRIPT}}": _read_asset(_VENDOR_ASSET),
        "{{KANDA_QT_BRIDGE_SCRIPT}}": _read_asset("qt_bridge_bootstrap.js"),
        "{{KANDA_BROWSER_DETAILS_SCRIPT}}": _read_asset("browser_details.js"),
        "{{KANDA_NAVIGATION_SCRIPT}}": _read_asset("graph_navigation.js"),
        "{{KANDA_PAINTER_SCRIPT}}": _read_asset("graph_painter.js"),
        "{{KANDA_SCRIPT}}": _read_asset("graph_renderer.js"),
        "{{KANDA_GRAPH_JSON}}": graph_json,
        "{{KANDA_GENERATION_ID}}": generation_id,
        "{{KANDA_EMBEDDED}}": "true" if embedded else "false",
    }
    html = template
    for token, value in replacements.items():
        html = html.replace(token, value)
    if "{{KANDA_" in html:
        raise RuntimeError("visualizer HTML contains an unresolved token")
    return html
