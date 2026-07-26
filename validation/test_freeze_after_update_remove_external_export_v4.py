from __future__ import annotations

from pathlib import Path
import py_compile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "kanda_reasoner_app" / "freeze_after_update_gui" / "freeze_after_update_tab.py"
PATCH_ZIP = ROOT / "kanda_freeze_after_update_remove_external_export_v4_patch.zip"
FEATURE = "freeze-after-update-remove-external-export-v4"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    py_compile.compile(str(SOURCE), doraise=True)

    require('QGroupBox("Box status and repair")' in text, "Box status and repair group missing")
    require("Check Box Status inspects the project-local freeze box" in text, "Check Box Status explanation missing")
    require("Create / Repair Box creates missing safe folder structure" in text, "Create / Repair Box explanation missing")
    require('self.check_button = QPushButton("Check Box Status")' in text, "Check Box Status button missing")
    require('self.create_button = QPushButton("Create / Repair Box")' in text, "Create / Repair Box button missing")
    require('self.open_box_button = QPushButton("Open project_freeze_after_update")' in text, "Open box button missing")

    forbidden = [
        "Export for External AI Review",
        "Advanced external AI review export",
        "Instruction MD:",
        "self.generate_button",
        "self.zip_edit",
        "self.instruction_edit",
        "self.open_output_button",
        "self.copy_output_path_button",
        "self.show_instruction_button",
    ]
    for marker in forbidden:
        require(marker not in text, "Deprecated external export UI marker still present: " + marker)

    require("self.help_button" in text and "self.external_ai_review_folder_button" in text, "host-row help/folder buttons lost")
    require("self.external_ai_review_folder_button.clicked.connect(self._open_output_folder)" in text, "External AI Review Folder button should still open folder")
    require("Preview Freeze Entry" in text and "remains read-only" in text, "protected preview rule missing from help")
    require("Confirm and Write" in text and "explicit human confirmation" in text, "confirmation protection wording missing")
    require("Ignore this Freeze" in text and "never writes frozen memory" in text, "ignore protection wording missing")
    require("write_confirmed_freeze_entry" in text, "local freeze write path missing")
    require("preview_freeze_entry" in text, "preview path missing")

    if PATCH_ZIP.exists():
        with zipfile.ZipFile(PATCH_ZIP, "r") as zf:
            names = set(zf.namelist())
        require("KANDA_FREEZE_HINT.json" in names, "KANDA_FREEZE_HINT.json missing from patch ZIP")
        require(str(SOURCE.relative_to(ROOT)).replace("\\", "/") in names, "patched source missing from ZIP")
        require("validation/test_freeze_after_update_remove_external_export_v4.py" in names, "validation script missing from ZIP")
        print("ZIP CONTRACT: PASS")
    else:
        print("ZIP CONTRACT: SKIPPED (patch ZIP not present beside project root)")

    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
