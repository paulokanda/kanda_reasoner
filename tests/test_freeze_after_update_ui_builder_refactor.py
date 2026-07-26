"""Static characterization tests for Freeze tab UI builder mixin."""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.freeze_after_update_gui._ui_builder import FreezeUiBuilderMixin
from kanda_reasoner_app.freeze_after_update_gui.freeze_after_update_tab import (
    FreezeAfterUpdateTab,
)


def test_ui_builder_mixin_stays_below_facade_and_import_compatible() -> None:
    source = Path(sys.modules[FreezeUiBuilderMixin.__module__].__file__).read_text(encoding="utf-8")

    assert issubclass(FreezeAfterUpdateTab, FreezeUiBuilderMixin)
    assert hasattr(FreezeAfterUpdateTab, "_build_ui")
    assert hasattr(FreezeAfterUpdateTab, "_connect_signals")
    assert "freeze_after_update_tab" not in source
    assert "__all__ = [\"FreezeUiBuilderMixin\"]" in source


def test_ui_builder_preserves_widget_names_and_button_text() -> None:
    source = Path(sys.modules[FreezeUiBuilderMixin.__module__].__file__).read_text(encoding="utf-8")

    for snippet in (
        'QPushButton("Help")',
        'QPushButton("Get Last Freeze")',
        'QPushButton("Get All Frozen")',
        'QPushButton("Get blueprint Freeze")',
        'QPushButton("Box Folder")',
        'QPushButton("External AI Review Folder")',
        'QPushButton("Local Freeze Entry")',
        '"freeze_after_update_project_root_edit"',
        '"freeze_after_update_box_folder_button"',
        '"freeze_after_update_external_ai_review_folder_button"',
    ):
        assert snippet in source


def test_ui_builder_preserves_signal_targets() -> None:
    source = Path(sys.modules[FreezeUiBuilderMixin.__module__].__file__).read_text(encoding="utf-8")

    for snippet in (
        "self.project_root_edit.textChanged.connect(self._refresh_derived_paths)",
        "self.choose_project_button.clicked.connect(self._choose_project_folder)",
        "self.check_button.clicked.connect(self._check_box_status)",
        "self.create_button.clicked.connect(self._create_or_repair_box)",
        "self.prepare_staged_action_button.clicked.connect(self._prepare_staged_freeze_action)",
        "self.do_staged_action_button.clicked.connect(self._do_staged_freeze_action)",
        "self.undo_staged_action_button.clicked.connect(self._undo_staged_freeze_action)",
        "self.new_local_freeze_entry_button.clicked.connect(self._open_local_freeze_entry_dialog)",
        "self.box_folder_button.clicked.connect(self._open_box_folder)",
        "self.external_ai_review_folder_button.clicked.connect(self._open_output_folder)",
        "self.help_button.clicked.connect(self._show_help_window)",
        "self.get_last_freeze_button.clicked.connect(self._copy_last_freeze_snippet)",
        "self.get_all_frozen_button.clicked.connect(self._copy_all_frozen_snippets)",
        "self.get_blueprint_freeze_button.clicked.connect(self._copy_freeze_form_blueprint)",
    ):
        assert snippet in source


def main() -> int:
    test_ui_builder_mixin_stays_below_facade_and_import_compatible()
    test_ui_builder_preserves_widget_names_and_button_text()
    test_ui_builder_preserves_signal_targets()
    print("VALIDATION OK: freeze-after-update-ui-builder-refactor")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
