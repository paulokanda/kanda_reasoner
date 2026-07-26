# project-path: tools/validate_error_memory_duplicate_cleanup_v13_single_match_repair.py
"""Focused validation for Error Memory duplicate cleanup single-match repair."""
from __future__ import annotations

import py_compile
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard as guard

TOUCHED = [
    "kanda_reasoner_app/error_memory_gui/_memorize_duplicate_guard.py",
    "tools/validate_error_memory_duplicate_cleanup_v13_single_match_repair.py",
]


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _lesson(lesson_id: str, *, status: str, active: bool, updated: str) -> dict[str, Any]:
    regression = {
        "type": "validation_command",
        "command": "python validation/test_duplicate_cleanup_v13.py",
        "expected_marker": "VALIDATION OK: duplicate-cleanup-v13",
        "required_before_freeze": True,
    }
    if not active:
        regression = {"type": "not_available"}
    return {
        "schema_version": "1.0",
        "lesson_id": lesson_id,
        "status": status,
        "superseded_by": "",
        "project_slug": "tmp_project",
        "operation_phase": "validation",
        "created_at_utc": "2026-07-02T00:00:00Z",
        "updated_at_utc": updated,
        "source_patch_zip": "patch.zip" if active else "",
        "raw_error_text": "Batch 19 cleanup left duplicate public ownership errors.",
        "raw_error_snapshot_scrubbed": "Architecture validation reported 17 duplicate public ownership errors.",
        "symptom": "Architecture validation failed with duplicate public ownership errors.",
        "root_cause": "A cleanup changed ownership declarations inconsistently.",
        "wrong_assumption": "Assumed ownership cleanup was globally safe.",
        "correct_fix": "Repair ownership declarations and validate architecture.",
        "do_not_repeat_rule": "Do not freeze cleanup while architecture validation has duplicate public ownership errors.",
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
            "strategy": "duplicate_public_ownership",
            "components": ["batch19", "duplicate public ownership", "Errors: 17"],
            "fingerprint_hash": "batch19-duplicate-public-ownership-v1",
        },
        "prevention_triggers": ["batch19", "duplicate public ownership"],
        "regression_check": regression,
        "validation_command_summary": "Run architecture validation." if active else "",
        "validation_evidence": ["VALIDATION OK: duplicate-cleanup-v13"] if active else ["Draft evidence placeholder."],
        "install_command_summary": "Install patch and validate." if active else "",
        "notes": "Active-ready canonical lesson." if active else "Draft duplicate.",
    }


class _PatchContext:
    def __init__(self, lessons: list[dict[str, Any]]):
        self.lessons = lessons
        self.deleted: list[str] = []
        self.rebuilt = False
        self.originals = (
            guard.list_lessons,
            guard.delete_lesson,
            guard.rebuild_index,
        )

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


def _ids(lessons: list[dict[str, Any]]) -> set[str]:
    return {str(item.get("lesson_id")) for item in lessons}


def _test_single_match_is_not_duplicate() -> None:
    only = _lesson("lesson-batch19-draft", status="draft", active=False, updated="2026-07-02T00:01:00Z")
    with _PatchContext([only]) as context:
        result = guard.resolve_duplicate_lesson_copies("unused-root", dict(only))
        assert result is None, "one stored match must not be duplicate cleanup"
        assert context.deleted == []
        assert _ids(context.lessons) == {"lesson-batch19-draft"}
        assert guard.find_memorize_duplicate("unused-root", dict(only)) is None


def _test_active_plus_draft_deletes_draft_only() -> None:
    active = _lesson("lesson-batch19-active", status="active", active=True, updated="2026-07-02T00:03:00Z")
    draft = _lesson("lesson-batch19-draft", status="draft", active=False, updated="2026-07-02T00:04:00Z")
    with _PatchContext([active, draft]) as context:
        result = guard.resolve_duplicate_lesson_copies("unused-root", dict(draft))
        assert result is not None, "two stored matches should trigger cleanup"
        assert result.deleted_lesson_ids == ("lesson-batch19-draft",)
        assert context.deleted == ["lesson-batch19-draft"]
        assert _ids(context.lessons) == {"lesson-batch19-active"}
        assert context.rebuilt is True


def _test_two_drafts_preserve_newest_delete_oldest() -> None:
    old = _lesson("lesson-batch19-draft-old", status="draft", active=False, updated="2026-07-02T00:01:00Z")
    new = _lesson("lesson-batch19-draft-new", status="draft", active=False, updated="2026-07-02T00:05:00Z")
    with _PatchContext([old, new]) as context:
        result = guard.resolve_duplicate_lesson_copies("unused-root", dict(old))
        assert result is not None, "two draft matches should trigger cleanup"
        assert "lesson-batch19-draft-new" in result.preserved_lesson_ids
        assert _ids(context.lessons) == {"lesson-batch19-draft-new"}
        assert context.deleted == ["lesson-batch19-draft-old"]


def _test_private_duplicate_threshold_helper_exists() -> None:
    assert hasattr(guard, "_has_true_duplicate_matches")
    single = [(_lesson("lesson-one", status="draft", active=False, updated="2026-07-02T00:00:00Z"), "same lesson_id target")]
    double = single + [(_lesson("lesson-two", status="draft", active=False, updated="2026-07-02T00:01:00Z"), "same fingerprint.fingerprint_hash")]
    assert guard._has_true_duplicate_matches(single) is False
    assert guard._has_true_duplicate_matches(double) is True


def main() -> int:
    root = Path.cwd()
    for rel in TOUCHED:
        path = root / rel
        if not path.exists():
            raise AssertionError("missing touched file: " + rel)
        if _line_count(path) > 500:
            raise AssertionError("line limit exceeded: " + rel)
        py_compile.compile(str(path), doraise=True)
    _test_private_duplicate_threshold_helper_exists()
    _test_single_match_is_not_duplicate()
    _test_active_plus_draft_deletes_draft_only()
    _test_two_drafts_preserve_newest_delete_oldest()
    print("VALIDATION OK: error-memory-duplicate-cleanup-v13-single-match-repair")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
