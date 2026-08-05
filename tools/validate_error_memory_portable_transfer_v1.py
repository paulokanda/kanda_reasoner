#!/usr/bin/env python3
"""Validate portable Error Memory folder export and merge-only import."""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import sys
import tempfile

FEATURE_ID = "error-memory-portable-export-import-merge-v1r2"
TAB_REL = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
TRANSFER_REL = Path(
    "kanda_reasoner_app/error_memory_gui/_portable_transfer.py"
)
CONTRACTS_REL = Path("tools/_error_memory_portable_transfer_contracts.py")
FIXTURES_REL = Path("tools/_error_memory_portable_transfer_fixtures.py")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read_python(root: Path, relative: Path) -> str:
    path = root / relative
    _require(path.is_file(), "Python source missing: " + relative.as_posix())
    text = path.read_text(encoding="utf-8-sig")
    ast.parse(text, filename=str(path))
    _require(
        len(text.splitlines()) <= 500,
        relative.as_posix() + " exceeds 500 lines",
    )
    return text


def _static_contract(root: Path) -> None:
    tab_text = _read_python(root, TAB_REL)
    transfer_text = _read_python(root, TRANSFER_REL)
    contracts_text = _read_python(root, CONTRACTS_REL)
    fixtures_text = _read_python(root, FIXTURES_REL)

    required_tab = (
        "QPushButton('Export Errors')",
        "QPushButton('Import Errors')",
        "error_memory_export_errors_button",
        "error_memory_import_errors_button",
        "export_errors_from_tab(self)",
        "import_errors_into_tab(self)",
        "preview_buttons.addWidget(self.export_errors_button)",
        "preview_buttons.addWidget(self.import_errors_button)",
        "preview_buttons.addWidget(self.export_button)",
    )
    for token in required_tab:
        _require(
            token in tab_text,
            "Error Memory button contract missing: " + token,
        )

    required_transfer = (
        '"scope": "all_valid_saved_lessons"',
        '"compact_limit_applied": False',
        '"partial_success_allowed": False',
        '"import_mode": "merge_unique_only"',
        '"delete_current_lessons": False',
        '"replace_current_lessons": False',
        "lesson_matches_candidate_error(candidate, stored)",
        "stored_lessons + accepted",
        "validate_lesson_shape",
        '"current_lessons_deleted": 0',
        '"current_lessons_replaced": 0',
        "transfer_provenance",
    )
    for token in required_transfer:
        _require(
            token in transfer_text,
            "portable transfer contract missing: " + token,
        )

    forbidden_transfer = (
        "delete_lesson(",
        "shutil.rmtree",
        '"replace_current_lessons": True',
        '"delete_current_lessons": True',
    )
    for token in forbidden_transfer:
        _require(
            token not in transfer_text,
            "destructive transfer primitive present: " + token,
        )

    required_fixture = (
        "resolve_show_project_to_ai_root",
        "uuid4().hex",
        "expected_dynamic_lessons_dir",
        "shutil.rmtree(support_root)",
    )
    for token in required_fixture:
        _require(
            token in fixtures_text,
            "dynamic fixture contract missing: " + token,
        )
    _require(
        "resolve_error_memory_lessons_dir(source_root)" in contracts_text,
        "backup failure fixture does not use the canonical dynamic path",
    )
    _require(
        "next(iter(lessons_dir.glob" not in contracts_text,
        "unsafe StopIteration fixture pattern remains",
    )

    print("ERROR_MEMORY_PORTABLE_TRANSFER_SOURCE: PASS")
    print("ERROR_MEMORY_PORTABLE_TRANSFER_BUTTONS: PASS")
    print("ERROR_MEMORY_PORTABLE_TRANSFER_CANONICAL_DUPLICATE_OWNER: PASS")
    print("ERROR_MEMORY_PORTABLE_TRANSFER_NON_DESTRUCTIVE_SOURCE: PASS")
    print("ERROR_MEMORY_PORTABLE_TRANSFER_DYNAMIC_FIXTURES: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")

    from tools._error_memory_portable_transfer_contracts import (
        run_complete_backup_contract,
        run_functional_contract,
    )

    run_complete_backup_contract()
    run_functional_contract()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def _real_qt_contract(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication, QPushButton
    from kanda_reasoner_app.error_memory.store import list_lessons, save_lesson
    from kanda_reasoner_app.error_memory_gui.error_memory_tab import (
        ErrorMemoryTab,
    )
    from tools._error_memory_portable_transfer_fixtures import (
        isolated_project_roots,
        lesson_fixture,
    )

    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(
        prefix="kanda_error_memory_transfer_qt_"
    ) as temp:
        base = Path(temp)
        destination = base / "exports"
        destination.mkdir()
        with isolated_project_roots(
            base,
            "source_gui_project",
            "target_gui_project",
        ) as roots:
            source_root, target_root = roots
            save_lesson(
                source_root,
                lesson_fixture(
                    source_root,
                    lesson_id="lesson-gui-portable-unique-v1",
                    raw_error="GUI portable unique error.",
                ),
            )
            save_lesson(
                target_root,
                lesson_fixture(
                    target_root,
                    lesson_id="lesson-gui-current-v1",
                    raw_error="GUI current lesson must remain.",
                ),
            )

            previous_cwd = Path.cwd()
            os.chdir(source_root)
            try:
                tab = ErrorMemoryTab()
                tab.set_project_root(source_root)
                tab.resize(1600, 1000)
                tab.show()
                app.processEvents()
                export_button = tab.findChild(
                    QPushButton,
                    "error_memory_export_errors_button",
                )
                import_button = tab.findChild(
                    QPushButton,
                    "error_memory_import_errors_button",
                )
                _require(export_button is not None, "Export button missing")
                _require(import_button is not None, "Import button missing")
                _require(
                    export_button.text() == "Export Errors",
                    "Export Errors label mismatch",
                )
                _require(
                    import_button.text() == "Import Errors",
                    "Import Errors label mismatch",
                )
                _require(
                    export_button.isVisible() and import_button.isVisible(),
                    "transfer buttons not visible",
                )
                _require(
                    export_button.isEnabled() and import_button.isEnabled(),
                    "transfer buttons not enabled",
                )
                _require(
                    export_button.x() < import_button.x(),
                    "transfer button order is unstable",
                )
                _require(
                    import_button.x() < tab.export_button.x(),
                    "buttons are not near clipboard export",
                )
                print("REAL_QT_ERROR_MEMORY_TRANSFER_BUTTONS: PASS")

                messages: list[tuple[str, str, str]] = []
                tab._show_action_done = (
                    lambda title, message, detail="": messages.append(
                        (str(title), str(message), str(detail))
                    )
                )
                tab._error_memory_transfer_directory_picker = (
                    lambda _title, _start: str(destination)
                )
                export_button.click()
                app.processEvents()
                exports = sorted(
                    destination.glob("kanda_error_memory_export_*")
                )
                _require(
                    len(exports) == 1,
                    "GUI Export Errors did not create one folder",
                )
                _require(
                    messages and messages[-1][0] == "Export Errors",
                    "GUI export completion missing",
                )
                print("REAL_QT_ERROR_MEMORY_EXPORT_ERRORS: PASS")

                tab.set_project_root(target_root)
                app.processEvents()
                before = {
                    item["lesson_id"]
                    for item in list_lessons(
                        target_root,
                        include_inactive=True,
                    )
                }
                tab._error_memory_transfer_directory_picker = (
                    lambda _title, _start: str(exports[0])
                )
                import_button.click()
                app.processEvents()
                after = {
                    item["lesson_id"]
                    for item in list_lessons(
                        target_root,
                        include_inactive=True,
                    )
                }
                _require(
                    "lesson-gui-current-v1" in after,
                    "GUI import removed current lesson",
                )
                _require(
                    "lesson-gui-portable-unique-v1" in after,
                    "GUI import did not add unique lesson",
                )
                _require(
                    before.issubset(after),
                    "GUI import replaced current lessons",
                )
                _require(
                    messages and messages[-1][0] == "Import Errors",
                    "GUI import completion missing",
                )
                _require(
                    tab.lessons_table.rowCount() >= 2,
                    "GUI lesson table did not refresh",
                )
                print("REAL_QT_ERROR_MEMORY_IMPORT_ERRORS_MERGE: PASS")
                print("REAL_QT_ERROR_MEMORY_CURRENT_LESSONS_PRESERVED: PASS")
                print("REAL_QT_ERROR_MEMORY_PORTABLE_TRANSFER: PASS")
                tab.close()
                app.processEvents()
            finally:
                os.chdir(previous_cwd)

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--real-qt-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))
    if args.real_qt_only:
        _real_qt_contract(root)
    elif args.static_only:
        _static_contract(root)
    else:
        _static_contract(root)
        _real_qt_contract(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
