#!/usr/bin/env python3
# project-path: tools/validate_freeze_after_update_box.py
"""Validate the current Freeze Feature After Update backend contract.

The legacy project-local ``files_to_send_ai`` ZIP generator is intentionally
retired. Freeze context is delivered through the external Show Project to AI
startup/source-archive channels. Fixture Projects use unique slugs and clean
their external support roots before and after every test so reruns cannot inherit
valid state from a prior process.
"""

from __future__ import annotations

__all__ = [
    "validate_fresh_project",
    "validate_existing_entry_preservation",
    "validate_invalid_inputs",
    "validate_no_kanda_contamination",
]

import json
import shutil
import sys
import tempfile
from pathlib import Path
from uuid import uuid4

PROJECT_ROOT = Path(__file__).resolve().parents[1]
_DEPRECATION_MARKER = "Deprecated project-local files_to_send_ai ZIP generation skipped"


def _ensure_project_root_on_path() -> None:
    project_root_text = str(PROJECT_ROOT)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)


def _load_freeze_after_update_api() -> None:
    global ensure_freeze_after_update_box
    global generate_freeze_after_update_ai_files
    global inspect_freeze_after_update_box
    global build_paths
    global FreezeAfterUpdateStatus

    _ensure_project_root_on_path()
    from kanda_reasoner_app.freeze_after_update.contract import (
        ensure_freeze_after_update_box as ensure_box,
        generate_freeze_after_update_ai_files as generate_files,
        inspect_freeze_after_update_box as inspect_box,
    )
    from kanda_reasoner_app.freeze_after_update.paths import build_paths as build_freeze_paths
    from kanda_reasoner_app.freeze_after_update.result import (
        FreezeAfterUpdateStatus as FreezeStatus,
    )

    ensure_freeze_after_update_box = ensure_box
    generate_freeze_after_update_ai_files = generate_files
    inspect_freeze_after_update_box = inspect_box
    build_paths = build_freeze_paths
    FreezeAfterUpdateStatus = FreezeStatus


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def assert_file(path: Path) -> None:
    assert_true(path.is_file(), f"Expected file: {path}")


def assert_dir(path: Path) -> None:
    assert_true(path.is_dir(), f"Expected directory: {path}")


def _unique_project(temp_root: Path, prefix: str) -> Path:
    project = temp_root / f"{prefix}_{uuid4().hex}"
    project.mkdir()
    return project


def _external_support_root(project: Path) -> Path:
    return build_paths(project).box_root.parent


def _reset_fixture_support(project: Path) -> Path:
    support_root = _external_support_root(project)
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


def _make_stale_project_local_pack(project: Path) -> Path:
    stale_root = project / "project_freeze_after_update" / "files_to_send_ai"
    stale_root.mkdir(parents=True, exist_ok=True)
    stale_zip = stale_root / "freeze_feature_ai_send_pack_stale.zip"
    stale_zip.write_bytes(b"stale")
    return stale_root


def validate_fresh_project() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_after_update_") as tmp:
        project = _unique_project(Path(tmp), "sample_project")
        support_root = _reset_fixture_support(project)
        try:
            paths = build_paths(project)
            before = inspect_freeze_after_update_box(project)
            assert_true(before.status == FreezeAfterUpdateStatus.INCOMPLETE, before.message)

            created = ensure_freeze_after_update_box(project)
            assert_true(created.ok, created.message)

            assert_dir(paths.box_root)
            assert_true(paths.box_root != project / "project_freeze_after_update", "freeze state written inside source")
            assert_dir(paths.memory_root)
            assert_dir(paths.entries_root)
            assert_dir(paths.send_root)
            assert_file(paths.root_readme)
            assert_file(paths.freeze_index)
            assert_file(paths.frozen_steps)
            assert_file(paths.entries_readme)
            assert_file(paths.send_readme)

            data = json.loads(paths.freeze_index.read_text(encoding="utf-8"))
            assert_true(data.get("schema_version") == "1.0", "schema_version mismatch")
            assert_true(data.get("freezes") == [], "new project should start with empty freezes")

            stale_root = _make_stale_project_local_pack(project)
            pack_result = generate_freeze_after_update_ai_files(project)
            _assert_deprecated_generation_result(pack_result)
            assert_true(not stale_root.exists(), "stale project-local AI-send folder was not removed")
            assert_true(
                not list(paths.send_root.glob("freeze_feature_ai_send_pack_*.zip")),
                "deprecated external Freeze ZIP was generated",
            )

            after_second = generate_freeze_after_update_ai_files(project)
            _assert_deprecated_generation_result(after_second)
            assert_true(paths.freeze_index.is_file(), "freeze memory was removed by cleanup")
        finally:
            shutil.rmtree(support_root, ignore_errors=True)
        assert_true(not support_root.exists(), "fixture external support root survived cleanup")


def validate_existing_entry_preservation() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_after_update_entry_") as tmp:
        project = _unique_project(Path(tmp), "project_with_entry")
        support_root = _reset_fixture_support(project)
        try:
            paths = build_paths(project)
            ensure_result = ensure_freeze_after_update_box(project)
            assert_true(ensure_result.ok, ensure_result.message)

            entry = paths.entries_root / "freeze-sample-feature.md"
            entry.write_text(
                """---
freeze_id: "freeze-sample-feature"
box: "sample/feature"
status: "frozen"
date: "2026-06-13"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-sample-feature.md"
protected_paths:
  - "sample_module/"
do_not_touch_summary:
  - "Do not regress sample behavior."
superseded_by: null
---

# freeze-sample-feature

Sample freeze entry.
""",
                encoding="utf-8",
            )
            before_text = entry.read_text(encoding="utf-8")
            stale_root = _make_stale_project_local_pack(project)

            result = generate_freeze_after_update_ai_files(project)
            _assert_deprecated_generation_result(result)
            assert_true(not stale_root.exists(), "stale project-local pack survived cleanup")
            assert_true(entry.is_file(), "existing frozen entry was removed")
            assert_true(entry.read_text(encoding="utf-8") == before_text, "existing frozen entry was mutated")

            inspected = inspect_freeze_after_update_box(project)
            assert_true(inspected.ok, inspected.message)
        finally:
            shutil.rmtree(support_root, ignore_errors=True)
        assert_true(not support_root.exists(), "entry fixture support root survived cleanup")


def validate_invalid_inputs() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_after_update_invalid_") as tmp:
        file_root = Path(tmp) / "not_a_dir.py"
        file_root.write_text("print('not a project')\n", encoding="utf-8")
        result = ensure_freeze_after_update_box(file_root)
        assert_true(
            result.status == FreezeAfterUpdateStatus.INVALID_PROJECT_ROOT,
            "file project root should be invalid",
        )

        project = _unique_project(Path(tmp), "invalid_project")
        support_root = _reset_fixture_support(project)
        try:
            paths = build_paths(project)
            paths.box_root.parent.mkdir(parents=True, exist_ok=True)
            paths.box_root.write_text("not a folder\n", encoding="utf-8")
            result = ensure_freeze_after_update_box(project)
            assert_true(
                result.status == FreezeAfterUpdateStatus.INVALID_BOX_PATH,
                "external box path file should be invalid",
            )
        finally:
            shutil.rmtree(support_root, ignore_errors=True)
        assert_true(not support_root.exists(), "invalid fixture support root survived cleanup")


def validate_no_kanda_contamination() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_after_update_clean_") as tmp:
        project = _unique_project(Path(tmp), "clean_project")
        support_root = _reset_fixture_support(project)
        try:
            ensured = ensure_freeze_after_update_box(project)
            assert_true(ensured.ok, ensured.message)
            result = generate_freeze_after_update_ai_files(project)
            _assert_deprecated_generation_result(result)
            paths = build_paths(project)
            generated_text = "\n".join(
                path.read_text(encoding="utf-8", errors="ignore")
                for path in paths.box_root.rglob("*.md")
                if path.is_file()
            )
            forbidden_markers = [
                "freeze-20260612-project-freeze-ledger",
                "E:\\kanda_reasoner",
                "E:/kanda_reasoner",
            ]
            for marker in forbidden_markers:
                assert_true(marker not in generated_text, f"KANDA-specific marker leaked: {marker}")
        finally:
            shutil.rmtree(support_root, ignore_errors=True)
        assert_true(not support_root.exists(), "clean fixture support root survived cleanup")


def main() -> int:
    _load_freeze_after_update_api()
    tests = [
        validate_fresh_project,
        validate_existing_entry_preservation,
        validate_invalid_inputs,
        validate_no_kanda_contamination,
    ]
    for test in tests:
        print(f"RUN {test.__name__}")
        test()
        print(f"PASS {test.__name__}")
    print("UNIQUE_EXTERNAL_SUPPORT_FIXTURES: PASS")
    print("FIXTURE_EXTERNAL_SUPPORT_CLEANUP: PASS")
    print("DEPRECATED_PROJECT_LOCAL_FREEZE_PACK_BLOCKED: PASS")
    print("EXTERNAL_FREEZE_MEMORY_PRESERVED: PASS")
    print("VALIDATION OK - Freeze Feature After Update backend passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
