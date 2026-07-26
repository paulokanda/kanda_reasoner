# project-path: tools/validate_project_tool_boundary_nested_support_root_v1.py
"""Validate the canonical external Project support-root hard gate."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import tempfile
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_support_boundary import (
    ProjectSupportBoundaryError,
    assert_no_forbidden_nested_support_root,
    canonical_project_support_root,
    canonical_transient_garbage_root,
    forbidden_nested_support_root,
    project_support_root_blockers,
)
from tools.repair_forbidden_nested_project_support_root_v1 import (
    migrate_nested_support_tree,
    remove_legacy_source_validation_fixture,
)

FEATURE_ID = "project-tool-boundary-nested-support-root-canon-startup-guard-v1r3"
APPROVED_DIRECT_CONSTRUCTORS = {
    "kanda_reasoner_app/_project_analysis_evidence_path_resolution.py",
    "kanda_reasoner_app/project_support_boundary.py",
    "kanda_prompt_workspace/prompt_tools/startup_freeze_context.py",
    "kanda_prompt_workspace/prompt_tools/startup_kernel/core_helpers.py",
}


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def _contains_suffix(node: ast.AST) -> bool:
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            if "_show_project_to_AI" in child.value:
                return True
    return False


def _scan_direct_constructors() -> list[str]:
    failures: list[str] = []
    roots = (
        PROJECT_ROOT / "kanda_reasoner_app",
        PROJECT_ROOT / "kanda_prompt_workspace/prompt_tools",
    )
    for source_root in roots:
        for path in sorted(source_root.rglob("*.py")):
            relative = path.relative_to(PROJECT_ROOT).as_posix()
            if relative in APPROVED_DIRECT_CONSTRUCTORS:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8", errors="strict"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.BinOp) or not isinstance(node.op, ast.Div):
                    continue
                if _contains_suffix(node.right):
                    failures.append(relative + ":" + str(node.lineno))
    return failures


def _expected_external_root(project: Path, suffix: str) -> Path:
    """Mirror the canon without creating the returned drive-root path."""
    normalized = project.expanduser().resolve(strict=False)
    base = Path(normalized.anchor) if normalized.drive else normalized.parent
    return (base / (normalized.name + suffix)).resolve(strict=False)


def _validate_runtime_boundary() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_boundary_") as temp:
        base = Path(temp)
        project = base / "sample_project"
        project.mkdir()
        canonical = canonical_project_support_root(project)
        expected_canonical = _expected_external_root(
            project,
            "_show_project_to_AI",
        )
        expected_transient = _expected_external_root(
            project,
            "_delete_after_daily_work",
        )
        forbidden = project / "sample_project_show_project_to_AI"
        _require(
            canonical == expected_canonical,
            "CANONICAL_SUPPORT_ROOT_IS_EXTERNAL_DRIVE_ROOT",
        )
        _require(
            canonical_transient_garbage_root(project) == expected_transient,
            "TRANSIENT_GARBAGE_ROOT_IS_EXTERNAL_DRIVE_ROOT",
        )
        _require(
            forbidden_nested_support_root(project) == forbidden,
            "FORBIDDEN_NESTED_SUPPORT_ROOT_IDENTIFIED",
        )
        _require(
            project_support_root_blockers(project, forbidden)
            == (
                "PROJECT_SUPPORT_ROOT_INSIDE_PROJECT_SOURCE",
                "PROJECT_SUPPORT_ROOT_NOT_CANONICAL_EXTERNAL_ROOT",
            ),
            "NESTED_SUPPORT_ROOT_BLOCKERS_COMPLETE",
        )
        forbidden.mkdir()
        legacy_fixture = project / "_release9_exchange_validation_fixture"
        legacy_fixture.mkdir()
        (legacy_fixture / "fixture.txt").write_text(
            "temporary\n", encoding="utf-8"
        )
        (forbidden / "second_prompt_files").mkdir()
        (forbidden / "second_prompt_files" / "sample.txt").write_text(
            "same\n", encoding="utf-8"
        )
        try:
            assert_no_forbidden_nested_support_root(project)
        except ProjectSupportBoundaryError:
            pass
        else:
            raise AssertionError("NESTED_SUPPORT_ROOT_RUNTIME_GATE")
        _require(True, "NESTED_SUPPORT_ROOT_RUNTIME_GATE")

        canonical_existed_before = canonical.exists()
        if not project.drive:
            canonical.mkdir(parents=True, exist_ok=True)
            canonical_existed_before = True

        isolated_canonical = base / "isolated_support_target"
        moved = migrate_nested_support_tree(forbidden, isolated_canonical)
        fixture_removed = remove_legacy_source_validation_fixture(project)
        _require(
            canonical.exists() == canonical_existed_before,
            "VALIDATION_DOES_NOT_CREATE_DRIVE_ROOT_SUPPORT_FIXTURE",
        )
        _require(moved == 1, "REPAIR_MIGRATES_UNIQUE_CONTENT")
        _require(not forbidden.exists(), "REPAIR_REMOVES_FORBIDDEN_NESTED_ROOT")
        _require(fixture_removed, "REPAIR_REMOVES_SOURCE_ROOT_VALIDATION_FIXTURE")
        _require(not legacy_fixture.exists(), "SOURCE_ROOT_VALIDATION_FIXTURE_ABSENT")
        _require(
            (isolated_canonical / "second_prompt_files" / "sample.txt").is_file(),
            "REPAIR_PRESERVES_SUPPORT_CONTENT",
        )
        assert_no_forbidden_nested_support_root(project)


def _validate_release9_fixture_ownership() -> None:
    path = PROJECT_ROOT / "tools/validate_external_ai_candidate_exchange_outbound_v1.py"
    source = path.read_text(encoding="utf-8", errors="strict")
    _require(
        "canonical_transient_garbage_root" in source,
        "RELEASE9_FIXTURE_USES_TRANSIENT_GARBAGE_ROOT",
    )
    _require(
        "_release9_exchange_validation_fixture" not in source,
        "RELEASE9_SOURCE_ROOT_FIXTURE_NAME_REMOVED",
    )
    _require(
        "patch.object" in source and "project_support_root" in source,
        "RELEASE9_VALIDATION_SUPPORT_ISOLATED",
    )
    _require(
        "PROJECT_ROOT = Path(__file__).resolve().parents[1]" in source,
        "RELEASE9_VALIDATOR_PROJECT_IMPORT_BOOTSTRAP",
    )
    fixture = canonical_transient_garbage_root(PROJECT_ROOT) / "validation_fixtures"
    try:
        fixture.resolve(strict=False).relative_to(PROJECT_ROOT.resolve(strict=False))
    except ValueError:
        pass
    else:
        raise AssertionError("RELEASE9_FIXTURE_OUTSIDE_PROJECT_SOURCE")
    _require(True, "RELEASE9_FIXTURE_OUTSIDE_PROJECT_SOURCE")




def _validate_workbench_path_owner_alignment() -> None:
    """Require Workbench production and validation paths to use canon."""
    support_paths = (
        PROJECT_ROOT
        / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
        / "workbench_project_support_paths.py"
    )
    support_source = support_paths.read_text(encoding="utf-8", errors="strict")
    _require(
        "canonical_transient_garbage_root" in support_source,
        "WORKBENCH_DAILY_ROOT_USES_SHARED_CANON",
    )
    _require(
        "return canonical_transient_garbage_root(active_project_root)"
        in support_source,
        "WORKBENCH_DAILY_ROOT_DIRECT_PARENT_DERIVATION_REMOVED",
    )

    validator = (
        PROJECT_ROOT
        / "tools/validate_large_file_refactor_workbench_project_support_boundary_v3.py"
    )
    validator_source = validator.read_text(encoding="utf-8", errors="strict")
    _require(
        "isolated_workbench_paths" in validator_source,
        "WORKBENCH_BOUNDARY_VALIDATION_SUPPORT_ISOLATED",
    )
    _require(
        'assert support_root == sandbox / "other_project_show_project_to_AI"'
        not in validator_source,
        "WORKBENCH_TEMP_SIBLING_SUPPORT_ASSUMPTION_REMOVED",
    )
    _require(
        "WORKBENCH_DRIVE_ROOT_FIXTURE_STATE_UNCHANGED" in validator_source,
        "WORKBENCH_DRIVE_ROOT_FIXTURE_REGRESSION_GATED",
    )


def _validate_patch5_projection_fixture_ownership() -> None:
    """Require Patch 5 proof validation to isolate synthetic support state."""
    validator = (
        PROJECT_ROOT
        / "tools/validate_workbench_patch5_executor_proof_status_projection_v1.py"
    )
    source = validator.read_text(encoding="utf-8", errors="strict")
    _require(
        "patch.object" in source
        and "assert_no_forbidden_nested_support_root" in source,
        "PATCH5_PROOF_VALIDATION_SUPPORT_OVERRIDE_SCOPED",
    )
    _require(
        "project_root.parent" not in source,
        "PATCH5_PROOF_TEMP_SIBLING_SUPPORT_ASSUMPTION_REMOVED",
    )
    _require(
        "PATCH5_VALIDATION_DRIVE_ROOT_FIXTURE_STATE_UNCHANGED" in source,
        "PATCH5_PROOF_DRIVE_ROOT_FIXTURE_REGRESSION_GATED",
    )


def _validate_startup_registration() -> None:
    source_map_path = (
        PROJECT_ROOT
        / "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
    )
    source_map = json.loads(source_map_path.read_text(encoding="utf-8"))
    entries = source_map["startup_sources"]
    matches = [
        item for item in entries
        if item.get("prompt_id") == "project_tool_boundary_startup_bridge"
    ]
    _require(len(matches) == 1, "BOUNDARY_CANON_STARTUP_SOURCE_UNIQUE")
    entry = matches[0]
    _require(entry.get("load_mode") == "always_startup", "BOUNDARY_CANON_ALWAYS_STARTUP")
    _require(
        entry.get("generated_filename") == "14_project_tool_boundary_canon.md",
        "BOUNDARY_CANON_STARTUP_FILENAME_STABLE",
    )
    metadata = json.loads(
        (
            PROJECT_ROOT
            / "kanda_prompt_workspace/prompt_library/METADATA/project_tool_boundary_startup_bridge.meta.json"
        ).read_text(encoding="utf-8")
    )
    _require(metadata.get("load_type") == "always_startup", "BOUNDARY_METADATA_ALWAYS_STARTUP")
    version_parts = tuple(int(part) for part in str(metadata.get("version", "")).split("."))
    _require(version_parts >= (1, 0), "BOUNDARY_BRIDGE_METADATA_VERSION_1_0")


def main() -> int:
    """Run focused source, runtime, migration, and startup checks."""
    failures = _scan_direct_constructors()
    _require(not failures, "PRODUCTION_DIRECT_SUPPORT_ROOT_CONSTRUCTORS_BLOCKED")
    _validate_runtime_boundary()
    _validate_release9_fixture_ownership()
    _validate_workbench_path_owner_alignment()
    _validate_patch5_projection_fixture_ownership()
    _validate_startup_registration()
    print("WINDOWS_DRIVE_ROOT_VALIDATION_FIXTURE_REGRESSION_BLOCKED: PASS")
    print("WORKBENCH_BOUNDARY_VALIDATOR_REGRESSION_BLOCKED: PASS")
    print("PATCH5_PROOF_VALIDATOR_REGRESSION_BLOCKED: PASS")
    print("FORBIDDEN_NESTED_PROJECT_SUPPORT_ROOT_CANON: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
