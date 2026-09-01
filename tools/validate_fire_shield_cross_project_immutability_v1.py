# project-path: tools/validate_fire_shield_cross_project_immutability_v1.py
"""Validate legacy cross-project invariants under spectator-boundary Fire Shield."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable

from fire_shield_validation_fixtures import (
    fire_shield_raw_backslash_zip,
    fire_shield_zip,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_fire_shield import (  # noqa: E402
    FIRE_SHIELD_FEATURE_ID,
    FIRE_SHIELD_PROJECT_SOURCE_MUTATION_UNSUPPORTED_MARKER,
    FireShieldError,
    FireShieldMode,
    FireShieldPhase,
    assert_fire_shield_payload_bytes_allowed,
    assert_fire_shield_write_allowed,
    build_fire_shield_context,
    preflight_fire_shield_archive,
    scan_project_python_source,
    verify_project_import_isolation,
    verify_tool_snapshot_unchanged,
)
from kanda_reasoner_app.project_selection_registry import (  # noqa: E402
    ProjectSelectionRegistry,
)
from kanda_reasoner_app.project_support_boundary import (  # noqa: E402
    ProjectSelectionMode,
)

VALIDATOR_CONTRACT_ID = (
    "kanda-reasoner-fire-shield-cross-project-immutability-v1"
)
CURRENT_FIRE_SHIELD_FEATURE_ID = (
    "kanda-reasoner-fire-shield-spectator-boundary-v2"
)


def gate(name: str, condition: bool) -> None:
    """Print one stable PASS marker or fail immediately."""
    if not condition:
        raise RuntimeError(name + ": FAIL")
    print(name + ": PASS")


def expect_block(
    name: str,
    marker: str,
    action: Callable[[], object],
) -> None:
    """Require one Fire Shield action to fail with the expected marker."""
    expect_block_any(name, (marker,), action)


def expect_block_any(
    name: str,
    markers: tuple[str, ...],
    action: Callable[[], object],
) -> None:
    """Require one Fire Shield action to fail with one accepted marker."""
    try:
        action()
    except FireShieldError as exc:
        gate(name, any(marker in str(exc) for marker in markers))
        return
    raise RuntimeError(name + ": FAIL - operation unexpectedly allowed")


def write(path: Path, text: str) -> None:
    """Write one UTF-8 test fixture."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_layout(base: Path) -> tuple[Path, Path, Path]:
    """Create isolated Tool, external Project, and registry roots."""
    tool_root = base / "tool" / "kanda_reasoner"
    project_root = base / "project" / "sample_project"
    registry_path = base / "registry" / "projects.json"
    write(
        tool_root / "kanda_reasoner_app" / "tool_core.py",
        "TOOL_SENTINEL = 'tool-core'\n",
    )
    write(
        tool_root / "kanda_reasoner_app" / "private_api.py",
        "PRIVATE = True\n",
    )
    write(project_root / "src" / "app.py", "VALUE = 'project'\n")
    return tool_root, project_root, registry_path


def select_external(
    tool_root: Path,
    project_root: Path,
    registry_path: Path,
) -> None:
    """Register one explicit external Project selection."""
    registry = ProjectSelectionRegistry(
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    registry.register_explicit_selection(
        project_root,
        ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
    )


def select_self_hosted(
    tool_root: Path,
    registry_path: Path,
) -> None:
    """Register the Tool root as explicit self-hosting."""
    registry = ProjectSelectionRegistry(
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    registry.register_explicit_selection(
        tool_root,
        ProjectSelectionMode.EXPLICIT_SELF_HOSTING,
    )


def create_link_or_junction(link_path: Path, target: Path) -> bool:
    """Create a real link escape when the local platform permits it."""
    try:
        link_path.symlink_to(target, target_is_directory=True)
        return True
    except OSError:
        pass
    if os.name != "nt":
        return False
    result = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link_path), str(target)],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and link_path.exists()


def run_external_matrix(base: Path) -> None:
    """Exercise current external-Project spectator allow and deny cases."""
    tool_root, project_root, registry_path = make_layout(base)
    select_external(tool_root, project_root, registry_path)

    gate(
        "FIRE_SHIELD_FEATURE_ID_STABLE",
        FIRE_SHIELD_FEATURE_ID == CURRENT_FIRE_SHIELD_FEATURE_ID,
    )
    gate(
        "FIRE_SHIELD_SOURCE_MUTATION_MARKER_STABLE",
        FIRE_SHIELD_PROJECT_SOURCE_MUTATION_UNSUPPORTED_MARKER
        == "FIRE_SHIELD_PROJECT_SOURCE_MUTATION_UNSUPPORTED:SPECTATOR_ONLY",
    )

    expect_block(
        "FIRE_SHIELD_EXTERNAL_PROJECT_SOURCE_MUTATION_DENIED",
        FIRE_SHIELD_PROJECT_SOURCE_MUTATION_UNSUPPORTED_MARKER,
        lambda: build_fire_shield_context(
            project_root,
            phase=FireShieldPhase.PROJECT_SOURCE_MUTATION,
            operation_id="validator-external-source",
            tool_source_root=tool_root,
            registry_path=registry_path,
        ),
    )

    read_only = build_fire_shield_context(
        project_root,
        phase=FireShieldPhase.VALIDATE_READ_ONLY,
        operation_id="validator-external-read-only",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    gate(
        "FIRE_SHIELD_MODE_EXTERNAL_PROJECT",
        read_only.mode is FireShieldMode.EXTERNAL_PROJECT,
    )
    gate(
        "FIRE_SHIELD_PROJECT_IDENTITY_VERIFIED",
        read_only.boundary.active_project_root == project_root.resolve(),
    )
    gate(
        "FIRE_SHIELD_TOOL_IDENTITY_VERIFIED",
        read_only.boundary.tool_source_root == tool_root.resolve(),
    )
    gate(
        "FIRE_SHIELD_EXTERNAL_READ_ONLY_WRITES_DISABLED",
        not read_only.writes_allowed,
    )
    expect_block(
        "FIRE_SHIELD_EXTERNAL_PROJECT_SOURCE_WRITE_DENIED",
        "FIRE_SHIELD_READ_ONLY_PHASE",
        lambda: assert_fire_shield_write_allowed(
            read_only,
            project_root / "src" / "new_module.py",
            operation="CREATE",
        ),
    )
    expect_block(
        "FIRE_SHIELD_EXTERNAL_TOOL_WRITE_DENIED",
        "FIRE_SHIELD_READ_ONLY_PHASE",
        lambda: assert_fire_shield_write_allowed(
            read_only,
            tool_root / "kanda_reasoner_app" / "tool_core.py",
            operation="REPLACE",
        ),
    )

    scan_project_python_source(
        read_only,
        b"from pathlib import Path\nVALUE = Path('.')\n",
        "src/safe.py",
    )
    gate("FIRE_SHIELD_SAFE_PROJECT_IMPORTS_ALLOWED", True)
    expect_block(
        "FIRE_SHIELD_PRIVATE_TOOL_IMPORT_DENIED",
        "FIRE_SHIELD_PROJECT_TOOL_PRIVATE_IMPORT_BLOCKED",
        lambda: scan_project_python_source(
            read_only,
            b"from kanda_reasoner_app import project_selection_registry\n",
            "src/bad_import.py",
        ),
    )
    expect_block(
        "FIRE_SHIELD_TOOL_ROOT_REFERENCE_DENIED",
        "FIRE_SHIELD_PROJECT_TOOL_PATH_LEAK_BLOCKED",
        lambda: scan_project_python_source(
            read_only,
            ("TOOL = " + repr(str(tool_root)) + "\n").encode("utf-8"),
            "src/tool_path.py",
        ),
    )
    verify_project_import_isolation(
        read_only,
        [str(project_root), str(project_root / "src")],
    )
    gate("FIRE_SHIELD_PROJECT_IMPORT_ISOLATION_ALLOWED", True)
    expect_block(
        "FIRE_SHIELD_TOOL_ROOT_SYS_PATH_DENIED",
        "FIRE_SHIELD_PROJECT_TOOL_PATH_LEAK_BLOCKED",
        lambda: verify_project_import_isolation(
            read_only,
            [str(project_root), str(tool_root)],
        ),
    )

    transient = build_fire_shield_context(
        project_root,
        phase=FireShieldPhase.PROJECT_TRANSIENT_WRITE,
        operation_id="validator-transient",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    gate("FIRE_SHIELD_TRANSIENT_MODE_EXTERNAL_PROJECT",
         transient.mode is FireShieldMode.EXTERNAL_PROJECT)
    assert_fire_shield_write_allowed(
        transient,
        transient.allowed_write_root / "fire_shield" / "receipt.json",
        operation="CREATE",
    )
    gate("FIRE_SHIELD_TRANSIENT_WRITE_ALLOWED", True)
    expect_block(
        "FIRE_SHIELD_TRANSIENT_TO_PROJECT_SOURCE_DENIED",
        "FIRE_SHIELD_PROJECT_WRITE_ZONE_ESCAPE",
        lambda: assert_fire_shield_write_allowed(
            transient,
            project_root / "src" / "bad.py",
            operation="CREATE",
        ),
    )
    expect_block(
        "FIRE_SHIELD_TRANSIENT_TO_TOOL_SOURCE_DENIED",
        "FIRE_SHIELD_TOOL_WRITE_BLOCKED",
        lambda: assert_fire_shield_write_allowed(
            transient,
            tool_root / "kanda_reasoner_app" / "bad.py",
            operation="CREATE",
        ),
    )

    assert_fire_shield_payload_bytes_allowed(
        transient,
        b"VALUE = 1\n",
        "src/safe_payload.py",
    )
    gate("FIRE_SHIELD_SAFE_PAYLOAD_BYTES_ALLOWED", True)
    expect_block(
        "FIRE_SHIELD_EXACT_TOOL_COPY_DENIED",
        "FIRE_SHIELD_EXACT_TOOL_FILE_COPY_BLOCKED",
        lambda: assert_fire_shield_payload_bytes_allowed(
            transient,
            (
                tool_root
                / "kanda_reasoner_app"
                / "private_api.py"
            ).read_bytes(),
            "src/copied_private_api.py",
        ),
    )
    expect_block(
        "FIRE_SHIELD_PAYLOAD_PRIVATE_TOOL_IMPORT_DENIED",
        "FIRE_SHIELD_PROJECT_TOOL_PRIVATE_IMPORT_BLOCKED",
        lambda: assert_fire_shield_payload_bytes_allowed(
            transient,
            b"import kanda_reasoner_app\n",
            "src/private_import.py",
        ),
    )

    verify_tool_snapshot_unchanged(transient)
    gate("FIRE_SHIELD_TOOL_POST_STATE_UNCHANGED", True)
    tool_core = tool_root / "kanda_reasoner_app" / "tool_core.py"
    original = tool_core.read_text(encoding="utf-8")
    write(tool_core, original + "MUTATED = True\n")
    expect_block(
        "FIRE_SHIELD_TOOL_MUTATION_DETECTED",
        "FIRE_SHIELD_TOOL_MUTATION_DETECTED",
        lambda: verify_tool_snapshot_unchanged(transient),
    )
    write(tool_core, original)

    package_payload = base / "packages" / "project_payload.zip"
    fire_shield_zip(
        package_payload,
        [
            ("INSTALL.ps1", b"Write-Host 'install'\n"),
            ("VALIDATE.ps1", b"Write-Host 'validate'\n"),
            ("payload/src/new_module.py", b"VALUE = 1\n"),
        ],
    )
    expect_block(
        "FIRE_SHIELD_EXTERNAL_PROJECT_ARCHIVE_PAYLOAD_DENIED",
        "FIRE_SHIELD_PROJECT_WRITE_ZONE_ESCAPE",
        lambda: preflight_fire_shield_archive(transient, package_payload),
    )

    package_control = base / "packages" / "control_only.zip"
    fire_shield_zip(
        package_control,
        [
            ("INSTALL.ps1", b"Write-Host 'install'\n"),
            ("VALIDATE.ps1", b"Write-Host 'validate'\n"),
            ("KANDA_FREEZE_HINT.json", b"{}\n"),
        ],
    )
    report = preflight_fire_shield_archive(transient, package_control)
    gate(
        "FIRE_SHIELD_CONTROL_ONLY_ARCHIVE_PREFLIGHT",
        report.project_payload_count == 0
        and report.delivery_control_count == 2
        and report.freeze_hint_count == 1,
    )

    package_bad = base / "packages" / "traversal.zip"
    fire_shield_zip(
        package_bad,
        [("payload/../escape.py", b"VALUE = 1\n")],
    )
    expect_block(
        "FIRE_SHIELD_ARCHIVE_TRAVERSAL_DENIED",
        "ARCHIVE_PARENT_TRAVERSAL_REJECTED",
        lambda: preflight_fire_shield_archive(transient, package_bad),
    )

    backslash_zip = base / "packages" / "backslash.zip"
    header_count = fire_shield_raw_backslash_zip(
        backslash_zip,
        "payload/escape.py",
        "payload\\escape.py",
        b"VALUE = 1\n",
    )
    gate(
        "FIRE_SHIELD_RAW_BACKSLASH_FIXTURE_HEADER_COUNT",
        header_count == 2,
    )
    expect_block(
        "FIRE_SHIELD_ARCHIVE_BACKSLASH_DENIED",
        "ARCHIVE_BACKSLASH_MEMBER_REJECTED",
        lambda: preflight_fire_shield_archive(transient, backslash_zip),
    )

    link_path = transient.allowed_write_root / "tool_link"
    if create_link_or_junction(link_path, tool_root):
        expect_block_any(
            "FIRE_SHIELD_LINK_OR_JUNCTION_ESCAPE_DENIED",
            (
                "FIRE_SHIELD_TOOL_WRITE_BLOCKED",
                "PROJECT_OPERATION_REPARSE_COMPONENT_REJECTED",
                "FIRE_SHIELD_PROJECT_WRITE_ZONE_ESCAPE",
            ),
            lambda: assert_fire_shield_write_allowed(
                transient,
                link_path / "escaped.py",
                operation="CREATE",
            ),
        )
    else:
        print(
            "FIRE_SHIELD_LINK_OR_JUNCTION_ESCAPE_DENIED: "
            "SKIP - platform fixture unavailable"
        )

    freeze_context = build_fire_shield_context(
        project_root,
        phase=FireShieldPhase.FREEZE_WRITE,
        operation_id="validator-freeze",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    assert_fire_shield_write_allowed(
        freeze_context,
        (
            freeze_context.allowed_write_root
            / "freeze_hint_intake"
            / "hint.json"
        ),
        operation="CREATE",
    )
    gate("FIRE_SHIELD_FREEZE_SUPPORT_WRITE_ALLOWED", True)
    expect_block(
        "FIRE_SHIELD_FREEZE_TO_PROJECT_SOURCE_DENIED",
        "FIRE_SHIELD_PROJECT_WRITE_ZONE_ESCAPE",
        lambda: assert_fire_shield_write_allowed(
            freeze_context,
            project_root / "src" / "bad.py",
            operation="CREATE",
        ),
    )

    error_context = build_fire_shield_context(
        project_root,
        phase=FireShieldPhase.ERROR_MEMORY_WRITE,
        operation_id="validator-error-memory",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    assert_fire_shield_write_allowed(
        error_context,
        (
            error_context.allowed_write_root
            / "pending_ai_assisted_error_lesson_intake"
            / "lesson.json"
        ),
        operation="CREATE",
    )
    gate("FIRE_SHIELD_ERROR_MEMORY_SUPPORT_WRITE_ALLOWED", True)

    other_project = base / "project" / "other_project"
    write(other_project / "app.py", "VALUE = 2\n")
    select_external(tool_root, other_project, registry_path)
    expect_block(
        "FIRE_SHIELD_STALE_PROJECT_SELECTION_DENIED",
        "FIRE_SHIELD_PROJECT_IDENTITY_STALE",
        lambda: assert_fire_shield_write_allowed(
            transient,
            transient.allowed_write_root / "stale.json",
            operation="CREATE",
        ),
    )
    select_external(tool_root, project_root, registry_path)


def run_self_hosting_matrix(base: Path) -> None:
    """Prove self-hosting does not restore source-mutation authority."""
    tool_root = base / "self" / "kanda_reasoner"
    registry_path = base / "self_registry" / "projects.json"
    write(
        tool_root / "kanda_reasoner_app" / "tool_core.py",
        "VALUE = 1\n",
    )
    select_self_hosted(tool_root, registry_path)

    expect_block(
        "FIRE_SHIELD_SELF_HOSTING_SOURCE_MUTATION_DENIED",
        FIRE_SHIELD_PROJECT_SOURCE_MUTATION_UNSUPPORTED_MARKER,
        lambda: build_fire_shield_context(
            tool_root,
            phase=FireShieldPhase.PROJECT_SOURCE_MUTATION,
            operation_id="validator-self-hosting-source",
            tool_source_root=tool_root,
            registry_path=registry_path,
        ),
    )

    read_only = build_fire_shield_context(
        tool_root,
        phase=FireShieldPhase.VALIDATE_READ_ONLY,
        operation_id="validator-self-hosting-read-only",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    gate(
        "FIRE_SHIELD_MODE_KANDA_SELF_HOSTING",
        read_only.mode is FireShieldMode.KANDA_SELF_HOSTING,
    )
    gate(
        "FIRE_SHIELD_SELF_HOSTING_PHYSICAL_EQUALITY_ROLE_AWARE",
        read_only.boundary.same_canonical_resolved_root,
    )


def run_spoof_matrix(base: Path) -> None:
    """Reject an external Project that claims the reserved Tool slug."""
    tool_root = base / "tool_spoof" / "kanda_reasoner"
    project_root = base / "project_spoof" / "kanda_reasoner"
    registry_path = base / "registry_spoof" / "projects.json"
    write(
        tool_root / "kanda_reasoner_app" / "core.py",
        "VALUE = 1\n",
    )
    write(project_root / "app.py", "VALUE = 2\n")
    select_external(tool_root, project_root, registry_path)
    expect_block(
        "FIRE_SHIELD_RESERVED_SLUG_SPOOF_DENIED",
        "FIRE_SHIELD_IDENTITY_AMBIGUOUS",
        lambda: build_fire_shield_context(
            project_root,
            phase=FireShieldPhase.VALIDATE_READ_ONLY,
            operation_id="validator-spoof",
            tool_source_root=tool_root,
            registry_path=registry_path,
        ),
    )


def run_static_current_contract_checks(project_root: Path) -> None:
    """Confirm current source declares the spectator-only contract."""
    source = (
        project_root
        / "kanda_reasoner_app"
        / "project_fire_shield.py"
    ).read_text(encoding="utf-8")
    gate(
        "FIRE_SHIELD_SPECTATOR_FEATURE_DECLARED",
        CURRENT_FIRE_SHIELD_FEATURE_ID in source,
    )
    gate(
        "FIRE_SHIELD_SOURCE_MUTATION_UNSUPPORTED_DECLARED",
        "FIRE_SHIELD_PROJECT_SOURCE_MUTATION_UNSUPPORTED:SPECTATOR_ONLY"
        in source,
    )


def main() -> int:
    """Run the legacy cross-project validator against the current contract."""
    print("FIRE SHIELD VALIDATION")
    print("Validator contract: " + VALIDATOR_CONTRACT_ID)
    print("Current feature: " + CURRENT_FIRE_SHIELD_FEATURE_ID)
    with tempfile.TemporaryDirectory(
        prefix="kanda_fire_shield_spectator_"
    ) as raw:
        base = Path(raw).resolve()
        run_external_matrix(base / "external")
        run_self_hosting_matrix(base / "self_hosting")
        run_spoof_matrix(base / "spoof")
    run_static_current_contract_checks(PROJECT_ROOT)
    print("FIRE_SHIELD_CROSS_PROJECT_CODE_TRANSFER: ZERO")
    print("FIRE_SHIELD_EXTERNAL_PROJECT_SOURCE_MUTATION: DENIED")
    print("VALIDATION OK: " + VALIDATOR_CONTRACT_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
