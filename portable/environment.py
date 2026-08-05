"""Environment, specification, confirmation, and collision controls."""

from __future__ import annotations

import importlib.metadata
import os
import struct
import sys
from pathlib import Path

from portable.constants import (
    BUILDER_VERSION,
    EXPECTED_PYINSTALLER,
    EXPECTED_PYTHON,
    FEATURE_ID,
    FINAL_ZIP_NAME,
)
from portable.errors import PortableBuildError
from portable.external_controls import (
    ExternalControlError,
    validate_external_build_controls,
)
from portable.models import BuildPaths


_REQUIRED_SPEC_TOKENS = (
    "reasoner_tools_gui.py",
    "collect_data_files",
    "collect_submodules",
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebChannel",
    "collector_main_help",
)

_FORBIDDEN_SPEC_TOKENS = (
    "E:\\kanda_reasoner",
    "C:\\Users\\paulo",
    "PyCharm",
    ".venv",
)


def print_builder_identity() -> None:
    """Print the installed creator identity before any long-running work."""

    print(f"PORTABLE BUILDER VERSION: {BUILDER_VERSION}")
    print(f"PORTABLE BUILDER FEATURE ID: {FEATURE_ID}")


def confirm_explicit_request(skip_confirmation: bool) -> None:
    """Require explicit human authorization for Portable creation."""

    if skip_confirmation:
        print("PORTABLE EXPLICIT USER REQUEST: PASS (--yes)")
        return

    print(
        "Independent Portable workflow. "
        "Show Project to AI will not be invoked."
    )
    answer = input(
        "Type BUILD KANDA PORTABLE to continue: "
    ).strip()
    if answer.casefold() != "build kanda portable":
        raise PortableBuildError(
            "Explicit Portable-build confirmation was denied."
        )
    print("PORTABLE EXPLICIT USER REQUEST: PASS")


def _audited_governed_python() -> Path:
    """Resolve the explicit governed KANDA Python 3.12 owner."""

    local_app_data = os.environ.get("LOCALAPPDATA", "").strip()
    if not local_app_data:
        raise PortableBuildError(
            "LOCALAPPDATA is unavailable; governed Python cannot be resolved."
        )
    return (
        Path(local_app_data)
        / "Programs"
        / "Python"
        / "Python312"
        / "python.exe"
    ).resolve()


def audit_spec_contract(paths: BuildPaths) -> None:
    """Validate the committed specification before PyInstaller starts."""

    try:
        source = paths.spec_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source = paths.spec_path.read_text(encoding="utf-8-sig")

    missing = [
        token
        for token in _REQUIRED_SPEC_TOKENS
        if token not in source
    ]
    if missing:
        raise PortableBuildError(
            "Canonical PyInstaller specification is missing required "
            f"contracts: {missing}"
        )

    forbidden = [
        token
        for token in _FORBIDDEN_SPEC_TOKENS
        if token.casefold() in source.casefold()
    ]
    if forbidden:
        raise PortableBuildError(
            "Canonical PyInstaller specification contains machine-specific "
            f"development paths: {forbidden}"
        )

    print("PORTABLE CANONICAL SPECIFICATION: PASS")
    print("PORTABLE SPEC MACHINE-SPECIFIC PATHS: ABSENT")
    print("PORTABLE QT WEBENGINE SPEC CONTRACT: PASS")
    print("PORTABLE PHYSICAL HELP DATA CONTRACT: PASS")


def require_environment(paths: BuildPaths) -> dict[str, object]:
    """Require the audited governed Python and PyInstaller."""

    governed = _audited_governed_python()
    current = Path(sys.executable).resolve()

    if not governed.is_file():
        raise PortableBuildError(
            f"Governed Python not found: {governed}"
        )
    if current != governed:
        raise PortableBuildError(
            "Run with the audited governed KANDA interpreter:\n"
            f"{governed} "
            f"{paths.project_root / 'portable' / 'create_kanda_reasoner_portable.py'}"
        )
    if paths.governed_python.resolve() != governed:
        raise PortableBuildError(
            "Resolved build interpreter does not match governed Python."
        )
    if sys.version_info[:2] != EXPECTED_PYTHON:
        raise PortableBuildError(
            "Python 3.12 is required; found "
            f"{sys.version.split()[0]}."
        )
    if struct.calcsize("P") * 8 != 64:
        raise PortableBuildError(
            "A 64-bit Python interpreter is required."
        )
    if not paths.spec_path.is_file():
        raise PortableBuildError(
            f"Canonical spec not found: {paths.spec_path}"
        )
    if not paths.zip_helper.is_file():
        raise PortableBuildError(
            f"Windows ZIP helper not found: {paths.zip_helper}"
        )

    try:
        external_controls = validate_external_build_controls(
            paths.project_root, paths.project_root / "portable"
        )
    except ExternalControlError as exc:
        raise PortableBuildError(
            "EXTERNAL_BUILD_CONTROL_PREFLIGHT_REJECTED:" + str(exc)
        ) from exc
    print("PORTABLE EXTERNAL BUILD CONTROL PREFLIGHT: PASS")
    print(
        "PORTABLE EXTERNAL BUILD CONTROL ITEM COUNT: "
        f"{external_controls['item_count']}"
    )
    print("PORTABLE EXTERNAL BUILD CONTROL EXACT SHA-256: PASS")
    try:
        version = importlib.metadata.version("pyinstaller")
    except importlib.metadata.PackageNotFoundError as exc:
        raise PortableBuildError(
            "PyInstaller is not installed in governed Python 3.12."
        ) from exc

    if version != EXPECTED_PYINSTALLER:
        raise PortableBuildError(
            f"PyInstaller {EXPECTED_PYINSTALLER} is required; found {version}."
        )

    audit_spec_contract(paths)
    print(f"GOVERNED PYTHON PATH: {governed}")
    print(f"PORTABLE PYTHON: {sys.version.split()[0]} 64-bit")
    print(f"PORTABLE PYINSTALLER: {version}")
    print("PORTABLE GOVERNED PYTHON IDENTITY: PASS")
    return external_controls


def check_output_collision(
    paths: BuildPaths,
    replace_existing: bool,
) -> None:
    """Fail closed when a final Portable already exists."""

    misplaced = paths.project_root / FINAL_ZIP_NAME
    if misplaced.exists():
        print("WARNING: Misplaced existing Portable will not be touched:")
        print(misplaced)

    if not paths.final_zip.exists():
        return

    if not replace_existing:
        raise PortableBuildError(
            "Selected-folder Portable already exists. Use --replace-existing "
            "only after approving replacement:\n"
            f"{paths.final_zip}"
        )

    answer = input(
        "Type REPLACE KANDA PORTABLE to authorize replacement: "
    ).strip()
    if answer.casefold() != "replace kanda portable":
        raise PortableBuildError(
            "Existing Portable replacement was not authorized."
        )
    print("PORTABLE EXISTING OUTPUT REPLACEMENT: AUTHORIZED")
