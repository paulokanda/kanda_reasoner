"""Focused tests for PA050E AI style selection bridge and preview refresh."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime import inline_corrector_runtime
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderRequest,
    AIProviderResult,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_row_bridge_runtime import (
    build_review_row_ai_request,
    generate_ai_review_draft_for_row,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_style_runtime import (
    selected_ai_docstring_verbosity_from_owner,
)

_ONE_LINE = "Reads and strips the value of an HTTP header."
_SOURCE = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations


def read_header_value(raw: str) -> str:
    return raw.strip()
"""


class _Combo:
    """Small currentText-compatible test double."""

    def __init__(self, value: str) -> None:
        self.value = value

    def currentText(self) -> str:
        """Return the configured combo value."""
        return self.value

    def setCurrentText(self, value: str) -> None:
        """Set the configured combo value."""
        self.value = value


class _CheckBox:
    """Small isChecked-compatible test double."""

    def __init__(self, checked: bool) -> None:
        self.checked = checked

    def isChecked(self) -> bool:
        """Return whether the box is checked."""
        return self.checked


class _LineEdit:
    """Small text-compatible test double."""

    def __init__(self, value: str) -> None:
        self.value = value

    def text(self) -> str:
        """Return the configured text."""
        return self.value


class _PlainText:
    """Small setPlainText-compatible test double."""

    def __init__(self) -> None:
        self.text = ""

    def setPlainText(self, value: str) -> None:
        """Store the displayed text."""
        self.text = value

    def toPlainText(self) -> str:
        """Return the displayed text."""
        return self.text


class _Item:
    """Small review-list item test double."""

    def __init__(self, row: dict) -> None:
        self.row_data = row
        self.text = ""

    def setText(self, value: str) -> None:
        """Store item text updates."""
        self.text = value


class _ReviewList:
    """Small currentItem-compatible review list."""

    def __init__(self, row: dict) -> None:
        self.item = _Item(row)

    def currentItem(self) -> _Item:
        """Return the current item."""
        return self.item


class _Owner:
    """Small Tab 3 owner test double."""

    def __init__(self, root: Path, row: dict) -> None:
        self._root_path_edit = _LineEdit(str(root))
        self._ai_enabled_checkbox = _CheckBox(True)
        self._ai_docstring_verbosity_combo = _Combo("Concise")
        self._review_list = _ReviewList(row)
        self._review_original_snippet = _PlainText()
        self._review_corrected_snippet = _PlainText()
        self._review_draft_status_label = _PlainText()
        self._review_engine_status_label = _PlainText()
        self.outputs: list[str] = []
        self.requests: list[AIProviderRequest] = []
        self._report_rows = [row]

    def _append_text(self, text: str) -> None:
        """Capture output panel text."""
        self.outputs.append(text)

    def _refresh_review_summary(self) -> None:
        """Compatibility hook used by inline refresh."""
        return None


def _row() -> dict:
    """Return one module review row for style bridge tests."""
    return {
        "action": "inserted",
        "target_kind": "module",
        "target_name": "encoding_header",
        "file": "app/encoding_header.py",
        "line": 1,
    }


def _provider(owner: _Owner):
    """Return a provider that always returns the same one-line text."""

    def provider(request: AIProviderRequest) -> AIProviderResult:
        owner.requests.append(request)
        return AIProviderResult(
            provider_name="fake_ai",
            success=True,
            docstring_body=_ONE_LINE,
            status="ai_draft_generated",
        )

    return provider


def test_owner_style_selection_helper_reads_real_combo_name() -> None:
    """The canonical helper should read the widget created by layout_runtime."""
    owner = type("Owner", (), {})()
    owner._ai_docstring_verbosity_combo = _Combo("Detailed")
    assert selected_ai_docstring_verbosity_from_owner(owner) == "detailed"
    owner._ai_docstring_verbosity_combo.setCurrentText("Balanced")
    assert selected_ai_docstring_verbosity_from_owner(owner) == "balanced"


def test_request_receives_owner_style_selection(tmp_path: Path) -> None:
    """Row bridge requests should carry the selected GUI style."""
    row = _row()
    owner = _Owner(tmp_path, row)
    owner._ai_docstring_verbosity_combo.setCurrentText("Detailed")
    request = build_review_row_ai_request(owner, row, _SOURCE)
    assert request.docstring_verbosity == "detailed"


def test_explicit_generate_draft_refreshes_style_preview_and_not_cached(tmp_path: Path) -> None:
    """Generate Draft should regenerate and display the newly selected style."""
    source_path = tmp_path / "app" / "encoding_header.py"
    source_path.parent.mkdir(parents=True)
    source_path.write_text(_SOURCE, encoding="utf-8")

    row = _row()
    owner = _Owner(tmp_path, row)
    owner._ai_docstring_provider = _provider(owner)

    owner._ai_docstring_verbosity_combo.setCurrentText("Concise")
    inline_corrector_runtime.generate_current_draft(owner)
    concise = str(row.get("draft_docstring") or "")
    concise_preview = owner._review_corrected_snippet.toPlainText()

    owner._ai_docstring_verbosity_combo.setCurrentText("Balanced")
    inline_corrector_runtime.generate_current_draft(owner)
    balanced = str(row.get("draft_docstring") or "")
    balanced_preview = owner._review_corrected_snippet.toPlainText()

    owner._ai_docstring_verbosity_combo.setCurrentText("Detailed")
    inline_corrector_runtime.generate_current_draft(owner)
    detailed = str(row.get("draft_docstring") or "")
    detailed_preview = owner._review_corrected_snippet.toPlainText()

    assert [request.docstring_verbosity for request in owner.requests] == [
        "concise",
        "balanced",
        "detailed",
    ]
    assert row["ai_docstring_verbosity"] == "detailed"
    assert concise == _ONE_LINE
    assert balanced != concise
    assert detailed != balanced
    assert "Includes read_header_value." in balanced
    assert "This module includes read_header_value" in detailed
    assert "Reads and strips the value of an HTTP header." in concise_preview
    assert "Includes read_header_value." in balanced_preview
    assert "This module includes read_header_value" in detailed_preview
    assert any("AI draft style: concise" in item for item in owner.outputs)
    assert any("AI draft style: balanced" in item for item in owner.outputs)
    assert any("AI draft style: detailed" in item for item in owner.outputs)


def test_direct_row_bridge_does_not_reuse_cached_draft(tmp_path: Path) -> None:
    """A new style selection should replace an existing cached AI draft."""
    row = _row()
    row["draft_docstring"] = "Old cached draft."
    row["ai_draft_docstring"] = "Old cached draft."
    owner = _Owner(tmp_path, row)
    owner._ai_docstring_provider = _provider(owner)

    owner._ai_docstring_verbosity_combo.setCurrentText("Detailed")
    draft = generate_ai_review_draft_for_row(owner, row, _SOURCE)

    assert draft != "Old cached draft."
    assert row["draft_docstring"] != "Old cached draft."
    assert row["ai_docstring_verbosity"] == "detailed"
    assert "This module includes read_header_value" in row["draft_docstring"]


if __name__ == "__main__":
    test_owner_style_selection_helper_reads_real_combo_name()
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as temp_dir:
        test_request_receives_owner_style_selection(Path(temp_dir))
    with TemporaryDirectory() as temp_dir:
        test_explicit_generate_draft_refreshes_style_preview_and_not_cached(Path(temp_dir))
    with TemporaryDirectory() as temp_dir:
        test_direct_row_bridge_does_not_reuse_cached_draft(Path(temp_dir))
    print("PA050E AI style selection bridge and preview refresh tests passed.")
