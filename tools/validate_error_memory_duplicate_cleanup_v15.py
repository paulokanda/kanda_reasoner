# project-path: tools/validate_error_memory_duplicate_cleanup_v15.py
"""Focused validation for Error Memory duplicate cleanup v15."""
from __future__ import annotations

import json
import py_compile
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard as guard
from kanda_reasoner_app.error_memory_gui._correction_duplicate_guard import (
    consume_duplicate_correction_candidate,
)
from kanda_reasoner_app.error_memory_gui._duplicate_pending_cleanup import (
    delete_matching_pending_duplicate_candidates,
)
from kanda_reasoner_app.error_memory_gui._memorize_flow import (
    resolve_duplicate_memorize_candidate,
)

ERROR_LESSON_JSON_BEGIN = "KANDA_ERROR_LESSON_JSON_BEGIN"
ERROR_LESSON_JSON_END = "KANDA_ERROR_LESSON_JSON_END"

TOUCHED = [
    "kanda_reasoner_app/error_memory_gui/_memorize_duplicate_guard.py",
    "kanda_reasoner_app/error_memory_gui/_duplicate_pending_cleanup.py",
    "kanda_reasoner_app/error_memory_gui/_memorize_flow.py",
    "kanda_reasoner_app/error_memory_gui/_correction_duplicate_guard.py",
    "tools/validate_error_memory_duplicate_cleanup_v15.py",
]


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _lesson(
    lesson_id: str,
    *,
    status: str = "draft",
    active: bool = False,
    updated: str = "2026-07-02T00:00:00Z",
    fingerprint_hash: str = "batch19-runner-help-duplicate-public-symbols-v1",
    raw_suffix: str = "",
) -> dict[str, Any]:
    regression = {
        "type": "validation_command",
        "command": "python validation/test_duplicate_cleanup_v15.py",
        "expected_marker": "VALIDATION OK: duplicate-cleanup-v15",
        "required_before_freeze": True,
    }
    if not active:
        regression = {
            "type": "not_available",
            "command": "",
            "expected_marker": "",
            "required_before_freeze": False,
        }
    return {
        "schema_version": "1.0",
        "lesson_id": lesson_id,
        "status": status,
        "superseded_by": "",
        "project_slug": "tmp_project",
        "operation_phase": "architecture_validation",
        "created_at_utc": "2026-07-02T00:00:00Z",
        "updated_at_utc": updated,
        "source_patch_zip": "patch.zip" if active else "",
        "raw_error_text": (
            "Focused Batch 19 validation failed with 17 duplicate public "
            "ownership errors in runner_help split helpers. " + raw_suffix
        ).strip(),
        "raw_error_snapshot_scrubbed": (
            "Architecture validation reported 17 duplicate public ownership "
            "errors for zip_json_files private helper modules."
        ),
        "symptom": (
            "A frozen Batch 19 cleanup left the project in an architecture-error "
            "state with duplicate public ownership errors."
        ),
        "root_cause": "Split helper modules had overlapping public ownership.",
        "wrong_assumption": "Assumed helper ownership cleanup was globally safe.",
        "correct_fix": "Repair ownership declarations and validate architecture.",
        "do_not_repeat_rule": (
            "Do not freeze cleanup while architecture validation has duplicate "
            "public ownership errors."
        ),
        "long_term_prevention": "Run architecture validation before freeze.",
        "redaction": {"applied": True, "export_safe": True, "rules": ["No secrets included."]},
        "exception": {
            "type": "ArchitectureDuplicatePublicOwnershipError" if active else "",
            "phase": "architecture_validation" if active else "",
            "relative_file_path": "manage_architecture.py" if active else "",
            "function_or_test_name": "architecture validation" if active else "",
            "message_normalized": "17 duplicate public ownership errors" if active else "",
            "stacktrace_scrubbed": "No traceback; validation failure." if active else "",
        },
        "fingerprint": {
            "strategy": "duplicate_public_symbol_family",
            "components": [
                "kanda_reasoner_app.reasoner_tools_shell.runner_help",
                "zip_json_files_private_impl",
                "zip_json_files_state_private_impl",
                "zip_json_files_process_private_impl",
                "duplicate public ownership",
            ],
            "fingerprint_hash": fingerprint_hash,
        },
        "prevention_triggers": ["batch19", "duplicate public ownership"],
        "regression_check": regression,
        "validation_command_summary": "Run architecture validation." if active else "",
        "validation_evidence": ["VALIDATION OK: duplicate-cleanup-v15"] if active else ["Draft evidence placeholder."],
        "install_command_summary": "Install patch and validate." if active else "",
        "notes": "Active-ready canonical lesson." if active else "Draft duplicate.",
    }


class _Edit:
    def clear(self) -> None:
        self.text = ""

    def setPlainText(self, value: str) -> None:
        self.text = value


class _Table:
    def blockSignals(self, _value: bool) -> None:
        return None

    def clearSelection(self) -> None:
        return None


class _Tab:
    def __init__(self, root: Path, pending_files: list[Path], *, loaded: Path | None = None):
        self.root = root
        self.pending_files = pending_files
        self.reloads = 0
        self.messages: list[tuple[str, str, str]] = []
        self._loaded_pending_intake_file = str(loaded or "")
        self._loaded_pending_intake_lesson_id = "lesson-loaded-pending"
        self._dismissed_pending_intake_files: set[str] = set()
        self._dismissed_pending_intake_lesson_ids: set[str] = set()
        self._last_received_lesson = None
        self._selected_lesson_id = ""
        self.raw_error_edit = _Edit()
        self.received_preview_edit = _Edit()
        self.lessons_table = _Table()

    def _current_project_root(self) -> Path:
        return self.root

    def _pending_intake_files_for_all_candidate_dirs(self) -> list[Path]:
        return list(self.pending_files)

    def _lesson_from_formatted_text(self, text: str) -> dict[str, Any]:
        text = text.strip()
        if text.startswith(ERROR_LESSON_JSON_BEGIN):
            text = text.split(ERROR_LESSON_JSON_BEGIN, 1)[1]
            text = text.split(ERROR_LESSON_JSON_END, 1)[0]
        return json.loads(text.strip())

    def _lesson_id_from_text_lenient(self, text: str) -> str:
        try:
            return str(self._lesson_from_formatted_text(text).get("lesson_id") or "")
        except Exception:
            return ""

    def _consume_loaded_pending_intake_file_if_matches(self, lesson: dict[str, Any], *, allow_lesson_id_change: bool = False) -> bool:
        marker = str(self._loaded_pending_intake_file or "").strip()
        if not marker:
            return False
        path = Path(marker)
        if path.exists():
            path.unlink()
        self._dismissed_pending_intake_files.add(str(path.resolve(strict=False)))
        self._loaded_pending_intake_file = ""
        self._loaded_pending_intake_lesson_id = ""
        return True

    def _reload_table(self) -> None:
        self.reloads += 1

    def _show_action_done(self, title: str, message: str, details: str = "") -> None:
        self.messages.append((title, message, details))

    def _refresh_heuristic_correction_button_state(self) -> None:
        return None


class _PatchContext:
    def __init__(self, lessons: list[dict[str, Any]]):
        self.lessons = lessons
        self.deleted: list[str] = []
        self.rebuilt = False
        self.originals = (guard.list_lessons, guard.delete_lesson, guard.rebuild_index)

    def __enter__(self):
        def fake_list_lessons(_root: object, *, include_inactive: bool = True) -> list[dict[str, Any]]:
            return list(self.lessons)

        def fake_delete_lesson(_root: object, lesson_id: str) -> dict[str, Any]:
            self.deleted.append(lesson_id)
            for item in list(self.lessons):
                if item.get("lesson_id") == lesson_id:
                    self.lessons.remove(item)
                    return item
            raise KeyError(lesson_id)

        def fake_rebuild_index(_root: object) -> dict[str, Any]:
            self.rebuilt = True
            return {"lessons": [item.get("lesson_id") for item in self.lessons]}

        guard.list_lessons = fake_list_lessons
        guard.delete_lesson = fake_delete_lesson
        guard.rebuild_index = fake_rebuild_index
        return self

    def __exit__(self, _exc_type: object, _exc: object, _tb: object) -> None:
        guard.list_lessons, guard.delete_lesson, guard.rebuild_index = self.originals


def _write_formatted(path: Path, lesson: dict[str, Any]) -> None:
    path.write_text(
        ERROR_LESSON_JSON_BEGIN + "\n" + json.dumps(lesson) + "\n" + ERROR_LESSON_JSON_END,
        encoding="utf-8",
    )


def _write_raw(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _ids(lessons: list[dict[str, Any]]) -> set[str]:
    return {str(item.get("lesson_id")) for item in lessons}


def _test_one_saved_match_deletes_unloaded_matching_pending_row() -> None:
    stored = _lesson("lesson-batch19-stored", updated="2026-07-02T00:01:00Z")
    pending_lesson = _lesson("lesson-batch19-pending", updated="2026-07-02T00:02:00Z")
    with tempfile.TemporaryDirectory() as tmp, _PatchContext([stored]) as context:
        pending = Path(tmp) / "pending.json"
        _write_formatted(pending, pending_lesson)
        tab = _Tab(Path(tmp) / "project", [pending], loaded=None)
        result = resolve_duplicate_memorize_candidate(tab, dict(stored))
        assert result is not None
        assert context.deleted == []
        assert _ids(context.lessons) == {"lesson-batch19-stored"}
        assert not pending.exists(), "unloaded pending duplicate row must be removed"
        assert tab.reloads == 1


def _test_loaded_pending_file_is_forced_deleted_even_if_text_was_changed() -> None:
    stored = _lesson("lesson-batch19-stored", updated="2026-07-02T00:01:00Z")
    with tempfile.TemporaryDirectory() as tmp, _PatchContext([stored]):
        pending = Path(tmp) / "loaded_raw.txt"
        _write_raw(pending, "temporary edited text without lesson id")
        tab = _Tab(Path(tmp) / "project", [pending], loaded=pending)
        result = resolve_duplicate_memorize_candidate(tab, dict(stored))
        assert result is not None
        assert not pending.exists(), "loaded pending candidate must be consumed directly"


def _test_saved_draft_duplicate_is_removed_and_active_preserved() -> None:
    active = _lesson("lesson-batch19-active", status="active", active=True, updated="2026-07-02T00:03:00Z")
    draft = _lesson("lesson-batch19-draft", status="draft", active=False, updated="2026-07-02T00:04:00Z")
    with _PatchContext([active, draft]) as context:
        result = guard.resolve_duplicate_lesson_copies(Path("unused"), dict(draft))
        assert result is not None
        assert context.deleted == ["lesson-batch19-draft"]
        assert _ids(context.lessons) == {"lesson-batch19-active"}


def _test_correction_guard_deletes_unloaded_pending_duplicate() -> None:
    stored = _lesson("lesson-batch19-stored", updated="2026-07-02T00:01:00Z")
    pending_lesson = _lesson("lesson-batch19-pending", updated="2026-07-02T00:02:00Z")
    with tempfile.TemporaryDirectory() as tmp, _PatchContext([stored]):
        pending = Path(tmp) / "pending.json"
        _write_formatted(pending, pending_lesson)
        tab = _Tab(Path(tmp) / "project", [pending], loaded=None)
        stopped = consume_duplicate_correction_candidate(tab, dict(stored), action_label="Correct with AI")
        assert stopped is True
        assert not pending.exists(), "correction guard must remove unloaded pending duplicate"


def _test_pending_cleanup_matches_raw_text_and_fingerprint_terms() -> None:
    candidate = _lesson("lesson-batch19-candidate", updated="2026-07-02T00:01:00Z")
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "raw_evidence.txt"
        _write_raw(raw, "Batch 19 duplicate public ownership in zip_json_files_private_impl")
        tab = _Tab(Path(tmp) / "project", [raw], loaded=None)
        count, failures = delete_matching_pending_duplicate_candidates(tab, dict(candidate))
        assert failures == ()
        assert count == 1
        assert not raw.exists()


def main() -> int:
    root = Path.cwd()
    for rel in TOUCHED:
        path = root / rel
        if not path.exists():
            raise AssertionError("missing touched file: " + rel)
        if _line_count(path) > 500:
            raise AssertionError("line limit exceeded: " + rel)
        py_compile.compile(str(path), doraise=True)
    _test_one_saved_match_deletes_unloaded_matching_pending_row()
    _test_loaded_pending_file_is_forced_deleted_even_if_text_was_changed()
    _test_saved_draft_duplicate_is_removed_and_active_preserved()
    _test_correction_guard_deletes_unloaded_pending_duplicate()
    _test_pending_cleanup_matches_raw_text_and_fingerprint_terms()
    print("VALIDATION OK: error-memory-duplicate-cleanup-v15")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
