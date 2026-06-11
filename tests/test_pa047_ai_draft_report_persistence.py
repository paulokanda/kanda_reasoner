"""Focused tests for PA047 AI draft report persistence."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderResult,
)
from kanda_reasoner_app.tab3_manual_review_runtime.inline_corrector_runtime import (
    generate_current_draft,
    undo_current_correction,
)
from kanda_reasoner_app.tab3_manual_review_runtime.report_io_runtime import (
    report_text_for_export,
)
from kanda_reasoner_app.tab3_manual_review_runtime.review_persistence_fields import (
    apply_persisted_review_state,
    build_persisted_review_state,
    clear_persisted_draft_fields,
    review_rows_jsonl,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.manual_docstring_review_support import (
    apply_saved_manual_review_state,
)


class _TextBox:
    def __init__(self, value: str = "") -> None:
        self._value = value
        self.plain_text = ""

    def text(self) -> str:
        return self._value

    def setPlainText(self, value: str) -> None:
        self.plain_text = value


class _CheckBox:
    def __init__(self, checked: bool) -> None:
        self._checked = checked

    def isEnabled(self) -> bool:
        return True

    def isChecked(self) -> bool:
        return self._checked


class _Item:
    def __init__(self, row: dict) -> None:
        self.row_data = row
        self.text = ""

    def setText(self, value: str) -> None:
        self.text = value


class _List:
    def __init__(self, item: _Item) -> None:
        self._item = item

    def currentItem(self) -> _Item:
        return self._item


class _Owner:
    def __init__(self, root: Path, row: dict | None, checked: bool = True) -> None:
        self._root_path_edit = _TextBox(str(root))
        self._ai_enabled_checkbox = _CheckBox(checked)
        self._review_original_snippet = _TextBox()
        self._review_corrected_snippet = _TextBox()
        self._review_draft_status_label = _TextBox()
        self._review_engine_status_label = _TextBox()
        self._review_list = _List(_Item(row or {}))
        self._report_rows = [row] if row is not None else []
        self.output = []

    def _append_text(self, value: str) -> None:
        self.output.append(value)


def _row() -> dict:
    return {
        "file": "app.py",
        "action": "inserted",
        "target_kind": "function",
        "target_name": "main",
        "line": 1,
        "suggested_docstring": "Return the integer status code.",
    }


def test_generate_ai_draft_is_persisted_in_manual_review_state() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "app.py").write_text("def main() -> int:\n    return 0\n", encoding="utf-8")
        row = _row()
        owner = _Owner(root, row, checked=True)

        def provider(request):
            del request
            return AIProviderResult(
                provider_name="fake_ai",
                success=True,
                docstring_body="Return the AI generated status code.",
                status="ai_draft_generated",
            )

        owner._ai_docstring_provider = provider
        generate_current_draft(owner)

        state_path = root / "_project_reference" / "manual_docstring_review_state.json"
        data = json.loads(state_path.read_text(encoding="utf-8"))
        saved = next(iter(data.values()))
        assert saved["ai_draft_docstring"] == "Return the AI generated status code."
        assert saved["ai_provider"] == "fake_ai"
        assert saved["ai_status"] == "ai_draft_generated"
        assert saved["selected_draft_source"] == "ai"
        assert saved["ai_used_fallback"] is False

        reloaded = _row()
        apply_saved_manual_review_state(owner, [reloaded])
        assert reloaded["ai_draft_docstring"] == "Return the AI generated status code."
        assert reloaded["selected_draft_source"] == "ai"
        assert reloaded["manual_review_state"]["ai_provider"] == "fake_ai"


def test_report_export_prefers_updated_rows_over_original_file() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        report_path = root / "report.jsonl"
        original = _row()
        report_path.write_text(json.dumps(original) + "\n", encoding="utf-8")
        updated = _row()
        updated["ai_draft_docstring"] = "Return the AI value."
        updated["ai_provider"] = "fake_ai"
        updated["ai_status"] = "ai_draft_generated"
        updated["selected_draft_source"] = "ai"
        updated["draft_docstring"] = "Return the AI value."
        owner = _Owner(root, None, checked=True)
        owner._report_path_edit = _TextBox(str(report_path))
        owner._report_rows = [updated]

        exported = report_text_for_export(owner)
        assert "Return the AI value." in exported
        assert "fake_ai" in exported
        assert "ai_draft_generated" in exported


def test_review_persistence_fields_public_contract() -> None:
    row = _row()
    row["ai_draft_docstring"] = "Return the AI value."
    row["ai_provider"] = "fake_ai"
    row["ai_status"] = "ok"
    row["ai_used_fallback"] = False
    row["selected_draft_source"] = "ai"
    payload = build_persisted_review_state(row, "Return the AI value.")
    restored = _row()
    apply_persisted_review_state(restored, payload)
    assert restored["ai_draft_docstring"] == "Return the AI value."
    assert restored["ai_provider"] == "fake_ai"
    assert restored["ai_used_fallback"] is False
    text = review_rows_jsonl([restored])
    assert "Return the AI value." in text
    clear_persisted_draft_fields(restored)
    assert restored["ai_draft_docstring"] == ""
    assert restored["selected_draft_source"] == ""
    assert restored["ai_used_fallback"] is False


def test_undo_clears_persisted_ai_draft_fields() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "app.py").write_text("def main() -> int:\n    return 0\n", encoding="utf-8")
        row = _row()
        row["draft_docstring"] = "Return the AI value."
        row["ai_draft_docstring"] = "Return the AI value."
        row["ai_provider"] = "fake_ai"
        row["ai_status"] = "ok"
        row["selected_draft_source"] = "ai"
        row["ai_used_fallback"] = False
        owner = _Owner(root, row, checked=True)
        undo_current_correction(owner)

        assert row["draft_docstring"] == ""
        assert row["ai_draft_docstring"] == ""
        assert row["selected_draft_source"] == ""
        state_path = root / "_project_reference" / "manual_docstring_review_state.json"
        saved = next(iter(json.loads(state_path.read_text(encoding="utf-8")).values()))
        assert saved.get("ai_draft_docstring", "") == ""
        assert saved.get("selected_draft_source", "") == ""


if __name__ == "__main__":
    test_generate_ai_draft_is_persisted_in_manual_review_state()
    test_report_export_prefers_updated_rows_over_original_file()
    test_review_persistence_fields_public_contract()
    test_undo_clears_persisted_ai_draft_fields()
    print("PA047 AI draft report persistence tests passed.")
