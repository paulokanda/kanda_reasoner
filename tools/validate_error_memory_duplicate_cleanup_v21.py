# project-path: tools/validate_error_memory_duplicate_cleanup_v21.py
"""Focused validation for Error Memory duplicate cleanup v21."""
from __future__ import annotations

import importlib
import py_compile
import sys
import types
from pathlib import Path
from typing import Any

FEATURE_ID = "error-memory-duplicate-cleanup-v21"
EXPECTED_VERSION = "v21_narrow_semantic_duplicate_cleanup"

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "kanda_reasoner_app/error_memory_gui/_duplicate_match_keys.py",
    "kanda_reasoner_app/error_memory_gui/_memorize_duplicate_guard.py",
    "kanda_reasoner_app/error_memory_gui/_duplicate_pending_cleanup.py",
    "kanda_reasoner_app/error_memory_gui/_memorize_flow.py",
    "kanda_reasoner_app/error_memory_gui/_correction_duplicate_guard.py",
    "tools/validate_error_memory_duplicate_cleanup_v21.py",
]


def _lesson(
    lesson_id: str,
    *,
    status: str = "draft",
    raw: str = "",
    symptom: str = "",
    rule: str = "",
    phase: str = "validation",
    fp_hash: str = "",
    components: list[Any] | None = None,
    path: str = "",
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "project_slug": "kanda_reasoner",
        "lesson_id": lesson_id,
        "status": status,
        "superseded_by": "",
        "operation_phase": phase,
        "created_at_utc": "2026-07-02T00:00:00Z",
        "updated_at_utc": "2026-07-02T00:00:00Z",
        "source_patch_zip": "fixture.zip",
        "raw_error_text": raw,
        "raw_error_snapshot_scrubbed": raw,
        "symptom": symptom or raw,
        "root_cause": "fixture root cause",
        "wrong_assumption": "fixture wrong assumption",
        "correct_fix": "fixture correct fix",
        "do_not_repeat_rule": rule or "fixture do not repeat rule",
        "long_term_prevention": "fixture prevention",
        "redaction": {"applied": True, "export_safe": True, "rules": ["fixture"]},
        "exception": {
            "type": "FixtureError",
            "phase": phase,
            "relative_file_path": path,
            "function_or_test_name": "fixture_test",
            "message_normalized": raw,
            "stacktrace_scrubbed": "no traceback",
        },
        "fingerprint": {
            "strategy": "fixture",
            "components": components or [path or lesson_id],
            "fingerprint_hash": fp_hash or lesson_id.replace("lesson-", ""),
        },
        "prevention_triggers": ["fixture trigger"],
        "regression_check": {
            "type": "validation_command",
            "command": "python fixture.py",
            "expected_marker": "VALIDATION OK: fixture",
            "required_before_freeze": True,
        },
        "validation_command_summary": "fixture validation",
        "validation_evidence": ["fixture evidence"],
        "install_command_summary": "fixture install",
        "notes": "fixture notes",
    }


def _candidate_batch20() -> dict[str, Any]:
    return _lesson(
        "lesson-batch20-empty-helper-all-public-api-instability-v1",
        status="draft",
        raw=(
            "Architecture validation reported PUBLIC_API_INSTABILITY errors "
            "after setting split helper __all__ = []."
        ),
        symptom=(
            "DUPLICATE_PUBLIC_SYMBOL errors were removed, but architecture "
            "validation still failed with PUBLIC_API_INSTABILITY errors."
        ),
        rule=(
            "Do not make a facade source module declare __all__ = [] when the "
            "facade re-exports public names from it."
        ),
        phase="architecture_warning_cleanup_repair",
        fp_hash="batch20-empty-helper-all-public-api-instability-v1",
        components=[
            "zip_json_files_private_impl.py",
            "zip_json_files_state_private_impl.py",
            "zip_json_files_process_private_impl.py",
            "zip_json_files_publish_private_impl.py",
            "zip_json_files_paths_private_impl.py",
            "__all__ = []",
            "PUBLIC_API_INSTABILITY",
        ],
        path="kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_private_impl.py",
    )


def _unrelated_active_public_surface_lessons() -> list[dict[str, Any]]:
    ids = [
        "lesson-active-compatibility-shim-stale-variant-classification-v1",
        "lesson-batch17-facade-all-validation-and-freeze-hint-contract-attempts-v1",
        "lesson-batch18-duplicate-public-symbol-patch-delivery-helpers-v1",
        "lesson-error-memory-plain-text-json-parser-circular-import-v1",
        "lesson-facade-owned-public-surface-under-500-v1",
        "lesson-manage-architecture-private-helper-public-dataclass-duplicate-v1",
        "lesson-manage-architecture-private-helper-public-surface-reexport-v2",
        "lesson-project-analysis-private-helper-public-surface-v1",
        "lesson-routing-signal-scorer-private-helper-public-surface-v1",
        "lesson-run-orchestrator-helper-public-run-duplicate-v2",
    ]
    result: list[dict[str, Any]] = []
    for lesson_id in ids:
        result.append(_lesson(
            lesson_id,
            status="active",
            raw=(
                "Architecture validation reported duplicate public symbol or "
                "public surface warning in a different helper/facade area."
            ),
            symptom="Public surface validation warning in unrelated module.",
            rule="Do not create duplicate public ownership in helper modules.",
            fp_hash=lesson_id.replace("lesson-", ""),
            components=[
                "DUPLICATE_PUBLIC_SYMBOL",
                "public helper facade",
                "architecture validation",
                lesson_id,
            ],
            path="kanda_reasoner_app/unrelated_area/unrelated_helper.py",
        ))
    return result


def _install_error_memory_stubs() -> None:
    """Install minimal Error Memory stubs for focused import validation."""
    package = types.ModuleType("kanda_reasoner_app.error_memory")
    package.__path__ = []
    models = types.ModuleType("kanda_reasoner_app.error_memory.models")
    store = types.ModuleType("kanda_reasoner_app.error_memory.store")
    models.active_ready = lambda lesson: str(lesson.get("status") or "").lower() == "active"
    store.list_lessons = lambda _root, include_inactive=True: []
    store.delete_lesson = lambda _root, lesson_id: {"lesson_id": lesson_id}
    store.rebuild_index = lambda _root: {"lessons": []}
    sys.modules["kanda_reasoner_app.error_memory"] = package
    sys.modules["kanda_reasoner_app.error_memory.models"] = models
    sys.modules["kanda_reasoner_app.error_memory.store"] = store


def _import_modules():
    _install_error_memory_stubs()
    guard = importlib.import_module(
        "kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard"
    )
    keys = importlib.import_module(
        "kanda_reasoner_app.error_memory_gui._duplicate_match_keys"
    )
    return guard, keys


def _patch_store(guard: Any, lessons: list[dict[str, Any]]) -> list[str]:
    deleted: list[str] = []
    guard.list_lessons = lambda _root, include_inactive=True: list(lessons)

    def _delete(_root: object, lesson_id: str) -> dict[str, Any]:
        deleted.append(lesson_id)
        lessons[:] = [item for item in lessons if item.get("lesson_id") != lesson_id]
        return {"lesson_id": lesson_id}

    guard.delete_lesson = _delete
    guard.rebuild_index = lambda _root: {"lessons": lessons}
    return deleted


def _assert_compile_and_line_counts() -> None:
    for rel in FILES:
        path = ROOT / rel
        if not path.exists():
            raise AssertionError("missing file: " + rel)
        py_compile.compile(str(path), doraise=True)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > 500:
            raise AssertionError(rel + " exceeds 500 lines: " + str(line_count))


def _test_broad_public_surface_false_positive_removed() -> None:
    guard, _keys = _import_modules()
    candidate = _candidate_batch20()
    exact_active = dict(candidate)
    exact_active["status"] = "active"
    stored = [exact_active] + _unrelated_active_public_surface_lessons()
    _patch_store(guard, stored)
    matches = guard.matching_stored_lesson_ids("unused-root", candidate)
    assert matches == ("lesson-batch20-empty-helper-all-public-api-instability-v1",), matches
    result = guard.resolve_duplicate_lesson_copies(
        "unused-root",
        candidate,
        candidate_has_pending_source=True,
        delete_candidate_lesson_id=candidate["lesson_id"],
    )
    assert result is not None
    assert result.deleted_lesson_ids == (), result.deleted_lesson_ids
    assert result.lesson_id == "lesson-batch20-empty-helper-all-public-api-instability-v1"
    assert result.preserved_lesson_ids == (
        "lesson-batch20-empty-helper-all-public-api-instability-v1",
    ), result.preserved_lesson_ids
    assert result.skipped_lesson_ids == (), result.skipped_lesson_ids


def _test_pending_prefix_matches_canonical_identifier() -> None:
    guard, _keys = _import_modules()
    candidate = _lesson(
        "lesson-pending-startup-stale-read-order-block-not-replaced-v1",
        fp_hash="lesson-pending-startup-stale-read-order-block-not-replaced-v1",
    )
    stored = [_lesson("lesson-startup-stale-read-order-block-not-replaced-v1", status="active")]
    _patch_store(guard, stored)
    matches = guard.matching_stored_lesson_ids("unused-root", candidate)
    assert matches == ("lesson-startup-stale-read-order-block-not-replaced-v1",), matches


def _test_specific_same_file_anchor_can_still_match() -> None:
    guard, keys = _import_modules()
    candidate = _lesson(
        "lesson-one",
        raw="Failure in custom_anchor_module.py caused a parser issue.",
        symptom="custom_anchor_module.py parser failed.",
        path="pkg/custom_anchor_module.py",
    )
    stored = _lesson(
        "lesson-two",
        raw="custom_anchor_module.py parser issue happened during validation.",
        symptom="custom_anchor_module.py parser failed in the same flow.",
        path="pkg/custom_anchor_module.py",
    )
    assert keys.same_anchor_semantic_family(candidate, stored)
    assert guard.lesson_matches_candidate_error(candidate, stored)


def main() -> int:
    _assert_compile_and_line_counts()
    guard, _keys = _import_modules()
    version = getattr(guard, "DUPLICATE_CLEANUP_GUARD_VERSION", "")
    assert version == EXPECTED_VERSION, version
    _test_broad_public_surface_false_positive_removed()
    _test_pending_prefix_matches_canonical_identifier()
    _test_specific_same_file_anchor_can_still_match()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
