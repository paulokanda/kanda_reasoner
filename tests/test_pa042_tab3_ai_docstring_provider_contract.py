"""Focused tests for PA042 Tab 3 AI docstring provider contract."""

from __future__ import annotations

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderRequest,
    AIProviderResult,
    build_ai_provider_request,
    build_openai_compatible_messages,
    generate_ai_docstring_with_fallback,
    normalize_ai_docstring_output,
)


def test_normalize_ai_docstring_output_removes_wrappers() -> None:
    raw = '''```python
def build_runner(name: str):
    """Build a runner.

    Parameters
    ----------
    name : str
        The runner name.
    """
    return name
```
Explanation: this is why.'''
    text = normalize_ai_docstring_output(raw)
    assert text.startswith("Build a runner.")
    assert "Parameters" in text
    assert "def build_runner" not in text
    assert '"""' not in text
    assert "Explanation" not in text


def test_build_ai_provider_request_uses_report_row_contract() -> None:
    row = {
        "file": "E:\\demo_project\\app\\main.py",
        "target_kind": "function",
        "target_name": "build_runner",
        "signature": "build_runner(name: str) -> PipelineRunner",
        "line": 5,
        "suggested_docstring": '"""Build a runner."""',
    }
    module_text = "\n".join(
        [
            "from __future__ import annotations",
            "",
            "from app.services.pipeline import PipelineRunner",
            "",
            "def build_runner(name: str) -> PipelineRunner:",
            "    return PipelineRunner(name=name)",
        ]
    )
    request = build_ai_provider_request(
        row,
        module_text,
        project_root="E:\\demo_project",
    )
    assert request.relative_file_path == "app/main.py"
    assert request.symbol_kind == "function"
    assert request.symbol_name == "build_runner"
    assert request.signature.startswith("build_runner")
    assert request.heuristic_draft == "Build a runner."
    assert "def build_runner" in request.source_snippet


def test_build_openai_compatible_messages_contains_only_contract_context() -> None:
    request = AIProviderRequest(
        project_root="E:\\demo_project",
        relative_file_path="app/main.py",
        symbol_kind="function",
        symbol_name="main",
        signature="main() -> int",
        source_snippet="def main() -> int:\n    return 0",
        heuristic_draft="Return the integer status code.",
    )
    messages = build_openai_compatible_messages(request)
    assert messages[0]["role"] == "system"
    assert "Return only the docstring body" in messages[0]["content"]
    assert messages[1]["role"] == "user"
    assert "Symbol name: main" in messages[1]["content"]
    assert "def main" in messages[1]["content"]


def test_generate_ai_docstring_with_fallback_uses_ai_when_valid() -> None:
    request = AIProviderRequest(
        project_root="",
        relative_file_path="app/main.py",
        symbol_kind="function",
        symbol_name="main",
        signature="main() -> int",
        source_snippet="def main() -> int:\n    return 0",
        heuristic_draft="Return the integer status code.",
    )

    def provider(item: AIProviderRequest) -> AIProviderResult:
        assert item.symbol_name == "main"
        return AIProviderResult(
            provider_name="fake_ai",
            success=True,
            docstring_body='"""Return the application status code."""',
            status="ai_draft_generated",
        )

    result = generate_ai_docstring_with_fallback(request, provider)
    assert result.success is True
    assert result.used_fallback is False
    assert result.provider_name == "fake_ai"
    assert result.docstring_body == "Return the application status code."


def test_generate_ai_docstring_with_fallback_uses_heuristic_on_failure() -> None:
    request = AIProviderRequest(
        project_root="",
        relative_file_path="app/main.py",
        symbol_kind="function",
        symbol_name="main",
        signature="main() -> int",
        source_snippet="def main() -> int:\n    return 0",
        heuristic_draft='"""Return the integer status code."""',
    )

    def provider(item: AIProviderRequest) -> AIProviderResult:
        del item
        raise RuntimeError("local model unavailable")

    result = generate_ai_docstring_with_fallback(request, provider)
    assert result.success is True
    assert result.used_fallback is True
    assert result.provider_name == "heuristic_fallback"
    assert result.status == "AI UNAVAILABLE - HEURISTIC FALLBACK"
    assert result.docstring_body == "Return the integer status code."


if __name__ == "__main__":
    test_normalize_ai_docstring_output_removes_wrappers()
    test_build_ai_provider_request_uses_report_row_contract()
    test_build_openai_compatible_messages_contains_only_contract_context()
    test_generate_ai_docstring_with_fallback_uses_ai_when_valid()
    test_generate_ai_docstring_with_fallback_uses_heuristic_on_failure()
    print("PA042 Tab 3 AI docstring provider contract tests passed.")
