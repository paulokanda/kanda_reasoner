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


def _ui_text() -> str:
    return UI_PATH.read_text(encoding="utf-8")


def test_run_collector_button_is_renamed_to_create_second_prompt_files() -> None:
    text = _ui_text()
    assert 'self.run_button = QPushButton("Create Second Prompt Files")' in text
    assert 'self.run_button = QPushButton("Run Collector")' not in text


def test_combined_button_is_bold_green_and_sits_left_of_project_root_label() -> None:
    text = _ui_text()
    combined_create = (
        'self.create_first_and_second_prompt_files_button = QPushButton("Create First and Second Prompt Files")'
    )
    add_combined = 'project_root_row.addWidget(self.create_first_and_second_prompt_files_button)'
    add_project_label = 'project_root_row.addWidget(QLabel("Project root:"))'
    browse_create = 'self.browse_project_button = QPushButton("Browse...")'
    columns_index = text.index('QGroupBox("Show Project to AI First Prompt Files")')

    assert combined_create in text
    assert add_combined in text
    assert add_project_label in text
    assert browse_create in text
    assert text.index(add_combined) < text.index(add_project_label) < text.index(browse_create) < columns_index
    assert 'combined_button_font.setBold(True)' in text
    assert 'self.create_first_and_second_prompt_files_button.setFont(combined_button_font)' in text
    assert 'self.create_first_and_second_prompt_files_button.setStyleSheet("color: green; font-weight: bold;")' in text


def test_combined_button_runs_first_prompt_then_second_prompt_in_series() -> None:
    text = _ui_text()
    helper_index = text.index('def _create_first_and_second_prompt_files() -> None:')
    first_index = text.index('_first_prompt_impl.run_create_first_prompt_files(self)', helper_index)
    second_index = text.index('self._run_collector()', helper_index)
    connect_index = text.index(
        'self.create_first_and_second_prompt_files_button.clicked.connect(_create_first_and_second_prompt_files)'
    )

    assert helper_index < first_index < second_index < connect_index
    assert '"failed", "invalid", "busy"' in text
    assert 'Create Second Prompt Files skipped because Create First Prompt Files did not finish cleanly.' in text


def test_inner_duplicate_show_project_to_ai_label_is_hidden() -> None:
    text = _ui_text()
    add_tab_index = text.index('self.tabs.addTab(collector_tab, "Show Project to AI")')
    hide_index = text.index('self.tabs.tabBar().setTabVisible(0, False)', add_tab_index)
    fallback_index = text.index('self.tabs.setTabText(0, "")', add_tab_index)
    json_splitter_index = text.index('self.tabs.addTab(self.splitter_panel, "JSON Splitter")')

    assert add_tab_index < hide_index < json_splitter_index
    assert add_tab_index < fallback_index < json_splitter_index


def main() -> int:
    test_run_collector_button_is_renamed_to_create_second_prompt_files()
    test_combined_button_is_bold_green_and_sits_left_of_project_root_label()
    test_combined_button_runs_first_prompt_then_second_prompt_in_series()
    test_inner_duplicate_show_project_to_ai_label_is_hidden()
    print("VALIDATION OK: show_project_to_ai_combined_actions_v1")
    print("VALIDATION OK: show project to AI combined actions")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
