"""Validation for Freeze Feature After Update header/action layout v3."""
from __future__ import annotations

import py_compile
import zipfile
from pathlib import Path

FEATURE_ID = "freeze-after-update-header-actions-v3"
PATCH_NAME = "kanda_freeze_after_update_header_actions_v3_patch.zip"
SOURCE = Path("kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py")
EXPECTED_ZIP_MEMBERS = {
    "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py",
    "validation/test_freeze_after_update_header_actions_v3.py",
    "KANDA_FREEZE_HINT.json",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def assert_source_contract() -> None:
    text = read_text(SOURCE)
    py_compile.compile(str(SOURCE), doraise=True)

    require('self.help_button = QPushButton("Help")' in text, "Help button missing")
    require('self.help_button,' in text, "Help button is not part of moved host-row controls")
    require('self.external_ai_review_folder_button,' in text, "External AI Review Folder button missing from moved controls")
    require(
        text.index('self.external_ai_review_folder_button,') < text.index('self.help_button,'),
        "Help button must be immediately after External AI Review Folder in moved controls",
    )

    require("header_layout = QHBoxLayout()" not in text, "old separate top header row must stay removed")
    require("root_layout.addLayout(header_layout)" not in text, "old header row must not be added to body")
    require("root_layout.addWidget(intro)" not in text, "intro text must not span full tab width")
    require("left_column.addWidget(intro)" in text, "intro text must be at top of first column")
    require("freeze_copy_row = QHBoxLayout()" in text, "Get Last/Get All row missing")
    require("freeze_copy_row.addWidget(self.get_last_freeze_button, 0)" in text, "Get Last Freeze not below intro")
    require("freeze_copy_row.addWidget(self.get_all_frozen_button, 0)" in text, "Get All Frozen not below intro")
    require("left_column.addLayout(freeze_copy_row)" in text, "copy row must be placed in first column")

    require('self.box_folder_button = QPushButton("Box Folder")' in text, "Box Folder must remain a button")
    require('self.external_ai_review_folder_button = QPushButton("External AI Review Folder")' in text, "External AI Review Folder must remain a button")
    require("box_folder_edit" not in text, "Box Folder path widget must not be restored")
    require("external_ai_review_edit" not in text, "External AI Review path widget must not be restored")

    require('self.get_last_freeze_button.setStyleSheet("color: #008000; font-weight: bold;")' in text, "Get Last Freeze green bold style missing")
    require('self.get_all_frozen_button.setStyleSheet("color: #003366; font-weight: bold;")' in text, "Get All Frozen dark blue bold style missing")

    require("Confirm and Write" in text, "Confirm and Write behavior text missing")
    require("write_confirmed_freeze_entry" in text, "freeze write confirmation path missing")


def find_patch_zip() -> Path:
    root = Path.cwd().resolve()
    candidates = [root / PATCH_NAME]
    drive = Path(root.anchor) if root.anchor else root.parent
    candidates.append(drive / PATCH_NAME)
    candidates.append(drive / f"{root.name}_delete_after_daily_work" / PATCH_NAME)
    for path in candidates:
        if path.exists():
            return path
    # Sandbox/build fallback: search nearby /mnt/data roots without requiring Windows layout.
    for parent in [root, root.parent, Path("/mnt/data")]:
        try:
            found = next(parent.rglob(PATCH_NAME))
            return found
        except StopIteration:
            continue
    raise AssertionError(f"patch ZIP not found: {PATCH_NAME}")


def assert_zip_contract() -> None:
    patch_zip = find_patch_zip()
    with zipfile.ZipFile(patch_zip, "r") as zf:
        names = set(zf.namelist())
    require(names == EXPECTED_ZIP_MEMBERS, f"unexpected ZIP members: {sorted(names)}")


def main() -> int:
    assert_source_contract()
    assert_zip_contract()
    print("VALIDATION OK: freeze-after-update-header-actions-v3")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
