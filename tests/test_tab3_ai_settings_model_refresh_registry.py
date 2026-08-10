"""Tests for Tab 3 AI model refresh model discovery."""

from __future__ import annotations

import json
from unittest.mock import patch

from kanda_reasoner_app.tab3_manual_review_runtime.ai_settings_runtime import (
    TAB3_AI_SETTINGS_RUNTIME_CONTRACT,
)

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help import (
    ai_settings,
)


class _TextWidget:
    def __init__(self, text: str) -> None:
        self._text = text

    def text(self) -> str:
        return self._text

    def setText(self, value: str) -> None:
        self._text = value


class _Combo:
    def __init__(self, current: str = "") -> None:
        self.items: list[str] = []
        self.current = current

    def currentText(self) -> str:
        return self.current

    def clear(self) -> None:
        self.items.clear()

    def addItems(self, items: list[str]) -> None:
        self.items.extend(items)

    def addItem(self, item: str) -> None:
        self.items.append(item)

    def setCurrentText(self, value: str) -> None:
        self.current = value


class _StatusBar:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def showMessage(self, message: str) -> None:
        self.messages.append(message)


class _Owner:
    def __init__(self) -> None:
        self._base_url_edit = _TextWidget("http://localhost:11434/v1")
        self._model_combo = _Combo("qwen3-coder:30b")
        self.status_bar = _StatusBar()

    def statusBar(self) -> _StatusBar:
        return self.status_bar


class _FakeResponse:
    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None

    def read(self) -> bytes:
        payload = {"models": [{"name": "qwen3-coder:30b"}]}
        return json.dumps(payload).encode("utf-8")


def test_ai_settings_runtime_imports_through_direct_contract() -> None:
    assert TAB3_AI_SETTINGS_RUNTIME_CONTRACT == "tab3_ai_settings_runtime"


def test_refresh_models_uses_local_sources_and_preserves_current_model() -> None:
    owner = _Owner()
    def fake_run(*args: object, **kwargs: object) -> object:
        return type("Result", (), {"returncode": 0, "stdout": "NAME ID SIZE MODIFIED\nqwen2.5-coder:7b abc 1GB today\n"})()

    with patch("urllib.request.urlopen", return_value=_FakeResponse()), patch("subprocess.run", side_effect=fake_run):
        ai_settings.refresh_models(owner)

    assert owner._model_combo.items == ["qwen2.5-coder:7b", "qwen3-coder:30b"]
    assert owner._model_combo.current == "qwen3-coder:30b"
    assert owner.status_bar.messages[-1] == "Loaded 2 installed model(s)."


def test_build_ai_config_uses_current_model_text() -> None:
    owner = _Owner()
    owner._model_combo.current = "qwen2.5-coder:7b"
    owner._workers_spin = type("Spin", (), {"value": lambda self: 3})()
    owner._include_private_checkbox = type("Check", (), {"isChecked": lambda self: False})()
    owner._min_confidence_combo = _Combo("medium")
    owner._no_uncertain_checkbox = type("Check", (), {"isChecked": lambda self: True})()

    cfg = ai_settings.build_ai_config(owner)

    assert cfg.model == "qwen2.5-coder:7b"
    assert cfg.workers == 3
    assert cfg.include_private is False
    assert cfg.min_confidence == "medium"
    assert cfg.uncertain_annotation is False


if __name__ == "__main__":
    test_ai_settings_runtime_imports_through_direct_contract()
    test_refresh_models_uses_local_sources_and_preserves_current_model()
    test_build_ai_config_uses_current_model_text()
    print("Tab 3 AI settings model refresh registry tests passed.")
