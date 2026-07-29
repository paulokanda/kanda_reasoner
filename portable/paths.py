"""Dynamic path resolution and Box-boundary checks."""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

from portable.constants import (
    FINAL_ZIP_NAME,
    PROJECT_FOLDER_NAME,
    SPEC_NAME,
)
from portable.errors import PortableBuildError
from portable.models import BuildPaths


def is_within(path: Path, parent: Path) -> bool:
    """Return whether path is located under parent."""

    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def resolve_paths(
    project_root: Path,
    output_directory: Path,
) -> BuildPaths:
    """Resolve build paths and the user-selected final destination."""

    project = project_root.resolve()
    if os.name != "nt" or not project.anchor:
        raise PortableBuildError(
            "Run this builder on Windows from the KANDA Reasoner project."
        )
    if project.name.casefold() != PROJECT_FOLDER_NAME.casefold():
        raise PortableBuildError(
            "This builder is owned by the kanda_reasoner project only: "
            f"{project}"
        )

    drive = Path(project.anchor).resolve()
    support = (drive / f"{project.name}_show_project_to_AI").resolve()
    transient = (
        drive / f"{project.name}_delete_after_daily_work"
    ).resolve()
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_root = (transient / "portable_build" / run_id).resolve()
    final_zip = output_directory.resolve() / FINAL_ZIP_NAME

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
        candidate_zip=run_root / FINAL_ZIP_NAME,
        clean_extract_root=run_root / "clean_zip_extraction",
        final_zip=final_zip,
        spec_path=project / SPEC_NAME,
        governed_python=Path(sys.executable).resolve(),
        zip_helper=project / "portable" / "create_windows_zip.ps1",
    )
    validate_boundaries(paths)
    return paths


def validate_boundaries(paths: BuildPaths) -> None:
    """Enforce independent Portable and Show Project Boxes."""

    invalid_checks = (
        (
            is_within(paths.run_root, paths.project_root),
            "Portable staging is inside the project.",
        ),
        (
            is_within(paths.run_root, paths.project_support_root),
            "Portable staging is inside Project Support.",
        ),
        (
            is_within(paths.final_zip, paths.project_root),
            "Selected Portable destination is inside the project.",
        ),
        (
            is_within(paths.final_zip, paths.project_support_root),
            "Selected Portable destination is inside Project Support.",
        ),
        (
            is_within(paths.final_zip, paths.transient_root),
            "Selected final destination is inside transient build storage.",
        ),
    )
    for invalid, message in invalid_checks:
        if invalid:
            raise PortableBuildError(message)

    distinct = {
        paths.project_root,
        paths.project_support_root,
        paths.run_root,
        paths.final_zip,
    }
    if len(distinct) != 4:
        raise PortableBuildError(
            "Project, Project Support, staging, and output must be distinct."
        )


def print_identity(paths: BuildPaths) -> None:
    """Print Project and independent Box identities."""

    print("PORTABLE BUILD IDENTITY")
    print(f"Selected project: {paths.project_root}")
    print(f"Project Support: {paths.project_support_root}")
    print(f"Transient staging: {paths.run_root}")
    print(f"Selected destination folder: {paths.final_zip.parent}")
    print(f"Final Portable output: {paths.final_zip}")
    print(f"Governed Python: {paths.governed_python}")
    print("Show Project workflow invoked: NO")
