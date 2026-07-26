#!/usr/bin/env python3
"""Validate portable Error Memory folder export and merge-only import."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any

FEATURE_ID = "error-memory-portable-export-import-merge-v1"
TAB_REL = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")
TRANSFER_REL = Path("kanda_reasoner_app/error_memory_gui/_portable_transfer.py")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _lesson(
    root: Path,
    *,
    lesson_id: str,
    raw_error: str,
    status: str = "draft",
    fingerprint_hash: str = "",
) -> dict[str, Any]:
    from kanda_reasoner_app.error_memory.models import build_lesson

    lesson = build_lesson(
        selected_project_root=root,
        raw_error_text=raw_error,
        operation_phase="validation",
        symptom="Portable transfer fixture symptom for " + lesson_id,
        root_cause="Portable transfer fixture root cause for " + lesson_id,
        wrong_assumption="Portable transfer fixture wrong assumption.",
        correct_fix="Portable transfer fixture correct fix.",
        long_term_prevention="Portable transfer fixture prevention.",
        do_not_repeat_rule="Portable transfer fixture rule for " + lesson_id,
        prevention_triggers=["portable transfer " + lesson_id],
        validation_evidence=["FIXTURE_VALIDATION: PASS"],
        status=status,
        lesson_id=lesson_id,
    )
    fingerprint = dict(lesson.get("fingerprint") or {})
    fingerprint["fingerprint_hash"] = (
        fingerprint_hash or hashlib.sha256(lesson_id.encode("utf-8")).hexdigest()
    )
    lesson["fingerprint"] = fingerprint
    return lesson


def _saved_bytes(root: Path) -> dict[str, bytes]:
    from kanda_reasoner_app.error_memory.paths import resolve_error_memory_lessons_dir

    return {
        path.name: path.read_bytes()
        for path in resolve_error_memory_lessons_dir(root).glob("lesson-*.json")
        if path.is_file()
    }


def _functional_contract() -> None:
    from kanda_reasoner_app.error_memory.paths import resolve_error_memory_lessons_dir
    from kanda_reasoner_app.error_memory.store import list_lessons, save_lesson
    from kanda_reasoner_app.error_memory_gui._portable_transfer import (
        ERROR_MEMORY_EXPORT_MANIFEST,
        export_error_lessons_folder,
        import_error_lessons_folder,
    )

    with tempfile.TemporaryDirectory(prefix="kanda_error_memory_transfer_") as temp:
        base = Path(temp)
        source_root = base / "source_project"
        target_root = base / "target_project"
        destination = base / "portable_exports"
        source_root.mkdir()
        target_root.mkdir()
        destination.mkdir()

        alpha = _lesson(
            source_root,
            lesson_id="lesson-portable-alpha-v1",
            raw_error="Portable alpha unique source error.",
        )
        beta = _lesson(
            source_root,
            lesson_id="lesson-portable-beta-v1",
            raw_error="Portable beta source error.",
            status="deprecated",
        )
        gamma = _lesson(
            source_root,
            lesson_id="lesson-portable-gamma-v1",
            raw_error="Portable gamma source error.",
            fingerprint_hash="portable-shared-fingerprint-v1",
        )
        for item in (alpha, beta, gamma):
            save_lesson(source_root, item)

        current_beta = _lesson(
            target_root,
            lesson_id="lesson-portable-beta-v1",
            raw_error="Target project owns the current beta lesson.",
        )
        current_fingerprint = _lesson(
            target_root,
            lesson_id="lesson-target-current-fingerprint-v1",
            raw_error="Target project owns the current fingerprint lesson.",
            fingerprint_hash="portable-shared-fingerprint-v1",
        )
        current_only = _lesson(
            target_root,
            lesson_id="lesson-target-current-only-v1",
            raw_error="Target-only lesson must remain byte identical.",
        )
        for item in (current_beta, current_fingerprint, current_only):
            save_lesson(target_root, item)

        source_before = _saved_bytes(source_root)
        target_before = _saved_bytes(target_root)
        exported = export_error_lessons_folder(source_root, destination)
        export_root = Path(exported["export_folder"])
        manifest_path = export_root / ERROR_MEMORY_EXPORT_MANIFEST
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        _require(exported["exported_count"] == 3, "export did not include every valid status")
        _require(manifest["lesson_count"] == 3, "manifest lesson_count mismatch")
        _require(
            {entry["status"] for entry in manifest["lessons"]} == {"draft", "deprecated"},
            "export did not preserve lesson statuses",
        )
        for entry in manifest["lessons"]:
            filename = entry["file"]
            _require(
                (export_root / "lessons" / filename).read_bytes() == source_before[filename],
                "export did not preserve exact lesson bytes: " + filename,
            )
        _require(_saved_bytes(source_root) == source_before, "export modified source lessons")
        print("ERROR_MEMORY_EXPORT_FOLDER_CONTRACT: PASS")
        print("ERROR_MEMORY_EXPORT_ALL_STATUSES: PASS")
        print("ERROR_MEMORY_EXPORT_SOURCE_READ_ONLY: PASS")

        imported = import_error_lessons_folder(target_root, export_root)
        _require(imported["imported_count"] == 1, "import did not add exactly one unique lesson")
        _require(imported["duplicate_count"] == 2, "import did not skip both canonical duplicates")
        _require(imported["current_lessons_deleted"] == 0, "import deleted current lessons")
        _require(imported["current_lessons_replaced"] == 0, "import replaced current lessons")
        target_after = _saved_bytes(target_root)
        for filename, raw in target_before.items():
            _require(target_after.get(filename) == raw, "current lesson changed: " + filename)
        lessons = list_lessons(target_root, include_inactive=True)
        by_id = {str(item.get("lesson_id") or ""): item for item in lessons}
        imported_alpha = by_id.get("lesson-portable-alpha-v1")
        _require(imported_alpha is not None, "unique alpha lesson was not imported")
        _require(imported_alpha.get("project_slug") == target_root.name, "imported lesson is not target-owned")
        provenance = imported_alpha.get("transfer_provenance")
        _require(isinstance(provenance, dict), "transfer provenance missing")
        _require(
            provenance.get("source_project_slug") == source_root.name,
            "source project provenance missing",
        )
        reasons = {item.get("reason") for item in imported["duplicates"]}
        _require("same lesson_id" in reasons, "same-ID duplicate was not recognized")
        _require(
            "same fingerprint.fingerprint_hash" in reasons,
            "same-fingerprint duplicate was not recognized",
        )
        print("ERROR_MEMORY_IMPORT_MERGE_ONLY: PASS")
        print("ERROR_MEMORY_IMPORT_DUPLICATE_ID_SKIPPED: PASS")
        print("ERROR_MEMORY_IMPORT_DUPLICATE_FINGERPRINT_SKIPPED: PASS")
        print("ERROR_MEMORY_IMPORT_CURRENT_LESSONS_UNCHANGED: PASS")
        print("ERROR_MEMORY_IMPORT_TARGET_PROJECT_OWNERSHIP: PASS")

        second = import_error_lessons_folder(target_root, export_root / "lessons")
        _require(second["imported_count"] == 0, "re-import created duplicate lessons")
        _require(second["duplicate_count"] == 3, "re-import did not skip all lessons")
        _require(_saved_bytes(target_root) == target_after, "re-import changed target lesson files")
        print("ERROR_MEMORY_IMPORT_REIMPORT_IDEMPOTENT: PASS")

        invalid_export = export_root / "lessons" / "lesson-invalid.json"
        invalid_export.write_text("{}", encoding="utf-8")
        manifest["lessons"].append(
            {
                "lesson_id": "lesson-invalid",
                "status": "draft",
                "file": invalid_export.name,
                "sha256": _sha256(invalid_export),
                "size_bytes": invalid_export.stat().st_size,
            }
        )
        manifest["lesson_count"] = len(manifest["lessons"])
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        invalid_result = import_error_lessons_folder(target_root, export_root)
        _require(invalid_result["invalid_count"] == 1, "invalid lesson was not skipped")
        _require(invalid_result["imported_count"] == 0, "invalid import added a lesson")
        _require(_saved_bytes(target_root) == target_after, "invalid import changed target lessons")
        print("ERROR_MEMORY_IMPORT_INVALID_LESSON_SKIPPED: PASS")

        target_lesson_dir = resolve_error_memory_lessons_dir(target_root)
        _require(len(list(target_lesson_dir.glob("lesson-*.json"))) == 4, "target lesson count is wrong")


def _static_contract(root: Path) -> None:
    tab_path = root / TAB_REL
    transfer_path = root / TRANSFER_REL
    _require(tab_path.is_file(), "Error Memory tab source missing")
    _require(transfer_path.is_file(), "portable transfer helper missing")
    tab_text = tab_path.read_text(encoding="utf-8-sig")
    transfer_text = transfer_path.read_text(encoding="utf-8-sig")
    ast.parse(tab_text, filename=str(tab_path))
    ast.parse(transfer_text, filename=str(transfer_path))
    _require(len(tab_text.splitlines()) <= 500, "error_memory_tab.py exceeds 500 lines")
    _require(len(transfer_text.splitlines()) <= 500, "_portable_transfer.py exceeds 500 lines")
    required_tab = (
        "QPushButton('Export Errors')",
        "QPushButton('Import Errors')",
        "error_memory_export_errors_button",
        "error_memory_import_errors_button",
        "export_errors_from_tab(self)",
        "import_errors_into_tab(self)",
        "transfer_buttons.addWidget(self.export_errors_button)",
        "transfer_buttons.addWidget(self.import_errors_button)",
        "transfer_buttons.addWidget(self.export_button)",
    )
    for token in required_tab:
        _require(token in tab_text, "Error Memory button contract missing: " + token)
    required_transfer = (
        '"import_mode": "merge_unique_only"',
        '"delete_current_lessons": False',
        '"replace_current_lessons": False',
        "lesson_matches_candidate_error(candidate, stored)",
        "validate_lesson_shape",
        "current_lessons_deleted\": 0",
        "current_lessons_replaced\": 0",
        "transfer_provenance",
    )
    for token in required_transfer:
        _require(token in transfer_text, "portable transfer contract missing: " + token)
    forbidden = (
        "delete_lesson(",
        "shutil.rmtree",
        "replace_current_lessons\": True",
        "delete_current_lessons\": True",
    )
    for token in forbidden:
        _require(token not in transfer_text, "destructive transfer primitive present: " + token)
    print("ERROR_MEMORY_PORTABLE_TRANSFER_SOURCE: PASS")
    print("ERROR_MEMORY_PORTABLE_TRANSFER_BUTTONS: PASS")
    print("ERROR_MEMORY_PORTABLE_TRANSFER_CANONICAL_DUPLICATE_OWNER: PASS")
    print("ERROR_MEMORY_PORTABLE_TRANSFER_NON_DESTRUCTIVE_SOURCE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    _functional_contract()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def _real_qt_contract(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication, QPushButton
    from kanda_reasoner_app.error_memory.store import list_lessons, save_lesson
    from kanda_reasoner_app.error_memory_gui.error_memory_tab import ErrorMemoryTab

    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(prefix="kanda_error_memory_transfer_qt_") as temp:
        base = Path(temp)
        source_root = base / "source_gui_project"
        target_root = base / "target_gui_project"
        destination = base / "exports"
        source_root.mkdir()
        target_root.mkdir()
        destination.mkdir()
        save_lesson(
            source_root,
            _lesson(
                source_root,
                lesson_id="lesson-gui-portable-unique-v1",
                raw_error="GUI portable unique error.",
            ),
        )
        target_current = _lesson(
            target_root,
            lesson_id="lesson-gui-current-v1",
            raw_error="GUI current lesson must remain.",
        )
        save_lesson(target_root, target_current)

        previous_cwd = Path.cwd()
        os.chdir(source_root)
        try:
            tab = ErrorMemoryTab()
            tab.set_project_root(source_root)
            tab.resize(1600, 1000)
            tab.show()
            app.processEvents()
            export_button = tab.findChild(QPushButton, "error_memory_export_errors_button")
            import_button = tab.findChild(QPushButton, "error_memory_import_errors_button")
            _require(export_button is not None, "Export Errors button not found")
            _require(import_button is not None, "Import Errors button not found")
            _require(export_button.text() == "Export Errors", "Export Errors label mismatch")
            _require(import_button.text() == "Import Errors", "Import Errors label mismatch")
            _require(export_button.isVisible() and import_button.isVisible(), "transfer buttons not visible")
            _require(export_button.isEnabled() and import_button.isEnabled(), "transfer buttons not enabled")
            _require(export_button.x() < import_button.x(), "transfer button order is unstable")
            _require(import_button.x() < tab.export_button.x(), "buttons are not near clipboard export")
            print("REAL_QT_ERROR_MEMORY_TRANSFER_BUTTONS: PASS")

            messages: list[tuple[str, str, str]] = []
            tab._show_action_done = lambda title, message, detail="": messages.append(
                (str(title), str(message), str(detail))
            )
            tab._error_memory_transfer_directory_picker = (
                lambda _title, _start: str(destination)
            )
            export_button.click()
            app.processEvents()
            exports = sorted(destination.glob("kanda_error_memory_export_*"))
            _require(len(exports) == 1, "GUI Export Errors did not create one export folder")
            _require(messages and messages[-1][0] == "Export Errors", "GUI export completion missing")
            print("REAL_QT_ERROR_MEMORY_EXPORT_ERRORS: PASS")

            tab.set_project_root(target_root)
            app.processEvents()
            before = {item["lesson_id"] for item in list_lessons(target_root, include_inactive=True)}
            tab._error_memory_transfer_directory_picker = (
                lambda _title, _start: str(exports[0])
            )
            import_button.click()
            app.processEvents()
            after = {item["lesson_id"] for item in list_lessons(target_root, include_inactive=True)}
            _require("lesson-gui-current-v1" in after, "GUI import removed current lesson")
            _require("lesson-gui-portable-unique-v1" in after, "GUI import did not add unique lesson")
            _require(before.issubset(after), "GUI import replaced current lessons")
            _require(messages and messages[-1][0] == "Import Errors", "GUI import completion missing")
            _require(tab.lessons_table.rowCount() >= 2, "GUI lesson table did not refresh")
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
