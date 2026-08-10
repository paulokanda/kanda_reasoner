# project-path: tools/validate_fire_shield_workbench_integration_v1.py
"""Validate Fire Shield coverage of Architecture Workbench mutation paths."""

from __future__ import annotations

import hashlib
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.project_fire_shield as fire_shield_module
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_source_mutation_primitives import (
    SourceMutationOperation,
    apply_source_mutation_operation,
)
from kanda_reasoner_app.project_fire_shield import FireShieldError
from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
from kanda_reasoner_app.project_support_boundary import ProjectSelectionMode

FEATURE_ID = "kanda-reasoner-fire-shield-cross-project-immutability-v1"


def gate(marker: str, condition: bool) -> None:
    """Print one deterministic PASS marker or fail."""
    if not condition:
        raise RuntimeError(marker + ": FAIL")
    print(marker + ": PASS")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _operation(payload: Path, destination: Path, relative: str) -> SourceMutationOperation:
    raw = payload.read_bytes()
    existed = destination.is_file()
    before = _sha256(destination.read_bytes()) if existed else ""
    return SourceMutationOperation(
        schema_version="1.0",
        feature_id="fixture",
        sequence_no=1,
        operation_type="REPLACE_FILE" if existed else "CREATE_FILE",
        relative_path=relative,
        payload_path=str(payload),
        destination_path=str(destination),
        payload_hash=_sha256(raw),
        precondition_hash=before,
        destination_existed=existed,
        byte_size=len(raw),
    )


def _expect_block(marker: str, fragment: str, action) -> None:
    try:
        action()
    except FireShieldError as exc:
        gate(marker, fragment in str(exc))
        return
    raise RuntimeError(marker + ": FAIL - operation unexpectedly allowed")


def _patch_current_registry(tool_root: Path, registry_path: Path) -> None:
    registry_type = ProjectSelectionRegistry

    def current_registry(**_kwargs):
        return registry_type(
            tool_source_root=tool_root,
            registry_path=registry_path,
        )

    fire_shield_module.ProjectSelectionRegistry = current_registry


def _validate_canonical_primitive(base: Path) -> None:
    tool_root = base / "tool" / "kanda_reasoner"
    project_root = base / "project" / "sample_project"
    registry_path = base / "registry" / "projects.json"
    staging = base / "staging"
    (tool_root / "kanda_reasoner_app").mkdir(parents=True)
    project_root.mkdir(parents=True)
    staging.mkdir(parents=True)
    tool_file = tool_root / "kanda_reasoner_app" / "core.py"
    tool_file.write_text("TOOL_VALUE = 1\n", encoding="utf-8")
    destination = project_root / "module.py"
    destination.write_text("VALUE = 1\n", encoding="utf-8")
    payload = staging / "module.py"
    payload.write_text("VALUE = 2\n", encoding="utf-8")

    registry = ProjectSelectionRegistry(
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    registry.register_explicit_selection(
        project_root,
        ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
    )
    _patch_current_registry(tool_root, registry_path)

    operation = _operation(payload, destination, "module.py")
    apply_source_mutation_operation(operation, operation_id="fire-shield-workbench-pass")
    gate(
        "FIRE_SHIELD_WORKBENCH_CANONICAL_PROJECT_WRITE_ALLOWED",
        destination.read_text(encoding="utf-8") == "VALUE = 2\n",
    )

    tool_payload = staging / "tool_target.py"
    tool_payload.write_text("VALUE = 3\n", encoding="utf-8")
    tool_operation = _operation(tool_payload, tool_file, "tool_target.py")
    _expect_block(
        "FIRE_SHIELD_WORKBENCH_TOOL_WRITE_DENIED",
        "FIRE_SHIELD_TOOL_WRITE_BLOCKED",
        lambda: apply_source_mutation_operation(
            tool_operation,
            operation_id="fire-shield-workbench-tool-deny",
        ),
    )

    copied_payload = staging / "copied_tool.py"
    copied_payload.write_bytes(tool_file.read_bytes())
    copied_destination = project_root / "copied_tool.py"
    copied_operation = _operation(
        copied_payload,
        copied_destination,
        "copied_tool.py",
    )
    _expect_block(
        "FIRE_SHIELD_WORKBENCH_TOOL_COPY_DENIED",
        "FIRE_SHIELD_EXACT_TOOL_FILE_COPY_BLOCKED",
        lambda: apply_source_mutation_operation(
            copied_operation,
            operation_id="fire-shield-workbench-copy-deny",
        ),
    )


def _validate_static_coverage(project_root: Path) -> None:
    paths = (
        "guarded_source_apply_executor.py",
        "workbench_source_mutation_primitives.py",
        "workbench_import_rewrite_apply_executor.py",
        "workbench_import_rewrite_rollback_executor.py",
        "workbench_rollback_executor.py",
        "source_apply_rollback_recovery.py",
        "workbench_transaction_rollback.py",
    )
    owner = (
        project_root
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
    )
    for name in paths:
        text = (owner / name).read_text(encoding="utf-8")
        gate(
            "FIRE_SHIELD_WORKBENCH_INTEGRATED_" + name[:-3].upper(),
            "project_fire_shield" in text,
        )


def main() -> int:
    """Run Workbench Fire Shield integration checks."""
    with tempfile.TemporaryDirectory(prefix="kanda_fire_shield_workbench_") as raw:
        _validate_canonical_primitive(Path(raw))
    _validate_static_coverage(PROJECT_ROOT)
    print("VALIDATION OK: " + FEATURE_ID + "-workbench-integration")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
