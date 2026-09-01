"""PyInstaller execution and release staging."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Sequence

from portable.constants import (
    MAX_ARCHIVE_PATH_BYTES,
)
from portable.errors import PortableBuildError
from portable.external_controls import (
    ExternalControlError,
    validate_external_build_controls,
)
from portable.models import BuildPaths, BuiltApplication
from portable.physical_runtime import (
    hydrate_physical_runtime,
    validate_physical_runtime,
)
from portable.packaged_worker_runtime import validate_packaged_worker_runtime
from portable.policy import (
    is_generated_handoff_or_release_path,
    is_forbidden_tool_capture_path,
    is_non_runtime_debris_path,
)


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
        for executable in sorted(folder.glob("*.exe")):
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


def _validate_packaged_runtime(application: BuiltApplication) -> None:
    """Require the known-good Qt runtime components."""

    webengine = list(
        application.app_root.rglob("QtWebEngineProcess.exe")
    )
    platform_plugins = list(
        application.app_root.rglob("qwindows.dll")
    )
    if not webengine:
        raise PortableBuildError(
            "QtWebEngineProcess.exe is missing from packaged output."
        )
    if not platform_plugins:
        raise PortableBuildError(
            "qwindows.dll is missing from packaged output."
        )

    print("PORTABLE QT WEBENGINE PROCESS: PASS")
    print("PORTABLE QT WINDOWS PLATFORM PLUGIN: PASS")


def _report_pyinstaller_warnings(paths: BuildPaths) -> None:
    """Report warning files without treating known optional warnings as fatal."""

    warning_files = sorted(
        paths.pyinstaller_work.rglob("warn-*.txt")
    )
    if not warning_files:
        print("PORTABLE PYINSTALLER WARNING FILE: NOT PRESENT")
        return

    print(f"PORTABLE PYINSTALLER WARNING FILE: {warning_files[0]}")
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in warning_files
    )
    marker = (
        "reasoner_context_collector.developer_tools"
        ".*collector_packaging_metadata"
    )
    normalized = combined.replace("\n", " ")
    if (
        "reasoner_context_collector.developer_tools"
        in normalized
        and "collector_packaging_metadata" in normalized
    ):
        print(
            "PORTABLE KNOWN DEVELOPER-TOOLS WARNING: "
            "PRESENT, RUNTIME VALIDATION REQUIRED"
        )
    else:
        print("PORTABLE PYINSTALLER WARNINGS: REVIEW FILE")


def build_application(paths: BuildPaths) -> BuiltApplication:
    """Build the canonical one-folder app outside source."""

    try:
        controls_before = validate_external_build_controls(
            paths.project_root, paths.project_root / "portable"
        )
    except ExternalControlError as exc:
        raise PortableBuildError(
            "EXTERNAL_BUILD_CONTROL_PRE_PYINSTALLER_REJECTED:" + str(exc)
        ) from exc
    print("PORTABLE EXTERNAL CONTROLS VERIFIED IMMEDIATELY BEFORE PYINSTALLER: PASS")

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

    try:
        controls_after = validate_external_build_controls(
            paths.project_root, paths.project_root / "portable"
        )
    except ExternalControlError as exc:
        raise PortableBuildError(
            "EXTERNAL_BUILD_CONTROL_POST_PYINSTALLER_REJECTED:" + str(exc)
        ) from exc
    if controls_after != controls_before:
        raise PortableBuildError(
            "EXTERNAL_BUILD_CONTROL_IDENTITY_CHANGED_DURING_PYINSTALLER"
        )
    print("PORTABLE EXTERNAL CONTROLS UNCHANGED THROUGH PYINSTALLER: PASS")

    application = _detect_built_application(paths)
    _validate_packaged_runtime(application)
    validate_packaged_worker_runtime(
        application.app_root,
        application.executable,
    )
    _report_pyinstaller_warnings(paths)
    print(f"PORTABLE PACKAGED APP ROOT: {application.app_root}")
    print(f"PORTABLE PACKAGED EXECUTABLE: {application.executable}")
    print("PORTABLE PYINSTALLER BUILD: PASS")
    print("PORTABLE BUILD PRODUCTS OUTSIDE PROJECT: PASS")
    return application


def _remove_non_runtime_debris(stage_app: Path) -> int:
    """Remove copied cache, editor debris, and backup files from staging."""

    removed = 0
    entries = sorted(
        stage_app.rglob("*"),
        key=lambda item: len(item.parts),
        reverse=True,
    )
    for entry in entries:
        relative = entry.relative_to(stage_app).as_posix()
        if not is_non_runtime_debris_path(relative):
            continue
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()
        removed += 1
    return removed


def _validate_stage_entry(
    entry: Path,
    stage_parent: Path,
) -> tuple[int, str]:
    relative = entry.relative_to(stage_parent).as_posix()
    path_bytes = len(relative.encode("utf-8"))

    if path_bytes > MAX_ARCHIVE_PATH_BYTES:
        raise PortableBuildError(
            f"Archive path is {path_bytes} bytes: {relative}"
        )
    if entry.is_symlink():
        raise PortableBuildError(
            f"Symlink found in staging: {relative}"
        )
    if entry.is_file() and entry.name.casefold().startswith(".env"):
        raise PortableBuildError(
            f"Environment credential file found in staging: {relative}"
        )
    if is_non_runtime_debris_path(relative):
        raise PortableBuildError(
            f"Non-runtime debris remained in staging: {relative}"
        )
    if is_generated_handoff_or_release_path(relative):
        raise PortableBuildError(
            f"Generated handoff/release artifact found in staging: {relative}"
        )
    if is_forbidden_tool_capture_path(relative):
        raise PortableBuildError(
            f"Forbidden external-Project capture found in staging: {relative}"
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
    hydrate_physical_runtime(paths.project_root, stage_app)

    removed_debris = _remove_non_runtime_debris(stage_app)
    print(
        "PORTABLE NON-RUNTIME BACKUP/CACHE DEBRIS REMOVED: "
        f"{removed_debris}"
    )

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
        evidence = _validate_stage_entry(
            entry,
            paths.stage_parent,
        )
        maximum = max(maximum, evidence)

    print(f"PORTABLE MAXIMUM ARCHIVE PATH: {maximum[0]} bytes")
    print(f"PORTABLE LONGEST ARCHIVE PATH: {maximum[1]}")
    validate_physical_runtime(stage_app)
    print("PORTABLE NON-RUNTIME DEBRIS ABSENT: PASS")
    print("PORTABLE GENERATED ARTIFACT PATH CLASSIFIER: PASS")
    print("PORTABLE STAGE CONTENTS: PASS")
    return stage_app
