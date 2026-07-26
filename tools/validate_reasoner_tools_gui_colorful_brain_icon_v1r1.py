# project-path: tools/validate_reasoner_tools_gui_colorful_brain_icon_v1r1.py
"""Validate the corrected KANDA Reasoner colorful brain icon path."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import os
from pathlib import Path
import struct
import sys
import zipfile

FEATURE_ID = "reasoner-tools-gui-colorful-brain-icon-v1r1"
EXPECTED_ICON_SHA256 = (
    "7222c2f171fc95538f85ae8bc4cf5a26f699ffdeca98b095439bef999dc9b62f"
)
EXPECTED_ICON_SIZES = {16, 20, 24, 32, 40, 48, 64, 128, 256}

APP_CONSTANTS = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/app_constants.py"
)
LAUNCH = Path("kanda_reasoner_app/reasoner_tools_gui_shell/launch.py")
MAIN_WINDOW = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py"
)
ICON = Path(
    "kanda_reasoner_app/reasoner_tools_gui_help/"
    "kanda_reasoner_color_icon.ico"
)
VALIDATOR = Path(
    "tools/validate_reasoner_tools_gui_colorful_brain_icon_v1r1.py"
)


def _read_text(root: Path, relative: Path) -> str:
    """Read one UTF-8 source file from the selected project root."""
    return (root / relative).read_text(encoding="utf-8")


def _sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest for one file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _ico_sizes(path: Path) -> set[int]:
    """Read square image sizes declared by a Windows ICO directory."""
    data = path.read_bytes()
    if len(data) < 6:
        raise AssertionError("ICON_FILE_TOO_SMALL")

    reserved, icon_type, image_count = struct.unpack_from("<HHH", data, 0)
    if reserved != 0 or icon_type != 1:
        raise AssertionError("ICON_DIRECTORY_INVALID")
    if image_count < len(EXPECTED_ICON_SIZES):
        raise AssertionError("ICON_SIZE_COUNT_INSUFFICIENT")

    sizes: set[int] = set()
    directory_end = 6 + (image_count * 16)
    if directory_end > len(data):
        raise AssertionError("ICON_DIRECTORY_TRUNCATED")

    for index in range(image_count):
        offset = 6 + (index * 16)
        width_raw, height_raw, _, _, planes, bits, byte_count, image_offset = (
            struct.unpack_from("<BBBBHHII", data, offset)
        )
        width = 256 if width_raw == 0 else width_raw
        height = 256 if height_raw == 0 else height_raw
        if width != height:
            raise AssertionError("ICON_ENTRY_NOT_SQUARE")
        if planes not in (0, 1):
            raise AssertionError("ICON_ENTRY_PLANES_INVALID")
        if bits not in (0, 32):
            raise AssertionError("ICON_ENTRY_BIT_DEPTH_INVALID")
        if image_offset < directory_end:
            raise AssertionError("ICON_ENTRY_OFFSET_INVALID")
        if image_offset + byte_count > len(data):
            raise AssertionError("ICON_ENTRY_TRUNCATED")
        sizes.add(width)

    return sizes


def _validate_python_sources(root: Path) -> None:
    """Validate source-level application and window icon contracts."""
    constants = _read_text(root, APP_CONSTANTS)
    launch = _read_text(root, LAUNCH)
    main_window = _read_text(root, MAIN_WINDOW)

    for relative, source in (
        (APP_CONSTANTS, constants),
        (LAUNCH, launch),
        (MAIN_WINDOW, main_window),
    ):
        ast.parse(source, filename=str(relative))

    required_constants = (
        "_PACKAGE_ROOT = Path(__file__).resolve().parents[1]",
        '"reasoner_tools_gui_help"',
        '"kanda_reasoner_color_icon.ico"',
    )
    for fragment in required_constants:
        if fragment not in constants:
            raise AssertionError(
                "APP_CONSTANTS_CONTRACT_MISSING: " + fragment
            )
    if "LEGACY_PACKAGE_NAME" in constants:
        raise AssertionError("APP_ICON_PATH_STILL_USES_LEGACY_PACKAGE")

    required_launch = (
        '_WINDOWS_APP_USER_MODEL_ID = "KANDA.Reasoner.Desktop"',
        "_set_windows_app_user_model_id()",
        "SetCurrentProcessExplicitAppUserModelID",
        "app.setWindowIcon(QIcon(str(APP_ICON_PATH)))",
        "app.setApplicationDisplayName(APP_DISPLAY_NAME)",
    )
    for fragment in required_launch:
        if fragment not in launch:
            raise AssertionError("LAUNCH_ICON_CONTRACT_MISSING: " + fragment)

    app_id_index = launch.find("_set_windows_app_user_model_id()")
    app_create_index = launch.find(
        "app = QApplication.instance() or QApplication(sys.argv)"
    )
    if app_id_index < 0 or app_create_index < 0:
        raise AssertionError("WINDOWS_APP_ID_ORDER_UNRESOLVED")
    if app_id_index > app_create_index:
        raise AssertionError("WINDOWS_APP_ID_SET_TOO_LATE")

    if "self.setWindowIcon(QIcon(str(APP_ICON_PATH)))" not in main_window:
        raise AssertionError("MAIN_WINDOW_ICON_CONTRACT_MISSING")

    print("WINDOW_TITLE_BAR_ICON_CONTRACT: PASS")
    print("WINDOWS_TASKBAR_ICON_CONTRACT: PASS")


def _clear_icon_modules() -> None:
    """Remove icon-owner modules so the selected root is imported fresh."""
    names = (
        "kanda_reasoner_app.reasoner_tools_gui_shell.app_constants",
        "kanda_reasoner_app.reasoner_tools_gui_shell",
        "kanda_reasoner_app",
    )
    for name in names:
        sys.modules.pop(name, None)


def _validate_resolved_icon_path(root: Path) -> Path:
    """Resolve APP_ICON_PATH through the real application module."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    _clear_icon_modules()
    module = importlib.import_module(
        "kanda_reasoner_app.reasoner_tools_gui_shell.app_constants"
    )
    resolved = Path(module.APP_ICON_PATH).resolve()
    expected = (root / ICON).resolve()
    if resolved != expected:
        raise AssertionError(
            "APP_ICON_RUNTIME_PATH_MISMATCH: "
            + str(resolved)
            + " != "
            + str(expected)
        )
    if not resolved.is_file():
        raise AssertionError("APP_ICON_RUNTIME_PATH_MISSING: " + str(resolved))
    if "ask_ai_project_reasoner" in resolved.as_posix():
        raise AssertionError("APP_ICON_RUNTIME_PATH_LEGACY_OWNER")
    print("APP_ICON_RUNTIME_PATH: PASS")
    print("CANONICAL_ICON_OWNER: PASS")
    return resolved


def _validate_icon_asset(icon_path: Path) -> None:
    """Validate the exact colorful brain ICO and multi-size inventory."""
    if _sha256(icon_path) != EXPECTED_ICON_SHA256:
        raise AssertionError("COLORFUL_BRAIN_ICON_HASH_MISMATCH")

    sizes = _ico_sizes(icon_path)
    missing_sizes = sorted(EXPECTED_ICON_SIZES - sizes)
    if missing_sizes:
        missing_text = ", ".join(str(item) for item in missing_sizes)
        raise AssertionError("COLORFUL_BRAIN_ICON_SIZE_MISSING: " + missing_text)

    print("COLORFUL_BRAIN_ICON_ASSET: PASS")
    print("MULTI_SIZE_WINDOWS_ICO: PASS")


def _validate_qt_icon_runtime(
    icon_path: Path,
    allow_missing_pyside6: bool,
) -> None:
    """Load the resolved icon through Qt and a real QMainWindow object."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtGui import QIcon
        from PySide6.QtWidgets import QApplication, QMainWindow
    except ImportError as exc:
        if allow_missing_pyside6:
            print("QT_ICON_RUNTIME: SKIPPED - PySide6 unavailable")
            print("QT_MAIN_WINDOW_ICON_RUNTIME: SKIPPED - PySide6 unavailable")
            return
        raise AssertionError("PYSIDE6_REQUIRED_FOR_QT_ICON_RUNTIME") from exc

    app = QApplication.instance() or QApplication([])
    icon = QIcon(str(icon_path))
    if icon.isNull():
        raise AssertionError("QT_ICON_RUNTIME_NULL")
    app.setWindowIcon(icon)
    if app.windowIcon().isNull():
        raise AssertionError("QT_APPLICATION_ICON_RUNTIME_NULL")

    window = QMainWindow()
    window.setWindowIcon(icon)
    if window.windowIcon().isNull():
        raise AssertionError("QT_MAIN_WINDOW_ICON_RUNTIME_NULL")
    available_sizes = {size.width() for size in window.windowIcon().availableSizes()}
    if not {16, 32, 48}.issubset(available_sizes):
        raise AssertionError("QT_MAIN_WINDOW_ICON_SIZES_INCOMPLETE")

    print("QT_ICON_RUNTIME: PASS")
    print("QT_MAIN_WINDOW_ICON_RUNTIME: PASS")


def _validate_patch_zip(patch_zip: Path) -> None:
    """Confirm that the patch ZIP carries the corrected icon owner payload."""
    expected = {
        "payload/" + APP_CONSTANTS.as_posix(),
        "payload/" + LAUNCH.as_posix(),
        "payload/" + ICON.as_posix(),
        "payload/" + VALIDATOR.as_posix(),
    }
    with zipfile.ZipFile(patch_zip, "r") as archive:
        names = set(archive.namelist())
        missing = sorted(expected - names)
        if missing:
            raise AssertionError("PATCH_PAYLOAD_MISSING: " + ", ".join(missing))
        icon_bytes = archive.read("payload/" + ICON.as_posix())
        icon_hash = hashlib.sha256(icon_bytes).hexdigest()
        if icon_hash != EXPECTED_ICON_SHA256:
            raise AssertionError("PATCH_ICON_HASH_MISMATCH")
        constants_text = archive.read(
            "payload/" + APP_CONSTANTS.as_posix()
        ).decode("utf-8")
        if "LEGACY_PACKAGE_NAME" in constants_text:
            raise AssertionError("PATCH_APP_CONSTANTS_STILL_LEGACY")
    print("PATCH_ICON_PATH_REPAIR_PAYLOAD: PASS")


def main() -> int:
    """Run focused source, runtime-path, asset, Qt, and package checks."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--patch-zip")
    parser.add_argument("--allow-missing-pyside6", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    _validate_python_sources(root)
    icon_path = _validate_resolved_icon_path(root)
    _validate_icon_asset(icon_path)
    _validate_qt_icon_runtime(icon_path, args.allow_missing_pyside6)
    if args.patch_zip:
        _validate_patch_zip(Path(args.patch_zip).expanduser().resolve())

    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
