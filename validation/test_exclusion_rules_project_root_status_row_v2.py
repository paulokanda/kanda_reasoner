from __future__ import annotations

from pathlib import Path
import py_compile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FEATURE = "exclusion-rules-project-root-status-row-v2"
IGNORE_TAB = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "ignore_rules_tab.py"
UI_BUILDERS = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "ignore_rules_tab_help" / "ui_builders.py"
MAIN_WINDOW = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "main_window.py"
PATCH_ZIP = ROOT / "kanda_exclusion_rules_project_root_status_row_v2_patch.zip"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    for path in (IGNORE_TAB, UI_BUILDERS, MAIN_WINDOW):
        py_compile.compile(str(path), doraise=True)

    tab_text = IGNORE_TAB.read_text(encoding="utf-8")
    ui_text = UI_BUILDERS.read_text(encoding="utf-8")
    main_text = MAIN_WINDOW.read_text(encoding="utf-8")

    require('self.project_root_label = QLabel("Project Root:")' in tab_text, "Project Root label object missing")
    require('color: #0B3D91; font-weight: bold;' in tab_text, "Project Root label is not bold blue")
    require('self.project_root_edit.setMinimumWidth(260)' in tab_text, "Project Root editor minimum width was not reduced")
    require('self.project_root_edit.setMaximumWidth(310)' in tab_text, "Project Root editor maximum width guard missing")
    require('self.project_scope_label.setWordWrap(False)' in tab_text, "Scope label should stay on one line")
    require('self.project_root_search_button = QPushButton("Search")' in tab_text, "Project Root Search button missing")
    require('self.project_root_search_button.clicked.connect(self._browse_project_root)' in tab_text, "Search button is not wired")
    require('Active project:' not in tab_text, "Visible Active project label text must not be restored")

    require('project_scope_row = QHBoxLayout()' in ui_text, "Project/scope row missing")
    require('project_scope_row.addWidget(self.project_root_label, 0)' in ui_text, "Bold blue Project Root label is not in row")
    require('QLabel("Project Root:")' not in ui_text, "Anonymous Project Root label must not be restored")
    require('project_scope_row.addWidget(self.project_root_edit, 0)' in ui_text, "Project Root editor should not consume stretch before scope")
    require('project_scope_row.addWidget(self.project_scope_label, 1)' in ui_text, "Scope label should receive row stretch")
    require('main_layout.addWidget(self.project_label)' not in ui_text, "Visible Active project label still added to layout")

    require('self._bind_project_root_field(self.ignore_rules_tab.project_root_edit)' in main_text, "Built-in Exclusion Rules Project Root field is not bound to shared project root propagation")
    require('self._set_project_root_field_text(' in main_text and 'self.ignore_rules_tab.project_root_edit' in main_text, "Shell does not initialize Exclusion Rules Project Root field")

    if PATCH_ZIP.exists():
        with zipfile.ZipFile(PATCH_ZIP, "r") as zf:
            names = set(zf.namelist())
        required = {
            "kanda_reasoner_app/reasoner_tools_gui_shell/ignore_rules_tab.py",
            "kanda_reasoner_app/reasoner_tools_gui_shell/ignore_rules_tab_help/ui_builders.py",
            "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py",
            "validation/test_exclusion_rules_project_root_status_row_v2.py",
            "KANDA_FREEZE_HINT.json",
        }
        missing = sorted(required - names)
        require(not missing, "Patch ZIP missing required members: " + ", ".join(missing))
        print("ZIP CONTRACT: PASS")
    else:
        print("ZIP CONTRACT: SKIPPED (patch ZIP not present beside project root)")

    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
