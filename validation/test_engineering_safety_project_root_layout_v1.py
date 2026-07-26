from __future__ import annotations

import ast
import py_compile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reasoner_tools_gui_engineering_safety_panel.py"
PATCH_ZIP = ROOT / "kanda_engineering_safety_project_root_layout_v1_patch.zip"


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


def assert_source_contract() -> None:
    text = read_text(SOURCE)
    tree = ast.parse(text)
    require(tree is not None, "source did not parse")

    require("QLineEdit" in text, "Project Root line edit import missing")
    require("QFileDialog" in text, "Search project file dialog import missing")
    require("QGridLayout" in text, "two-column grid layout import missing")
    require("QSizePolicy" in text, "fixed symmetric button sizing import missing")

    require('QLabel("Project Root:")' in text, "Project Root label missing")
    require('setObjectName("engineering_safety_project_root_edit")' in text, "Engineering Safety project-root object name missing")
    require('QPushButton("Search")' in text, "Search button missing")
    require("def search_project_root()" in text, "Search project-root handler missing")
    require("QFileDialog.getExistingDirectory" in text, "Search button does not open directory chooser")
    require("def current_project_root_text()" in text, "current project root reader missing")
    require("current_project_root_text()," in text, "run command does not use project-root widget value")

    require('heading = QLabel("Engineering Safety")' not in text, "duplicated Engineering Safety heading restored")
    require('outer.addWidget(heading)' not in text, "duplicated Engineering Safety heading added to layout")
    require('status_label = QLabel("Ready.")' not in text, "visible Ready label restored")
    require('outer.addWidget(status_label)' not in text, "status label should not be visible in layout")
    require("status_label.setVisible(False)" in text, "internal status label should remain hidden")

    require("button_layout = QGridLayout(button_host)" in text, "button host is not a two-column grid")
    require("group_layout = QGridLayout(group)" in text, "section buttons are not arranged in a two-column grid")
    require("button_layout.setColumnStretch(0, 1)" in text, "outer button column 0 stretch missing")
    require("button_layout.setColumnStretch(1, 1)" in text, "outer button column 1 stretch missing")
    require("group_layout.setColumnStretch(0, 1)" in text, "inner button column 0 stretch missing")
    require("group_layout.setColumnStretch(1, 1)" in text, "inner button column 1 stretch missing")
    require("button_width = 170" in text, "symmetric button width constant missing")
    require("button.setMinimumWidth(button_width)" in text, "button minimum width not normalized")
    require("button.setMaximumWidth(button_width)" in text, "button maximum width not normalized")
    require("QSizePolicy.Fixed" in text, "button fixed size policy missing")
    require("group_layout.addWidget(button, index // 2, index % 2)" in text, "section buttons not split into two columns")
    require("button_layout.addWidget(group, section_index // 2, section_index % 2)" in text, "section groups not split into two columns")

    require("run_engineering_safety_panel_cli_command," in text, "command runner submit missing")
    require("root," not in text, "stale fixed root variable still passed into commands")


def assert_patch_zip_contract() -> None:
    require(PATCH_ZIP.exists(), "patch ZIP missing from validation root")
    with zipfile.ZipFile(PATCH_ZIP, "r") as zf:
        names = set(zf.namelist())
    expected = {
        "reasoner_tools_gui_engineering_safety_panel.py",
        "validation/test_engineering_safety_project_root_layout_v1.py",
        "KANDA_FREEZE_HINT.json",
    }
    require(expected.issubset(names), f"patch ZIP missing files: {sorted(expected - names)}")
    forbidden = [name for name in names if name.startswith("project_freeze_after_update/")]
    require(not forbidden, "patch ZIP must not contain frozen memory entries")


def main() -> int:
    assert_ascii(SOURCE)
    py_compile.compile(str(SOURCE), doraise=True)
    assert_source_contract()
    if PATCH_ZIP.exists():
        assert_patch_zip_contract()
    print("VALIDATION OK: engineering-safety-project-root-layout-v1")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
