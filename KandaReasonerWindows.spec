# -*- mode: python ; coding: utf-8 -*-
"""Governed PyInstaller specification for the KANDA Reasoner Tool.

Non-Python data is selected through the Release 3 Tool-source classification
manifest.  The specification intentionally does not use package-wide
the package-wide PyInstaller data collector because that previously made any
unregistered file beneath the package eligible for Portable distribution.
"""

from __future__ import annotations

from pathlib import Path
import importlib

from PyInstaller.utils.hooks import collect_submodules

from portable.packaged_worker_runtime import (
    build_worker_runtime_binaries,
    build_worker_runtime_hooks,
)

from kanda_reasoner_app.source_hygiene.tool_archive_policy import (
    ToolArchivePolicyError,
    is_project_capture_forbidden_relative,
    iter_packaged_resource_files,
    validate_registered_synthetic_fixtures,
)


TOOL_ROOT = Path(SPECPATH).resolve()
APPLICATION_NAME = "kanda_reasoner"
ENTRYPOINT = "reasoner_tools_gui.py"

_BASE_HIDDEN_IMPORTS = [
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebChannel",
    "reasoner_tools_gui_engineering_safety_panel",
    "_reasoner_tools_gui_engineering_safety_panel_catalog",
    "_reasoner_tools_gui_engineering_safety_panel_commands",
    "_reasoner_tools_gui_engineering_safety_full_audit",
    "_reasoner_tools_gui_engineering_safety_sonar",
    "_reasoner_tools_gui_ruff_correction_dialog",
]


def _normalized_destination(destination: str) -> str:
    return str(destination).replace("\\", "/").strip("/")


def _build_allowlisted_datas() -> list[tuple[str, str]]:
    """Return deterministic resource tuples from the Tool policy owner."""
    validate_registered_synthetic_fixtures(TOOL_ROOT)
    try:
        records = iter_packaged_resource_files(TOOL_ROOT)
    except ToolArchivePolicyError as exc:
        raise RuntimeError(
            "PYINSTALLER_DATA_ALLOWLIST_REJECTED:" + str(exc)
        ) from exc
    return sorted(
        records,
        key=lambda item: (
            _normalized_destination(item[1]).casefold(),
            str(item[0]).replace("\\", "/").casefold(),
        ),
    )


def _validate_allowlisted_datas(
    records: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    """Reject duplicates, paths outside Tool root, and capture destinations."""
    if not records:
        raise RuntimeError("PYINSTALLER_DATA_ALLOWLIST_EMPTY")
    seen: set[tuple[str, str]] = set()
    validated: list[tuple[str, str]] = []
    for source_text, destination_text in records:
        source = Path(source_text).expanduser().resolve(strict=False)
        try:
            relative_source = source.relative_to(TOOL_ROOT).as_posix()
        except ValueError as exc:
            raise RuntimeError(
                "PYINSTALLER_DATA_SOURCE_OUTSIDE_TOOL_ROOT:" + str(source)
            ) from exc
        destination = _normalized_destination(destination_text)
        if is_project_capture_forbidden_relative(relative_source):
            raise RuntimeError(
                "PYINSTALLER_PROJECT_CAPTURE_SOURCE_REJECTED:"
                + relative_source
            )
        packaged_relative = (
            destination + "/" + source.name
            if destination
            else source.name
        )
        if is_project_capture_forbidden_relative(packaged_relative):
            raise RuntimeError(
                "PYINSTALLER_PROJECT_CAPTURE_DESTINATION_REJECTED:"
                + packaged_relative
            )
        key = (str(source).casefold(), destination.casefold())
        if key in seen:
            raise RuntimeError(
                "PYINSTALLER_DATA_DUPLICATE_REJECTED:" + relative_source
            )
        seen.add(key)
        validated.append((str(source), destination))
    return validated


def _validate_submodule_import_preflight() -> None:
    """Fail before collection if the known ML advisory facade is broken."""
    module = importlib.import_module(
        "kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal"
    )
    required = (
        "FORBIDDEN_RUNTIME_APP_HOST_VISIBILITY_CAPABILITIES",
        "REQUIRED_RUNTIME_APP_HOST_VISIBILITY_CONTRACT_LABELS",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise RuntimeError(
            "PYINSTALLER_SUBMODULE_IMPORT_PREFLIGHT_MISSING:" + ",".join(missing)
        )
    print("PORTABLE PYINSTALLER SUBMODULE IMPORT PREFLIGHT: PASS")


def _build_hidden_imports() -> list[str]:
    """Return stable explicit and package-discovered Python imports."""
    _validate_submodule_import_preflight()
    discovered = collect_submodules("kanda_reasoner_app")
    return sorted(set(_BASE_HIDDEN_IMPORTS + discovered), key=str.casefold)


datas = _validate_allowlisted_datas(_build_allowlisted_datas())
hiddenimports = _build_hidden_imports()


worker_runtime_binaries = build_worker_runtime_binaries(TOOL_ROOT)
worker_runtime_hooks = build_worker_runtime_hooks(TOOL_ROOT)


a = Analysis(
    [ENTRYPOINT],
    pathex=[str(TOOL_ROOT)],
    binaries=worker_runtime_binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=worker_runtime_hooks,
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APPLICATION_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APPLICATION_NAME,
)
