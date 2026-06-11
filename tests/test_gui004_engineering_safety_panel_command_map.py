"""Focused tests for GUI004 Engineering Safety panel command mapping."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel


def test_gui004_catalog_has_unique_command_names() -> None:
    catalog = panel.get_engineering_safety_panel_catalog()
    commands = [tool.command_name for tool in catalog]
    assert len(commands) == len(set(commands)), commands
    expected = {
        "api-contract",
        "bom-scan",
        "crash-triage",
        "facade-fix-plan",
        "list-tools",
        "property-test",
        "push-plan",
        "refactor-playbook",
        "release-notes",
        "risk-radar",
        "shadow-audit",
        "shadow-plan",
        "stack-brief",
    }
    assert set(commands) == expected


def test_gui004_source_hygiene_buttons_call_correct_commands() -> None:
    assert panel.build_engineering_safety_panel_cli_args("bom-scan")[0] == "bom-scan"
    assert panel.build_engineering_safety_panel_cli_args("shadow-audit")[0] == "shadow-audit"
    assert panel.build_engineering_safety_panel_cli_args("shadow-plan")[0] == "shadow-plan"
    assert panel.build_engineering_safety_panel_cli_args("facade-fix-plan")[0] == "facade-fix-plan"


def test_gui004_release_notes_includes_required_title() -> None:
    args = panel.build_engineering_safety_panel_cli_args("release-notes")
    assert args[0] == "release-notes"
    assert "--title" in args
    assert "--bundle-name" in args
    assert "--summary" in args
    assert "--status" in args


def test_gui004_public_command_alias_still_works() -> None:
    first = panel.get_engineering_safety_panel_catalog()[0]
    assert first.command == first.command_name
    assert panel.build_engineering_safety_panel_command("risk-radar")[0] == "risk-radar"


def main() -> None:
    test_gui004_catalog_has_unique_command_names()
    test_gui004_source_hygiene_buttons_call_correct_commands()
    test_gui004_release_notes_includes_required_title()
    test_gui004_public_command_alias_still_works()
    print("GUI004 Engineering Safety panel command map tests passed.")


if __name__ == "__main__":
    main()
