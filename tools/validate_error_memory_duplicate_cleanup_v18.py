# project-path: tools/validate_error_memory_duplicate_cleanup_v18.py
"""Focused validation for Error Memory duplicate cleanup v17."""
from __future__ import annotations

import ast
from pathlib import Path
import py_compile
import tempfile
from typing import Any

from kanda_reasoner_app.error_memory.store import list_lessons, save_lesson
from kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard import (
    DUPLICATE_CLEANUP_GUARD_VERSION,
    lesson_matches_candidate_error,
    resolve_duplicate_lesson_copies,
)

FEATURE_ID = "error-memory-duplicate-cleanup-v18"
FILES_UNDER_TEST = [
    "kanda_reasoner_app/error_memory_gui/_memorize_duplicate_guard.py",
    "kanda_reasoner_app/error_memory_gui/_memorize_flow.py",
    "kanda_reasoner_app/error_memory_gui/_correction_duplicate_guard.py",
    "kanda_reasoner_app/error_memory_gui/_duplicate_pending_cleanup.py",
]


def _project_root(base: Path) -> Path:
    root = base / "kanda_reasoner"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _lesson(
    lesson_id: str,
    *,
    status: str = "draft",
    updated: str = "2026-07-02T00:00:00Z",
    raw_error: str = "Architecture validation reported duplicate public symbols.",
    symptom: str = "Duplicate public ownership error.",
    components: list[str] | None = None,
    fingerprint_hash: str | None = None,
) -> dict[str, Any]:
    components = components or ["duplicate_public_symbol", "zip_json_files_private_impl"]
    return {
        "schema_version": "1.0",
        "project_slug": "kanda_reasoner",
        "lesson_id": lesson_id,
        "status": status,
        "superseded_by": "",
        "operation_phase": "architecture_validation",
        "created_at_utc": "2026-07-02T00:00:00Z",
        "updated_at_utc": updated,
        "source_patch_zip": "kanda_test_patch.zip",
        "raw_error_text": raw_error,
        "raw_error_snapshot_scrubbed": raw_error,
        "symptom": symptom,
        "root_cause": "Private helper public ownership overlapped with a facade.",
        "wrong_assumption": "Assumed helper __all__ ownership was safe.",
        "correct_fix": "Keep the facade as public owner and remove duplicate helper ownership.",
        "do_not_repeat_rule": "Do not create duplicate public ownership between facade and helper modules.",
        "long_term_prevention": "Check helper/facade ownership before changing __all__.",
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": ["No secrets included."],
        },
        "exception": {
            "type": "DuplicatePublicSymbolArchitectureFinding",
            "phase": "architecture_validation",
            "relative_file_path": "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_private_impl.py",
            "function_or_test_name": "manage_architecture --validate",
            "message_normalized": "DUPLICATE_PUBLIC_SYMBOL",
            "stacktrace_scrubbed": "No runtime traceback.",
        },
        "fingerprint": {
            "strategy": "duplicate_public_symbol_family",
            "components": components,
            "fingerprint_hash": fingerprint_hash or lesson_id.replace("lesson-", ""),
        },
        "prevention_triggers": ["DUPLICATE_PUBLIC_SYMBOL", "facade helper split"],
        "regression_check": {
            "type": "validation_command",
            "command": "python kanda_reasoner_app/manage_architecture/manage_architecture.py --root E:/kanda_reasoner --validate",
            "expected_marker": "Errors: 0",
            "required_before_freeze": True,
        },
        "validation_command_summary": "Run architecture validation and confirm Errors: 0.",
        "validation_evidence": ["No successful validation evidence was provided in the input; keep status draft."],
        "install_command_summary": "Install staged test patch.",
        "notes": "Focused validator fixture.",
    }


def _ids(root: Path) -> set[str]:
    return {str(item.get("lesson_id")) for item in list_lessons(root, include_inactive=True)}


def _write(root: Path, *lessons: dict[str, Any]) -> None:
    for lesson in lessons:
        save_lesson(root, lesson)


def _test_single_saved_match_is_never_cleanup_without_pending() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = _project_root(Path(temp))
        candidate = _lesson("lesson-one-draft")
        _write(root, candidate)
        result = resolve_duplicate_lesson_copies(
            root,
            candidate,
            candidate_has_pending_source=False,
            delete_candidate_lesson_id="lesson-one-draft",
        )
        assert result is None, "one saved match without pending source must not clean up"
        assert _ids(root) == {"lesson-one-draft"}


def _test_pending_candidate_deletes_single_saved_draft_row() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = _project_root(Path(temp))
        candidate = _lesson("lesson-pending-family")
        _write(root, candidate)
        result = resolve_duplicate_lesson_copies(
            root,
            candidate,
            candidate_has_pending_source=True,
            delete_candidate_lesson_id="lesson-pending-family",
        )
        assert result is not None, "pending candidate plus one saved draft is duplicate cleanup"
        assert result.deleted_lesson_ids == ("lesson-pending-family",)
        assert _ids(root) == set()


def _test_selected_saved_candidate_deleted_when_related_saved_duplicate_exists() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = _project_root(Path(temp))
        candidate = _lesson(
            "lesson-batch20-batch19-runner-help-duplicate-public-symbols-v1",
            updated="2026-07-02T01:50:00Z",
            raw_error="Focused Batch 19 validation failed with 17 DUPLICATE_PUBLIC_SYMBOL errors.",
            symptom="A frozen Batch 19 cleanup left architecture duplicate ownership errors.",
            components=[
                "kanda_reasoner_app.reasoner_tools_shell.runner_help",
                "zip_json_files_private_impl",
                "zip_json_files_state_private_impl",
                "zip_json_files_process_private_impl",
                "zip_json_files_publish_private_impl",
                "zip_json_files_paths_private_impl",
            ],
            fingerprint_hash="batch20-batch19-runner-help-duplicate-public-symbols-v1",
        )
        related = _lesson(
            "lesson-batch20-empty-helper-all-public-api-instability-v1",
            updated="2026-07-01T03:25:00Z",
            raw_error="Architecture validation reported PUBLIC_API_INSTABILITY errors after setting split helper __all__ = [].",
            symptom="DUPLICATE_PUBLIC_SYMBOL errors were removed, but PUBLIC_API_INSTABILITY errors remained.",
            components=[
                "zip_json_files_private_impl.py",
                "zip_json_files_state_private_impl.py",
                "zip_json_files_process_private_impl.py",
                "zip_json_files_publish_private_impl.py",
                "zip_json_files_paths_private_impl.py",
                "__all__ = []",
                "PUBLIC_API_INSTABILITY",
            ],
            fingerprint_hash="batch20-empty-helper-all-public-api-instability-v1",
        )
        assert lesson_matches_candidate_error(candidate, related)
        _write(root, candidate, related)
        result = resolve_duplicate_lesson_copies(
            root,
            candidate,
            candidate_has_pending_source=False,
            delete_candidate_lesson_id="lesson-batch20-batch19-runner-help-duplicate-public-symbols-v1",
        )
        assert result is not None, "related saved drafts must trigger duplicate cleanup"
        assert result.deleted_lesson_ids == (
            "lesson-batch20-batch19-runner-help-duplicate-public-symbols-v1",
        )
        assert _ids(root) == {"lesson-batch20-empty-helper-all-public-api-instability-v1"}


def _test_active_ready_copy_is_preserved_over_draft() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = _project_root(Path(temp))
        draft = _lesson("lesson-visible-draft", updated="2026-07-02T01:00:00Z")
        active = _lesson("lesson-active-copy", status="active", updated="2026-07-01T01:00:00Z")
        active["fingerprint"]["fingerprint_hash"] = draft["fingerprint"]["fingerprint_hash"]
        _write(root, draft, active)
        result = resolve_duplicate_lesson_copies(
            root,
            draft,
            candidate_has_pending_source=False,
            delete_candidate_lesson_id="lesson-visible-draft",
        )
        assert result is not None
        assert result.deleted_lesson_ids == ("lesson-visible-draft",)
        assert _ids(root) == {"lesson-active-copy"}


def _test_module_hygiene(project_root: Path) -> None:
    for rel in FILES_UNDER_TEST:
        path = project_root / rel
        text = path.read_text(encoding="utf-8")
        assert len(text.splitlines()) <= 500, rel + " exceeds 500 lines"
        ast.parse(text)
        py_compile.compile(str(path), doraise=True)


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    assert DUPLICATE_CLEANUP_GUARD_VERSION == "v18_hard_single_saved_no_cleanup"
    import kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard as guard
    guard_path = Path(guard.__file__).resolve()
    assert "kanda_reasoner_app" in str(guard_path).replace("\\", "/")
    guard_text = guard_path.read_text(encoding="utf-8")
    assert "v18_hard_single_saved_no_cleanup" in guard_text
    assert "if stored_count < 2 and not candidate_has_pending_source" in guard_text
    _test_module_hygiene(project_root)
    _test_single_saved_match_is_never_cleanup_without_pending()
    _test_pending_candidate_deletes_single_saved_draft_row()
    _test_selected_saved_candidate_deleted_when_related_saved_duplicate_exists()
    _test_active_ready_copy_is_preserved_over_draft()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
