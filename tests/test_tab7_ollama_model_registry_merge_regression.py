"""Regression tests for Tab 7 Ollama registry model discovery."""

from __future__ import annotations

import subprocess
from typing import Any
from unittest.mock import patch

import requests

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
        return _FakeResponse({"data": [{"id": "qwen3-coder:30b"}]})
    raise AssertionError("Unexpected URL: " + url)


def _failing_get(*args: Any, **kwargs: Any) -> None:
    del args, kwargs
    raise requests.RequestException("offline endpoint")


def _fake_run(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    assert args[0] == ["ollama", "list"]
    assert kwargs["capture_output"] is True
    assert kwargs["text"] is True
    return subprocess.CompletedProcess(
        args=args[0],
        returncode=0,
        stdout=(
            "NAME                ID              SIZE      MODIFIED\n"
            "qwen3-coder:30b     06c1097efce0    18 GB     23 hours ago\n"
            "qwen2.5-coder:7b    dae161e27b0e    4.7 GB    8 weeks ago\n"
        ),
        stderr="",
    )


def test_registry_merges_all_supported_ollama_sources() -> None:
    with patch.object(v10_model_registry.requests, "get", side_effect=_fake_get):
        with patch.object(v10_model_registry.subprocess, "run", side_effect=_fake_run):
            models = LocalModelRegistry().list_models()

    assert models == ["qwen2.5-coder:7b", "qwen3-coder:30b"]


def test_registry_uses_ollama_cli_when_http_endpoints_fail() -> None:
    with patch.object(v10_model_registry.requests, "get", side_effect=_failing_get):
        with patch.object(v10_model_registry.subprocess, "run", side_effect=_fake_run):
            models = LocalModelRegistry().list_models()

    assert models == ["qwen2.5-coder:7b", "qwen3-coder:30b"]


if __name__ == "__main__":
    test_registry_merges_all_supported_ollama_sources()
    test_registry_uses_ollama_cli_when_http_endpoints_fail()
    print("Tab 7 Ollama model registry merge regression tests passed.")
