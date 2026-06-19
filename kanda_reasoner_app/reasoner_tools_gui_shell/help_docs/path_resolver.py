"""Safe path resolution for local desktop help documents."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HELP_DOCS_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = HELP_DOCS_ROOT / "manifest.json"

__all__ = [
    "HelpPage",
    "HELP_DOCS_ROOT",
    "MANIFEST_PATH",
    "find_page_by_legacy_catalog",
    "load_help_manifest",
    "resolve_help_child",
]


@dataclass(frozen=True)
class HelpPage:
    """Resolved local help page paths."""

    page_id: str
    title: str
    legacy_help_catalog: str
    source_path: Path
    rendered_path: Path
    css_path: Path
    asset_paths: tuple[Path, ...]


def load_help_manifest() -> dict[str, Any]:
    """Load the local help manifest."""

    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def resolve_help_child(relative_path: str) -> Path:
    """Resolve a help-doc path and reject traversal outside the help root."""

    text = str(relative_path or "").replace("\\", "/").strip()
    if not text:
        raise ValueError("help path is empty")
    if text.startswith("/") or ":" in text:
        raise ValueError("help path must be relative")
    candidate = (HELP_DOCS_ROOT / text).resolve()
    root = HELP_DOCS_ROOT.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("help path escapes help_docs")
    return candidate


def _page_from_manifest_entry(entry: dict[str, Any]) -> HelpPage:
    assets = tuple(resolve_help_child(path) for path in entry.get("assets", []))
    return HelpPage(
        page_id=str(entry["id"]),
        title=str(entry["title"]),
        legacy_help_catalog=str(entry.get("legacy_help_catalog", "")),
        source_path=resolve_help_child(str(entry["source"])),
        rendered_path=resolve_help_child(str(entry["rendered"])),
        css_path=resolve_help_child(str(entry["css"])),
        asset_paths=assets,
    )


def find_page_by_legacy_catalog(legacy_help_catalog: str) -> HelpPage | None:
    """Return the rich help page mapped to a legacy JSON help catalog."""

    catalog = str(legacy_help_catalog or "").strip()
    if not catalog:
        return None
    manifest = load_help_manifest()
    for entry in manifest.get("pages", []):
        if not isinstance(entry, dict):
            continue
        if str(entry.get("legacy_help_catalog", "")).strip() == catalog:
            return _page_from_manifest_entry(entry)
    return None
