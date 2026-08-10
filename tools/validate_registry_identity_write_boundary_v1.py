# project-path: tools/validate_registry_identity_write_boundary_v1.py
"""Validate registry-backed identity and cross-root Project write authority."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.memory_ownership.context import (  # noqa: E402
    project_owner_context,
)
from kanda_reasoner_app.project_operation_authority import (  # noqa: E402
    ProjectOperationAuthorityError,
    ProjectOperationKind,
    assert_authorized_project_target,
    assert_project_authority_current,
    build_project_operation_authority,
    resolve_registered_project_boundary,
)
from kanda_reasoner_app.project_selection_registry import (  # noqa: E402
    ProjectSelectionRegistry,
)
from kanda_reasoner_app.project_support_boundary import (  # noqa: E402
    ProjectSelectionMode,
)

FEATURE_ID = "registry-identity-write-boundary-v1"


def bind_fixture_registry(registry_path: Path, tool_root: Path) -> None:
    """Bind authority resolution to one isolated registry in this process."""
    from kanda_reasoner_app import project_operation_authority as authority_module

    registry_type = ProjectSelectionRegistry
    authority_module.ProjectSelectionRegistry = lambda **kwargs: registry_type(
        tool_source_root=tool_root, registry_path=registry_path
    )

TOUCHED_SOURCE = (
    "kanda_reasoner_app/project_selection_registry.py",
    "kanda_reasoner_app/project_operation_authority.py",
    "kanda_reasoner_app/memory_ownership/context.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_boundary_context.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_bridge.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_write_broker.py",
)


def gate(marker: str, condition: bool) -> None:
    """Print one marker or fail the focused release validation."""
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def expect_rejection(marker: str, callback, expected: str) -> None:
    """Require one fail-closed authority rejection."""
    try:
        callback()
    except ProjectOperationAuthorityError as exc:
        gate(marker, expected in str(exc))
        return
    raise AssertionError(marker + ": expected rejection")


def validate_external_project(temp_root: Path) -> None:
    """Validate one external Project cannot borrow Tool write authority."""
    tool_root = temp_root / "kanda_reasoner"
    project_root = temp_root / "eeg_kanda"
    registry_path = temp_root / "tool_support" / "projects.json"
    tool_root.mkdir(parents=True)
    project_root.mkdir()
    registry = ProjectSelectionRegistry(
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    boundary = registry.register_explicit_root(project_root)
    bind_fixture_registry(registry_path, tool_root)
    resolved = resolve_registered_project_boundary(
        project_root,
        tool_source_root=tool_root,
    )
    gate(
        "REGISTRY_STABLE_PROJECT_ID_AUTHORITY",
        resolved.active_project_id == boundary.active_project_id,
    )
    authority = build_project_operation_authority(
        project_root,
        operation_kind=ProjectOperationKind.PROJECT_SOURCE_WRITE,
        operation_id="external-project-operation",
        project_epoch=7,
        source_snapshot_identity="snapshot-external",
        tool_source_root=tool_root,
    )
    target = project_root / "module.py"
    gate(
        "EXTERNAL_PROJECT_SOURCE_TARGET_ACCEPTED",
        assert_authorized_project_target(authority, target) == target.resolve(),
    )
    expect_rejection(
        "EXTERNAL_PROJECT_TOOL_SOURCE_WRITE_REJECTED",
        lambda: assert_authorized_project_target(
            authority, tool_root / "kanda_reasoner_app" / "module.py"
        ),
        "PROJECT_OPERATION_TARGET_OUTSIDE_ALLOWED_ROOT",
    )
    expect_rejection(
        "EXTERNAL_PROJECT_SUPPORT_AS_SOURCE_REJECTED",
        lambda: assert_authorized_project_target(
            authority, boundary.active_project_support_root / "evidence.json"
        ),
        "PROJECT_OPERATION_TARGET_OUTSIDE_ALLOWED_ROOT",
    )
    assert_project_authority_current(
        authority,
        selected_project_root=project_root,
        project_epoch=7,
        tool_source_root=tool_root,
    )
    expect_rejection(
        "STALE_PROJECT_EPOCH_REJECTED",
        lambda: assert_project_authority_current(
            authority,
            selected_project_root=project_root,
            project_epoch=8,
            tool_source_root=tool_root,
        ),
        "PROJECT_AUTHORITY_EPOCH_STALE",
    )
    owner = project_owner_context(
        project_root,
        tool_source_root=tool_root,
    )
    gate(
        "DURABLE_MEMORY_USES_REGISTRY_PROJECT_ID",
        owner.owner_id == boundary.active_project_id,
    )


def validate_project_switch(temp_root: Path) -> None:
    """Validate a registered Project switch invalidates old authority."""
    tool_root = temp_root / "tool"
    first = temp_root / "first_project"
    second = temp_root / "second_project"
    registry_path = temp_root / "support" / "projects.json"
    for path in (tool_root, first, second):
        path.mkdir(parents=True)
    registry = ProjectSelectionRegistry(
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    registry.register_explicit_root(first)
    bind_fixture_registry(registry_path, tool_root)
    authority = build_project_operation_authority(
        first,
        operation_kind=ProjectOperationKind.PROJECT_SOURCE_WRITE,
        operation_id="switch-operation",
        project_epoch=1,
        tool_source_root=tool_root,
    )
    registry.register_explicit_root(second)
    expect_rejection(
        "PROJECT_SWITCH_INVALIDATES_OLD_AUTHORITY",
        lambda: assert_project_authority_current(
            authority,
            selected_project_root=first,
            project_epoch=1,
            tool_source_root=tool_root,
        ),
        "ACTIVE_PROJECT_SELECTION_ROOT_MISMATCH",
    )


def validate_self_hosting(temp_root: Path) -> None:
    """Validate KANDA can modify itself only through explicit Project role."""
    tool_root = temp_root / "kanda_reasoner"
    registry_path = temp_root / "tool_support" / "projects.json"
    tool_root.mkdir(parents=True)
    registry = ProjectSelectionRegistry(
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    boundary = registry.register_explicit_selection(
        tool_root,
        ProjectSelectionMode.EXPLICIT_SELF_HOSTING,
    )
    bind_fixture_registry(registry_path, tool_root)
    authority = build_project_operation_authority(
        tool_root,
        operation_kind=ProjectOperationKind.PROJECT_SOURCE_WRITE,
        operation_id="self-hosted-project-operation",
        project_epoch=3,
        tool_source_root=tool_root,
    )
    gate(
        "EXPLICIT_SELF_HOSTING_PROJECT_WRITE_ACCEPTED",
        boundary.self_hosting_mode
        and assert_authorized_project_target(
            authority, tool_root / "kanda_reasoner_app" / "module.py"
        ).is_absolute(),
    )
    expect_rejection(
        "SELF_HOSTING_SUPPORT_ROOT_AS_SOURCE_REJECTED",
        lambda: assert_authorized_project_target(
            authority, boundary.active_project_support_root / "memory.json"
        ),
        "PROJECT_OPERATION_TARGET_OUTSIDE_ALLOWED_ROOT",
    )


def validate_source_contract(project_root: Path) -> None:
    """Validate source ownership, compatibility limits, and module sizes."""
    authority_source = (
        project_root / "kanda_reasoner_app" / "project_operation_authority.py"
    ).read_text(encoding="utf-8")
    memory_source = (
        project_root / "kanda_reasoner_app" / "memory_ownership" / "context.py"
    ).read_text(encoding="utf-8")
    broker_source = (
        project_root
        / "kanda_reasoner_app"
        / "reasoner_engine"
        / "project_web_ai_write_broker.py"
    ).read_text(encoding="utf-8")
    gate(
        "GLOBAL_REGISTRY_AUTHORITY_MODULE_PRESENT",
        "resolve_registered_project_boundary" in authority_source,
    )
    gate(
        "MEMORY_COMPATIBILITY_IDENTITY_REMOVED",
        "resolve_project_tool_boundary_identity" not in memory_source,
    )
    gate(
        "WRITE_BROKER_COMPATIBILITY_IDENTITY_REMOVED",
        "resolve_project_tool_boundary_identity" not in broker_source,
    )
    for relative in TOUCHED_SOURCE:
        path = project_root / relative
        lines = len(path.read_text(encoding="utf-8").splitlines())
        gate(
            "MODULE_SIZE_" + path.name.upper().replace(".", "_"),
            100 < lines < 500,
        )
    print("TOUCHED_SOURCE_MODULES_STRICTLY_101_TO_499: PASS")


def run_regression(project_root: Path, relative: str, marker: str) -> None:
    """Run one existing focused regression validator."""
    completed = subprocess.run(
        [sys.executable, str(project_root / relative)],
        cwd=str(project_root),
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0 or marker not in completed.stdout:
        raise AssertionError(completed.stdout + completed.stderr)
    print("REGRESSION_" + Path(relative).stem.upper() + ": PASS")


def main() -> int:
    """Run registry, cross-root, self-hosting, and regression gates."""
    with tempfile.TemporaryDirectory(prefix="kanda_registry_boundary_") as raw:
        root = Path(raw)
        validate_external_project(root / "external")
        validate_project_switch(root / "switch")
        validate_self_hosting(root / "self_hosting")
    validate_source_contract(PROJECT_ROOT)
    run_regression(
        PROJECT_ROOT,
        "tools/validate_tool_project_boundary_identity_explicit_selection_v1.py",
        "VALIDATION OK: tool-project-boundary-identity-explicit-selection-v1",
    )
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
