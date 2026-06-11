"""FINAL001 safety suite hardening checks.

This focused test verifies that the completed Safety Suite integration remains
visible through the public GUI and CLI contracts without starting the GUI event
loop or modifying source files.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


EXPECTED_GUI_TITLE = "Engineering Safety"
EXPECTED_PANEL_MODULE = "reasoner_tools_gui_engineering_safety_panel"
EXPECTED_PANEL_FACTORY = "create_engineering_safety_panel"


EXPECTED_CLI_COMMANDS = {
    "bom-scan",
    "shadow-audit",
    "shadow-plan",
    "facade-fix-plan",
    "risk-radar",
    "crash-triage",
    "refactor-playbook",
    "release-notes",
    "push-plan",
    "stack-brief",
    "api-contract",
    "property-test",
    "list-tools",
}


def test_final001_engineering_safety_tab_is_registered_once() -> None:
    """The public GUI tab registry exposes exactly one Engineering Safety tab."""
    gui = importlib.import_module("reasoner_tools_gui")
    tools = tuple(getattr(gui, "TOOLS"))
    titles = [getattr(tool, "step_title", "") for tool in tools]

    assert titles.count(EXPECTED_GUI_TITLE) == 1, titles

    matching = [tool for tool in tools if getattr(tool, "step_title", "") == EXPECTED_GUI_TITLE]
    spec = matching[0]

    assert EXPECTED_PANEL_MODULE in tuple(getattr(spec, "module_candidates", ()))
    assert EXPECTED_PANEL_FACTORY in tuple(getattr(spec, "class_candidates", ()))
    assert getattr(spec, "source_hint", "") == "reasoner_tools_gui_engineering_safety_panel.py"


def test_final001_panel_public_contract_is_import_safe() -> None:
    """The panel companion module imports without PySide6 side effects."""
    panel = importlib.import_module(EXPECTED_PANEL_MODULE)

    assert hasattr(panel, EXPECTED_PANEL_FACTORY)
    assert hasattr(panel, "get_engineering_safety_panel_catalog")
    assert hasattr(panel, "build_engineering_safety_panel_command")

    catalog = panel.get_engineering_safety_panel_catalog()
    sections = {getattr(tool, "section", "") for tool in catalog}

    assert "Source Hygiene" in sections
    assert "Engineering Safety" in sections
    assert "Governance Automation" in sections
    assert "Stack Compatibility" in sections
    assert "Draft Reliability" in sections


def test_final001_safety_suite_cli_public_contract_is_import_safe() -> None:
    """The CLI facade exposes the expected command parser and commands."""
    commands = importlib.import_module("kanda_reasoner_app.safety_suite_cli.commands")

    assert hasattr(commands, "build_safety_suite_parser")
    assert hasattr(commands, "main")

    parser = commands.build_safety_suite_parser()
    subcommands = set()

    for action in parser._actions:  # argparse exposes subparsers through public Action objects.
        choices = getattr(action, "choices", None)
        if choices:
            subcommands.update(str(name) for name in choices.keys())

    missing = sorted(EXPECTED_CLI_COMMANDS - subcommands)
    assert not missing, missing


def main() -> None:
    """Run all FINAL001 hardening checks without pytest."""
    test_final001_engineering_safety_tab_is_registered_once()
    test_final001_panel_public_contract_is_import_safe()
    test_final001_safety_suite_cli_public_contract_is_import_safe()
    print("FINAL001 Safety Suite hardening tests passed.")


if __name__ == "__main__":
    main()
