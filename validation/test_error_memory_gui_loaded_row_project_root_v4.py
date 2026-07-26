from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERROR_TAB = ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
LAZY_TABS = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    error_text = ERROR_TAB.read_text(encoding="utf-8")
    lazy_text = LAZY_TABS.read_text(encoding="utf-8")

    require('QLabel("Error Memory")' not in error_text, "Duplicate inner Error Memory title label must be removed.")
    require('error_memory_title_label' not in error_text, "Duplicate Error Memory title object name must be removed.")
    require('Loaded project context' not in error_text, "Loaded project context label must remain removed.")
    require('def move_project_root_controls_to_layout' in error_text, "Error Memory tab must expose a move method for host row insertion.")
    require('self.project_root_value_label.setMaximumWidth(320)' in error_text, "Project Root path field must have reduced maximum width.")
    require('outer.addLayout(root_row)' not in error_text, "Project Root row must not be added inside the tab body.")
    require('self._project_root_controls_moved = False' in error_text, "Move guard must be present.")
    require('self.search_project_button = QPushButton("Search")' in error_text, "Search button must remain present.")
    require('self.open_memory_button = QPushButton("Open EM Folder")' in error_text, "Open EM Folder button must remain present.")
    require('self.open_second_prompt_button = QPushButton("Open Second Prompt Files")' in error_text, "Open Second Prompt Files button must remain present.")
    require('self.copy_memory_path_button = QPushButton("Get path to EM Folder")' in error_text, "Get path to EM Folder button must remain present.")
    require('self.copy_second_prompt_path_button = QPushButton("Get path to Second Prompt Files")' in error_text, "Get path to Second Prompt Files button must remain present.")
    require('operation_phase_combo' not in error_text, "Manual Operation phase combo must remain removed.")
    require('Save Draft from Raw Error' not in error_text, "Save Draft from Raw Error button must remain removed.")
    require('Memorize Error' in error_text, "Memorize Error button must remain present.")

    require('_ERROR_MEMORY_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/error_memory_gui/error_memory_tab.py"' in lazy_text, "Lazy host must define Error Memory source hint.")
    require('def _move_error_memory_project_root_controls_to_status_row' in lazy_text, "Lazy host must expose Error Memory mover.")
    require('move_project_root_controls_to_layout' in lazy_text, "Lazy host must call Error Memory move method.")
    require('self._move_error_memory_project_root_controls_to_status_row(widget)' in lazy_text, "Lazy host must call mover during load_tool.")
    require('mover(self.status_source_row, self._status_source_insert_index)' in lazy_text, "Mover must insert controls into LOADED/Source row before stretch.")

    print("VALIDATION OK: error-memory-gui-loaded-row-project-root-v4")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
