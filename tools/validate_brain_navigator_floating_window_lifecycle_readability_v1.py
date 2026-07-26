# project-path: tools/validate_brain_navigator_floating_window_lifecycle_readability_v1.py
"""Validate Brain Navigator floating-window cleanup and readable typography."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import py_compile
import sys
from pathlib import Path

from brain_navigator_lifecycle_qt_probe import (
    validate_real_qt_tab_hide,
    validate_simulated_tab_hide,
)

__all__ = ["main"]

FEATURE_ID = "brain-navigator-floating-window-lifecycle-readability-v1r6"
MAX_CODE_LINES = 500
TEMPLATE_PATH = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/"
    "assets/brain_visual_floating_window_template.py"
)
PREVIEW_PATH = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/"
    "_neural_architecture_preview.py"
)
MANIFEST_PATH = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/"
    "box_manifest.json"
)
README_PATH = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/README.md"
)
CATALOG_VALIDATOR_PATH = "tools/validate_brain_navigator_tab_catalog_sync_v1.py"
VALIDATOR_PATH = (
    "tools/validate_brain_navigator_floating_window_lifecycle_readability_v1.py"
)
QT_PROBE_PATH = "tools/brain_navigator_lifecycle_qt_probe.py"
TOUCHED_PYTHON = (TEMPLATE_PATH, PREVIEW_PATH, VALIDATOR_PATH, QT_PROBE_PATH)


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""

    if not condition:
        raise AssertionError(message)


def read_text(root: Path, relative: str) -> str:
    """Read one required project file."""

    path = root / relative
    require(path.is_file(), "missing required file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_source_contract(root: Path) -> None:
    """Validate readable CSS and page-local transient cleanup wiring."""

    template = read_text(root, TEMPLATE_PATH)
    preview = read_text(root, PREVIEW_PATH)

    required_font_fragments = (
        "font-family: 'Segoe UI', Arial, sans-serif;",
        "font-size: 20px;",
        "font-size: 14px;",
        "font-size: 12px;",
        "font-size: 11px;",
    )
    for fragment in required_font_fragments:
        require(fragment in template, "missing readable font fragment: " + fragment)
    require(
        template.count("font-family: 'Segoe UI', Arial, sans-serif;") >= 2,
        "system font stack must style the window and its action button",
    )
    require("Courier New" not in template, "low-readability monospace font remains")
    require("color: #0a1d45;" in template, "title contrast contract changed")
    require("color: #182c55;" in template, "body contrast contract changed")
    print("FLOATING_WINDOW_READABLE_SYSTEM_FONT: PASS")
    print("FLOATING_WINDOW_HIGH_CONTRAST_TEXT: PASS")

    action_fragments = (
        "const delivered = callBrainBridgeOpenModule(windowData.region_id);",
        "if (delivered) {",
        "hideFloatingRememberWindow();",
    )
    for fragment in action_fragments:
        require(fragment in template, "missing successful navigation cleanup: " + fragment)
    print("OPEN_MODULE_SUCCESS_CLOSES_FLOATING_WINDOW: PASS")

    preview_fragments = (
        "_CLOSE_FLOATING_WINDOW_JS",
        "def _request_floating_window_close",
        "def hideEvent(self, event: object) -> None:",
        'getattr(self, "_brain_navigator_web_view", None)',
        "page.runJavaScript(_CLOSE_FLOATING_WINDOW_JS)",
        'setattr(widget, "_brain_navigator_web_view", web_view)',
        "except (AttributeError, RuntimeError):",
    )
    for fragment in preview_fragments:
        require(fragment in preview, "missing tab-hide cleanup fragment: " + fragment)
    print("BRAIN_NAVIGATOR_TAB_HIDE_CLEANUP: PASS")
    print("WEBENGINE_TEARDOWN_FAILURE_CONTAINED: PASS")

    imported = set()
    for source, filename in ((template, TEMPLATE_PATH), (preview, PREVIEW_PATH)):
        tree = ast.parse(source, filename=filename)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
    for forbidden in ("main_window", "tool_specs", "tab_navigation_controller"):
        require(
            not any(forbidden in name for name in imported),
            "forbidden cross-box import introduced: " + forbidden,
        )
    print("BRAIN_NAVIGATOR_PAGE_LOCAL_LIFECYCLE_OWNER: PASS")


def validate_metadata(root: Path) -> None:
    """Validate the Brain Navigator box metadata and focused validator registry."""

    manifest = json.loads(read_text(root, MANIFEST_PATH))
    require(manifest.get("version") == "1.1.0", "Brain Navigator manifest version is stale")
    validation = manifest.get("validation", {})
    for key in ("focused_tests", "boundary_tests", "contamination_tests"):
        require(
            VALIDATOR_PATH in validation.get(key, []),
            f"focused validator missing from manifest {key}",
        )
    route = str(manifest.get("communication_route", ""))
    require(
        "floating_window_closes_on_brain_navigator_tab_hide_without_main_window_reach_in"
        in route,
        "tab-hide cleanup route is undocumented",
    )
    require(
        "floating_window_uses_readable_system_font_stack_and_larger_text" in route,
        "readability route is undocumented",
    )
    readme = read_text(root, README_PATH)
    require(
        "## Floating window lifecycle and readability correction" in readme,
        "README lifecycle section is missing",
    )
    print("BRAIN_NAVIGATOR_LIFECYCLE_METADATA_CURRENT: PASS")


def validate_compile_and_size(root: Path) -> None:
    """Compile touched Python and enforce the module-size gate."""

    for relative in TOUCHED_PYTHON:
        path = root / relative
        require(path.is_file(), "missing touched Python file: " + relative)
        py_compile.compile(str(path), doraise=True)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        require(
            0 < line_count <= MAX_CODE_LINES,
            f"module-size violation {relative}: {line_count}",
        )
    print("PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def validate_catalog_regression(root: Path) -> None:
    """Run the frozen Brain Navigator catalog validator on current source."""

    path = root / CATALOG_VALIDATOR_PATH
    require(path.is_file(), "catalog regression validator is missing")
    module_name = "_brain_catalog_regression_validator"
    spec = importlib.util.spec_from_file_location(module_name, path)
    require(spec is not None and spec.loader is not None, "cannot load catalog validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    original_argv = sys.argv[:]
    try:
        sys.argv = [str(path), "--root", str(root)]
        result = int(module.main())
    finally:
        sys.argv = original_argv
    require(result == 0, "Brain Navigator catalog regression failed")
    print("BRAIN_NAVIGATOR_FROZEN_CATALOG_REGRESSION: PASS")


def main() -> int:
    """Run focused lifecycle, readability, and frozen-catalog checks."""

    stream = getattr(sys.stdout, "reconfigure", None)
    if callable(stream):
        stream(line_buffering=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.cwd()))
    parser.add_argument("--require-real-qt", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)

    phases = (
        ("SOURCE_CONTRACT", lambda: validate_source_contract(root)),
        ("METADATA", lambda: validate_metadata(root)),
        ("SIMULATED_TAB_HIDE", lambda: validate_simulated_tab_hide(root)),
    )
    for name, action in phases:
        print("VALIDATION PHASE: " + name, flush=True)
        action()
    print("VALIDATION PHASE: REAL_QT_WRAPPER", flush=True)
    real_qt_ran = validate_real_qt_tab_hide(root)
    if args.require_real_qt:
        require(real_qt_ran, "real PySide6 QWidget validation is required")
    print("VALIDATION PHASE: COMPILE_AND_SIZE", flush=True)
    validate_compile_and_size(root)
    print("VALIDATION PHASE: FROZEN_CATALOG", flush=True)
    validate_catalog_regression(root)
    print(f"VALIDATION OK: {FEATURE_ID}", flush=True)
    print("STATUS: IN_SYNC", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
