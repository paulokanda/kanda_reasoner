"""PyInstaller execution and release staging."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Sequence

from portable.constants import (
    FORBIDDEN_GENERATED_TOKENS,
    MAX_ARCHIVE_PATH_BYTES,
    NON_RUNTIME_LONG_PATH_DOCS,
)
from portable.errors import PortableBuildError
from portable.models import BuildPaths, BuiltApplication


def run_command(
    command: Sequence[str],
    *,
    cwd: Path,
    environment: dict[str, str] | None = None,
) -> None:
    """Run a native command with exit-code authority."""

    rendered = subprocess.list2cmdline([str(item) for item in command])
    print(f"RUN: {rendered}")
    result = subprocess.run(
        [str(item) for item in command],
        cwd=str(cwd),
        env=environment,
        check=False,
    )
    if result.returncode != 0:
        raise PortableBuildError(
            "Command failed with exit code "
            f"{result.returncode}: {rendered}"
        )


def _detect_built_application(paths: BuildPaths) -> BuiltApplication:
    candidates: list[BuiltApplication] = []
    if not paths.pyinstaller_dist.is_dir():
        raise PortableBuildError(
            f"PyInstaller dist root was not created: {paths.pyinstaller_dist}"
        )

    for folder in paths.pyinstaller_dist.iterdir():
        if not folder.is_dir():
            continue
        top_level_exes = sorted(folder.glob("*.exe"))
        for executable in top_level_exes:
            candidates.append(
                BuiltApplication(app_root=folder, executable=executable)
            )

    preferred = [
        item
        for item in candidates
        if item.executable.name.casefold()
        in {"kanda_reasoner.exe", "kandareasoner.exe"}
    ]
    selected = preferred or candidates
    if len(selected) != 1:
        rendered = [str(item.executable) for item in selected]
        raise PortableBuildError(
            "Expected exactly one top-level packaged executable; found: "
            f"{rendered}"
        )

    application = selected[0]
    if not (application.app_root / "_internal").is_dir():
        raise PortableBuildError(
            "Packaged _internal folder was not created."
        )
    return application


def build_application(paths: BuildPaths) -> BuiltApplication:
    """Build the canonical one-folder app outside source."""

    for directory in (
        paths.run_root,
        paths.pyinstaller_work,
        paths.pyinstaller_dist,
        paths.pyinstaller_config,
        paths.temporary_root,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    environment = os.environ.copy()
    environment.update(
        {
            "PYINSTALLER_CONFIG_DIR": str(paths.pyinstaller_config),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPYCACHEPREFIX": str(paths.run_root / "pycache"),
            "TEMP": str(paths.temporary_root),
            "TMP": str(paths.temporary_root),
        }
    )
    command = [
        str(paths.governed_python),
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--workpath",
        str(paths.pyinstaller_work),
        "--distpath",
        str(paths.pyinstaller_dist),
        str(paths.spec_path),
    ]
    run_command(
        command,
        cwd=paths.project_root,
        environment=environment,
    )

    application = _detect_built_application(paths)
    print(f"PORTABLE PACKAGED APP ROOT: {application.app_root}")
    print(f"PORTABLE PACKAGED EXECUTABLE: {application.executable}")
    print("PORTABLE PYINSTALLER BUILD: PASS")
    print("PORTABLE BUILD PRODUCTS OUTSIDE PROJECT: PASS")
    return application


def _validate_stage_entry(entry: Path, stage_parent: Path) -> tuple[int, str]:
    relative = entry.relative_to(stage_parent).as_posix()
    path_bytes = len(relative.encode("utf-8"))

    if path_bytes > MAX_ARCHIVE_PATH_BYTES:
        raise PortableBuildError(
            f"Archive path is {path_bytes} bytes: {relative}"
        )
    if entry.is_symlink():
        raise PortableBuildError(f"Symlink found in staging: {relative}")
    if entry.is_file() and entry.name.casefold().startswith(".env"):
        raise PortableBuildError(
            f"Environment credential file found in staging: {relative}"
        )

    lowered = relative.casefold()
    if any(token in lowered for token in FORBIDDEN_GENERATED_TOKENS):
        raise PortableBuildError(
            f"Generated handoff/release artifact found in staging: {relative}"
        )
    return path_bytes, relative


def stage_application(
    paths: BuildPaths,
    application: BuiltApplication,
) -> Path:
    """Copy the built app to a single-root release stage."""

    paths.stage_parent.mkdir(parents=True, exist_ok=True)
    stage_app = paths.stage_parent / application.app_root.name
    shutil.copytree(application.app_root, stage_app)

    long_path_docs = stage_app / NON_RUNTIME_LONG_PATH_DOCS
    if long_path_docs.exists():
        shutil.rmtree(long_path_docs)
        print("PORTABLE NON-RUNTIME LONG-PATH DOCS REMOVED: PASS")
    else:
        print("PORTABLE NON-RUNTIME LONG-PATH DOCS: NOT PRESENT")

    top_level = [item.name for item in paths.stage_parent.iterdir()]
    if top_level != [application.app_root.name]:
        raise PortableBuildError(
            f"Staging top-level contract failed: {top_level}"
        )

    maximum = (0, "")
    entries = sorted(
        paths.stage_parent.rglob("*"),
        key=lambda item: item.relative_to(
            paths.stage_parent
        ).as_posix().casefold(),
    )
    for entry in entries:
        evidence = _validate_stage_entry(entry, paths.stage_parent)
        maximum = max(maximum, evidence)

    print(f"PORTABLE MAXIMUM ARCHIVE PATH: {maximum[0]} bytes")
    print(f"PORTABLE LONGEST ARCHIVE PATH: {maximum[1]}")
    print("PORTABLE STAGE CONTENTS: PASS")
    return stage_app
