"""Project-root header labels must keep the shared blue bold style."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT_LABEL_STYLE = "color: #0B3D91; font-weight: bold;"


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_error_memory_project_root_label_is_blue_bold() -> None:
    source = _read("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")

    assert "self.project_root_header_label = QLabel('Project Root:')" in source
    assert (
        f"self.project_root_header_label.setStyleSheet('{PROJECT_ROOT_LABEL_STYLE}')"
        in source
    )


def test_docstring_assistant_project_root_label_is_blue_bold() -> None:
    source = _read(
        "kanda_reasoner_app/insert_missing_docstrings_gui/"
        "insert_missing_docstrings_gui_help/window_state.py"
    )

    assert 'self._root_path_label = QLabel("Project Root:")' in source
    assert (
        f'self._root_path_label.setStyleSheet("{PROJECT_ROOT_LABEL_STYLE}")'
        in source
    )


def test_project_qa_project_root_label_is_blue_bold() -> None:
    source = _read(
        "kanda_reasoner_app/reasoner_engine/"
        "ai_reasoner_main_window_help/ui_builder.py"
    )

    assert 'window.project_root_label = QLabel("Project root:")' in source
    assert (
        f'window.project_root_label.setStyleSheet("{PROJECT_ROOT_LABEL_STYLE}")'
        in source
    )


if __name__ == "__main__":
    test_error_memory_project_root_label_is_blue_bold()
    test_docstring_assistant_project_root_label_is_blue_bold()
    test_project_qa_project_root_label_is_blue_bold()
    print("Project-root label blue bold tests passed.")
