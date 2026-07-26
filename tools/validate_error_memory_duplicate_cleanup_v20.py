# project-path: tools/validate_error_memory_duplicate_cleanup_v20.py
"""Focused validation for Error Memory duplicate cleanup v20."""
from __future__ import annotations

import ast
from pathlib import Path
import py_compile
import tempfile
from typing import Any

from kanda_reasoner_app.error_memory.paths import resolve_error_memory_lessons_dir
from kanda_reasoner_app.error_memory.store import list_lessons, save_lesson
from kanda_reasoner_app.error_memory_gui._duplicate_match_keys import (
    component_variants,
    same_canonical_identifier_family,
)
from kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard import (
    DUPLICATE_CLEANUP_GUARD_VERSION,
    lesson_matches_candidate_error,
    resolve_duplicate_lesson_copies,
)

FEATURE_ID = "error-memory-duplicate-cleanup-v20"
FILES_UNDER_TEST = [
    "kanda_reasoner_app/error_memory_gui/_memorize_duplicate_guard.py",
    "kanda_reasoner_app/error_memory_gui/_duplicate_match_keys.py",
    "kanda_reasoner_app/error_memory_gui/_memorize_flow.py",
    "kanda_reasoner_app/error_memory_gui/_correction_duplicate_guard.py",
    "kanda_reasoner_app/error_memory_gui/_duplicate_pending_cleanup.py",
]


def _project_root(base: Path) -> Path:
    root = base / "kanda_reasoner_show_project_to_AI"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _assert_isolated_store(root: Path, temp_base: Path) -> None:
    lessons_dir = resolve_error_memory_lessons_dir(root).resolve(strict=False)
    try:
        lessons_dir.relative_to(temp_base.resolve(strict=False))
    except ValueError as exc:
        raise AssertionError("validator store escaped temp directory: " + str(lessons_dir)) from exc


def _lesson(
    lesson_id: str,
    *,
    status: str = "draft",
    updated: str = "2026-07-02T00:00:00Z",
    raw_error: str = "Architecture validation reported duplicate public symbols.",
    symptom: str = "Duplicate public ownership error.",
    root_cause: str = "Private helper public ownership overlapped with a facade.",
    correct_fix: str = "Keep the facade as public owner and remove duplicate helper ownership.",
    rule: str = "Do not create duplicate public ownership between facade and helper modules.",
    components: list[Any] | None = None,
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
        "root_cause": root_cause,
        "wrong_assumption": "Assumed helper ownership was safe.",
        "correct_fix": correct_fix,
        "do_not_repeat_rule": rule,
        "long_term_prevention": "Check helper/facade ownership before changing __all__.",
        "redaction": {"applied": True, "export_safe": True, "rules": ["No secrets."]},
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


def _startup_pending_lesson() -> dict[str, Any]:
    return _lesson(
        "lesson-pending-startup-stale-read-order-block-not-replaced-v1",
        raw_error="Earlier validation failed because tell_AI_read_before_all.md did not contain the exact optional/pass maintenance-file step.",
        symptom="Validation failure in tell_AI_read_before_all.md",
        root_cause="Maintenance-file step was not included in the file as expected",
        correct_fix="Add the exact maintenance-file step to tell_AI_read_before_all.md",
        rule="Document all requirements, including maintenance steps, in relevant files and include them clearly marked as optional or required",
        components=[{
            "component_id": "maintenance_steps_doc",
            "description": "Documentation for maintenance steps in files",
        }],
        fingerprint_hash="lesson-pending-startup-stale-read-order-block-not-replaced-v1",
    )


def _startup_active_lesson() -> dict[str, Any]:
    return _lesson(
        "lesson-startup-stale-read-order-block-not-replaced-v1",
        status="active",
        updated="2026-07-02T00:20:00Z",
        raw_error="Validation failed because tell_AI_read_before_all.md did not contain the exact optional/pass maintenance-file step after the startup read-order guard patch.",
        symptom="Validation failed because tell_AI_read_before_all.md did not contain the exact optional/pass maintenance-file step after the startup read-order guard patch.",
        root_cause="The generated read-order block was not reliably replaced when an older read-order marker already existed.",
        correct_fix="Generated startup read-order blocks must be replaced with the canonical current notice every time.",
        rule="Do not skip generated startup read-order notice replacement just because the marker already exists.",
        components=[
            "StartupArtifactReadOrderValidationError",
            "tell_AI_read_before_all.md",
            "assert_read_order_text",
            "validation",
            "optional-pass-step-not-exact",
        ],
        fingerprint_hash="0be3b8c2e35d029d76ef46f6d7a7069d9a39098ba3c8619b20d814ef8867a4d9",
    )


def _ids(root: Path) -> set[str]:
    return {str(item.get("lesson_id")) for item in list_lessons(root, include_inactive=True)}


def _write(root: Path, *lessons: dict[str, Any]) -> None:
    for lesson in lessons:
        save_lesson(root, lesson)


def _test_single_saved_match_stays_without_pending() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = _project_root(Path(temp))
        _assert_isolated_store(root, Path(temp))
        candidate = _lesson("lesson-one-draft")
        _write(root, candidate)
        result = resolve_duplicate_lesson_copies(
            root, candidate, candidate_has_pending_source=False,
            delete_candidate_lesson_id="lesson-one-draft",
        )
        assert result is None
        assert _ids(root) == {"lesson-one-draft"}


def _test_pending_candidate_deletes_single_saved_draft_row() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = _project_root(Path(temp))
        _assert_isolated_store(root, Path(temp))
        candidate = _lesson("lesson-pending-family")
        _write(root, candidate)
        result = resolve_duplicate_lesson_copies(
            root, candidate, candidate_has_pending_source=True,
            delete_candidate_lesson_id="lesson-pending-family",
        )
        assert result is not None
        assert result.deleted_lesson_ids == ("lesson-pending-family",)
        assert _ids(root) == set()


def _test_pending_startup_slug_matches_active_and_deletes_draft() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = _project_root(Path(temp))
        _assert_isolated_store(root, Path(temp))
        candidate = _startup_pending_lesson()
        active = _startup_active_lesson()
        assert same_canonical_identifier_family(candidate, active)
        assert lesson_matches_candidate_error(candidate, active)
        _write(root, candidate, active)
        result = resolve_duplicate_lesson_copies(
            root, candidate, candidate_has_pending_source=False,
            delete_candidate_lesson_id=candidate["lesson_id"],
        )
        assert result is not None
        assert result.deleted_lesson_ids == (candidate["lesson_id"],)
        assert _ids(root) == {active["lesson_id"]}


def _test_dict_components_are_flattened() -> None:
    variants = component_variants({
        "component_id": "maintenance_steps_doc",
        "description": "Documentation for maintenance steps in files",
    })
    assert "maintenance_steps_doc" in variants


def _test_active_ready_copy_is_preserved_over_draft() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = _project_root(Path(temp))
        _assert_isolated_store(root, Path(temp))
        draft = _lesson("lesson-visible-draft", updated="2026-07-02T01:00:00Z")
        active = _lesson("lesson-active-copy", status="active", updated="2026-07-01T01:00:00Z")
        active["fingerprint"]["fingerprint_hash"] = draft["fingerprint"]["fingerprint_hash"]
        _write(root, draft, active)
        result = resolve_duplicate_lesson_copies(
            root, draft, candidate_has_pending_source=False,
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
    assert DUPLICATE_CLEANUP_GUARD_VERSION == "v20_pending_slug_and_semantic_family_cleanup"
    _test_module_hygiene(project_root)
    _test_single_saved_match_stays_without_pending()
    _test_pending_candidate_deletes_single_saved_draft_row()
    _test_pending_startup_slug_matches_active_and_deletes_draft()
    _test_dict_components_are_flattened()
    _test_active_ready_copy_is_preserved_over_draft()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
