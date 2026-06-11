"""Focused tests for GUI001 Engineering Safety panel companion module."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel


def test_gui001_panel_companion_module_has_public_contract() -> None:
    """The companion GUI module must expose its stable public API."""
    expected_names = {
        "ENGINEERING_SAFETY_PANEL_CATALOG",
        "EngineeringSafetyPanelTool",
        "build_engineering_safety_panel_command",
        "create_engineering_safety_panel",
        "get_engineering_safety_panel_catalog",
    }
    assert expected_names.issubset(set(panel.__all__))


def test_gui001_panel_catalog_is_static_and_import_safe() -> None:
    """Catalog access must work without constructing Qt widgets."""
    catalog = panel.get_engineering_safety_panel_catalog()
    assert catalog
    assert len(catalog) >= 10

    sections = {tool.section for tool in catalog}
    assert "Source Hygiene" in sections
    assert "Engineering Safety" in sections
    assert "Governance Automation" in sections
    assert "Stack Compatibility" in sections
    assert "Draft Reliability" in sections


def test_gui001_panel_command_builder_uses_safety_suite_cli() -> None:
    """Tool commands should delegate to the safety-suite CLI facade."""
    catalog = panel.get_engineering_safety_panel_catalog()
    first_tool = catalog[0]
    command = panel.build_engineering_safety_panel_command(first_tool.command_name)

    assert isinstance(command, list)
    assert command
    assert any("safety_suite_cli" in part for part in command)
    assert first_tool.command_name in command


def test_gui001_qt_factory_is_present_but_not_called_on_import() -> None:
    """The Qt factory remains lazy so importing this module is safe."""
    assert callable(panel.create_engineering_safety_panel)


def main() -> None:
    test_gui001_panel_companion_module_has_public_contract()
    test_gui001_panel_catalog_is_static_and_import_safe()
    test_gui001_panel_command_builder_uses_safety_suite_cli()
    test_gui001_qt_factory_is_present_but_not_called_on_import()
    print("GUI001E Engineering Safety panel command-contract repair tests passed.")


if __name__ == "__main__":
    main()
