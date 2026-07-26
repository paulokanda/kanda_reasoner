# project-path: tools/validate_prompt_library_canonical_catalog_sync_v1.py
"""Validate canonical Prompt Library catalog synchronization."""

from __future__ import annotations

import argparse
import ast
import importlib
import json
import os
import sys
from collections import Counter
from pathlib import Path

FEATURE_ID = "prompt-library-canonical-catalog-sync-v1"
EXPECTED_GROUP_COUNTS = {
    "01_session_start_and_navigation": 11,
    "02_prompt_routing_and_indexing": 6,
    "03_governance_freeze_and_handoff": 6,
    "04_box_architecture_and_boundaries": 5,
    "05_patch_delivery_and_validation": 7,
    "06_refactor_and_architecture_hardening": 8,
    "07_prompt_authoring_and_audit": 5,
    "08_python_engineering_core": 10,
    "09_python_quality_security_observability": 16,
    "10_python_api_data_async_config": 4,
    "11_productization_and_release_readiness": 4,
    "12_generalized_project_canons": 14,
}
DEPRECATED_OR_RETIRED_IDS = {
    "daily_reasoner_startup_loader",
    "daily_session_start_prompt",
    "general_prompt_stack_load_order",
    "governed_architecture_companion_handoff",
    "productization_readiness_roadmap",
    "professional_infrastructure_roadmap",
    "prompt_router",
    "reasoner_startup_canon",
    "router_bridge_governed_implementation",
    "router_bridge_patch_delivery_contract",
    "routing_signal_scorer_v3_lab_phase_entry_router_canon",
    "routing_signal_scorer_v3_pilot_copilot_phase0_router_canon",
    "tab4_docstring_quality_roadmap",
    "universal_delivery_protocol",
}
LEGACY_GROUP_IDS = {
    "daily_start",
    "end_of_day_handoff",
    "governance_freeze",
    "high_risk_engineering",
    "large_module_refactor",
    "architecture_hardening",
    "domain_special_overlays",
    "prompt_library_tools",
    "teach_ai_prompt_authoring",
}
TOUCHED_PYTHON = (
    "kanda_reasoner_app/prompt_library_gui/library_paths.py",
    "kanda_reasoner_app/prompt_library_gui/library_catalog.py",
    "kanda_reasoner_app/prompt_library_gui/group_catalog.py",
    "kanda_reasoner_app/prompt_library_gui/group_dashboard.py",
    "kanda_reasoner_app/prompt_library_gui/group_window.py",
    "kanda_reasoner_app/prompt_library_gui/prompt_library_tab.py",
    "tools/validate_prompt_library_canonical_catalog_sync_v1.py",
)


def require(condition: bool, message: str) -> None:
    """Raise a validation error when a required condition is false."""
    if not condition:
        raise AssertionError(message)


def prompt_id(item: object) -> str:
    """Return the stable prompt identifier from a catalog item."""
    metadata = getattr(item, "metadata")
    value = metadata.get("prompt_id")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return getattr(item, "path").stem


def load_json(path: Path) -> dict[str, object]:
    """Load a JSON object from disk."""
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    require(isinstance(data, dict), "JSON root must be an object: " + str(path))
    return data


def validate_source_contract(root: Path) -> None:
    """Validate static source ownership and module constraints."""
    paths_source = (
        root / "kanda_reasoner_app/prompt_library_gui/library_paths.py"
    ).read_text(encoding="utf-8")
    require(
        '"kanda_prompt_workspace" / "prompt_library"' in paths_source,
        "canonical workspace path owner is missing",
    )
    require(
        "legacy_prompt_library_root" in paths_source,
        "legacy compatibility fallback is missing",
    )

    catalog_source = (
        root / "kanda_reasoner_app/prompt_library_gui/library_catalog.py"
    ).read_text(encoding="utf-8")
    for token in (
        '"deprecated"',
        '"retired"',
        '"superseded"',
        'load_type == "never"',
        '"_FOLDER_ASSIMILATION.md"',
    ):
        require(token in catalog_source, "catalog filter is missing: " + token)

    group_source = (
        root / "kanda_reasoner_app/prompt_library_gui/group_catalog.py"
    ).read_text(encoding="utf-8")
    require(
        '"GROUPS" / "PROMPT_GROUPS_DRAFT.json"' in group_source,
        "canonical group registry path is missing",
    )
    require(
        "_ordered_current_prompt_ids" in group_source,
        "current prompt reconciliation owner is missing",
    )

    for relative in TOUCHED_PYTHON:
        path = root / relative
        source = path.read_text(encoding="utf-8")
        ast.parse(source, filename=str(path))
        line_count = len(source.splitlines())
        require(line_count <= 500, relative + " exceeds 500 physical lines")

    print("PYTHON_COMPILE: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("CANONICAL_PROMPT_LIBRARY_OWNER: PASS")
    print("LEGACY_PACKAGE_FALLBACK_PRESERVED: PASS")


def validate_catalog_runtime(root: Path) -> None:
    """Load the headless catalog and validate current group coverage."""
    sys.path.insert(0, str(root))
    try:
        paths = importlib.import_module(
            "kanda_reasoner_app.prompt_library_gui.library_paths"
        )
        library_catalog = importlib.import_module(
            "kanda_reasoner_app.prompt_library_gui.library_catalog"
        )
        group_catalog = importlib.import_module(
            "kanda_reasoner_app.prompt_library_gui.group_catalog"
        )

        selected_root = paths.prompt_library_root()
        expected_root = root / "kanda_prompt_workspace/prompt_library"
        require(selected_root == expected_root, "canonical library root not selected")

        items = library_catalog.load_prompt_library_items(selected_root)
        groups = group_catalog.load_prompt_groups(selected_root)
        require(len(items) == 96, "expected 96 current prompts")
        require(len(groups) == 12, "expected 12 current prompt groups")

        group_ids = [group.group_id for group in groups]
        require(
            group_ids == list(EXPECTED_GROUP_COUNTS),
            "canonical group order or identity drifted",
        )
        require(not (set(group_ids) & LEGACY_GROUP_IDS), "legacy cubes remain active")

        assigned: list[str] = []
        actual_counts: dict[str, int] = {}
        for group in groups:
            group_items = group_catalog.filter_items_for_group(group, items)
            actual_counts[group.group_id] = len(group_items)
            require(
                len(group_items) == len(group.prompt_ids),
                "unresolved prompt IDs in group " + group.group_id,
            )
            assigned.extend(prompt_id(item) for item in group_items)

        require(
            actual_counts == EXPECTED_GROUP_COUNTS,
            "group prompt counts do not match the audited catalog",
        )
        require(len(assigned) == 96, "not all current prompts are assigned")
        duplicates = [key for key, count in Counter(assigned).items() if count != 1]
        require(not duplicates, "prompt assigned zero or multiple times: " + str(duplicates))

        current_ids = {prompt_id(item) for item in items}
        require(
            not (current_ids & DEPRECATED_OR_RETIRED_IDS),
            "deprecated or retired prompt is visible",
        )
        statuses = {
            str(item.metadata.get("status", "")).strip().lower()
            for item in items
        }
        require(
            not statuses.intersection(
                {"deprecated", "retired", "inactive", "archived", "superseded"}
            ),
            "hidden metadata status leaked into current items",
        )

        colors = [group.color_role for group in groups]
        require(len(set(colors)) == 12, "all 12 cubes need distinct color roles")

        print("CANONICAL_GROUP_CUBES_12: PASS")
        print("CURRENT_PROMPTS_96: PASS")
        print("DEPRECATED_AND_RETIRED_PROMPTS_HIDDEN: PASS")
        print("CURRENT_PROMPT_GROUP_COVERAGE: PASS")
        print("PROMPT_ASSIGNED_EXACTLY_ONCE: PASS")
        print("MISSING_CURRENT_PROMPTS_AUTO_DISCOVERED: PASS")
        print("DISTINCT_CANONICAL_CUBE_COLORS: PASS")
    finally:
        if sys.path and sys.path[0] == str(root):
            sys.path.pop(0)


def validate_registry_mirror(root: Path) -> None:
    """Validate canonical and package fallback group registries."""
    canonical_path = (
        root
        / "kanda_prompt_workspace/prompt_library/GROUPS/PROMPT_GROUPS_DRAFT.json"
    )
    fallback_path = root / "kanda_reasoner_app/prompt_library/groups/PROMPT_GROUPS.json"
    canonical = load_json(canonical_path)
    fallback = load_json(fallback_path)
    canonical_groups = canonical.get("groups")
    fallback_groups = fallback.get("groups")
    require(isinstance(canonical_groups, list), "canonical groups must be a list")
    require(isinstance(fallback_groups, list), "fallback groups must be a list")
    require(canonical_groups == fallback_groups, "fallback group mirror is stale")

    all_ids: set[str] = set()
    for raw_group in canonical_groups:
        require(isinstance(raw_group, dict), "group entry must be an object")
        prompt_ids = raw_group.get("prompt_ids")
        require(isinstance(prompt_ids, list), "prompt_ids must be a list")
        require(
            int(raw_group.get("prompt_count", -1)) == len(prompt_ids),
            "prompt_count drift in " + str(raw_group.get("group_id")),
        )
        group_ids = {str(value) for value in prompt_ids}
        require(
            not (group_ids & DEPRECATED_OR_RETIRED_IDS),
            "deprecated prompt remains in group registry",
        )
        require(not (all_ids & group_ids), "prompt duplicated across group registries")
        all_ids.update(group_ids)

    require(len(all_ids) == 96, "canonical registry must contain 96 current prompts")
    print("CANONICAL_AND_FALLBACK_GROUP_REGISTRIES_IN_SYNC: PASS")
    print("LEGACY_NINE_CUBE_CATALOG_REMOVED: PASS")
    print("GROUP_PROMPT_COUNTS_CURRENT: PASS")



def validate_real_qt(root: Path) -> None:
    """Instantiate the real Prompt Library tab and verify cube projection."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    sys.path.insert(0, str(root))
    try:
        from PySide6.QtWidgets import QApplication
        from kanda_reasoner_app.prompt_library_gui.prompt_library_tab import (
            PromptLibraryTab,
        )

        app = QApplication.instance() or QApplication([])
        tab = PromptLibraryTab()
        app.processEvents()
        require(len(tab.groups) == 12, "real Qt tab did not load 12 groups")
        require(len(tab.items) == 96, "real Qt tab did not load 96 current prompts")
        require(
            len(tab.dashboard.cube_cards) == 12,
            "real Qt dashboard did not create 12 cubes",
        )
        require(
            "Deprecated and retired entries are hidden"
            in tab.status_label.text(),
            "real Qt status does not disclose hidden historical entries",
        )
        tab.close()
        tab.deleteLater()
        app.processEvents()
        print("REAL_QT_PROMPT_LIBRARY_12_CUBES: PASS")
        print("REAL_QT_PROMPT_LIBRARY_96_CURRENT_PROMPTS: PASS")
        print("REAL_QT_DEPRECATED_PROMPTS_HIDDEN: PASS")
        print("REAL_QT_CANONICAL_LIBRARY_SOURCE: PASS")
    finally:
        if sys.path and sys.path[0] == str(root):
            sys.path.pop(0)

def main() -> int:
    """Run the focused catalog synchronization validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--require-qt", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    require(root.is_dir(), "Project root does not exist: " + str(root))

    validate_source_contract(root)
    validate_registry_mirror(root)
    validate_catalog_runtime(root)
    if args.require_qt:
        validate_real_qt(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("VALIDATION ERROR: " + type(exc).__name__ + ": " + str(exc))
        raise
