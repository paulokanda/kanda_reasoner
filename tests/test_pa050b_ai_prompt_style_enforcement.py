"""Focused tests for PA050B AI prompt style enforcement."""

from __future__ import annotations

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderRequest,
    AIProviderResult,
    build_openai_compatible_messages,
    generate_ai_docstring_with_fallback,
    normalize_ai_docstring_output_for_verbosity,
)


_VERBOSE_DOCSTRING = """Reads and strips the value of an HTTP header.

The read_header_value function takes a string representing the value of an HTTP header,
trims any leading or trailing whitespace, and returns the cleaned value.

Parameters
----------
raw : str
    A string representing the value of an HTTP header.

Returns
-------
str
    The cleaned value of the HTTP header with leading and trailing whitespace removed.
"""


def test_concise_normalization_removes_explanatory_paragraph() -> None:
    """Concise mode should remove verbose free-text paragraphs."""
    body = normalize_ai_docstring_output_for_verbosity(_VERBOSE_DOCSTRING, "concise")

    assert "The read_header_value function takes" not in body
    assert body.startswith("Reads and strips the value of an HTTP header.")
    assert "Parameters" in body
    assert "Returns" in body


def test_balanced_normalization_keeps_shorter_intro_only() -> None:
    """Balanced mode should be less aggressive than concise but not long-form."""
    body = normalize_ai_docstring_output_for_verbosity(_VERBOSE_DOCSTRING, "balanced")

    assert body.startswith("Reads and strips the value of an HTTP header.")
    assert "Parameters" in body
    assert "Returns" in body


def test_prompt_modes_have_distinct_hard_contracts() -> None:
    """Prompt contracts should be visibly different for each verbosity."""
    base = dict(
        project_root=r"E:\demo_project",
        relative_file_path="app/encoding_header.py",
        symbol_kind="function",
        symbol_name="read_header_value",
        signature="read_header_value(raw: str) -> str",
        source_snippet="def read_header_value(raw: str) -> str:\n    return raw.strip()",
        heuristic_draft="Return the header value.",
    )
    concise = build_openai_compatible_messages(
        AIProviderRequest(**base, docstring_verbosity="concise")
    )
    balanced = build_openai_compatible_messages(
        AIProviderRequest(**base, docstring_verbosity="balanced")
    )
    detailed = build_openai_compatible_messages(
        AIProviderRequest(**base, docstring_verbosity="detailed")
    )

    concise_text = concise[0]["content"] + "\n" + concise[1]["content"]
    balanced_text = balanced[0]["content"] + "\n" + balanced[1]["content"]
    detailed_text = detailed[0]["content"] + "\n" + detailed[1]["content"]

    assert "VERBOSITY CONTRACT: CONCISE" in concise_text
    assert "VERBOSITY CONTRACT: BALANCED" in balanced_text
    assert "VERBOSITY CONTRACT: DETAILED" in detailed_text
    assert "Do not reuse a concise one-line answer" in detailed_text
    assert concise_text != balanced_text
    assert balanced_text != detailed_text


def test_provider_result_is_clamped_by_request_verbosity() -> None:
    """Provider output should be post-processed according to request verbosity."""
    request = AIProviderRequest(
        project_root=r"E:\demo_project",
        relative_file_path="app/encoding_header.py",
        symbol_kind="function",
        symbol_name="read_header_value",
        signature="read_header_value(raw: str) -> str",
        source_snippet="def read_header_value(raw: str) -> str:\n    return raw.strip()",
        heuristic_draft="Return the header value.",
        docstring_verbosity="concise",
    )

    def provider(_: AIProviderRequest) -> AIProviderResult:
        return AIProviderResult(
            provider_name="fake_ai",
            success=True,
            docstring_body=_VERBOSE_DOCSTRING,
            status="ai_draft_generated",
        )

    result = generate_ai_docstring_with_fallback(request, provider)

    assert result.success is True
    assert result.used_fallback is False
    assert "The read_header_value function takes" not in result.docstring_body
    assert "Parameters" in result.docstring_body


if __name__ == "__main__":
    test_concise_normalization_removes_explanatory_paragraph()
    test_balanced_normalization_keeps_shorter_intro_only()
    test_prompt_modes_have_distinct_hard_contracts()
    test_provider_result_is_clamped_by_request_verbosity()
    print("PA050B AI prompt style enforcement tests passed.")
