# project-path: tools/validate_error_memory_memorize_duplicate_guard_v9.py
"""Focused validation for duplicate-aware Error Memory Memorize Error."""
from __future__ import annotations

import ast
import json
import py_compile
import tempfile
from pathlib import Path
from typing import Any

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILES = [
    Path("kanda_reasoner_app/error_memory_gui/_memorize_duplicate_guard.py"),
    Path("kanda_reasoner_app/error_memory_gui/_memorize_flow.py"),
    Path("kanda_reasoner_app/error_memory_gui/_intake_actions_mixin.py"),
]
MAX_LINES = 500


def _source(rel_path: Path) -> str:
    path = PROJECT_ROOT / rel_path
    if not path.exists():
        raise AssertionError(f"Missing file: {rel_path}")
    return path.read_text(encoding="utf-8")


def _function(tree: ast.AST, name: str) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"Missing function: {name}")


def validate_files_compile_and_line_counts() -> None:
    for rel_path in FILES:
        path = PROJECT_ROOT / rel_path
        py_compile.compile(str(path), doraise=True)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > MAX_LINES:
            raise AssertionError(f"{rel_path} has {line_count} lines; max {MAX_LINES}")


def validate_memorize_flow_routes_duplicate_before_save() -> None:
    source = _source(FILES[1])
    if "find_memorize_duplicate" not in source:
        raise AssertionError("Memorize flow does not import duplicate guard")
    if "Candidate deleted because it is already there in Lessons." not in source:
        raise AssertionError("Expected duplicate candidate message is missing")
    tree = ast.parse(source)
    fn = _function(tree, "memorize_error_from_text_window")
    fn_text = ast.get_source_segment(source, fn) or ""
    duplicate_index = fn_text.find("_resolve_duplicate_memorize_candidate")
    draft_index = fn_text.find("_save_draft_lesson_from_partial")
    active_index = fn_text.find("_save_active_ready_lesson")
    if duplicate_index < 0:
        raise AssertionError("Memorize Error does not call duplicate resolver")
    if draft_index >= 0 and duplicate_index > draft_index:
        raise AssertionError("Duplicate resolver must run before draft save")
    if active_index >= 0 and duplicate_index > active_index:
        raise AssertionError("Duplicate resolver must run before active save")


def validate_mixin_facade_exists() -> None:
    source = _source(FILES[2])
    if "resolve_duplicate_memorize_candidate" not in source:
        raise AssertionError("Mixin does not import duplicate resolver")
    tree = ast.parse(source)
    _function(tree, "_resolve_duplicate_memorize_candidate")


def _lesson(lesson_id: str, raw_text: str, fingerprint_hash: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "lesson_id": lesson_id,
        "status": "draft",
        "project_slug": "kanda_reasoner",
        "operation_phase": "validation",
        "created_at_utc": "2026-07-02T00:00:00Z",
        "updated_at_utc": "2026-07-02T00:00:00Z",
        "raw_error_text": raw_text,
        "raw_error_snapshot_scrubbed": raw_text,
        "symptom": raw_text,
        "root_cause": "Known root cause.",
        "wrong_assumption": "Known wrong assumption.",
        "correct_fix": "Known fix.",
        "long_term_prevention": "Known prevention.",
        "do_not_repeat_rule": "Do not repeat this error.",
        "prevention_triggers": ["duplicate guard"],
        "exception": {
            "type": "UserReportedError",
            "phase": "validation",
            "relative_file_path": "Error Memory",
            "function_or_test_name": "Memorize Error",
            "message_normalized": raw_text,
            "stacktrace_scrubbed": "No traceback.",
        },
        "fingerprint": {
            "strategy": "test",
            "components": [raw_text],
            "fingerprint_hash": fingerprint_hash,
        },
        "regression_check": {"type": "not_available"},
        "validation_evidence": ["Draft duplicate guard test evidence."],
        "redaction": {"applied": True, "export_safe": True, "rules": ["test"]},
    }


def validate_duplicate_detection_functional() -> None:
    from kanda_reasoner_app.error_memory.store import save_lesson
    from kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard import (
        find_memorize_duplicate,
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "kanda_reasoner"
        root.mkdir()
        saved = _lesson("lesson-existing-duplicate-v1", "Repeated root cleanliness error", "hash-one")
        save_lesson(root, saved)

        same_id = _lesson("lesson-existing-duplicate-v1", "Different text", "hash-two")
        match = find_memorize_duplicate(root, same_id)
        if match is None or match.reason != "same lesson_id":
            raise AssertionError("Exact lesson_id duplicate was not detected")

        same_hash = _lesson("lesson-new-id-v1", "Different text", "hash-one")
        match = find_memorize_duplicate(root, same_hash)
        if match is None or match.reason != "same fingerprint.fingerprint_hash":
            raise AssertionError("Fingerprint duplicate was not detected")

        same_error = _lesson("lesson-another-id-v1", "Repeated root cleanliness error", "hash-three")
        match = find_memorize_duplicate(root, same_error)
        if match is None or "raw_error_text" not in match.reason:
            raise AssertionError("Same raw error duplicate was not detected")

        different = _lesson("lesson-different-v1", "A clearly unrelated issue", "hash-four")
        if find_memorize_duplicate(root, different) is not None:
            raise AssertionError("Unrelated lesson was incorrectly treated as duplicate")


def validate_duplicate_resolution_consumes_candidate() -> None:
    from kanda_reasoner_app.error_memory.store import save_lesson
    from kanda_reasoner_app.error_memory_gui._memorize_flow import (
        resolve_duplicate_memorize_candidate,
    )

    class FakeEdit:
        def __init__(self) -> None:
            self.cleared = False

        def clear(self) -> None:
            self.cleared = True

    class FakeTab:
        def __init__(self, root: Path, pending_file: Path) -> None:
            self.root = root
            self._loaded_pending_intake_file = str(pending_file)
            self._loaded_pending_intake_lesson_id = "lesson-pending-duplicate-v1"
            self._dismissed_pending_intake_files: set[str] = set()
            self._dismissed_pending_intake_lesson_ids: set[str] = set()
            self._last_received_lesson = {"lesson_id": "lesson-pending-duplicate-v1"}
            self._selected_lesson_id = "lesson-pending-duplicate-v1"
            self.raw_error_edit = FakeEdit()
            self.received_preview_edit = FakeEdit()
            self.reloaded = False
            self.done_message = ""

        def _current_project_root(self) -> Path:
            return self.root

        def _consume_loaded_pending_intake_file_if_matches(
            self,
            lesson: dict[str, Any],
            *,
            allow_lesson_id_change: bool = False,
        ) -> bool:
            path = Path(self._loaded_pending_intake_file)
            if path.exists():
                path.unlink()
            self._loaded_pending_intake_file = ""
            self._loaded_pending_intake_lesson_id = ""
            return True

        def _reload_table(self) -> None:
            self.reloaded = True

        def _show_action_done(self, title: str, message: str, details: str = "") -> None:
            self.done_message = message + "\n" + details

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "kanda_reasoner"
        root.mkdir()
        pending = Path(temp_dir) / "pending.json"
        pending.write_text(json.dumps({"pending": True}), encoding="utf-8")
        saved = _lesson("lesson-existing-duplicate-v1", "Repeated root cleanliness error", "hash-one")
        save_lesson(root, saved)
        candidate = _lesson("lesson-existing-duplicate-v1", "Repeated root cleanliness error", "hash-one")
        tab = FakeTab(root, pending)
        match = resolve_duplicate_memorize_candidate(tab, candidate)
        if match is None:
            raise AssertionError("Duplicate resolver did not return a match")
        if pending.exists():
            raise AssertionError("Duplicate candidate pending file was not deleted")
        if not tab.raw_error_edit.cleared or not tab.received_preview_edit.cleared:
            raise AssertionError("Duplicate resolver did not clear both work windows")
        if not tab.reloaded:
            raise AssertionError("Duplicate resolver did not reload table")
        if "Candidate deleted because it is already there in Lessons." not in tab.done_message:
            raise AssertionError("Duplicate resolver did not show expected message")


def main() -> None:
    validate_files_compile_and_line_counts()
    validate_memorize_flow_routes_duplicate_before_save()
    validate_mixin_facade_exists()
    validate_duplicate_detection_functional()
    validate_duplicate_resolution_consumes_candidate()
    print("VALIDATION OK: error-memory-memorize-duplicate-guard-v9")


if __name__ == "__main__":
    main()
