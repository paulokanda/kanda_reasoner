"""Environment, specification, confirmation, and collision controls."""

from __future__ import annotations

import ast
import importlib.metadata
import re
import struct
import sys
from pathlib import Path

from portable.constants import (
    BUILDER_VERSION,
    EXPECTED_PYINSTALLER,
    EXPECTED_PYTHON,
    FEATURE_ID,
    FINAL_ZIP_NAME,
    VENV_PYTHON_RELATIVE,
)
from portable.errors import PortableBuildError
from portable.external_controls import (
    ExternalControlError,
    validate_external_build_controls,
)
from portable.models import BuildPaths


_REQUIRED_SPEC_TOKENS = (
    "reasoner_tools_gui.py",
    "collect_submodules",
    "iter_packaged_resource_files",
    "validate_registered_synthetic_fixtures",
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebChannel",
    "build_worker_runtime_binaries",
    "build_worker_runtime_hooks",
)

_FORBIDDEN_SPEC_TOKENS = (
    "PyCharm",
    ".venv",
)

_PROHIBITED_SPEC_PACKAGING_TOKENS = (
    "collect_data_files",
)
_WINDOWS_ABSOLUTE_PATH_RE = re.compile(
    r"(?i)(?:^|[\s(])(?:[a-z]:[\\/]|\\\\[a-z0-9_.-]+[\\/])"
)


def _machine_specific_windows_literals(source: str) -> list[str]:
    """Return decoded string literals containing absolute Windows paths."""

    tree = ast.parse(source, filename="KandaReasonerWindows.spec")
    matches: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if _WINDOWS_ABSOLUTE_PATH_RE.search(node.value):
            matches.append(node.value)
    return matches


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


def _audited_governed_python(project_root: Path) -> Path:
    """Resolve the Tool-owned virtual-environment Python."""

    project = project_root.resolve()
    governed = (project / VENV_PYTHON_RELATIVE).resolve()
    try:
        governed.relative_to(project)
    except ValueError as exc:
        raise PortableBuildError(
            "Governed Tool virtual-environment Python escaped Tool root."
        ) from exc
    return governed


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

    prohibited = [
        token
        for token in _PROHIBITED_SPEC_PACKAGING_TOKENS
        if token in source
    ]
    if prohibited:
        raise PortableBuildError(
            "Canonical PyInstaller specification contains prohibited "
            f"package-wide data collection: {prohibited}"
        )

    forbidden = [
        token
        for token in _FORBIDDEN_SPEC_TOKENS
        if token.casefold() in source.casefold()
    ]
    if _machine_specific_windows_literals(source):
        forbidden.append("absolute_windows_path_literal")
    if forbidden:
        raise PortableBuildError(
            "Canonical PyInstaller specification contains machine-specific "
            f"development paths: {forbidden}"
        )

    print("PORTABLE CANONICAL SPECIFICATION: PASS")
    print("PORTABLE SPEC MACHINE-SPECIFIC PATHS: ABSENT")
    print("PORTABLE QT WEBENGINE SPEC CONTRACT: PASS")
    print("PORTABLE SPEC TOOL DATA ALLOWLIST OWNER: PASS")
    print("PORTABLE SPEC PACKAGE-WIDE DATA COLLECTION: ABSENT")


def require_environment(paths: BuildPaths) -> dict[str, object]:
    """Require the audited governed Python and PyInstaller."""

    governed = _audited_governed_python(paths.project_root)
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
            "PyInstaller is not installed in the KANDA Tool .venv Python."
        ) from exc

    if version != EXPECTED_PYINSTALLER:
        raise PortableBuildError(
            f"PyInstaller {EXPECTED_PYINSTALLER} is required; found {version}."
        )

    audit_spec_contract(paths)
    print(f"GOVERNED PYTHON PATH: {governed}")
    print("PORTABLE TOOL VENV PYTHON: PASS")
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
