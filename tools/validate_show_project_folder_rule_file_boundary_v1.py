# project-path: tools/validate_show_project_folder_rule_file_boundary_v1.py
"""Validate folder-rule/file-basename separation for Show Project to AI."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_exclusion_policy import (
    iter_reasoner_project_files,
    should_exclude_reasoner_project_path,
)
from kanda_reasoner_app.reasoner_context_bundle.exclusion_engine import (
    decide_path_exclusion,
)
from kanda_reasoner_app.reasoner_context_bundle.schema_models import ExclusionRules

FEATURE_ID = "show-project-ai-folder-rule-file-boundary-v1"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_validation() -> None:
    rules_dict = {"folders": ["*backup*"], "files": [], "extensions": []}
    bundle_rules = ExclusionRules(
        folders=("*backup*",),
        files=(),
        extensions=(),
        source="focused-validator",
    )

    with tempfile.TemporaryDirectory(prefix="kanda_show_project_exclusion_") as tmp:
        root = Path(tmp).resolve()
        legitimate = root / "source_apply_preflight_backup_contract.py"
        legitimate.write_text("VALUE = 1\n", encoding="utf-8")
        second_legitimate = root / "workbench_preflight_backup_readiness.py"
        second_legitimate.write_text("VALUE = 2\n", encoding="utf-8")
        ordinary = root / "ordinary.py"
        ordinary.write_text("VALUE = 3\n", encoding="utf-8")

        excluded_folder = root / "my_backup_area"
        excluded_folder.mkdir()
        excluded_child = excluded_folder / "normal.py"
        excluded_child.write_text("VALUE = 4\n", encoding="utf-8")

        nested = root / "pkg"
        nested.mkdir()
        nested_legitimate = nested / "backup_contract_runtime.py"
        nested_legitimate.write_text("VALUE = 5\n", encoding="utf-8")

        _assert(
            not should_exclude_reasoner_project_path(legitimate, root, rules_dict),
            "Folder rule incorrectly excluded a legitimate file basename.",
        )
        _assert(
            not should_exclude_reasoner_project_path(second_legitimate, root, rules_dict),
            "Folder rule incorrectly excluded another legitimate backup-named file.",
        )
        _assert(
            not should_exclude_reasoner_project_path(nested_legitimate, root, rules_dict),
            "Folder rule incorrectly excluded a nested legitimate file basename.",
        )
        print("FOLDER_RULE_DOES_NOT_MATCH_FILE_BASENAME: PASS")

        _assert(
            should_exclude_reasoner_project_path(excluded_folder, root, rules_dict),
            "Wildcard folder rule no longer excludes a matching folder.",
        )
        _assert(
            should_exclude_reasoner_project_path(excluded_child, root, rules_dict),
            "File inside an excluded folder was not excluded.",
        )
        print("MATCHING_BACKUP_FOLDER_STILL_EXCLUDED: PASS")
        print("FILES_INSIDE_EXCLUDED_FOLDER_STILL_EXCLUDED: PASS")

        included = {
            path.relative_to(root).as_posix()
            for path in iter_reasoner_project_files(root, suffixes=(".py",), rules=rules_dict)
        }
        _assert(legitimate.name in included, "Legitimate backup-named source missing from iteration.")
        _assert(second_legitimate.name in included, "Second legitimate source missing from iteration.")
        _assert("pkg/backup_contract_runtime.py" in included, "Nested legitimate source missing.")
        _assert("my_backup_area/normal.py" not in included, "Excluded folder leaked into iteration.")
        print("SOURCE_ARCHIVE_ITERATION_PRESERVES_LEGITIMATE_BACKUP_NAMED_FILES: PASS")

        file_decision = decide_path_exclusion(legitimate, root, bundle_rules)
        folder_decision = decide_path_exclusion(excluded_child, root, bundle_rules)
        _assert(not file_decision.excluded, "Bundle exclusion engine excluded legitimate source file.")
        _assert(folder_decision.excluded, "Bundle exclusion engine failed to exclude folder child.")
        _assert(folder_decision.rule_type == "folder", "Bundle rule reporting lost folder ownership.")
        _assert(folder_decision.matched_rule == "*backup*", "Bundle reported wrong matched rule.")
        print("SHOW_PROJECT_BUNDLE_DECISION_ALIGNED: PASS")

    policy = Path("kanda_reasoner_app/project_exclusion_policy.py")
    helper = Path("kanda_reasoner_app/project_exclusion_path_matching.py")
    engine = Path("kanda_reasoner_app/reasoner_context_bundle/exclusion_engine.py")
    for path in (policy, helper, engine):
        _assert(path.is_file(), f"Missing required source file: {path}")
        _assert(len(path.read_text(encoding="utf-8").splitlines()) <= 500, f"Module too large: {path}")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")

    helper_text = helper.read_text(encoding="utf-8")
    _assert("folder_parts = parts if path_is_dir else parts[:-1]" in helper_text, "Missing basename boundary.")
    print("FOLDER_FILE_BOUNDARY_STATIC_GUARD: PASS")
    print("STATUS: IN_SYNC")
    print(f"VALIDATION OK: {FEATURE_ID}")


if __name__ == "__main__":
    run_validation()
