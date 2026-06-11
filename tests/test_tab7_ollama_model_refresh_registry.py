"""Compatibility regression test for Tab 7 Ollama model refresh discovery."""

from __future__ import annotations

import subprocess
from typing import Any
from unittest.mock import patch

from kanda_reasoner_app.project_reasoner_v10 import v10_model_registry
from kanda_reasoner_app.project_reasoner_v10.v10_model_registry import (
    LocalModelRegistry,
)


class _FakeResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        return self._payload


def _fake_get(url: str, timeout: int) -> _FakeResponse:
    del timeout
    if url == v10_model_registry.OLLAMA_TAGS_URL:
        return _FakeResponse({"models": [{"name": "qwen2.5-coder:7b"}]})
    if url == v10_model_registry.OLLAMA_MODELS_URL:
        return _FakeResponse({"data": [{"id": "devstral-small:latest"}]})
    raise AssertionError("Unexpected URL: " + url)


def _fake_run(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    assert args[0] == ["ollama", "list"]
    assert kwargs["capture_output"] is True
    assert kwargs["text"] is True
    return subprocess.CompletedProcess(
        args=args[0],
        returncode=0,
        stdout=(
            "NAME                    ID              SIZE      MODIFIED\n"
            "deepseek-r1:14b         abcdef123456    9 GB      1 day ago\n"
            "devstral-small:latest   123456abcdef    7 GB      1 minute ago\n"
        ),
        stderr="",
    )


def test_list_models_merges_tags_v1_and_cli_sources() -> None:
    with patch.object(v10_model_registry.requests, "get", side_effect=_fake_get):
        with patch.object(v10_model_registry.subprocess, "run", side_effect=_fake_run):
            models = LocalModelRegistry().list_models()

    assert models == [
        "deepseek-r1:14b",
        "devstral-small:latest",
        "qwen2.5-coder:7b",
    ]


if __name__ == "__main__":
    test_list_models_merges_tags_v1_and_cli_sources()
    print("Tab 7 Ollama model refresh registry tests passed.")
