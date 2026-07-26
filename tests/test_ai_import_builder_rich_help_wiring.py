"""Regression tests for removed AI Import Builder rich-help surface."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_tools_gui_shell.help_docs.path_resolver import (
    find_page_by_legacy_catalog,
)

HELP_DOCS_ROOT = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "help_docs"
)
HELP_SOURCE = HELP_DOCS_ROOT / "source" / "ai_import_builder.md"
HELP_RENDERED = HELP_DOCS_ROOT / "rendered" / "ai_import_builder.html"
HELP_MANIFEST = HELP_DOCS_ROOT / "manifest.json"
HELP_FALLBACK = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_help"
    / "ai_import_builder.json"
)
HELP_ASSETS = (
    "assets/drawings/ai_import_builder_opener_shipping_desk.png",
    "assets/drawings/ai_import_builder_startup_pack_intake.png",
    "assets/drawings/ai_import_builder_reassembly_validation.png",
)


def test_rich_help_manifest_no_longer_exposes_ai_import_builder() -> None:
    manifest = json.loads(HELP_MANIFEST.read_text(encoding="utf-8"))
    pages = manifest.get("pages", [])

    assert all(page.get("id") != "ai_import_builder" for page in pages)
    assert all(page.get("tab_id") != "ai_import_builder" for page in pages)
    assert all(page.get("legacy_help_catalog") != "ai_import_builder.json" for page in pages)


def test_legacy_catalog_no_longer_resolves_to_rich_help_page() -> None:
    assert find_page_by_legacy_catalog("ai_import_builder.json") is None


def test_deprecated_help_files_are_removed_from_active_help_surface() -> None:
    assert not HELP_SOURCE.exists()
    assert not HELP_RENDERED.exists()
    assert not HELP_FALLBACK.exists()
    for asset in HELP_ASSETS:
        assert not (HELP_DOCS_ROOT / asset).exists()


def test_json_splitter_owner_code_remains_available_for_non_gui_contracts() -> None:
    assert (PROJECT_ROOT / "kanda_reasoner_app" / "json_splitter" / "json_splitter_8.py").is_file()


if __name__ == "__main__":
    test_rich_help_manifest_no_longer_exposes_ai_import_builder()
    test_legacy_catalog_no_longer_resolves_to_rich_help_page()
    test_deprecated_help_files_are_removed_from_active_help_surface()
    test_json_splitter_owner_code_remains_available_for_non_gui_contracts()
    print("AI Import Builder GUI surface removal tests passed.")
