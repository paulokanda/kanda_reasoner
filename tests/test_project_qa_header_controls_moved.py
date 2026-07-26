"""Regression coverage for Project Q&A header control relocation."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_project_qa_body_labels_are_movable_widgets() -> None:
    """The moved rows must not leave orphan labels behind in the body."""
    source = _read(
        "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/ui_builder.py"
    )

    assert 'window.project_root_label = QLabel("Project root:")' in source
    assert "layout.addWidget(window.project_root_label, 0, 0)" in source
    assert 'window.local_ai_model_label = QLabel("Model:")' in source
    assert "layout.addWidget(window.local_ai_model_label, 2, 0)" in source


def test_project_qa_exports_live_widget_move_hooks() -> None:
    """Project Q&A should move the real connected widgets, not clones."""
    source = _read("kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py")

    assert "def move_project_root_controls_to_layout(" in source
    assert "self.project_root_edit" in source
    assert "self.pick_project_root_button" in source
    assert "self.run_analysis_button" in source
    assert "def move_ai_runtime_controls_to_layout(" in source
    assert "self.model_combo" in source
    assert "self.refresh_models_button" in source
    assert "_project_root_controls_moved_to_host" in source
    assert "_ai_runtime_controls_moved_to_host" in source


def test_lazy_shell_uses_project_qa_hooks_without_second_ai_combo() -> None:
    """The shell should route Q&A controls to the template slots once."""
    source = _read("kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py")

    install_start = source.index("if spec.source_hint in {")
    install_end = source.index("}:", install_start)
    install_set = source[install_start:install_end]

    assert "_PROJECT_QA_GUI_SOURCE" not in install_set
    assert "def _move_project_qa_project_root_controls_to_header_row" in source
    assert "def _move_project_qa_ai_controls_to_header_row" in source
    assert 'getattr(widget, "move_project_root_controls_to_layout", None)' in source
    assert 'getattr(widget, "move_ai_runtime_controls_to_layout", None)' in source
    assert "self._move_project_qa_project_root_controls_to_header_row(widget)" in source
    assert "self._move_project_qa_ai_controls_to_header_row(widget)" in source


if __name__ == "__main__":
    test_project_qa_body_labels_are_movable_widgets()
    test_project_qa_exports_live_widget_move_hooks()
    test_lazy_shell_uses_project_qa_hooks_without_second_ai_combo()
    print("Project Q&A header control relocation tests passed.")
