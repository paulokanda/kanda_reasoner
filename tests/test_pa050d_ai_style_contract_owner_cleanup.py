"""Focused tests for PA050D AI style contract owner cleanup."""

from __future__ import annotations

import inspect

from kanda_reasoner_app.tab3_manual_review_runtime import ai_docstring_provider_runtime
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderRequest,
    AIProviderResult,
    generate_ai_docstring_with_fallback,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_style_runtime import (
    apply_ai_docstring_style_contract,
)


_ONE_LINE = "Reads and strips the value of an HTTP header."
_SOURCE = "def read_header_value(raw: str) -> str:\n    return raw.strip()"


def _function_request(mode: str) -> AIProviderRequest:
    """Return a function request for style owner cleanup tests."""
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


def test_style_contract_has_single_public_owner() -> None:
    """Provider facade should not export the style contract owner symbol."""
    assert "apply_ai_docstring_style_contract" not in ai_docstring_provider_runtime.__all__
    assert not hasattr(ai_docstring_provider_runtime, "apply_ai_docstring_style_contract")
    assert callable(apply_ai_docstring_style_contract)


def test_provider_uses_private_style_contract_alias() -> None:
    """Provider runtime should call the style contract through a private alias."""
    source = inspect.getsource(ai_docstring_provider_runtime.generate_ai_docstring_with_fallback)
    assert "_apply_ai_docstring_style_contract" in source
    assert "from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_style_runtime" not in source


def test_provider_pipeline_still_applies_detailed_style_contract() -> None:
    """Owner cleanup should not change request-aware style behavior."""

    def provider(_: AIProviderRequest) -> AIProviderResult:
        return AIProviderResult(
            provider_name="fake_ai",
            success=True,
            docstring_body='"""' + _ONE_LINE + '"""',
            status="ai_draft_generated",
        )

    result = generate_ai_docstring_with_fallback(_function_request("detailed"), provider)

    assert result.success
    assert "Parameters" in result.docstring_body
    assert "Returns" in result.docstring_body
    assert "This function accepts raw and returns str." in result.docstring_body


if __name__ == "__main__":
    test_style_contract_has_single_public_owner()
    test_provider_uses_private_style_contract_alias()
    test_provider_pipeline_still_applies_detailed_style_contract()
    print("PA050D AI style contract owner cleanup tests passed.")
