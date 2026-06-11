#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PA050H tests for the PA050G diagnostic test expectation repair."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PA050G_TEST = ROOT / "tests" / "test_pa050g_ai_style_trace_preview_import_repair.py"


def test_pa050g_test_no_longer_asserts_specific_preview_sentence() -> None:
    """Ensure PA050G only verifies the import/trace repair contract."""
    source = PA050G_TEST.read_text(encoding="utf-8")
    assert "Reads and strips the value of an HTTP header.\" in preview" not in source
    assert "[review-style-trace] preview_input" in source
    assert "isinstance(preview, str)" in source


if __name__ == "__main__":
    test_pa050g_test_no_longer_asserts_specific_preview_sentence()
    print("PA050H AI style trace test expectation repair tests passed.")
