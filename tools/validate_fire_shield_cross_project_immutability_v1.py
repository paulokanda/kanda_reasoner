# project-path: tools/validate_fire_shield_cross_project_immutability_v1.py
"""Focused validator for Fire Shield cross-project immutability v1."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from fire_shield_validation_fixtures import fire_shield_raw_backslash_zip, fire_shield_zip

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
from kanda_reasoner_app.project_support_boundary import ProjectSelectionMode
from kanda_reasoner_app.project_fire_shield import (
    FIRE_SHIELD_FEATURE_ID,
    FireShieldError,
    FireShieldMode,
    FireShieldPhase,
    assert_fire_shield_source_transfer_allowed,
    assert_fire_shield_write_allowed,
    build_fire_shield_context,
    preflight_fire_shield_archive,
    scan_project_python_source,
    verify_project_import_isolation,
    verify_tool_snapshot_unchanged,
)

FEATURE_ID = "kanda-reasoner-fire-shield-cross-project-immutability-v1"


def gate(name: str, condition: bool) -> None:
    """Print one stable PASS marker or fail immediately."""
    if not condition:
        raise RuntimeError(name + ": FAIL")
    print(name + ": PASS")


def expect_block(name: str, marker: str, action) -> None:
    """Require one Fire Shield action to fail with the expected marker."""
    expect_block_any(name, (marker,), action)


def expect_block_any(name: str, markers: tuple[str, ...], action) -> None:
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
    write(tool_root / "kanda_reasoner_app" / "tool_core.py", "TOOL_SENTINEL = 'tool-core'\n")
    write(tool_root / "kanda_reasoner_app" / "private_api.py", "PRIVATE = True\n")
    write(project_root / "src" / "app.py", "VALUE = 'project'\n")
    return tool_root, project_root, registry_path


def select_external(tool_root: Path, project_root: Path, registry_path: Path) -> None:
    """Register one explicit external Project selection."""
    registry = ProjectSelectionRegistry(
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    registry.register_explicit_selection(
        project_root,
        ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
    )


def select_self_hosted(tool_root: Path, registry_path: Path) -> None:
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
    """Exercise external-Project allow and deny cases."""
    tool_root, project_root, registry_path = make_layout(base)
    select_external(tool_root, project_root, registry_path)
    context = build_fire_shield_context(
        project_root,
        phase=FireShieldPhase.PROJECT_SOURCE_MUTATION,
        operation_id="validator-external-source",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    gate("FIRE_SHIELD_FEATURE_ID_STABLE", FIRE_SHIELD_FEATURE_ID == FEATURE_ID)
    gate("FIRE_SHIELD_MODE_EXTERNAL_PROJECT", context.mode is FireShieldMode.EXTERNAL_PROJECT)
    gate("FIRE_SHIELD_PROJECT_IDENTITY_VERIFIED", context.boundary.active_project_root == project_root.resolve())
    gate("FIRE_SHIELD_TOOL_IDENTITY_VERIFIED", context.boundary.tool_source_root == tool_root.resolve())
    gate(
        "FIRE_SHIELD_PROJECT_WRITE_ALLOWED",
        assert_fire_shield_write_allowed(
            context,
            project_root / "src" / "new_module.py",
            operation="CREATE",
        ).parent == (project_root / "src").resolve(),
    )
    expect_block(
        "FIRE_SHIELD_TOOL_WRITE_DENIED",
        "FIRE_SHIELD_TOOL_WRITE_BLOCKED",
        lambda: assert_fire_shield_write_allowed(
            context,
            tool_root / "kanda_reasoner_app" / "tool_core.py",
            operation="REPLACE",
        ),
    )
    for mutation in ("CREATE", "DELETE", "MOVE", "RENAME", "RESTORE", "EXTRACT"):
        expect_block(
            "FIRE_SHIELD_TOOL_" + mutation + "_DENIED",
            "FIRE_SHIELD_TOOL_WRITE_BLOCKED",
            lambda mutation=mutation: assert_fire_shield_write_allowed(
                context,
                tool_root / "kanda_reasoner_app" / (mutation.lower() + ".py"),
                operation=mutation,
            ),
        )
    expect_block(
        "FIRE_SHIELD_PROJECT_WRITE_ZONE_ESCAPE_DENIED",
        "FIRE_SHIELD_PROJECT_WRITE_ZONE_ESCAPE",
        lambda: assert_fire_shield_write_allowed(
            context,
            base / "project" / "sample_project2" / "bad.py",
            operation="CREATE",
        ),
    )

    link_path = project_root / "src" / "tool_link"
    if create_link_or_junction(link_path, tool_root):
        expect_block_any(
            "FIRE_SHIELD_LINK_OR_JUNCTION_ESCAPE_DENIED",
            (
                "FIRE_SHIELD_TOOL_WRITE_BLOCKED",
                "PROJECT_OPERATION_REPARSE_COMPONENT_REJECTED",
            ),
            lambda: assert_fire_shield_write_allowed(
                context,
                link_path / "escaped.py",
                operation="CREATE",
            ),
        )
    else:
        print("FIRE_SHIELD_LINK_OR_JUNCTION_ESCAPE_DENIED: SKIP - platform fixture unavailable")

    hardlink = project_root / "src" / "tool_alias.py"
    try:
        os.link(tool_root / "kanda_reasoner_app" / "tool_core.py", hardlink)
    except OSError:
        print("FIRE_SHIELD_HARDLINK_TOOL_ALIAS_DENIED: SKIP - platform fixture unavailable")
    else:
        expect_block(
            "FIRE_SHIELD_HARDLINK_TOOL_ALIAS_DENIED",
            "FIRE_SHIELD_TOOL_FILE_ALIAS_BLOCKED",
            lambda: assert_fire_shield_write_allowed(context, hardlink, operation="REPLACE"),
        )

    expect_block(
        "FIRE_SHIELD_TOOL_SOURCE_TRANSFER_DENIED",
        "FIRE_SHIELD_TOOL_SOURCE_IN_PROJECT_PAYLOAD",
        lambda: assert_fire_shield_source_transfer_allowed(
            context,
            tool_root / "kanda_reasoner_app" / "private_api.py",
            project_root / "src" / "copied.py",
        ),
    )
    copied = base / "staging" / "renamed_tool_file.py"
    copied.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(tool_root / "kanda_reasoner_app" / "private_api.py", copied)
    expect_block(
        "FIRE_SHIELD_RENAMED_EXACT_TOOL_COPY_DENIED",
        "FIRE_SHIELD_EXACT_TOOL_FILE_COPY_BLOCKED",
        lambda: assert_fire_shield_source_transfer_allowed(
            context,
            copied,
            project_root / "src" / "renamed_tool_file.py",
        ),
    )

    scan_project_python_source(context, b"from pathlib import Path\nVALUE = Path('.')\n", "src/safe.py")
    gate("FIRE_SHIELD_SAFE_PROJECT_IMPORTS_ALLOWED", True)
    expect_block(
        "FIRE_SHIELD_PRIVATE_TOOL_IMPORT_DENIED",
        "FIRE_SHIELD_PROJECT_TOOL_PRIVATE_IMPORT_BLOCKED",
        lambda: scan_project_python_source(
            context,
            b"from kanda_reasoner_app import project_selection_registry\n",
            "src/bad_import.py",
        ),
    )
    expect_block(
        "FIRE_SHIELD_TOOL_ROOT_REFERENCE_DENIED",
        "FIRE_SHIELD_PROJECT_TOOL_PATH_LEAK_BLOCKED",
        lambda: scan_project_python_source(
            context,
            ("TOOL = " + repr(str(tool_root)) + "\n").encode("utf-8"),
            "src/tool_path.py",
        ),
    )
    verify_project_import_isolation(context, [str(project_root), str(project_root / "src")])
    gate("FIRE_SHIELD_PROJECT_IMPORT_ISOLATION_ALLOWED", True)
    expect_block(
        "FIRE_SHIELD_TOOL_ROOT_SYS_PATH_DENIED",
        "FIRE_SHIELD_PROJECT_TOOL_PATH_LEAK_BLOCKED",
        lambda: verify_project_import_isolation(
            context,
            [str(project_root), str(tool_root)],
        ),
    )

    package_ok = base / "packages" / "ok.zip"
    fire_shield_zip(
        package_ok,
        [
            ("INSTALL.ps1", b"Write-Host 'install'\n"),
            ("VALIDATE.ps1", b"Write-Host 'validate'\n"),
            ("payload/src/new_module.py", b"VALUE = 1\n"),
            ("KANDA_FREEZE_HINT.json", b"{}\n"),
        ],
    )
    report = preflight_fire_shield_archive(context, package_ok)
    gate("FIRE_SHIELD_ARCHIVE_CONTAINMENT", report.project_payload_count == 1)
    gate("FIRE_SHIELD_TOOL_SOURCE_TRANSFER_ZERO", report.tool_source_transfer_count == 0)
    gate("FIRE_SHIELD_PROJECT_TOOL_PRIVATE_IMPORTS_ZERO", report.private_tool_import_count == 0)

    package_bad = base / "packages" / "traversal.zip"
    fire_shield_zip(package_bad, [("payload/../escape.py", b"VALUE = 1\n")])
    expect_block(
        "FIRE_SHIELD_ARCHIVE_TRAVERSAL_DENIED",
        "ARCHIVE_PARENT_TRAVERSAL_REJECTED",
        lambda: preflight_fire_shield_archive(context, package_bad),
    )

    package_private = base / "packages" / "private_import.zip"
    fire_shield_zip(
        package_private,
        [("payload/src/private.py", b"import kanda_reasoner_app\n")],
    )
    expect_block(
        "FIRE_SHIELD_ARCHIVE_PRIVATE_TOOL_IMPORT_DENIED",
        "FIRE_SHIELD_PROJECT_TOOL_PRIVATE_IMPORT_BLOCKED",
        lambda: preflight_fire_shield_archive(context, package_private),
    )

    backslash_zip = base / "packages" / "backslash.zip"
    header_count = fire_shield_raw_backslash_zip(
        backslash_zip, "payload/escape.py", "payload\\escape.py", b"VALUE = 1\n"
    )
    gate("FIRE_SHIELD_RAW_BACKSLASH_FIXTURE_HEADER_COUNT", header_count == 2)
    expect_block(
        "FIRE_SHIELD_ARCHIVE_BACKSLASH_DENIED",
        "ARCHIVE_BACKSLASH_MEMBER_REJECTED",
        lambda: preflight_fire_shield_archive(context, backslash_zip),
    )

    for label, member, marker in (
        ("ADS", "payload/src/file.py:stream", "ARCHIVE_WINDOWS_ADS_MEMBER_REJECTED"),
        ("UNC", "//server/share/escape.py", "ARCHIVE_ABSOLUTE_MEMBER_REJECTED"),
    ):
        unsafe_zip = base / "packages" / (label.lower() + ".zip")
        fire_shield_zip(unsafe_zip, [(member, b"VALUE = 1\n")])
        expect_block(
            "FIRE_SHIELD_ARCHIVE_" + label + "_DENIED",
            marker,
            lambda unsafe_zip=unsafe_zip: preflight_fire_shield_archive(
                context, unsafe_zip
            ),
        )

    package_tool = base / "packages" / "tool_copy.zip"
    fire_shield_zip(
        package_tool,
        [
            (
                "payload/src/copied.py",
                (tool_root / "kanda_reasoner_app" / "private_api.py").read_bytes(),
            )
        ],
    )
    expect_block(
        "FIRE_SHIELD_ARCHIVE_EXACT_TOOL_COPY_DENIED",
        "FIRE_SHIELD_EXACT_TOOL_FILE_COPY_BLOCKED",
        lambda: preflight_fire_shield_archive(context, package_tool),
    )

    verify_tool_snapshot_unchanged(context)
    gate("FIRE_SHIELD_TOOL_POST_STATE_UNCHANGED", True)
    original = (tool_root / "kanda_reasoner_app" / "tool_core.py").read_text(encoding="utf-8")
    write(tool_root / "kanda_reasoner_app" / "tool_core.py", original + "MUTATED = True\n")
    expect_block(
        "FIRE_SHIELD_TOOL_MUTATION_DETECTED",
        "FIRE_SHIELD_TOOL_MUTATION_DETECTED",
        lambda: verify_tool_snapshot_unchanged(context),
    )
    write(tool_root / "kanda_reasoner_app" / "tool_core.py", original)

    freeze_context = build_fire_shield_context(
        project_root,
        phase=FireShieldPhase.FREEZE_WRITE,
        operation_id="validator-freeze",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    assert_fire_shield_write_allowed(
        freeze_context,
        freeze_context.allowed_write_root / "freeze_hint_intake" / "hint.json",
        operation="CREATE",
    )
    gate("FIRE_SHIELD_FREEZE_SUPPORT_WRITE_ALLOWED", True)
    expect_block(
        "FIRE_SHIELD_FREEZE_OTHER_SUPPORT_DENIED",
        "FIRE_SHIELD_PROJECT_WRITE_ZONE_ESCAPE",
        lambda: assert_fire_shield_write_allowed(
            freeze_context,
            freeze_context.boundary.active_project_support_root / "other" / "bad.json",
            operation="CREATE",
        ),
    )

    transient_context = build_fire_shield_context(
        project_root,
        phase=FireShieldPhase.PROJECT_TRANSIENT_WRITE,
        operation_id="validator-transient",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    assert_fire_shield_write_allowed(
        transient_context,
        transient_context.allowed_write_root / "fire_shield" / "receipt.json",
        operation="CREATE",
    )
    gate("FIRE_SHIELD_TRANSIENT_WRITE_ALLOWED", True)

    read_only = build_fire_shield_context(
        project_root,
        phase=FireShieldPhase.VALIDATE_READ_ONLY,
        operation_id="validator-read-only",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    expect_block(
        "FIRE_SHIELD_VALIDATE_READ_ONLY_WRITE_DENIED",
        "FIRE_SHIELD_READ_ONLY_PHASE",
        lambda: assert_fire_shield_write_allowed(
            read_only, project_root / "src" / "bad.py", operation="WRITE"
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
        error_context.allowed_write_root / "pending_ai_assisted_error_lesson_intake" / "lesson.json",
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
            context, project_root / "src" / "stale.py", operation="CREATE"
        ),
    )
    select_external(tool_root, project_root, registry_path)


def run_self_hosting_matrix(base: Path) -> None:
    """Prove same physical root preserves explicit logical self-hosting."""
    tool_root = base / "self" / "kanda_reasoner"
    registry_path = base / "self_registry" / "projects.json"
    write(tool_root / "kanda_reasoner_app" / "tool_core.py", "VALUE = 1\n")
    select_self_hosted(tool_root, registry_path)
    context = build_fire_shield_context(
        tool_root,
        phase=FireShieldPhase.PROJECT_SOURCE_MUTATION,
        operation_id="validator-self-hosting",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    gate("FIRE_SHIELD_MODE_KANDA_SELF_HOSTING", context.mode is FireShieldMode.KANDA_SELF_HOSTING)
    assert_fire_shield_write_allowed(
        context,
        tool_root / "kanda_reasoner_app" / "tool_core.py",
        operation="REPLACE",
    )
    gate("FIRE_SHIELD_SELF_HOSTING_PHYSICAL_EQUALITY_ROLE_AWARE", True)


def run_spoof_matrix(base: Path) -> None:
    """Reject an external Project that claims the reserved Tool slug."""
    tool_root = base / "tool_spoof" / "kanda_reasoner"
    project_root = base / "project_spoof" / "kanda_reasoner"
    registry_path = base / "registry_spoof" / "projects.json"
    write(tool_root / "kanda_reasoner_app" / "core.py", "VALUE = 1\n")
    write(project_root / "app.py", "VALUE = 2\n")
    select_external(tool_root, project_root, registry_path)
    expect_block(
        "FIRE_SHIELD_RESERVED_SLUG_SPOOF_DENIED",
        "FIRE_SHIELD_IDENTITY_AMBIGUOUS",
        lambda: build_fire_shield_context(
            project_root,
            phase=FireShieldPhase.PROJECT_SOURCE_MUTATION,
            operation_id="validator-spoof",
            tool_source_root=tool_root,
            registry_path=registry_path,
        ),
    )


def run_static_integration_checks(project_root: Path) -> None:
    """Confirm the two governed source-write paths invoke Fire Shield."""
    broker = (
        project_root
        / "kanda_reasoner_app"
        / "reasoner_engine"
        / "project_web_ai_write_broker.py"
    ).read_text(encoding="utf-8")
    gate(
        "FIRE_SHIELD_PROJECT_WEB_AI_BROKER_INTEGRATED",
        "project_fire_shield" in broker
        and "verify_tool_snapshot_unchanged" in broker,
    )
    archive_source = (
        project_root / "kanda_reasoner_app" / "archive_safety.py"
    ).read_text(encoding="utf-8")
    gate(
        "FIRE_SHIELD_ARCHIVE_PUBLIC_PREFLIGHT_REUSED",
        "require_single_top_level" in archive_source,
    )


def main() -> int:
    """Run all Fire Shield v1 checks."""
    print("FIRE SHIELD VALIDATION")
    print("Feature ID: " + FEATURE_ID)
    with tempfile.TemporaryDirectory(prefix="kanda_fire_shield_") as raw:
        base = Path(raw).resolve()
        run_external_matrix(base / "external")
        run_self_hosting_matrix(base / "self_hosting")
        run_spoof_matrix(base / "spoof")
    run_static_integration_checks(PROJECT_ROOT)
    print("FIRE_SHIELD_CROSS_PROJECT_CODE_TRANSFER: ZERO")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
