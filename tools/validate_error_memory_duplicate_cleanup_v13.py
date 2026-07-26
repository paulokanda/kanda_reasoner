# project-path: tools/validate_error_memory_duplicate_cleanup_v13.py
"""Focused validation for Error Memory duplicate cleanup v13."""
from __future__ import annotations

import py_compile
import shutil
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kanda_reasoner_app.error_memory.store import list_lessons, save_lesson
from kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard import (
    find_memorize_duplicate,
    resolve_duplicate_lesson_copies,
)

TOUCHED = [
    "kanda_reasoner_app/error_memory_gui/_memorize_duplicate_guard.py",
    "kanda_reasoner_app/error_memory_gui/_memorize_flow.py",
    "kanda_reasoner_app/error_memory_gui/_correction_duplicate_guard.py",
    "tools/validate_error_memory_duplicate_cleanup_v13.py",
]


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _lesson(lesson_id: str, *, status: str, active: bool, updated: str) -> dict:
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
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": ["No secrets included."],
        },
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


def _create_project() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="kanda_em_v13_"))
    project = tmp / "tmp_project"
    project.mkdir(parents=True)
    return project


def _read_ids(project: Path) -> set[str]:
    return {str(item.get("lesson_id")) for item in list_lessons(project, include_inactive=True)}


def _test_single_match_is_not_duplicate() -> None:
    project = _create_project()
    try:
        only = _lesson("lesson-batch19-draft", status="draft", active=False, updated="2026-07-02T00:01:00Z")
        save_lesson(project, only)
        result = resolve_duplicate_lesson_copies(project, dict(only))
        assert result is None, "one stored match must not be duplicate cleanup"
        assert _read_ids(project) == {"lesson-batch19-draft"}
        assert find_memorize_duplicate(project, dict(only)) is None
    finally:
        shutil.rmtree(project.parent, ignore_errors=True)


def _test_active_plus_draft_deletes_draft_only() -> None:
    project = _create_project()
    try:
        active = _lesson("lesson-batch19-active", status="active", active=True, updated="2026-07-02T00:03:00Z")
        draft = _lesson("lesson-batch19-draft", status="draft", active=False, updated="2026-07-02T00:04:00Z")
        save_lesson(project, active)
        save_lesson(project, draft)
        result = resolve_duplicate_lesson_copies(project, dict(draft))
        assert result is not None, "two stored matches should trigger cleanup"
        assert result.deleted_lesson_ids == ("lesson-batch19-draft",)
        assert _read_ids(project) == {"lesson-batch19-active"}
    finally:
        shutil.rmtree(project.parent, ignore_errors=True)


def _test_two_drafts_preserve_newest_delete_oldest() -> None:
    project = _create_project()
    try:
        old = _lesson("lesson-batch19-draft-old", status="draft", active=False, updated="2026-07-02T00:01:00Z")
        new = _lesson("lesson-batch19-draft-new", status="draft", active=False, updated="2026-07-02T00:05:00Z")
        save_lesson(project, old)
        save_lesson(project, new)
        result = resolve_duplicate_lesson_copies(project, dict(old))
        assert result is not None, "two draft matches should trigger cleanup"
        assert "lesson-batch19-draft-new" in result.preserved_lesson_ids
        remaining = _read_ids(project)
        assert remaining == {"lesson-batch19-draft-new"}, remaining
        assert "lesson-batch19-draft-old" not in remaining
    finally:
        shutil.rmtree(project.parent, ignore_errors=True)


def main() -> int:
    root = Path.cwd()
    for rel in TOUCHED:
        path = root / rel
        if not path.exists():
            raise AssertionError("missing touched file: " + rel)
        if _line_count(path) > 500:
            raise AssertionError("line limit exceeded: " + rel)
        py_compile.compile(str(path), doraise=True)
    _test_single_match_is_not_duplicate()
    _test_active_plus_draft_deletes_draft_only()
    _test_two_drafts_preserve_newest_delete_oldest()
    print("VALIDATION OK: error-memory-duplicate-cleanup-v13")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
