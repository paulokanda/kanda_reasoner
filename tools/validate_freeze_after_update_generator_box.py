#!/usr/bin/env python3
# project-path: tools/validate_freeze_after_update_generator_box.py
"""Validate the retired Freeze AI-send generator bridge.

The public generator entry point is intentionally a cleanup-only compatibility
bridge. Fixture Projects use unique slugs and deterministic external-support
cleanup so repeated real-Windows validation cannot inherit prior fixture state.
"""

from __future__ import annotations

__all__ = [
    "validate_fresh_external_project",
    "validate_existing_freeze_entry",
    "validate_current_project_regeneration",
]

import shutil
import tempfile
from pathlib import Path
from uuid import uuid4

from kanda_reasoner_app.freeze_after_update.contract import (
    ensure_freeze_after_update_box,
    generate_freeze_after_update_ai_files,
    inspect_freeze_after_update_box,
)
from kanda_reasoner_app.freeze_after_update.paths import build_paths

_DEPRECATION_MARKER = "Deprecated project-local files_to_send_ai ZIP generation skipped"


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _unique_project(temp_root: Path, prefix: str) -> Path:
    project_root = temp_root / f"{prefix}_{uuid4().hex}"
    project_root.mkdir()
    return project_root


def _external_support_root(project_root: Path) -> Path:
    return build_paths(project_root).box_root.parent


def _reset_fixture_support(project_root: Path) -> Path:
    support_root = _external_support_root(project_root)
    shutil.rmtree(support_root, ignore_errors=True)
    return support_root


def _assert_deprecated_generation_result(result: object) -> None:
    assert_true(bool(getattr(result, "ok", False)), str(getattr(result, "message", "")))
    assert_true(getattr(result, "output_zip", None) is None, "deprecated ZIP output was recreated")
    assert_true(
        getattr(result, "output_instruction", None) is None,
        "deprecated instruction output was recreated",
    )
    assert_true(
        _DEPRECATION_MARKER in str(getattr(result, "message", "")),
        "deprecated-generation status message missing",
    )


def _seed_stale_project_local_output(project_root: Path) -> Path:
    stale_root = project_root / "project_freeze_after_update" / "files_to_send_ai"
    stale_root.mkdir(parents=True, exist_ok=True)
    (stale_root / "freeze_feature_ai_send_pack_stale.zip").write_bytes(b"stale")
    (stale_root / "what_to_say_to_ai_freeze_feature.md").write_text(
        "stale instruction\n",
        encoding="utf-8",
    )
    return stale_root


def _assert_no_generated_pack(project_root: Path) -> None:
    paths = build_paths(project_root)
    assert_true(
        not list(paths.send_root.glob("freeze_feature_ai_send_pack_*.zip")),
        "deprecated external Freeze ZIP was generated",
    )
    assert_true(
        not (project_root / "project_freeze_after_update" / "files_to_send_ai").exists(),
        "deprecated project-local files_to_send_ai folder exists",
    )


def validate_fresh_external_project() -> None:
    temp_root = Path(tempfile.mkdtemp(prefix="freeze_after_update_generator_"))
    project_root = _unique_project(temp_root, "external_project")
    support_root = _reset_fixture_support(project_root)
    try:
        (project_root / "README.md").write_text("# External Project\n", encoding="utf-8")
        paths = build_paths(project_root)

        before = inspect_freeze_after_update_box(project_root)
        assert_true(not before.ok, "unique fresh fixture unexpectedly inherited valid support state")

        ensure_result = ensure_freeze_after_update_box(project_root)
        assert_true(ensure_result.ok, ensure_result.message)
        assert_true(paths.box_root.is_dir(), "external support box was not created")
        assert_true(
            not (project_root / "project_freeze_after_update").exists(),
            "freeze state must not be created in Project source",
        )
        assert_true(not (project_root / "project_freeze_ledger").exists(), "external project must not receive project_freeze_ledger")

        inspect_result = inspect_freeze_after_update_box(project_root)
        assert_true(inspect_result.ok, inspect_result.message)

        _seed_stale_project_local_output(project_root)
        generate_result = generate_freeze_after_update_ai_files(project_root)
        _assert_deprecated_generation_result(generate_result)
        assert_true(generate_result.freeze_count == 0, "cleanup bridge must not synthesize freeze count")
        _assert_no_generated_pack(project_root)
        assert_true(paths.freeze_index.is_file(), "external freeze index missing")
    finally:
        shutil.rmtree(support_root, ignore_errors=True)
        shutil.rmtree(temp_root, ignore_errors=True)
    assert_true(not support_root.exists(), "fresh generator fixture support root survived cleanup")


def validate_existing_freeze_entry() -> None:
    temp_root = Path(tempfile.mkdtemp(prefix="freeze_after_update_generator_existing_"))
    project_root = _unique_project(temp_root, "project_with_freeze")
    support_root = _reset_fixture_support(project_root)
    try:
        paths = build_paths(project_root)
        ensure_result = ensure_freeze_after_update_box(project_root)
        assert_true(ensure_result.ok, ensure_result.message)

        entry_path = paths.entries_root / "freeze-test-generator-box.md"
        entry_path.write_text(
            """---
freeze_id: "freeze-test-generator-box"
box: "test_box"
status: "frozen"
date: "2026-06-13"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-test-generator-box.md"
protected_paths:
  - "src/example.py"
do_not_touch_summary:
  - "Preserve example behavior."
superseded_by: null
---
# freeze-test-generator-box
""",
            encoding="utf-8",
        )
        original = entry_path.read_text(encoding="utf-8")
        _seed_stale_project_local_output(project_root)

        generate_result = generate_freeze_after_update_ai_files(project_root)
        _assert_deprecated_generation_result(generate_result)
        _assert_no_generated_pack(project_root)
        assert_true(entry_path.is_file(), "existing freeze entry was removed")
        assert_true(entry_path.read_text(encoding="utf-8") == original, "existing freeze entry changed")
    finally:
        shutil.rmtree(support_root, ignore_errors=True)
        shutil.rmtree(temp_root, ignore_errors=True)
    assert_true(not support_root.exists(), "entry generator fixture support root survived cleanup")


def validate_current_project_regeneration(project_root: Path) -> None:
    paths = build_paths(project_root)
    before_entries = {
        path.resolve(): path.read_bytes()
        for path in paths.entries_root.glob("freeze-*.md")
        if path.is_file()
    }
    stale_root = _seed_stale_project_local_output(project_root)

    result = generate_freeze_after_update_ai_files(project_root)
    _assert_deprecated_generation_result(result)
    assert_true(not stale_root.exists(), "current Project stale local pack was not cleaned")
    _assert_no_generated_pack(project_root)

    after_entries = {
        path.resolve(): path.read_bytes()
        for path in paths.entries_root.glob("freeze-*.md")
        if path.is_file()
    }
    assert_true(after_entries == before_entries, "cleanup bridge mutated frozen feature entries")
    print("current_project_freeze_entries_preserved=", len(after_entries))


def main() -> int:
    project_root = Path.cwd().resolve()
    print("Validating retired Freeze Feature After Update AI-send bridge...")
    print("Project root:", project_root)
    validate_fresh_external_project()
    print("PASS fresh external project")
    validate_existing_freeze_entry()
    print("PASS existing freeze entry")
    validate_current_project_regeneration(project_root)
    print("PASS current project regeneration")
    print("UNIQUE_GENERATOR_SUPPORT_FIXTURES: PASS")
    print("GENERATOR_FIXTURE_SUPPORT_CLEANUP: PASS")
    print("DEPRECATED_FREEZE_AI_SEND_GENERATION_BLOCKED: PASS")
    print("EXISTING_FREEZE_MEMORY_PRESERVED: PASS")
    print("VALIDATION OK - deprecated Freeze AI-send generation remains disabled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
