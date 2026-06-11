"""Tests for Tab 3 manual review AI suggestion owner-widget lookup."""

from __future__ import annotations

import io
import json
from unittest.mock import patch

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.manual_docstring_review_ai import (
    suggest_manual_review_docstring,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_suggestion import (
    generate_manual_review_docstring,
)


class _TextWidget:
    def __init__(self, text: str) -> None:
        self._text = text

    def text(self) -> str:
        return self._text


class _Combo:
    def __init__(self, text: str) -> None:
        self._text = text

    def currentText(self) -> str:
        return self._text


class _Owner:
    def __init__(self) -> None:
        self._base_url_edit = _TextWidget("http://localhost:11434/v1")
        self._model_combo = _Combo("qwen3-coder:30b")


class _FakeResponse:
    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None

    def read(self) -> bytes:
        payload = {"choices": [{"message": {"content": "\"\"\"Describe selected target.\"\"\""}}]}
        return json.dumps(payload).encode("utf-8")


def test_manual_review_runtime_public_contract_is_importable() -> None:
    assert callable(generate_manual_review_docstring)


def test_manual_review_ai_uses_tab3_owner_widgets() -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(request: object, timeout: float) -> _FakeResponse:
        captured["timeout"] = timeout
        captured["url"] = getattr(request, "full_url", "")
        data = getattr(request, "data", b"{}")
        captured["payload"] = json.loads(data.decode("utf-8"))
        return _FakeResponse()

    location = {
        "file": "pkg/mod.py",
        "line": 1,
        "target_kind": "function",
        "target_name": "build_value",
    }
    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = suggest_manual_review_docstring(_Owner(), location, "def build_value():\n    pass\n")

    payload = captured["payload"]
    assert captured["url"] == "http://localhost:11434/v1/chat/completions"
    assert payload["model"] == "qwen3-coder:30b"
    assert result == '"""Describe selected target."""'


def test_manual_review_ai_falls_back_without_model() -> None:
    owner = _Owner()
    owner._model_combo = _Combo("")
    location = {"target_name": "build_value"}

    result = suggest_manual_review_docstring(owner, location, "")

    assert result == '"""Support build value behavior."""'


if __name__ == "__main__":
    test_manual_review_runtime_public_contract_is_importable()
    test_manual_review_ai_uses_tab3_owner_widgets()
    test_manual_review_ai_falls_back_without_model()
    print("Tab 3 manual review AI owner-widget tests passed.")
