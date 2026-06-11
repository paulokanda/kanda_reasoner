"""Public contract tests for Insert Missing Docstring help runtime."""

from __future__ import annotations

import kanda_reasoner_app.tab3_manual_review_runtime.insert_missing_docstring_help_runtime as help_runtime


EXPECTED_PUBLIC_EXPORTS = {
    "FALLBACK_HELP_TEXT",
    "HELP_FILE_NAME",
    "get_insert_missing_docstring_help_text",
    "open_insert_missing_docstring_help",
}


def test_help_runtime_exports_public_contract() -> None:
    """Verify the help runtime exposes the expected public API."""
    exported = set(getattr(help_runtime, "__all__", ()))

    missing = EXPECTED_PUBLIC_EXPORTS.difference(exported)
    assert not missing, f"Missing public exports: {sorted(missing)}"

    for name in EXPECTED_PUBLIC_EXPORTS:
        assert hasattr(help_runtime, name), name


def test_help_runtime_text_is_available() -> None:
    """Verify help text can be loaded through the public function."""
    text = help_runtime.get_insert_missing_docstring_help_text()

    assert isinstance(text, str)
    assert text.strip()
    assert "Insert Missing Docstring" in text
    assert "Generate Draft" in text
    assert "Scan Files for Missing Docstrings" in text


def test_help_runtime_constants_are_valid() -> None:
    """Verify help runtime constants have useful values."""
    assert isinstance(help_runtime.HELP_FILE_NAME, str)
    assert help_runtime.HELP_FILE_NAME.endswith(".md")
    assert isinstance(help_runtime.FALLBACK_HELP_TEXT, str)
    assert "Insert Missing Docstring" in help_runtime.FALLBACK_HELP_TEXT


if __name__ == "__main__":
    test_help_runtime_exports_public_contract()
    test_help_runtime_text_is_available()
    test_help_runtime_constants_are_valid()
    print("insert_missing_docstring_help_runtime public contract tests passed.")
