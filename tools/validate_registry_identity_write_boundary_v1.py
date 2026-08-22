# project-path: tools/validate_registry_identity_write_boundary_v1.py
"""Validate registry identity under the spectator Project-write boundary."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_operation_authority import (  # noqa: E402
    PROJECT_SOURCE_WRITE_UNSUPPORTED_MARKER,
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


def _authority(
    project_root: Path,
    registry_path: Path,
    tool_root: Path,
    kind: ProjectOperationKind,
    *,
    ticket: int,
):
    return build_project_operation_authority(
        project_root,
        operation_kind=kind,
        operation_id="registry-boundary-validation",
        project_epoch=ticket,
        source_snapshot_identity="s7a-registry-boundary",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )


def validate_external_project(temp_root: Path) -> None:
    """External Project is readable/support-writable but never source-writable."""
    tool_root = temp_root / "kanda_reasoner"
    project_root = temp_root / "external_project"
    registry_path = temp_root / "tool_support" / "projects.json"
    tool_root.mkdir(parents=True)
    project_root.mkdir()
    registry = ProjectSelectionRegistry(
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    boundary = registry.register_explicit_selection(
        project_root,
        ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
    )
    resolved = resolve_registered_project_boundary(
        project_root,
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    gate(
        "REGISTRY_STABLE_PROJECT_ID_OBSERVATION",
        resolved.active_project_id == boundary.active_project_id,
    )
    expect_rejection(
        "EXTERNAL_PROJECT_SOURCE_WRITE_DENIED",
        lambda: _authority(
            project_root,
            registry_path,
            tool_root,
            ProjectOperationKind.PROJECT_SOURCE_WRITE,
            ticket=7,
        ),
        PROJECT_SOURCE_WRITE_UNSUPPORTED_MARKER,
    )

    read_authority = _authority(
        project_root,
        registry_path,
        tool_root,
        ProjectOperationKind.PROJECT_SOURCE_READ,
        ticket=7,
    )
    target = project_root / "module.py"
    gate(
        "EXTERNAL_PROJECT_SOURCE_READ_ALLOWED",
        assert_authorized_project_target(read_authority, target)
        == target.resolve(),
    )

    support_authority = _authority(
        project_root,
        registry_path,
        tool_root,
        ProjectOperationKind.PROJECT_SUPPORT_WRITE,
        ticket=7,
    )
    support_target = boundary.active_project_support_root / "evidence.json"
    gate(
        "EXTERNAL_PROJECT_SUPPORT_WRITE_GOVERNED_ALLOWED",
        assert_authorized_project_target(
            support_authority,
            support_target,
        )
        == support_target.resolve(),
    )
    expect_rejection(
        "SUPPORT_AUTHORITY_CANNOT_WRITE_PROJECT_SOURCE",
        lambda: assert_authorized_project_target(
            support_authority,
            project_root / "source.py",
        ),
        "PROJECT_OPERATION_TARGET_OUTSIDE_ALLOWED_ROOT",
    )


def validate_project_switch(temp_root: Path) -> None:
    """A switch invalidates an authority captured for the former observation."""
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
    registry.register_explicit_selection(
        first,
        ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
    )
    authority = _authority(
        first,
        registry_path,
        tool_root,
        ProjectOperationKind.PROJECT_SOURCE_READ,
        ticket=1,
    )
    registry.register_explicit_selection(
        second,
        ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
    )
    expect_rejection(
        "PROJECT_SWITCH_INVALIDATES_OLD_OBSERVATION",
        lambda: assert_project_authority_current(
            authority,
            selected_project_root=first,
            project_epoch=1,
            tool_source_root=tool_root,
            registry_path=registry_path,
        ),
        "PROJECT_OPERATION_CONTEXT_ROOT_MISMATCH",
    )


def validate_self_hosting(temp_root: Path) -> None:
    """Same-root self-hosting preserves roles and never grants Project writes."""
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
    gate("EXPLICIT_SELF_HOSTING_ROLE_OBSERVED", boundary.self_hosting_mode)
    expect_rejection(
        "SELF_HOSTING_PROJECT_SOURCE_WRITE_DENIED",
        lambda: _authority(
            tool_root,
            registry_path,
            tool_root,
            ProjectOperationKind.PROJECT_SOURCE_WRITE,
            ticket=3,
        ),
        PROJECT_SOURCE_WRITE_UNSUPPORTED_MARKER,
    )

    read_authority = _authority(
        tool_root,
        registry_path,
        tool_root,
        ProjectOperationKind.PROJECT_SOURCE_READ,
        ticket=3,
    )
    source_target = tool_root / "kanda_reasoner_app" / "module.py"
    gate(
        "SELF_HOSTING_PROJECT_SOURCE_READ_ALLOWED",
        assert_authorized_project_target(read_authority, source_target)
        == source_target.resolve(),
    )

    support_authority = _authority(
        tool_root,
        registry_path,
        tool_root,
        ProjectOperationKind.PROJECT_SUPPORT_WRITE,
        ticket=3,
    )
    support_target = boundary.active_project_support_root / "memory.json"
    gate(
        "SELF_HOSTING_PROJECT_SUPPORT_WRITE_GOVERNED_ALLOWED",
        assert_authorized_project_target(
            support_authority,
            support_target,
        )
        == support_target.resolve(),
    )


def validate_source_contract(project_root: Path) -> None:
    """Prove the frozen S4 source-write denial remains the canonical owner."""
    source = (
        project_root
        / "kanda_reasoner_app"
        / "project_operation_authority.py"
    ).read_text(encoding="utf-8")
    gate(
        "CENTRAL_PROJECT_SOURCE_WRITE_DENIAL_PRESENT",
        "PROJECT_SOURCE_WRITE_UNSUPPORTED:SPECTATOR_ONLY" in source,
    )
    gate(
        "CENTRAL_SELF_HOSTING_PROJECT_WRITE_CARVEOUT_ABSENT",
        ("EXPLICIT_SELF_HOSTING_" + "PROJECT_WRITE_ACCEPTED") not in source,
    )
    print("PROJECT_SELECTION_WRITE_AUTHORITY: ABSENT")
    print("REGISTRY_WRITE_BOUNDARY_SPECTATOR_SEMANTICS: PASS")


def run_regression(project_root: Path) -> None:
    """Preserve explicit Tool/Project identity and self-host role separation."""
    relative = "tools/validate_tool_project_boundary_identity_explicit_selection_v1.py"
    completed = subprocess.run(
        [sys.executable, str(project_root / relative)],
        cwd=str(project_root),
        text=True,
        capture_output=True,
        check=False,
    )
    marker = "VALIDATION OK: tool-project-boundary-identity-explicit-selection-v1"
    if completed.returncode != 0 or marker not in completed.stdout:
        raise AssertionError(completed.stdout + completed.stderr)
    print("REGRESSION_VALIDATE_TOOL_PROJECT_BOUNDARY_IDENTITY: PASS")


def main() -> int:
    """Run external, switch, self-hosting, and source-contract gates."""
    with tempfile.TemporaryDirectory(prefix="kanda_registry_boundary_") as raw:
        root = Path(raw)
        validate_external_project(root / "external")
        validate_project_switch(root / "switch")
        validate_self_hosting(root / "self_hosting")
    validate_source_contract(PROJECT_ROOT)
    run_regression(PROJECT_ROOT)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
