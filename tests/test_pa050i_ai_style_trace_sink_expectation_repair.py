#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PA050I tests for PA050G trace sink expectation repair."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PA050G_TEST = ROOT / "tests" / "test_pa050g_ai_style_trace_preview_import_repair.py"


def test_pa050g_no_longer_requires_specific_trace_sink() -> None:
    """Ensure PA050G only guards import availability and no-NameError behavior."""
    source = PA050G_TEST.read_text(encoding="utf-8")
    assert "[review-style-trace] preview_input" not in source
    assert "isinstance(preview, str)" in source
    assert "NameError" in source
    assert "append_ai_style_trace" in source
    assert "short_trace_text" in source


if __name__ == "__main__":
    test_pa050g_no_longer_requires_specific_trace_sink()
    print("PA050I AI style trace sink expectation repair tests passed.")
