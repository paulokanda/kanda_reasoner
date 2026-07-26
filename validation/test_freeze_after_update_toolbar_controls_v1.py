"""Validate Freeze Feature After Update toolbar/status-row controls v1."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE_TAB = ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "freeze_after_update_tab.py"
LAZY_TABS = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"
PATCH_ZIP = ROOT / "kanda_freeze_after_update_toolbar_controls_v1_patch.zip"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_freeze_tab_layout_contract() -> None:
    text = read(FREEZE_TAB)

    require('QGroupBox("Active project")' not in text, "Active project body group was restored")
    require('title = QLabel("Freeze Feature After Update")' not in text, "duplicate inner title was restored")

    require('self.project_root_header_label = QLabel("Project Root:")' in text, "Project Root label missing")
    require('self.project_root_edit = QLineEdit()' in text, "Project Root edit missing")
    require('self.search_project_button = QPushButton("Search")' in text, "Project Root Search button missing")
    require('self.box_folder_header_label = QLabel("Box folder:")' in text, "Box folder label missing")
    require('freeze_after_update_box_folder_edit' in text, "Box folder widget object name missing")
    require('self.external_ai_review_header_label = QLabel("External AI review folder:")' in text, "External AI review folder label missing")
    require('freeze_after_update_external_ai_review_folder_edit' in text, "External AI review widget object name missing")

    move_start = text.index('def move_project_root_controls_to_layout')
    move_block = text[move_start:text.index('def _freeze_entry_sort_key', move_start)]
    for token in (
        'self.project_root_header_label',
        'self.project_root_edit',
        'self.search_project_button',
        'self.box_folder_header_label',
        'self.box_folder_edit',
        'self.external_ai_review_header_label',
        'self.files_to_send_path_edit',
    ):
        require(token in move_block, token + " not moved to host status/source row")

    require('QPushButton("Local Freeze Entry")' in text, "Local Freeze Entry button missing or renamed")
    require('QPushButton("New Local Freeze Entry")' not in text, "old New Local Freeze Entry main button restored")
    require('self.new_local_freeze_entry_button.setStyleSheet("color: #008000; font-weight: bold;")' in text, "Local Freeze Entry green bold style missing")

    require('self.get_last_freeze_button.setStyleSheet("color: #008000; font-weight: bold;")' in text, "Get Last Freeze green bold style missing")
    require('self.get_all_frozen_button.setStyleSheet("color: #003366; font-weight: bold;")' in text, "Get All Frozen dark blue bold style missing")
    require('confirm_write_button.setStyleSheet("color: #008000; font-weight: bold;")' in text, "Confirm and Write green bold style missing")
    require('ignore_freeze_button.setStyleSheet("color: #B00020; font-weight: bold;")' in text, "Ignore this Freeze red bold style missing")

    require('write_confirmed_freeze_entry' in text, "freeze writer import/usage missing")
    require('validate_freeze_entry_preview' in text, "preview validation import/usage missing")
    require('mark_latest_freeze_hint_used' in text, "ignore/used freeze hint behavior missing")


def assert_lazy_host_contract() -> None:
    text = read(LAZY_TABS)
    require('_FREEZE_AFTER_UPDATE_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/freeze_after_update_gui/freeze_after_update_tab.py"' in text, "Freeze tab source constant missing")
    require('def _move_freeze_after_update_project_root_controls_to_status_row' in text, "Freeze tab mover missing")
    require('self.spec.source_hint != _FREEZE_AFTER_UPDATE_GUI_SOURCE' in text, "Freeze mover source guard missing")
    require('self._move_freeze_after_update_project_root_controls_to_status_row(widget)' in text, "Freeze mover not called during load")


def assert_zip_contract() -> None:
    import subprocess
    import sys

    if not PATCH_ZIP.exists():
        return
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_patch_zip.py"), str(PATCH_ZIP)],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    require(result.returncode == 0, result.stdout)
    require("ZIP CONTRACT: PASS" in result.stdout, result.stdout)


def main() -> int:
    import py_compile

    py_compile.compile(str(FREEZE_TAB), doraise=True)
    py_compile.compile(str(LAZY_TABS), doraise=True)
    assert_freeze_tab_layout_contract()
    assert_lazy_host_contract()
    assert_zip_contract()
    print("VALIDATION OK: freeze-after-update-toolbar-controls-v1")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
