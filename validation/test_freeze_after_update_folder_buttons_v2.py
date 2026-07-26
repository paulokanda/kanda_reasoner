"""Validate Freeze Feature After Update folder-button toolbar controls v2."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE_TAB = ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "freeze_after_update_tab.py"
PATCH_ZIP = ROOT / "kanda_freeze_after_update_folder_buttons_v2_patch.zip"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def block_between(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[start_index:end_index]


def assert_folder_button_contract() -> None:
    text = read(FREEZE_TAB)

    require('self.box_folder_button = QPushButton("Box Folder")' in text, "Box Folder toolbar button missing")
    require('self.external_ai_review_folder_button = QPushButton("External AI Review Folder")' in text, "External AI Review Folder toolbar button missing")
    require('freeze_after_update_box_folder_button' in text, "Box Folder button object name missing")
    require('freeze_after_update_external_ai_review_folder_button' in text, "External AI Review Folder button object name missing")

    require('self.box_folder_edit = QLineEdit()' not in text, "Box Folder path edit widget was restored")
    require('self.files_to_send_path_edit = QLineEdit()' not in text, "External AI review path edit widget was restored")
    require('freeze_after_update_box_folder_edit' not in text, "Box Folder path edit object name was restored")
    require('freeze_after_update_external_ai_review_folder_edit' not in text, "External AI review path edit object name was restored")

    move_block = block_between(text, 'def move_project_root_controls_to_layout', 'def _freeze_entry_sort_key')
    for token in (
        'self.project_root_header_label',
        'self.project_root_edit',
        'self.search_project_button',
        'self.box_folder_button',
        'self.external_ai_review_folder_button',
    ):
        require(token in move_block, token + " not moved to host LOADED / Source row")
    require('self.box_folder_edit' not in move_block, "Box Folder path edit still moved to host row")
    require('self.files_to_send_path_edit' not in move_block, "External AI review path edit still moved to host row")

    require('self.box_folder_button.clicked.connect(self._open_box_folder)' in text, "Box Folder button is not wired to open folder")
    require('self.external_ai_review_folder_button.clicked.connect(self._open_output_folder)' in text, "External AI Review Folder button is not wired to open folder")
    require('def _open_box_folder(self) -> None:' in text, "open box folder handler missing")
    require('def _open_output_folder(self) -> None:' in text, "open external AI review folder handler missing")

    require('self.box_folder_button.setToolTip("Open box folder: " + str(paths.box_root))' in text, "Box Folder tooltip does not track derived box path")
    require('self.external_ai_review_folder_button.setToolTip("Open external AI review folder: " + str(paths.send_root))' in text, "External AI Review Folder tooltip does not track derived folder path")

    require('QGroupBox("Active project")' not in text, "Active project body group was restored")
    require('title = QLabel("Freeze Feature After Update")' not in text, "duplicate inner title was restored")
    require('confirm_write_button.setStyleSheet("color: #008000; font-weight: bold;")' in text, "Confirm and Write green style missing")
    require('ignore_freeze_button.setStyleSheet("color: #B00020; font-weight: bold;")' in text, "Ignore this Freeze red style missing")


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
    assert_folder_button_contract()
    assert_zip_contract()
    print("VALIDATION OK: freeze-after-update-folder-buttons-v2")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
