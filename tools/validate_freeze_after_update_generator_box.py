#!/usr/bin/env python3
"""Validate the Freeze Feature After Update blueprint generator box."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from kanda_reasoner_app.freeze_after_update.contract import (
    ensure_freeze_after_update_box,
    generate_freeze_after_update_ai_files,
    inspect_freeze_after_update_box,
)


WORKFLOW_MARKERS = [
    "Required AI delivery workflow for freeze patches",
    "ZIP placement and root-to-staging rule",
    "<project_name>_delete_after_daily_work",
    "$ROOT_PATCH_ZIP",
    "$WORK_PATCH_ZIP",
    "Move-Item -Path $ROOT_PATCH_ZIP -Destination $WORK_PATCH_ZIP -Force",
    "zip is not in root of drive:\\ where project is",
    "The install block must be adapted to the exact files in the patch ZIP",
    "not depend on an installer script inside the ZIP",
    "$env:PYTHONPATH = $PROJECT_ROOT",
    "Do not use Bash heredoc syntax",
    "temporary .py file under the delete-after-daily-work folder",
    "Mandatory sandbox pre-delivery validation rule",
    "Before giving the user any ZIP, install block, or validation block, AI must test the deliverable in its own sandbox first",
    "Do not validate by reading guessed or private result attributes",
    "The process is not complete when AI gives the ZIP",
    "The patch is freezeable only after clean validation evidence",
]

FORBIDDEN_WORKFLOW_MARKERS = [
    "_PATCH_NAME",
    "install_patch.ps1",
    "validate_patch.ps1",
    "Join-Path $PROJECT_DRIVE (\"_\" + $PATCH_NAME)",
    "powershell -ExecutionPolicy Bypass -File (Join-Path $PATCH_DIR",
]


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_fresh_external_project() -> None:
    temp_root = Path(tempfile.mkdtemp(prefix="freeze_after_update_generator_"))
    try:
        project_root = temp_root / "external_project"
        project_root.mkdir()
        (project_root / "README.md").write_text("# External Project\n", encoding="utf-8")

        ensure_result = ensure_freeze_after_update_box(project_root)
        assert_true(ensure_result.ok, ensure_result.message)
        assert_true((project_root / "project_freeze_after_update").is_dir(), "box was not created")
        assert_true(not (project_root / "project_freeze_ledger").exists(), "external project must not receive project_freeze_ledger")

        inspect_result = inspect_freeze_after_update_box(project_root)
        assert_true(inspect_result.ok, inspect_result.message)

        generate_result = generate_freeze_after_update_ai_files(project_root)
        assert_true(generate_result.ok, generate_result.message)
        assert_true(generate_result.freeze_count == 0, "fresh external project should have zero freezes")
        assert_true(generate_result.output_zip is not None and generate_result.output_zip.exists(), "ZIP missing")
        assert_true(
            generate_result.output_instruction is not None and generate_result.output_instruction.exists(),
            "instruction file missing",
        )

        text = read_text(generate_result.output_instruction)
        for marker in WORKFLOW_MARKERS:
            assert_true(marker in text, "missing workflow marker: " + marker)
        for marker in FORBIDDEN_WORKFLOW_MARKERS:
            assert_true(marker not in text, "forbidden stale workflow marker still present: " + marker)

        index_path = project_root / "project_freeze_after_update" / "frozen_features_memory" / "freeze_index.json"
        data = json.loads(read_text(index_path))
        assert_true(data.get("schema_version") == "1.0", "schema version mismatch")
        assert_true(data.get("freezes") == [], "fresh freeze index should be empty")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def validate_existing_freeze_entry() -> None:
    temp_root = Path(tempfile.mkdtemp(prefix="freeze_after_update_generator_existing_"))
    try:
        project_root = temp_root / "project_with_freeze"
        project_root.mkdir()
        ensure_result = ensure_freeze_after_update_box(project_root)
        assert_true(ensure_result.ok, ensure_result.message)

        entry_path = (
            project_root
            / "project_freeze_after_update"
            / "frozen_features_memory"
            / "entries"
            / "freeze-test-generator-box.md"
        )
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

        generate_result = generate_freeze_after_update_ai_files(project_root)
        assert_true(generate_result.ok, generate_result.message)
        assert_true(generate_result.freeze_count == 1, "expected one freeze entry")
        assert_true(generate_result.output_instruction is not None, "instruction missing from result")
        text = read_text(generate_result.output_instruction)
        assert_true("This project currently has 1 frozen feature entry file(s)." in text, "freeze count not reported")
        assert_true("freeze-test-generator-box.md" in text, "freeze entry not listed")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def validate_current_project_regeneration(project_root: Path) -> None:
    generator_path = project_root / "project_freeze_ledger" / "freeze_tools" / "freeze_after_update_generator.py"
    assert_true(generator_path.exists(), "blueprint generator missing")

    result = generate_freeze_after_update_ai_files(project_root)
    assert_true(result.ok, result.message)
    assert_true(result.output_zip is not None and result.output_zip.exists(), "current project ZIP missing")
    assert_true(result.output_instruction is not None and result.output_instruction.exists(), "current project instruction missing")

    text = read_text(result.output_instruction)
    for marker in WORKFLOW_MARKERS:
        assert_true(marker in text, "current project instruction missing marker: " + marker)
    for marker in FORBIDDEN_WORKFLOW_MARKERS:
        assert_true(marker not in text, "current project instruction still contains stale marker: " + marker)

    expected_entries = len(list((project_root / "project_freeze_after_update" / "frozen_features_memory" / "entries").glob("freeze-*.md")))
    assert_true(result.freeze_count == expected_entries, "result freeze_count does not match entry files")
    print("current_project_freeze_count=", result.freeze_count)


def main() -> int:
    project_root = Path.cwd().resolve()
    print("Validating Freeze Feature After Update generator box...")
    print("Project root:", project_root)
    validate_fresh_external_project()
    print("PASS fresh external project")
    validate_existing_freeze_entry()
    print("PASS existing freeze entry")
    validate_current_project_regeneration(project_root)
    print("PASS current project regeneration")
    print("VALIDATION OK - generator logic lives in the blueprint box and regenerates instructions correctly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
