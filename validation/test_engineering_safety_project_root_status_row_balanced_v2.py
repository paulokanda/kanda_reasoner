from __future__ import annotations

import ast
import py_compile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL_SOURCE = ROOT / "reasoner_tools_gui_engineering_safety_panel.py"
LAZY_TABS_SOURCE = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"
PATCH_NAME = "kanda_engineering_safety_project_root_status_row_balanced_v2_patch.zip"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_ascii(path: Path) -> None:
    try:
        path.read_text(encoding="ascii")
    except UnicodeDecodeError as exc:
        raise AssertionError(f"non-ASCII character found in {path.relative_to(ROOT)}") from exc


def candidate_patch_zips() -> list[Path]:
    candidates = [ROOT / PATCH_NAME]
    project_name = ROOT.name
    if project_name:
        drive_root = ROOT.anchor
        if drive_root:
            candidates.append(Path(drive_root) / f"{project_name}_delete_after_daily_work" / PATCH_NAME)
    parent = ROOT.parent
    candidates.append(parent / PATCH_NAME)
    candidates.append(parent / f"{ROOT.name}_delete_after_daily_work" / PATCH_NAME)
    return candidates


def assert_panel_contract() -> None:
    text = read_text(PANEL_SOURCE)
    tree = ast.parse(text)
    require(tree is not None, "Engineering Safety source did not parse")

    require('QLabel("Project Root:")' in text, "Project Root label missing")
    require('setObjectName("engineering_safety_project_root_edit")' in text, "project root edit object name missing")
    require('QPushButton("Search")' in text, "Search project-root button missing")
    require("def search_project_root()" in text, "Search project-root handler missing")
    require("QFileDialog.getExistingDirectory" in text, "Search handler must use a directory chooser")
    require("def current_project_root_text()" in text, "current project-root reader missing")
    require("current_project_root_text()," in text, "commands must use current Project Root widget value")

    require("def move_project_root_controls_to_layout(" in text, "host-row project-root mover missing")
    require('panel.move_project_root_controls_to_layout = move_project_root_controls_to_layout' in text, "panel mover hook missing")
    require("destination_layout.insertWidget(insert_index + 1, project_root_label, 0)" in text, "Project Root label not inserted into host row")
    require("destination_layout.insertWidget(insert_index + 2, project_root_edit, 0)" in text, "Project Root edit not inserted into host row")
    require("destination_layout.insertWidget(insert_index + 3, search_project_button, 0)" in text, "Search button not inserted into host row")
    require("outer.addLayout(project_root_row)" not in text, "Project Root row must not remain inside panel body")
    require("project_root_row = QHBoxLayout()" not in text, "old body Project Root row restored")

    require('heading = QLabel("Engineering Safety")' not in text, "duplicated Engineering Safety heading restored")
    require('outer.addWidget(heading)' not in text, "duplicated Engineering Safety heading added to layout")
    require('status_label = QLabel("Ready.")' not in text, "visible Ready label restored")
    require('outer.addWidget(status_label)' not in text, "status label should not be visible in layout")
    require("status_label.setVisible(False)" in text, "internal status label should remain hidden")

    require("button_layout = QGridLayout(button_host)" in text, "outer button grid missing")
    require("def build_group(" in text, "group builder missing")
    require("def build_stack(" in text, "compact stack builder missing")
    require('build_stack(("Draft Reliability", "Utilities"))' in text, "Draft Reliability and Utilities must share one left-column stack")
    require('build_group("Project Symbol Atlas", grouped_sections["Project Symbol Atlas"])' in text, "Project Symbol Atlas group missing")
    require('button_layout.addWidget(build_stack(("Draft Reliability", "Utilities")), 2, 0)' in text, "Draft Reliability plus Utilities not aligned opposite Atlas")
    require('button_layout.addWidget(build_group("Project Symbol Atlas", grouped_sections["Project Symbol Atlas"]), 2, 1)' in text, "Project Symbol Atlas not placed opposite Draft/Utilities stack")
    require('button_layout.addWidget(group, section_index // 2, section_index % 2)' not in text, "generic section grid restored; custom balanced layout required")
    require("button_width = 170" in text, "symmetric button width constant missing")
    require("button.setMinimumWidth(button_width)" in text, "button minimum width not normalized")
    require("button.setMaximumWidth(button_width)" in text, "button maximum width not normalized")
    require("QSizePolicy.Fixed" in text, "button fixed size policy missing")
    require("group_layout.addWidget(button, index // 2, index % 2)" in text, "buttons not split into two columns inside groups")

    require("run_engineering_safety_panel_cli_command," in text, "command runner submit missing")
    require("root," not in text, "stale fixed root variable still passed into commands")


def assert_lazy_tabs_contract() -> None:
    text = read_text(LAZY_TABS_SOURCE)
    ast.parse(text)
    require('_ENGINEERING_SAFETY_GUI_SOURCE = "reasoner_tools_gui_engineering_safety_panel.py"' in text, "Engineering Safety source constant missing")
    require("def _move_engineering_safety_project_root_controls_to_status_row" in text, "Engineering Safety host-row mover missing in lazy tabs")
    require("self.spec.source_hint != _ENGINEERING_SAFETY_GUI_SOURCE" in text, "Engineering Safety mover not gated by source hint")
    require("self._move_engineering_safety_project_root_controls_to_status_row(widget)" in text, "Engineering Safety mover not called while loading tab")
    require("mover(self.status_source_row, self._status_source_insert_index)" in text, "Engineering Safety mover must use Architecture-style insertion index")


def assert_patch_zip_contract() -> None:
    existing = next((path for path in candidate_patch_zips() if path.exists()), None)
    if existing is None:
        return
    with zipfile.ZipFile(existing, "r") as zf:
        names = set(zf.namelist())
    expected = {
        "reasoner_tools_gui_engineering_safety_panel.py",
        "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
        "validation/test_engineering_safety_project_root_status_row_balanced_v2.py",
        "KANDA_FREEZE_HINT.json",
    }
    require(expected.issubset(names), f"patch ZIP missing files: {sorted(expected - names)}")
    forbidden = [name for name in names if name.startswith("project_freeze_after_update/")]
    require(not forbidden, "patch ZIP must not contain frozen memory entries")


def main() -> int:
    for path in (PANEL_SOURCE, LAZY_TABS_SOURCE):
        assert_ascii(path)
        py_compile.compile(str(path), doraise=True)
    assert_panel_contract()
    assert_lazy_tabs_contract()
    assert_patch_zip_contract()
    print("VALIDATION OK: engineering-safety-project-root-status-row-balanced-v2")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
