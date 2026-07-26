"""Characterization tests for Freeze tab frozen-memory export mixin."""
from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.freeze_after_update_gui._freeze_memory_exports import (
    FreezeMemoryExportMixin,
)
from kanda_reasoner_app.freeze_after_update_gui.freeze_after_update_tab import (
    FreezeAfterUpdateTab,
)


class _DummyExports(FreezeMemoryExportMixin):
    def __init__(self, project_root: Path) -> None:
        self._root = project_root
        self.logged: list[str] = []

    def _project_root(self) -> Path:
        return self._root

    def _append_log(self, message: str) -> None:
        self.logged.append(message)


def test_export_mixin_stays_below_facade_and_import_compatible() -> None:
    source = Path(sys.modules[FreezeMemoryExportMixin.__module__].__file__).read_text(encoding="utf-8")

    assert issubclass(FreezeAfterUpdateTab, FreezeMemoryExportMixin)
    assert "freeze_after_update_tab" not in source
    assert "__all__ = [\"FreezeMemoryExportMixin\"]" in source


def test_freeze_snippet_text_preserves_entry_content_and_markers() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        entry = root / "freeze-entry.md"
        entry.write_text("---\ndate: 2026-06-30\n---\n\n# Demo Freeze\n", encoding="utf-8")
        dummy = _DummyExports(root)

        snippet = dummy._build_freeze_snippet_text([entry], title="Last frozen feature entry")

    assert snippet.startswith("KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_BEGIN")
    assert "Title: Last frozen feature entry" in snippet
    assert "Entry count: 1" in snippet
    assert "Path: " in snippet
    assert "# Demo Freeze" in snippet
    assert snippet.rstrip().endswith("KANDA_FROZEN_FEATURE_MEMORY_SNIPPET_END")


def test_help_html_keeps_local_freeze_contract_text() -> None:
    dummy = _DummyExports(Path("E:/demo_project"))

    html = dummy._render_help_html()

    assert "Freeze Feature After Update - Practical Help" in html
    assert "Confirm and Write" in html
    assert "project_freeze_ledger" in html
    assert "project_freeze_after_update" in html


def test_freeze_form_blueprint_has_receiver_contract_and_required_fields() -> None:
    dummy = _DummyExports(Path("E:/demo_project"))

    blueprint = dummy._build_freeze_form_blueprint_text()

    assert "KANDA_FREEZE_FORM_JSON_BEGIN" in blueprint
    assert "KANDA_FREEZE_FORM_JSON_END" in blueprint
    assert "VALIDATION OK: <feature_id>" in blueprint
    assert "STATUS: IN_SYNC" in blueprint
    assert "ZIP CONTRACT: PASS" in blueprint
    for field_name in (
        "feature_title",
        "primary_box",
        "box_type",
        "validated_files",
        "generated_files",
        "protected_paths",
        "do_not_regress_rules",
        "validation_evidence_summary",
        "known_warnings",
        "planned_next_step",
        "notes",
    ):
        assert '"' + field_name + '"' in blueprint


def main() -> int:
    test_export_mixin_stays_below_facade_and_import_compatible()
    test_freeze_snippet_text_preserves_entry_content_and_markers()
    test_help_html_keeps_local_freeze_contract_text()
    test_freeze_form_blueprint_has_receiver_contract_and_required_fields()
    print("VALIDATION OK: freeze-after-update-export-mixin-refactor")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
