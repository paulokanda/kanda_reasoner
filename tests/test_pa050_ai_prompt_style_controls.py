"""Focused tests for PA050 Tab 3 AI prompt style controls."""

from __future__ import annotations

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderRequest,
    build_ai_provider_request,
    build_openai_compatible_messages,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_row_bridge_runtime import (
    build_review_row_ai_request,
)


class _ComboBox:
    """Small combo-box fake for verbosity selection tests."""

    def __init__(self, value: str) -> None:
        self._value = value

    def currentText(self) -> str:
        return self._value


class _TextBox:
    """Small text-widget fake for project root tests."""

    def __init__(self, value: str) -> None:
        self._value = value

    def text(self) -> str:
        return self._value


class _Owner:
    """Small owner fake carrying Local AI prompt controls."""

    def __init__(self, verbosity: str) -> None:
        self._root_path_edit = _TextBox(r"E:\demo_project")
        self._ai_docstring_verbosity_combo = _ComboBox(verbosity)


def test_build_provider_messages_include_concise_guidance_by_default() -> None:
    request = AIProviderRequest(
        project_root=r"E:\demo_project",
        relative_file_path="app/main.py",
        symbol_kind="function",
        symbol_name="main",
        signature="main() -> int",
        source_snippet="def main() -> int:\n    return 0",
        heuristic_draft="Return the integer status code.",
    )
    messages = build_openai_compatible_messages(request)
    system = messages[0]["content"]
    user = messages[1]["content"]

    assert "Use a concise docstring" in system
    assert "Avoid extra explanatory paragraphs" in system
    assert "Verbosity: concise" in user
    assert "NumPy-style" in system


def test_build_provider_messages_respect_detailed_verbosity() -> None:
    request = AIProviderRequest(
        project_root=r"E:\demo_project",
        relative_file_path="app/main.py",
        symbol_kind="function",
        symbol_name="build_runner",
        signature="build_runner(name: str) -> object",
        source_snippet="def build_runner(name: str) -> object:\n    return object()",
        heuristic_draft="Build a runner.",
        docstring_verbosity="Detailed",
    )
    messages = build_openai_compatible_messages(request)

    assert "Verbosity: detailed" in messages[1]["content"]
    assert "Use a detailed but reviewable docstring" in messages[0]["content"]


def test_build_provider_request_normalizes_unknown_verbosity_to_concise() -> None:
    row = {
        "file": r"E:\demo_project\app\main.py",
        "target_kind": "function",
        "target_name": "main",
        "line": 1,
        "suggested_docstring": "Return the integer status code.",
    }
    request = build_ai_provider_request(
        row,
        "def main() -> int:\n    return 0",
        project_root=r"E:\demo_project",
        docstring_verbosity="verbose",
    )

    assert request.docstring_verbosity == "concise"


def test_row_bridge_reads_owner_verbosity_combo() -> None:
    owner = _Owner("Balanced")
    row = {
        "file": r"E:\demo_project\app\main.py",
        "target_kind": "function",
        "target_name": "main",
        "line": 1,
        "suggested_docstring": "Return the integer status code.",
    }
    request = build_review_row_ai_request(
        owner,
        row,
        "def main() -> int:\n    return 0",
    )

    assert request.docstring_verbosity == "balanced"


def test_layout_declares_ai_draft_style_control() -> None:
    from pathlib import Path

    text = Path(
        'ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime/layout_runtime.py'
    ).read_text(encoding="utf-8")

    assert "AI draft style" in text
    assert "_ai_docstring_verbosity_combo" in text
    assert "Concise" in text
    assert "Balanced" in text
    assert "Detailed" in text


if __name__ == "__main__":
    test_build_provider_messages_include_concise_guidance_by_default()
    test_build_provider_messages_respect_detailed_verbosity()
    test_build_provider_request_normalizes_unknown_verbosity_to_concise()
    test_row_bridge_reads_owner_verbosity_combo()
    test_layout_declares_ai_draft_style_control()
    print("PA050 AI prompt style control tests passed.")
