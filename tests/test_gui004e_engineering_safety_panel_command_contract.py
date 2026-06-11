"""Focused tests for GUI004E Engineering Safety panel command contract."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel


def test_gui004e_legacy_list_tools_display_contract() -> None:
    command = panel.build_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert command == ["list-tools"]


def test_gui004e_shadow_audit_and_release_notes_defaults_are_correct() -> None:
    shadow = panel.build_engineering_safety_panel_command("shadow-audit", project_root=ROOT)
    assert shadow[:3] == ["shadow-audit", "--root", str(ROOT)]
    release = panel.build_engineering_safety_panel_command("release-notes", project_root=ROOT)
    assert "--title" in release
    assert "--status" in release


def test_gui004e_runner_preserves_status_aliases() -> None:
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status == 0
    assert result.status_code == 0
    assert "list-tools" in result.stdout


def main() -> None:
    test_gui004e_legacy_list_tools_display_contract()
    test_gui004e_shadow_audit_and_release_notes_defaults_are_correct()
    test_gui004e_runner_preserves_status_aliases()
    print("GUI004E Engineering Safety panel command contract tests passed.")


if __name__ == "__main__":
    main()
