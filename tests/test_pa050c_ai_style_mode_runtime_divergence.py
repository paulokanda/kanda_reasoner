"""Focused tests for PA050C AI style mode runtime divergence."""

from __future__ import annotations

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderRequest,
    AIProviderResult,
    generate_ai_docstring_with_fallback,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_style_runtime import (
    AI_DOCSTRING_STYLE_CONTRACT,
    apply_ai_docstring_style_contract,
)


_ONE_LINE = "Reads and strips the value of an HTTP header."
_SOURCE = "def read_header_value(raw: str) -> str:\n    return raw.strip()"


def _module_request(mode: str) -> AIProviderRequest:
    """Return a module request for style enforcement tests."""
    return AIProviderRequest(
        project_root=r"E:\demo_project",
        relative_file_path="app/encoding_header.py",
        symbol_kind="module",
        symbol_name="encoding_header",
        signature="",
        source_snippet=_SOURCE,
        heuristic_draft="Utilities and definitions for encoding header.",
        docstring_verbosity=mode,
    )


def _function_request(mode: str) -> AIProviderRequest:
    """Return a function request for style enforcement tests."""
    return AIProviderRequest(
        project_root=r"E:\demo_project",
        relative_file_path="app/encoding_header.py",
        symbol_kind="function",
        symbol_name="read_header_value",
        signature="read_header_value(raw: str) -> str",
        source_snippet=_SOURCE,
        heuristic_draft="Return the header value.",
        docstring_verbosity=mode,
    )


def test_module_modes_diverge_when_model_returns_same_one_line() -> None:
    """Module style modes should differ even with identical model output."""
    assert AI_DOCSTRING_STYLE_CONTRACT == "tab3_ai_docstring_style_contract_v1"
    concise = apply_ai_docstring_style_contract(_ONE_LINE, _module_request("concise"))
    balanced = apply_ai_docstring_style_contract(_ONE_LINE, _module_request("balanced"))
    detailed = apply_ai_docstring_style_contract(_ONE_LINE, _module_request("detailed"))

    assert concise == _ONE_LINE
    assert balanced != concise
    assert detailed != concise
    assert "Includes read_header_value." in balanced
    assert "This module includes read_header_value" in detailed


def test_function_modes_diverge_when_model_returns_same_one_line() -> None:
    """Function style modes should add sections outside concise mode."""
    concise = apply_ai_docstring_style_contract(_ONE_LINE, _function_request("concise"))
    balanced = apply_ai_docstring_style_contract(_ONE_LINE, _function_request("balanced"))
    detailed = apply_ai_docstring_style_contract(_ONE_LINE, _function_request("detailed"))

    assert concise == _ONE_LINE
    assert "Parameters" in balanced
    assert "Returns" in balanced
    assert "This function accepts raw and returns str." in detailed
    assert detailed != balanced


def test_provider_pipeline_applies_request_aware_style_contract() -> None:
    """Provider results should be styled after normalization using request context."""

    def provider(_: AIProviderRequest) -> AIProviderResult:
        return AIProviderResult(
            provider_name="fake_ai",
            success=True,
            docstring_body='"""' + _ONE_LINE + '"""',
            status="ai_draft_generated",
        )

    concise = generate_ai_docstring_with_fallback(_function_request("concise"), provider)
    detailed = generate_ai_docstring_with_fallback(_function_request("detailed"), provider)

    assert concise.docstring_body == _ONE_LINE
    assert "Parameters" in detailed.docstring_body
    assert "Returns" in detailed.docstring_body
    assert concise.docstring_body != detailed.docstring_body


if __name__ == "__main__":
    test_module_modes_diverge_when_model_returns_same_one_line()
    test_function_modes_diverge_when_model_returns_same_one_line()
    test_provider_pipeline_applies_request_aware_style_contract()
    print("PA050C AI style mode runtime divergence tests passed.")
