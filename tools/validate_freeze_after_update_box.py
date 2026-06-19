#!/usr/bin/env python3
"""Validate the Freeze Feature After Update backend box without opening the GUI."""

from __future__ import annotations

import json
import sys
import tempfile
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.freeze_after_update.contract import (  # noqa: E402
    ensure_freeze_after_update_box,
    generate_freeze_after_update_ai_files,
    inspect_freeze_after_update_box,
)
from kanda_reasoner_app.freeze_after_update.paths import build_paths  # noqa: E402
from kanda_reasoner_app.freeze_after_update.result import FreezeAfterUpdateStatus  # noqa: E402


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def assert_file(path: Path) -> None:
    assert_true(path.is_file(), f"Expected file: {path}")


def assert_dir(path: Path) -> None:
    assert_true(path.is_dir(), f"Expected directory: {path}")


def validate_fresh_project() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_after_update_") as tmp:
        project = Path(tmp) / "sample_project"
        project.mkdir()
        paths = build_paths(project)

        before = inspect_freeze_after_update_box(project)
        assert_true(before.status == FreezeAfterUpdateStatus.INCOMPLETE, before.message)

        created = ensure_freeze_after_update_box(project)
        assert_true(created.ok, created.message)

        assert_dir(paths.box_root)
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

        pack_result = generate_freeze_after_update_ai_files(project)
        assert_true(pack_result.ok, pack_result.message)
        assert_true(pack_result.output_zip is not None, "ZIP path missing")
        assert_true(pack_result.output_instruction is not None, "instruction path missing")
        assert_file(pack_result.output_zip)
        assert_file(pack_result.output_instruction)

        with zipfile.ZipFile(pack_result.output_zip) as zip_file:
            names = set(zip_file.namelist())
        assert_true(
            "project_freeze_after_update/frozen_features_memory/freeze_index.json" in names,
            "ZIP missing freeze_index.json",
        )
        assert_true(
            "project_freeze_after_update/files_to_send_ai/what_to_say_to_ai_freeze_feature.md" in names,
            "ZIP missing instruction markdown",
        )

        after_second = generate_freeze_after_update_ai_files(project)
        assert_true(after_second.ok, after_second.message)
        zips = list(paths.send_root.glob("freeze_feature_ai_send_pack_*.zip"))
        assert_true(len(zips) == 1, "output folder should keep one current ZIP")
        assert_file(paths.what_to_say)


def validate_existing_freeze_entry() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_after_update_entry_") as tmp:
        project = Path(tmp) / "project_with_entry"
        project.mkdir()
        paths = build_paths(project)
        ensure_freeze_after_update_box(project)
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
        result = generate_freeze_after_update_ai_files(project)
        assert_true(result.ok, result.message)
        data = json.loads(paths.freeze_index.read_text(encoding="utf-8"))
        assert_true(len(data.get("freezes", [])) == 1, "expected one freeze entry")
        freeze = data["freezes"][0]
        assert_true(freeze["freeze_id"] == "freeze-sample-feature", "wrong freeze_id")
        assert_true(freeze["protected_paths"] == ["sample_module/"], "protected path missing")
        with zipfile.ZipFile(result.output_zip) as zip_file:  # type: ignore[arg-type]
            names = set(zip_file.namelist())
        assert_true(
            "project_freeze_after_update/frozen_features_memory/entries/freeze-sample-feature.md" in names,
            "ZIP missing freeze entry",
        )


def validate_invalid_inputs() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_after_update_invalid_") as tmp:
        file_root = Path(tmp) / "not_a_dir.py"
        file_root.write_text("print('not a project')\n", encoding="utf-8")
        result = ensure_freeze_after_update_box(file_root)
        assert_true(
            result.status == FreezeAfterUpdateStatus.INVALID_PROJECT_ROOT,
            "file project root should be invalid",
        )

        project = Path(tmp) / "project"
        project.mkdir()
        box_file = project / "project_freeze_after_update"
        box_file.write_text("not a folder\n", encoding="utf-8")
        result = ensure_freeze_after_update_box(project)
        assert_true(
            result.status == FreezeAfterUpdateStatus.INVALID_BOX_PATH,
            "box path file should be invalid",
        )


def validate_no_kanda_contamination() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_after_update_clean_") as tmp:
        project = Path(tmp) / "clean_project"
        project.mkdir()
        result = generate_freeze_after_update_ai_files(project)
        assert_true(result.ok, result.message)
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


def main() -> int:
    tests = [
        validate_fresh_project,
        validate_existing_freeze_entry,
        validate_invalid_inputs,
        validate_no_kanda_contamination,
    ]
    for test in tests:
        print(f"RUN {test.__name__}")
        test()
        print(f"PASS {test.__name__}")
    print("VALIDATION OK - Freeze Feature After Update backend passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
