"""Project Q&A Ask Local AI button enablement tests."""

from __future__ import annotations

import tempfile
from pathlib import Path

from kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help.runtime_controller import (
    RuntimeController,
)


class _FakeText:
    def __init__(self, value: str = "") -> None:
        self.value = value

    def text(self) -> str:
        return self.value

    def setText(self, value: str) -> None:
        self.value = value


class _FakeEnabled:
    def __init__(self) -> None:
        self.enabled: bool | None = None

    def setEnabled(self, value: bool) -> None:
        self.enabled = bool(value)


class _FakeProjectIndex:
    def __init__(self, loaded: bool = False) -> None:
        self.index_data = {"project_summary": {}} if loaded else {}


class _FakeWindow:
    def __init__(self, *, question: str, json_path: str, loaded: bool) -> None:
        self.project_root_edit = _FakeText("E:/example_project")
        self.question_edit = _FakeText(question)
        self.json_path_edit = _FakeText(json_path)
        self.project_index = _FakeProjectIndex(loaded)
        self._analysis_running = False
        self._manual_project_profile_name = ""
        self.pick_project_root_button = _FakeEnabled()
        self.run_analysis_button = _FakeEnabled()
        self.load_button = _FakeEnabled()
        self.ask_ai_button = _FakeEnabled()
        self.static_context_button = _FakeEnabled()
        self.profile_override_combo = _FakeEnabled()
        self.reset_profile_override_button = _FakeEnabled()
        self.ensure_local_ai_json_button = _FakeEnabled()
        self.refresh_local_ai_json_button = _FakeEnabled()


def test_ask_button_enables_for_question_and_loadable_json_path() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        json_path = Path(tmp_dir) / "demo__complete_local_AI.json"
        json_path.write_text("{}", encoding="utf-8")
        window = _FakeWindow(
            question="Where is the architecture entry point?",
            json_path=str(json_path),
            loaded=False,
        )

        RuntimeController().refresh_workflow_controls(window)

        assert window.ask_ai_button.enabled is True


def test_ask_button_enables_for_question_even_when_json_not_loaded_yet() -> None:
    window = _FakeWindow(
        question="Where is the architecture entry point?",
        json_path="",
        loaded=False,
    )

    RuntimeController().refresh_workflow_controls(window)

    assert window.ask_ai_button.enabled is True


def test_ask_button_stays_disabled_without_question() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        json_path = Path(tmp_dir) / "demo__complete_local_AI.json"
        json_path.write_text("{}", encoding="utf-8")
        window = _FakeWindow(question="", json_path=str(json_path), loaded=True)

        RuntimeController().refresh_workflow_controls(window)

        assert window.ask_ai_button.enabled is False


def test_ask_button_enables_for_question_and_loaded_json() -> None:
    window = _FakeWindow(
        question="Explain the retrieval flow.",
        json_path="",
        loaded=True,
    )

    RuntimeController().refresh_workflow_controls(window)

    assert window.ask_ai_button.enabled is True


def test_question_and_json_path_changes_refresh_workflow_controls() -> None:
    source = Path(
        "kanda_reasoner_app/reasoner_engine/"
        "ai_reasoner_main_window_help/signal_wiring.py"
    ).read_text(encoding="utf-8")

    assert (
        "window.question_edit.textChanged.connect(lambda _text: "
        "window._refresh_workflow_controls())"
        in source
    )
    assert (
        "window.json_path_edit.textChanged.connect(lambda _text: "
        "window._refresh_workflow_controls())"
        in source
    )


def test_ask_handler_auto_loads_json_path_before_session_execute() -> None:
    source = Path(
        "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py"
    ).read_text(encoding="utf-8")

    auto_load_index = source.index("ensure_project_json_loaded_for_question")
    execute_index = source.index("self.session_service.execute")
    assert auto_load_index < execute_index


if __name__ == "__main__":
    test_ask_button_enables_for_question_and_loadable_json_path()
    test_ask_button_enables_for_question_even_when_json_not_loaded_yet()
    test_ask_button_stays_disabled_without_question()
    test_ask_button_enables_for_question_and_loaded_json()
    test_question_and_json_path_changes_refresh_workflow_controls()
    test_ask_handler_auto_loads_json_path_before_session_execute()
    print("Project Q&A Ask Local AI enablement tests passed.")
