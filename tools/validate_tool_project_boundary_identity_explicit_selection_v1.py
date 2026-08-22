# project-path: tools/validate_tool_project_boundary_identity_explicit_selection_v1.py
"""Validate Release 1 Tool/Project boundary identity and explicit selection."""

from __future__ import annotations

import os
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_root_resolver import (  # noqa: E402
    PROJECT_ROOT_ENV_NAMES,
    resolve_selected_project_root,
)
from kanda_reasoner_app.project_selection_registry import (  # noqa: E402
    ProjectSelectionRegistry,
)
from kanda_reasoner_app.project_support_boundary import (  # noqa: E402
    ProjectSelectionMode,
    ProjectSupportBoundaryError,
    canonical_project_support_root,
    canonical_tool_support_root,
    resolve_explicit_project_tool_boundary_identity,
)

FEATURE_ID = "tool-project-boundary-identity-explicit-selection-v1"
TOUCHED_SOURCE = (
    "kanda_reasoner_app/project_root_resolver.py",
    "kanda_reasoner_app/project_support_boundary.py",
    "kanda_reasoner_app/project_selection_registry.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/"
    "window_project_root.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/"
    "window_tool_patches.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/"
    "window_state.py",
)


def gate(marker: str, condition: bool) -> None:
    """Print one deterministic marker or fail the focused validation."""
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


@contextmanager
def without_project_environment():
    """Temporarily remove every Project-root environment variable."""
    saved = {name: os.environ.get(name) for name in PROJECT_ROOT_ENV_NAMES}
    for name in PROJECT_ROOT_ENV_NAMES:
        os.environ.pop(name, None)
    try:
        yield
    finally:
        for name, value in saved.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def expect_boundary_error(marker: str, callback, expected: str) -> None:
    """Require one strict boundary rejection with a stable reason."""
    try:
        callback()
    except ProjectSupportBoundaryError as exc:
        gate(marker, expected in str(exc))
        return
    raise AssertionError(marker + ": expected rejection")


def validate_strict_selection(temp_root: Path) -> None:
    """Validate external and self-hosting modes without inferred authority."""
    tool_root = temp_root / "kanda_reasoner"
    project_root = temp_root / "eeg_kanda"
    tool_root.mkdir(parents=True)
    project_root.mkdir()

    external = resolve_explicit_project_tool_boundary_identity(
        project_root,
        selection_mode=ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
        stable_project_id="external-project-id",
        tool_source_root=tool_root,
    )
    gate(
        "EXPLICIT_EXTERNAL_PROJECT_BOUNDARY",
        external.selection_mode
        is ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT
        and not external.self_hosting_mode
        and not external.same_canonical_resolved_root,
    )
    gate(
        "PROJECT_SUPPORT_EXTERNAL_TO_PROJECT_SOURCE",
        external.active_project_support_root
        == canonical_project_support_root(project_root),
    )

    self_hosted = resolve_explicit_project_tool_boundary_identity(
        tool_root,
        selection_mode=ProjectSelectionMode.EXPLICIT_SELF_HOSTING,
        stable_project_id="self-hosted-project-id",
        tool_source_root=tool_root,
    )
    gate(
        "EXPLICIT_SELF_HOSTING_BOUNDARY",
        self_hosted.self_hosting_mode
        and self_hosted.same_canonical_resolved_root
        and self_hosted.selection_mode
        is ProjectSelectionMode.EXPLICIT_SELF_HOSTING,
    )

    expect_boundary_error(
        "IMPLICIT_SELF_HOSTING_REJECTED",
        lambda: resolve_explicit_project_tool_boundary_identity(
            tool_root,
            selection_mode=ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
            stable_project_id="wrong-mode",
            tool_source_root=tool_root,
        ),
        "SELF_HOSTING_REQUIRES_EXPLICIT_SELECTION",
    )
    expect_boundary_error(
        "FALSE_SELF_HOSTING_REJECTED",
        lambda: resolve_explicit_project_tool_boundary_identity(
            project_root,
            selection_mode=ProjectSelectionMode.EXPLICIT_SELF_HOSTING,
            stable_project_id="wrong-root",
            tool_source_root=tool_root,
        ),
        "SELF_HOSTING_SELECTION_ROOT_MISMATCH",
    )


def validate_registry(temp_root: Path) -> None:
    """Validate Tool-owned persistence, stable ID reuse, and stale rejection."""
    tool_root = temp_root / "tool"
    project_root = temp_root / "project"
    tool_root.mkdir(parents=True)
    project_root.mkdir()
    registry_path = temp_root / "tool_support" / "projects.json"
    registry = ProjectSelectionRegistry(
        tool_source_root=tool_root,
        registry_path=registry_path,
    )

    first = registry.register_explicit_root(project_root)
    second = registry.register_explicit_root(project_root)
    gate(
        "STABLE_PROJECT_ID_REUSED",
        first.active_project_id == second.active_project_id,
    )
    gate(
        "TOOL_OWNED_SELECTION_REGISTRY_WRITTEN",
        registry_path.is_file()
        and registry_path.parent != project_root
        and registry_path.parent != tool_root,
    )
    loaded = registry.resolve_current_boundary()
    gate(
        "REGISTERED_SELECTION_RELOADS_STRICTLY",
        loaded is not None
        and loaded.active_project_id == first.active_project_id
        and loaded.selection_mode
        is ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
    )

    project_root.rmdir()
    gate(
        "MISSING_PERSISTED_PROJECT_FAILS_UNSELECTED",
        registry.resolve_current_boundary() is None,
    )
    registry.clear_current_selection()
    gate(
        "CLEAR_SELECTION_RETURNS_UNSELECTED",
        registry.load_current_record() is None,
    )


def validate_no_implicit_root_fallback(temp_root: Path) -> None:
    """Validate the strict selector never converts Tool runtime into Project."""
    with without_project_environment():
        gate(
            "NO_PROJECT_SELECTION_RETURNS_NONE",
            resolve_selected_project_root() is None,
        )
        missing = temp_root / "missing"
        gate(
            "MISSING_PERSISTED_ROOT_RETURNS_NONE",
            resolve_selected_project_root(persisted_root=missing) is None,
        )
        selected = temp_root / "selected"
        selected.mkdir(parents=True)
        gate(
            "EXPLICIT_EXISTING_ROOT_ACCEPTED",
            resolve_selected_project_root(selected) == selected.resolve(),
        )


def validate_source_contract(project_root: Path) -> None:
    """Validate shell integration and focused module-size contracts."""
    main_window = (
        project_root
        / "kanda_reasoner_app"
        / "reasoner_tools_gui_shell"
        / "main_window.py"
    ).read_text(encoding="utf-8")
    state = (
        project_root
        / "kanda_reasoner_app"
        / "reasoner_tools_gui_shell"
        / "main_window_help"
        / "window_state.py"
    ).read_text(encoding="utf-8")
    root_mixin = (
        project_root
        / "kanda_reasoner_app"
        / "reasoner_tools_gui_shell"
        / "main_window_help"
        / "window_project_root.py"
    ).read_text(encoding="utf-8")

    gate(
        "SHELL_USES_REGISTRY_OWNED_PROJECT_OBSERVATION",
        "ProjectSelectionRegistry" in main_window
        and "load_current_observation" in main_window
        and "resolve_current_boundary" in main_window
        and "current_project_observation" in main_window
        and "current_project_boundary" in main_window,
    )
    gate(
        "SHELL_OBSERVED_ROOT_FALLBACK_IS_REGISTRY_BOUND",
        "resolve_observed_project_root" in main_window
        and "register_legacy_external_root" in main_window
        and "if observation is None:" in main_window,
    )
    gate(
        "SHELL_RETIRED_ACTIVE_PROJECT_RESOLVER_ABSENT",
        "resolve_active_project_root" not in main_window,
    )
    gate(
        "TOOL_PREFS_EXTERNAL_TO_TOOL_SOURCE",
        "canonical_tool_support_root" in state
        and "_legacy_prefs_path" in state,
    )
    gate(
        "GUI_PROJECT_CHANGE_IS_EXPLICIT_SELECTION",
        "explicit_selection=True" in root_mixin,
    )

    for relative in TOUCHED_SOURCE:
        path = project_root / relative
        lines = len(path.read_text(encoding="utf-8").splitlines())
        gate(
            "MODULE_SIZE_" + path.name.upper().replace(".", "_"),
            100 < lines < 500,
        )
    print("TOUCHED_SOURCE_MODULES_STRICTLY_101_TO_499: PASS")


def main() -> int:
    """Run all Release 1 focused validation gates."""
    with tempfile.TemporaryDirectory(prefix="kanda_boundary_release1_") as raw:
        temp_root = Path(raw)
        validate_strict_selection(temp_root / "strict")
        validate_registry(temp_root / "registry")
        validate_no_implicit_root_fallback(temp_root / "resolver")
    validate_source_contract(PROJECT_ROOT)
    tool_support = canonical_tool_support_root(PROJECT_ROOT)
    gate(
        "TOOL_SUPPORT_EXTERNAL_TO_TOOL_SOURCE",
        tool_support != PROJECT_ROOT
        and not str(tool_support).startswith(str(PROJECT_ROOT) + os.sep),
    )
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
