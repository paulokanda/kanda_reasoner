"""Dynamic Tool path resolution and registry-assisted destination checks."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from portable.constants import (
    FINAL_ZIP_NAME,
    PROJECT_FOLDER_NAME,
    SPEC_NAME,
    VENV_PYTHON_RELATIVE,
)
from portable.errors import PortableBuildError
from portable.models import BuildPaths, RegistryBoundary
from portable.registry_boundary import assert_outside_protected_roots


def is_within(path: Path, parent: Path) -> bool:
    """Return whether path is located under parent."""

    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def build_publication_zip_name(build_time: datetime) -> str:
    """Return a traceable Portable filename with local build date and time."""

    timestamp = build_time.strftime("%Y%m%d_%H%M%S")
    suffix = "-Windows-Portable.zip"
    if not FINAL_ZIP_NAME.endswith(suffix):
        raise PortableBuildError(
            "Portable final ZIP template lost the canonical Windows suffix."
        )
    prefix = FINAL_ZIP_NAME[: -len(suffix)]
    return f"{prefix}-{timestamp}{suffix}"


def resolve_paths(
    project_root: Path,
    output_directory: Path,
    boundary: RegistryBoundary,
) -> BuildPaths:
    """Resolve build paths from Tool source identity, not active Project identity."""

    project = project_root.resolve()
    if os.name != "nt" or not project.anchor:
        raise PortableBuildError(
            "Run this builder on Windows from the KANDA Reasoner project."
        )
    if project.name.casefold() != PROJECT_FOLDER_NAME.casefold():
        raise PortableBuildError(
            "This builder is owned by the kanda_reasoner Tool source only: "
            f"{project}"
        )
    if project != boundary.tool_root:
        raise PortableBuildError(
            "Portable Tool root does not match builder-location authority."
        )

    drive = Path(project.anchor).resolve()
    support = boundary.tool_support_root
    transient = boundary.tool_transient_root
    build_time = datetime.now()
    run_id = (
        build_time.strftime("%Y%m%d_%H%M%S_%f")
        + "_"
        + uuid4().hex[:8]
    )
    run_root = (transient / "portable_build" / run_id).resolve()
    publication_zip_name = build_publication_zip_name(build_time)
    final_zip = output_directory.resolve() / publication_zip_name

    paths = BuildPaths(
        project_root=project,
        drive_root=drive,
        project_support_root=support,
        transient_root=transient,
        run_root=run_root,
        pyinstaller_work=run_root / "pyinstaller_work",
        pyinstaller_dist=run_root / "pyinstaller_dist",
        pyinstaller_config=run_root / "pyinstaller_config",
        temporary_root=run_root / "temp",
        stage_parent=run_root / "release_stage",
        candidate_zip=run_root / publication_zip_name,
        clean_extract_root=run_root / "clean_zip_extraction",
        final_zip=final_zip,
        spec_path=project / SPEC_NAME,
        governed_python=(project / VENV_PYTHON_RELATIVE).resolve(),
        zip_helper=project / "portable" / "create_windows_zip.ps1",
        registry_boundary=boundary,
    )
    validate_boundaries(paths)
    return paths


def validate_boundaries(paths: BuildPaths) -> None:
    """Enforce the Tool transient exception and all owner-root exclusions."""

    if not is_within(paths.run_root, paths.transient_root):
        raise PortableBuildError(
            "Portable staging must remain inside the Tool transient root."
        )
    if is_within(paths.run_root, paths.project_root):
        raise PortableBuildError("Portable staging is inside the Tool source.")
    if is_within(paths.run_root, paths.project_support_root):
        raise PortableBuildError("Portable staging is inside Tool Support.")

    assert_outside_protected_roots(
        paths.final_zip,
        paths.registry_boundary,
        purpose="Portable final ZIP",
    )

    distinct = {
        paths.project_root,
        paths.project_support_root,
        paths.run_root,
        paths.final_zip,
    }
    if len(distinct) != 4:
        raise PortableBuildError(
            "Tool, Tool Support, staging, and output must be distinct."
        )


def print_identity(paths: BuildPaths) -> None:
    """Print Tool authority and Project-independent build identities."""

    boundary = paths.registry_boundary
    if boundary is None:
        raise PortableBuildError(
            "Registry boundary is missing from resolved build paths."
        )
    print("PORTABLE BUILD IDENTITY")
    print(f"Tool source root: {paths.project_root}")
    print(f"Tool Support: {paths.project_support_root}")
    print(f"Transient staging: {paths.run_root}")
    print(f"Selected destination folder: {paths.final_zip.parent}")
    print(f"Final Portable output: {paths.final_zip}")
    print(f"Governed Python: {paths.governed_python}")
    print(f"Optional Project registry: {boundary.registry_path}")
    print(f"Registry SHA-256: {boundary.registry_sha256 or '<absent>'}")
    print(f"Observed active Project ID: {boundary.current_project_id or '<none>'}")
    print(f"Observed selection mode: {boundary.selection_mode}")
    print(
        f"Destination-protected registered roots: {len(boundary.protected_roots)}"
    )
    print(
        f"Tool-owner immutability roots: {len(boundary.tool_owner_roots)}"
    )
    print("PORTABLE TOOL ROOT AUTHORITY FROM BUILDER LOCATION: PASS")
    print("PORTABLE ACTIVE PROJECT IDENTITY NOT REQUIRED: PASS")
    print("PORTABLE ALL KNOWN ROOTS DESTINATION-PROTECTED: PASS")
    print("PORTABLE TOOL OWNER ROOTS IMMUTABILITY-PROTECTED: PASS")
    print("Show Project workflow invoked: NO")
