"""Validate show-project-bridge-buttons-startup-on-demand-v1."""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "show-project-bridge-buttons-startup-on-demand-v1"
UI_REL = "kanda_reasoner_app/reasoner_tools_shell/runner_help/window_methods_private_impl.py"
WRAP_REL = "kanda_reasoner_app/reasoner_tools_shell/runner_help/bridge_list_wrapper_buttons_private_impl.py"


def fail(message: str) -> None:
    raise AssertionError(message)


def read(root: Path, rel: str) -> str:
    path = root / rel
    if not path.is_file():
        fail("Missing file: " + rel)
    return path.read_text(encoding="utf-8")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail("Missing " + label + ": " + needle)


def reject(text: str, needle: str, label: str) -> None:
    if needle in text:
        fail("Forbidden " + label + ": " + needle)


def validate_ui(root: Path) -> None:
    text = read(root, UI_REL)
    require(text, 'self.copy_terminal_cleanup_contract_button = QPushButton("Clean 2sec 2xEnter")', 'existing Clean button')
    require(text, 'self.bridges_label = QLabel("Bridges")', 'Bridges label')
    require(text, 'QPalette.WindowText', 'orange label palette role')
    require(text, 'self.copy_startup_bridge_list_button = QPushButton("Startup")', 'Startup button')
    require(text, 'self.copy_on_demand_bridge_list_button = QPushButton("On Demand")', 'On Demand button')
    require(text, 'QColor("#ff4d00")', 'orange font color')
    require(text, 'startup_bridge_button_font.setBold(True)', 'Startup bold font')
    require(text, 'on_demand_bridge_button_font.setBold(True)', 'On Demand bold font')
    require(text, 'bridges_label_font.setBold(True)', 'Bridges label bold font')
    require(text, 'bridge_list_wrapper_buttons_private_impl as _bridge_button_impl', 'new wrapper module import')
    require(text, 'copy_startup_bridge_list_to_clipboard(self)', 'Startup wrapper connection')
    require(text, 'copy_on_demand_bridge_list_to_clipboard(self)', 'On Demand wrapper connection')
    reject(text, 'self.bridge_list_label = QLabel("Bridge List:")', 'old Bridge List label')
    reject(text, 'self.copy_complete_bridge_list_button = QPushButton("Complete Bridge List")', 'old Complete Bridge List button')
    reject(text, 'copy_complete_bridge_list_to_clipboard(self)', 'old Complete Bridge List UI connection')


def validate_wrapper(root: Path) -> None:
    text = read(root, WRAP_REL)
    require(text, 'build_startup_bridge_list', 'startup builder')
    require(text, 'build_on_demand_bridge_list', 'on-demand builder')
    require(text, '_complete_bridge_list.build_complete_bridge_list(project_root)', 'dynamic complete-list source')
    require(text, '_STARTUP_BEGIN = "KANDA_STARTUP_BRIDGE_LIST_BEGIN"', 'startup begin marker')
    require(text, '_ON_DEMAND_BEGIN = "KANDA_ON_DEMAND_BRIDGE_LIST_BEGIN"', 'on-demand begin marker')
    require(text, 'section_title="ACTIVE STARTUP BRIDGES"', 'startup section title')
    require(text, 'section_title="ON-DEMAND BRIDGES"', 'on-demand section title')
    require(text, 'QApplication.clipboard().setText(text)', 'clipboard copy')
    require(text, 'Copied " + label + " Bridges: "', 'status message')


def validate_line_counts(root: Path) -> None:
    for rel in (UI_REL, WRAP_REL):
        lines = read(root, rel).splitlines()
        if len(lines) > 500:
            fail(rel + " exceeds 500 physical lines: " + str(len(lines)))


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_show_project_bridge_buttons_startup_on_demand_v1.py <project_root>")
        return 2
    root = Path(sys.argv[1]).resolve()
    validate_ui(root)
    validate_wrapper(root)
    validate_line_counts(root)
    py_compile.compile(str(root / UI_REL), doraise=True)
    py_compile.compile(str(root / WRAP_REL), doraise=True)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
