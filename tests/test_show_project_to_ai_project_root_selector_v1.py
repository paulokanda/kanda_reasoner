from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
UI_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_shell"
    / "runner_help"
    / "window_methods_private_impl.py"
)
FIRST_PROMPT_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_shell"
    / "runner_help"
    / "first_prompt_files_private_impl.py"
)
SECOND_PROMPT_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_shell"
    / "runner_help"
    / "window_process_private_impl.py"
)


def _ui_text() -> str:
    return UI_PATH.read_text(encoding="utf-8")


def test_project_root_selector_is_shared_above_first_and_second_columns() -> None:
    text = _ui_text()

    project_row_index = text.index("project_root_row = QHBoxLayout()")
    first_column_index = text.index('QGroupBox("Show Project to AI First Prompt Files")')
    second_column_index = text.index('QGroupBox("Show Project to AI Second Prompt Files")')
    splitter_index = text.index("QSplitter(Qt.Horizontal)")

    assert project_row_index < first_column_index < second_column_index < splitter_index
    assert 'project_root_row.addWidget(QLabel("Project root:"))' in text
    assert 'self.project_root_edit = QLineEdit(' in text
    assert 'self.browse_project_button = QPushButton("Browse...")' in text
    assert 'collector_layout.addLayout(project_root_row)' in text


def test_second_prompt_column_no_longer_owns_project_root_row() -> None:
    text = _ui_text()
    second_column_index = text.index('QGroupBox("Show Project to AI Second Prompt Files")')
    out_row_index = text.index("out_row = QHBoxLayout()")
    second_column_slice = text[second_column_index:out_row_index]

    assert "Project root:" not in second_column_slice
    assert "project_root_edit" not in second_column_slice
    assert "browse_project_button" not in second_column_slice


def test_both_first_and_second_prompt_actions_use_shared_project_root_edit() -> None:
    first_text = FIRST_PROMPT_PATH.read_text(encoding="utf-8")
    second_text = SECOND_PROMPT_PATH.read_text(encoding="utf-8")

    assert "window.project_root_edit.text().strip()" in first_text
    assert "self.project_root_edit.text().strip()" in second_text
    assert "Uses the Project root field above as the source folder." in _ui_text()


def main() -> int:
    test_project_root_selector_is_shared_above_first_and_second_columns()
    test_second_prompt_column_no_longer_owns_project_root_row()
    test_both_first_and_second_prompt_actions_use_shared_project_root_edit()
    print("VALIDATION OK: show_project_to_ai_project_root_selector_v1")
    print("VALIDATION OK: show project to AI project root selector")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
