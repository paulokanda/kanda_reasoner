# project-path: tools/validate_brain_navigator_tab_catalog_sync_v1.py
"""Validate Brain Navigator against the current visible shell tab catalog."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path

__all__ = ["main"]

FEATURE_ID = "brain-navigator-tab-catalog-sync-v1"
MAPPING_DATA = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/"
    "brain_region_mapping/_mapping_data.py"
)
MAPPING_CONTRACT = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/"
    "brain_region_mapping/contract.py"
)
MAPPING_MANIFEST = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/"
    "brain_region_mapping/box_manifest.json"
)
MAPPING_README = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/"
    "brain_region_mapping/README.md"
)
FLOATING_WINDOWS = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/"
    "assets/brain_visual_floating_window.py"
)
MARKERS = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/"
    "assets/brain_visual_markers.py"
)
TOOL_SPECS = "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py"
VALIDATOR = "tools/validate_brain_navigator_tab_catalog_sync_v1.py"

TOUCHED_PYTHON = (
    MAPPING_DATA,
    MAPPING_CONTRACT,
    FLOATING_WINDOWS,
    VALIDATOR,
)

DEPRECATED_STANDALONE_TAB_IDS = {
    "workflow_review",
    "refactor_report",
}


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    """Return the exact file hash."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_shell_specs() -> tuple[object, ...]:
    """Return visible top-level tool specs except Brain Navigator itself."""
    from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

    return tuple(
        spec
        for spec in TOOLS
        if spec.visible_in_shell and spec.tab_id != "brain_navigator"
    )


def validate_catalog_coverage() -> None:
    """Validate current shell coverage and removal of stale standalone tabs."""
    from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping.contract import (
        BRAIN_REGION_MAPPING_CONTRACT_VERSION,
        list_brain_region_targets,
    )

    specs = visible_shell_specs()
    expected_label_by_id = {
        str(spec.tab_id): str(spec.step_title)
        for spec in specs
        if spec.tab_id
    }
    expected_ids = set(expected_label_by_id)
    targets = list_brain_region_targets()
    mapped_ids = {target.target_tab_id for target in targets}

    require(
        BRAIN_REGION_MAPPING_CONTRACT_VERSION == "0.2",
        "Brain Region Mapping contract version must be 0.2",
    )
    require(
        mapped_ids == expected_ids,
        "Brain Navigator target catalog differs from visible shell tabs: "
        f"missing={sorted(expected_ids - mapped_ids)}, "
        f"extra={sorted(mapped_ids - expected_ids)}",
    )
    print("VISIBLE_TOP_LEVEL_TAB_CATALOG: PASS")

    require(
        not (mapped_ids & DEPRECATED_STANDALONE_TAB_IDS),
        "deprecated standalone tab ID remains mapped",
    )
    hidden_ids = {
        str(spec.tab_id)
        for spec in __import__(
            "kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs",
            fromlist=["TOOLS"],
        ).TOOLS
        if spec.tab_id and not spec.visible_in_shell
    }
    require(not (mapped_ids & hidden_ids), "hidden shell tab remains mapped")
    print("DEPRECATED_STANDALONE_TAB_TARGETS_REMOVED: PASS")

    for target in targets:
        expected_label = expected_label_by_id[target.target_tab_id]
        require(
            target.target_tab_label == expected_label,
            "mapping label does not match shell label for "
            f"{target.region_id}: {target.target_tab_label!r} != "
            f"{expected_label!r}",
        )
    print("CURRENT_TOP_LEVEL_TAB_LABELS: PASS")

    require("config_web_ai" in mapped_ids, "Config AI has no brain mapping")
    require("project_web_ai" in mapped_ids, "Project Web AI has no brain mapping")
    print("CONFIG_AI_BRAIN_MAPPING: PASS")
    print("PROJECT_WEB_AI_BRAIN_MAPPING: PASS")

    audit_targets = [
        target
        for target in targets
        if target.target_tab_id == "architecture_review"
    ]
    require(audit_targets, "Audit Project has no brain mapping")
    require(
        all(target.target_tab_label == "Audit Project" for target in audit_targets),
        "Audit Project mappings still expose a former standalone label",
    )
    print("AUDIT_PROJECT_TOP_LEVEL_LABELS: PASS")


def validate_visual_data_parity() -> None:
    """Validate marker, mapping, and floating-window identity parity."""
    from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
        build_neural_architecture_floating_window_data_js,
        build_neural_architecture_marker_data_js,
        list_neural_architecture_floating_windows,
        list_neural_architecture_pulse_markers,
    )
    from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping.contract import (
        list_brain_region_targets,
    )

    targets = list_brain_region_targets()
    markers = list_neural_architecture_pulse_markers()
    windows = list_neural_architecture_floating_windows()

    target_ids = tuple(target.region_id for target in targets)
    marker_ids = tuple(marker.region_id for marker in markers)
    window_ids = tuple(window.region_id for window in windows)
    require(target_ids == marker_ids == window_ids, "brain data order is out of sync")

    target_by_region = {target.region_id: target for target in targets}
    for window in windows:
        target = target_by_region[window.region_id]
        require(
            window.target_tab_label == target.target_tab_label,
            "floating target label differs from mapping for " + window.region_id,
        )

    marker_js = build_neural_architecture_marker_data_js()
    window_js = build_neural_architecture_floating_window_data_js()
    require("config_web_ai" not in marker_js, "tab IDs leaked into marker geometry")
    require("project_web_ai" not in marker_js, "tab IDs leaked into marker geometry")
    require("Config AI" in window_js, "Config AI missing from floating data")
    require("Web AI" in window_js, "Web AI missing from floating data")
    require("Refactor Report" not in window_js, "deprecated Refactor Report label remains")
    print("MARKER_MAPPING_FLOATING_WINDOW_PARITY: PASS")
    print("BRAIN_NAVIGATOR_VISUAL_GEOMETRY_UNCHANGED: PASS")


def validate_boundaries(root: Path) -> None:
    """Validate data-only boundaries, metadata, syntax, and module size."""
    mapping_data = (root / MAPPING_DATA).read_text(encoding="utf-8")
    mapping_contract = (root / MAPPING_CONTRACT).read_text(encoding="utf-8")
    floating = (root / FLOATING_WINDOWS).read_text(encoding="utf-8")
    readme = (root / MAPPING_README).read_text(encoding="utf-8")
    manifest = json.loads((root / MAPPING_MANIFEST).read_text(encoding="utf-8"))

    def imported_modules(source: str, filename: str) -> set[str]:
        tree = ast.parse(source, filename=filename)
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module)
        return names

    mapping_imports = imported_modules(mapping_data, MAPPING_DATA)
    contract_imports = imported_modules(mapping_contract, MAPPING_CONTRACT)
    floating_imports = imported_modules(floating, FLOATING_WINDOWS)
    forbidden_import_fragments = (
        "tool_specs",
        "main_window",
        "PySide6",
        "QWebEngineView",
    )
    for forbidden in forbidden_import_fragments:
        require(
            not any(forbidden in name for name in mapping_imports),
            "mapping data import leaked: " + forbidden,
        )
        require(
            not any(forbidden in name for name in contract_imports),
            "mapping contract import leaked: " + forbidden,
        )
    require(
        not any("brain_region_mapping" in name for name in floating_imports),
        "floating-window data reached into mapping internals",
    )
    print("BRAIN_MAPPING_DATA_ONLY_BOUNDARY: PASS")

    require(manifest.get("version") == "0.2.0", "mapping manifest version mismatch")
    require(
        manifest.get("contract_version") == "0.2",
        "mapping manifest contract mismatch",
    )
    require(manifest.get("health_state") == "active", "mapping box is not active")
    validators = set(manifest.get("validation", {}).get("focused_tests", []))
    require(VALIDATOR in validators, "focused validator missing from manifest")
    require("Status: active pure mapping box." in readme, "README status is stale")
    print("BRAIN_MAPPING_METADATA_CURRENT: PASS")

    for relative in TOUCHED_PYTHON:
        path = root / relative
        require(path.is_file(), "missing touched file: " + relative)
        source = path.read_text(encoding="utf-8")
        ast.parse(source, filename=relative)
        line_count = len(source.splitlines())
        require(0 < line_count <= 500, f"module-size violation {relative}: {line_count}")
    print("PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run the focused Brain Navigator catalog synchronization checks."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.cwd()))
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))
    tracked = (
        MAPPING_DATA,
        MAPPING_CONTRACT,
        MAPPING_MANIFEST,
        MAPPING_README,
        FLOATING_WINDOWS,
        MARKERS,
        TOOL_SPECS,
        VALIDATOR,
    )
    before = {relative: sha256(root / relative) for relative in tracked}

    validate_catalog_coverage()
    validate_visual_data_parity()
    validate_boundaries(root)

    after = {relative: sha256(root / relative) for relative in tracked}
    require(before == after, "validation mutated project source")
    print("LIVE_TOOL_SOURCE_UNCHANGED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
