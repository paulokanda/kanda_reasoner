"""PA021 Project Symbol Atlas GUI integration tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reasoner_tools_gui_engineering_safety_panel import (  # noqa: E402
    build_engineering_safety_panel_cli_args,
    get_engineering_safety_panel_catalog,
)

EXPECTED_COMMANDS = {
    "atlas-report",
    "evidence-freshness",
    "find-symbol",
    "find-owner",
    "facade-owner",
    "main-helpers",
    "related-files",
    "pre-patch-gate",
}


def test_pa021_catalog_exposes_reasoner_symbol_atlas_buttons() -> None:
    catalog = get_engineering_safety_panel_catalog()
    atlas_tools = [tool for tool in catalog if tool.section == "Project Symbol Atlas"]
    command_names = {tool.command_name for tool in atlas_tools}

    assert EXPECTED_COMMANDS.issubset(command_names)
    labels = {tool.label for tool in atlas_tools}
    assert "Evidence Freshness" in labels
    assert "Pre-Patch Gate" in labels


def test_pa021_reasoner_symbol_atlas_commands_build_cli_args() -> None:
    root = r"C:\demo_project"
    for command_name in sorted(EXPECTED_COMMANDS):
        args = list(build_engineering_safety_panel_cli_args(command_name, root))
        assert args[0] == command_name
        assert "--root" in args
        root_index = args.index("--root")
        assert args[root_index + 1] == root


def test_pa021_query_commands_include_safe_defaults() -> None:
    find_symbol = list(build_engineering_safety_panel_cli_args("find-symbol", r"C:\demo_project"))
    assert "--symbol" in find_symbol
    assert "build_reasoner_symbol_atlas_reports" in find_symbol

    facade_owner = list(build_engineering_safety_panel_cli_args("facade-owner", r"C:\demo_project"))
    assert "--target" in facade_owner
    assert "reasoner_tools_gui.py" in facade_owner

    pre_patch_gate = list(build_engineering_safety_panel_cli_args("pre-patch-gate", r"C:\demo_project"))
    assert "--task" in pre_patch_gate
    assert "--symbol" in pre_patch_gate
    assert "create_engineering_safety_panel" in pre_patch_gate


def main() -> int:
    test_pa021_catalog_exposes_reasoner_symbol_atlas_buttons()
    test_pa021_reasoner_symbol_atlas_commands_build_cli_args()
    test_pa021_query_commands_include_safe_defaults()
    print("PA021 Project Symbol Atlas GUI integration tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
