"""Regression tests for Show Project to AI path-copy buttons and combined button placement."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "kanda_reasoner_app" / "reasoner_tools_shell" / "runner_help" / "window_methods_private_impl.py"


def _text() -> str:
    return SOURCE.read_text(encoding="utf-8")


def test_combined_button_is_green_and_left_of_project_root_label() -> None:
    text = _text()
    button_create = 'self.create_first_and_second_prompt_files_button = QPushButton("Create First and Second Prompt Files")'
    green_style = 'self.create_first_and_second_prompt_files_button.setStyleSheet("color: green; font-weight: bold;")'
    add_button = 'project_root_row.addWidget(self.create_first_and_second_prompt_files_button)'
    add_label = 'project_root_row.addWidget(QLabel("Project root:"))'
    browse = 'self.browse_project_button = QPushButton("Browse...")'

    assert button_create in text
    assert green_style in text
    assert text.index(add_button) < text.index(add_label) < text.index(browse)


def test_path_copy_buttons_exist_inside_columns_and_are_blue() -> None:
    text = _text()
    assert 'self.path_to_first_prompt_files_button = QPushButton("Path to First Prompt Files")' in text
    assert 'self.path_to_first_prompt_files_button.setStyleSheet("color: blue;")' in text
    assert 'left_layout.addWidget(self.path_to_first_prompt_files_button)' in text

    assert 'self.path_to_second_prompt_files_button = QPushButton("Path to Second Prompt Files")' in text
    assert 'self.path_to_second_prompt_files_button.setStyleSheet("color: blue;")' in text
    assert 'button_row.addWidget(self.path_to_second_prompt_files_button)' in text


def test_path_buttons_copy_dynamic_first_and_second_paths() -> None:
    text = _text()
    assert 'def _copy_show_project_to_ai_path(kind: str) -> None:' in text
    assert 'analysis_first_prompt_files_dir' in text
    assert 'analysis_json_complete_dir' in text
    assert 'QApplication.clipboard().setText(str(target_path))' in text
    assert 'self.path_to_first_prompt_files_button.clicked.connect(' in text
    assert 'lambda: _copy_show_project_to_ai_path("first")' in text
    assert 'self.path_to_second_prompt_files_button.clicked.connect(' in text
    assert 'lambda: _copy_show_project_to_ai_path("second")' in text


def test_no_regression_of_existing_action_labels() -> None:
    text = _text()
    assert 'self.run_button = QPushButton("Create Second Prompt Files")' in text
    assert 'self.create_first_prompt_files_button = QPushButton("Create First Prompt Files")' in text
    assert 'self.zip_json_files_button = QPushButton("Zip JSON files")' not in text
    assert 'button_row.addWidget(QLabel("ZIP size limit:"))' in text
    for label in ("100 MB", "200 MB", "300 MB", "400 MB", "500 MB"):
        assert f'QRadioButton("{label}")' in text


if __name__ == "__main__":
    test_combined_button_is_green_and_left_of_project_root_label()
    test_path_copy_buttons_exist_inside_columns_and_are_blue()
    test_path_buttons_copy_dynamic_first_and_second_paths()
    test_no_regression_of_existing_action_labels()
    print("VALIDATION OK: show_project_to_ai_path_buttons_v1")
    print("VALIDATION OK: show project to AI path buttons")
