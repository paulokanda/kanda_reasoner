"""Tests for PA035B inline preview public symbol ownership."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.tab3_manual_review_runtime import inline_corrector_runtime
from kanda_reasoner_app.tab3_manual_review_runtime.inline_preview_runtime import (
    build_corrected_snippet_text,
    build_original_snippet_text,
)


def test_preview_builders_are_owned_by_preview_runtime_only() -> None:
    """Verify preview builders are not public symbols in the corrector runtime."""
    public_names = set(getattr(inline_corrector_runtime, "__all__", ()))

    assert "build_corrected_snippet_text" not in public_names
    assert "build_original_snippet_text" not in public_names
    assert callable(build_corrected_snippet_text)
    assert callable(build_original_snippet_text)


if __name__ == "__main__":
    test_preview_builders_are_owned_by_preview_runtime_only()
    print("PA035B inline preview public owner tests passed.")
