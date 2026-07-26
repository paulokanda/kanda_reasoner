# project-path: tools/validate_reasoner_tools_gui_colorful_brain_icon_v1r3.py
"""Validate the colorful brain icon and GUI shell import compatibility."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
import os
from pathlib import Path
import struct
import sys
import zipfile

FEATURE_ID = "reasoner-tools-gui-colorful-brain-icon-v1r3"
EXPECTED_ICON_SHA256 = (
    "7222c2f171fc95538f85ae8bc4cf5a26f699ffdeca98b095439bef999dc9b62f"
)
EXPECTED_ICON_SIZES = {16, 20, 24, 32, 40, 48, 64, 128, 256}
APP_CONSTANTS = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/app_constants.py"
)
SHELL_ROOT = Path("kanda_reasoner_app/reasoner_tools_gui_shell")
LAUNCH = SHELL_ROOT / "launch.py"
MAIN_WINDOW = SHELL_ROOT / "main_window.py"
GUI_SUPPORT = SHELL_ROOT / "gui_support.py"
ICON = Path(
    "kanda_reasoner_app/reasoner_tools_gui_help/"
    "kanda_reasoner_color_icon.ico"
)
VALIDATOR = Path(
    "tools/validate_reasoner_tools_gui_colorful_brain_icon_v1r3.py"
)
RELEASE_SCRIPTS = ("INSTALL.ps1", "VALIDATE.ps1", "FREEZE.ps1")
EXPECTED_PREDECESSOR_HASHES = {
    "1efedcac41d3f729d701500f54118b59eae5c61bc1891c70f3298ff228768f92",
    "b38e89f1277b3d50d0bfb5eb70fce8624514d915e9e008b7dbe516530e7cf426",
}


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


def _module_defined_names(tree: ast.Module) -> set[str]:
    """Collect names made available by one module at import time."""
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name != "*":
                    names.add(alias.asname or alias.name)
    return names


def _app_constant_consumers(root: Path) -> dict[str, set[str]]:
    """Return direct app_constants imports from all GUI shell modules."""
    consumers: dict[str, set[str]] = {}
    shell_path = root / SHELL_ROOT
    for path in sorted(shell_path.rglob("*.py")):
        relative = path.relative_to(root).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        imported: set[str] = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if node.module != "app_constants" or node.level < 1:
                continue
            imported.update(
                alias.name for alias in node.names if alias.name != "*"
            )
        if imported:
            consumers[relative] = imported
    return consumers


def _validate_python_sources(root: Path) -> None:
    """Validate source and private compatibility contracts."""
    constants = _read_text(root, APP_CONSTANTS)
    launch = _read_text(root, LAUNCH)
    main_window = _read_text(root, MAIN_WINDOW)
    gui_support = _read_text(root, GUI_SUPPORT)

    parsed_constants = ast.parse(constants, filename=str(APP_CONSTANTS))
    for relative, source in (
        (LAUNCH, launch),
        (MAIN_WINDOW, main_window),
        (GUI_SUPPORT, gui_support),
    ):
        ast.parse(source, filename=str(relative))

    required_constants = (
        "from kanda_reasoner_app.project_root_resolver import ",
        "resolve_app_runtime_root",
        "_PROJECT_ROOT = resolve_app_runtime_root()",
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

    defined_names = _module_defined_names(parsed_constants)
    consumers = _app_constant_consumers(root)
    if not consumers:
        raise AssertionError("APP_CONSTANTS_CONSUMER_INVENTORY_EMPTY")
    missing: list[str] = []
    for relative, names in consumers.items():
        for name in sorted(names):
            if name not in defined_names:
                missing.append(relative + ":" + name)
    if missing:
        raise AssertionError(
            "APP_CONSTANTS_CONSUMER_IMPORT_MISSING: " + ", ".join(missing)
        )
    if "_PROJECT_ROOT" not in defined_names:
        raise AssertionError("PRIVATE_PROJECT_ROOT_COMPATIBILITY_MISSING")

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

    print("APP_CONSTANTS_CONSUMER_SURFACE: PASS")
    print("PRIVATE_PROJECT_ROOT_COMPATIBILITY: PASS")
    print("WINDOW_TITLE_BAR_ICON_CONTRACT: PASS")
    print("WINDOWS_TASKBAR_ICON_CONTRACT: PASS")


def _clear_shell_modules() -> None:
    """Remove shell modules so the selected root is imported fresh."""
    prefixes = (
        "kanda_reasoner_app.reasoner_tools_gui_shell",
        "kanda_reasoner_app",
    )
    for name in list(sys.modules):
        if name == prefixes[1] or name.startswith(prefixes[0]):
            sys.modules.pop(name, None)


def _validate_resolved_icon_path(root: Path) -> Path:
    """Resolve APP_ICON_PATH through the real application constants module."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    _clear_shell_modules()
    module = importlib.import_module(
        "kanda_reasoner_app.reasoner_tools_gui_shell.app_constants"
    )
    if not hasattr(module, "_PROJECT_ROOT"):
        raise AssertionError("APP_CONSTANTS_RUNTIME_PROJECT_ROOT_MISSING")
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


def _validate_gui_shell_import_smoke(
    root: Path,
    allow_missing_pyside6: bool,
) -> None:
    """Import the real shell modules to catch import-time compatibility loss."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    _clear_shell_modules()
    modules = (
        "kanda_reasoner_app.reasoner_tools_gui_shell.gui_support",
        "kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_help",
        "kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_state",
        "kanda_reasoner_app.reasoner_tools_gui_shell.main_window",
        "kanda_reasoner_app.reasoner_tools_gui_shell.launch",
    )
    try:
        for module_name in modules:
            importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        if allow_missing_pyside6 and exc.name and exc.name.startswith("PySide6"):
            print("GUI_SHELL_IMPORT_COMPATIBILITY: SKIPPED - PySide6 unavailable")
            return
        raise
    print("GUI_SHELL_IMPORT_COMPATIBILITY: PASS")


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
    sizes = {size.width() for size in window.windowIcon().availableSizes()}
    if not {16, 32, 48}.issubset(sizes):
        raise AssertionError("QT_MAIN_WINDOW_ICON_SIZES_INCOMPLETE")

    print("QT_ICON_RUNTIME: PASS")
    print("QT_MAIN_WINDOW_ICON_RUNTIME: PASS")


def _validate_release_scripts(archive: zipfile.ZipFile) -> None:
    """Reject hidden control characters and malformed validator paths."""
    for member in RELEASE_SCRIPTS:
        data = archive.read(member)
        invalid = [
            value
            for value in data
            if value < 32 and value not in (9, 10, 13)
        ]
        if invalid:
            raise AssertionError(
                "POWERSHELL_CONTROL_CHARACTER_FOUND: "
                + member
                + ": "
                + ",".join(str(value) for value in sorted(set(invalid)))
            )
        data.decode("ascii")

    validate_text = archive.read("VALIDATE.ps1").decode("ascii")
    required_paths = (
        "tools/validate_reasoner_tools_gui_colorful_brain_icon_v1r3.py",
        "scripts/validate_patch_zip.py",
    )
    for path_text in required_paths:
        if path_text not in validate_text:
            raise AssertionError(
                "VALIDATOR_PATH_LITERAL_MISSING: " + path_text
            )

    print("POWERSHELL_CONTROL_CHARACTER_GUARD: PASS")
    print("VALIDATOR_PATH_LITERAL_CONTRACT: PASS")


def _validate_predecessor_hashes(archive: zipfile.ZipFile) -> None:
    """Confirm the cumulative installer accepts governed predecessor states."""
    manifest = json.loads(archive.read("INSTALL_MANIFEST.json"))
    rows = {item["path"]: item for item in manifest["files"]}
    row = rows.get(APP_CONSTANTS.as_posix())
    if row is None:
        raise AssertionError("APP_CONSTANTS_MANIFEST_ROW_MISSING")
    allowed = {str(value).lower() for value in row["accepted_existing_sha256"]}
    missing = EXPECTED_PREDECESSOR_HASHES - allowed
    if missing:
        raise AssertionError(
            "CUMULATIVE_PREDECESSOR_HASH_MISSING: "
            + ",".join(sorted(missing))
        )
    print("CUMULATIVE_PREDECESSOR_HASH_ALLOWLIST: PASS")


def _validate_patch_zip(patch_zip: Path) -> None:
    """Confirm that the patch ZIP carries the cumulative repair payload."""
    expected = {
        "payload/" + APP_CONSTANTS.as_posix(),
        "payload/" + LAUNCH.as_posix(),
        "payload/" + ICON.as_posix(),
        "payload/" + VALIDATOR.as_posix(),
        "INSTALL.ps1",
        "VALIDATE.ps1",
        "FREEZE.ps1",
        "INSTALL_MANIFEST.json",
        "KANDA_FREEZE_HINT.json",
        "README.txt",
    }
    with zipfile.ZipFile(patch_zip, "r") as archive:
        names = set(archive.namelist())
        missing = sorted(expected - names)
        if missing:
            raise AssertionError("PATCH_PAYLOAD_MISSING: " + ", ".join(missing))
        _validate_release_scripts(archive)
        _validate_predecessor_hashes(archive)
    print("PATCH_ICON_IMPORT_REPAIR_PAYLOAD: PASS")


def main() -> int:
    """Run the focused colorful brain icon regression checks."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--patch-zip")
    parser.add_argument("--allow-missing-pyside6", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    _validate_python_sources(root)
    icon_path = _validate_resolved_icon_path(root)
    _validate_gui_shell_import_smoke(root, args.allow_missing_pyside6)
    _validate_icon_asset(icon_path)
    _validate_qt_icon_runtime(icon_path, args.allow_missing_pyside6)
    if args.patch_zip:
        _validate_patch_zip(Path(args.patch_zip).resolve())

    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
