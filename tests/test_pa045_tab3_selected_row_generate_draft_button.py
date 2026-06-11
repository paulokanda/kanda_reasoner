"""Focused tests for PA045 selected-row Generate Draft behavior."""

from __future__ import annotations

from pathlib import Path
import tempfile

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderResult,
)
from kanda_reasoner_app.tab3_manual_review_runtime.inline_corrector_runtime import (
    generate_current_draft,
    save_current_correction,
    wire_inline_corrector_events,
)


class _Signal:
    def __init__(self) -> None:
        self.slots = []

    def connect(self, slot):
        self.slots.append(slot)

    def emit(self, *args) -> None:
        for slot in list(self.slots):
            slot(*args)


class _Button:
    def __init__(self) -> None:
        self.clicked = _Signal()


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
        self.toggled = _Signal()

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
    def __init__(self, root: Path, row: dict, checked: bool) -> None:
        self._root_path_edit = _TextBox(str(root))
        self._ai_enabled_checkbox = _CheckBox(checked)
        self._review_original_snippet = _TextBox()
        self._review_corrected_snippet = _TextBox()
        self._review_list = _List(_Item(row))
        self._review_generate_draft_button = _Button()
        self._review_save_change_button = _Button()
        self._review_previous_button = None
        self._review_next_button = None
        self._review_reset_button = None
        self._review_approve_row_button = None
        self._review_reject_row_button = None
        self._review_undo_button = None
        self._review_save_all_button = None
        self._review_engine_status_label = None
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


def test_save_review_decision_does_not_generate_hidden_ai_draft() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / "app.py"
        source.write_text("def main() -> int:\n    return 0\n", encoding="utf-8")
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
        save_current_correction(owner)

        assert row.get("ai_draft_docstring") in (None, "")
        assert row.get("approval_state") != "review_saved"
        assert "Click Generate Draft first" in "".join(owner.output)
        assert source.read_text(encoding="utf-8") == "def main() -> int:\n    return 0\n"


def test_generate_draft_then_save_review_decision_uses_ai_without_source_write() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / "app.py"
        source.write_text("def main() -> int:\n    return 0\n", encoding="utf-8")
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
        before = source.read_text(encoding="utf-8")
        generate_current_draft(owner)
        save_current_correction(owner)
        after = source.read_text(encoding="utf-8")

        assert before == after
        assert row["ai_draft_docstring"] == "Return the AI generated status code."
        assert row["draft_docstring"] == "Return the AI generated status code."
        assert row["approval_state"] == "review_saved"
        assert "Return the AI generated status code." in owner._review_corrected_snippet.plain_text


def test_generate_draft_button_is_wired_to_selected_row_generation() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / "app.py"
        source.write_text("def main() -> int:\n    return 0\n", encoding="utf-8")
        row = _row()
        owner = _Owner(root, row, checked=True)

        def provider(request):
            del request
            return AIProviderResult(
                provider_name="fake_ai",
                success=True,
                docstring_body="Return the generated value.",
                status="ai_draft_generated",
            )

        owner._ai_docstring_provider = provider
        wire_inline_corrector_events(owner)
        assert owner._review_generate_draft_button.clicked.slots
        owner._review_generate_draft_button.clicked.emit(False)

        assert row["draft_docstring"] == "Return the generated value."
        assert row["selected_draft_source"] == "ai"


def test_layout_declares_generate_draft_button() -> None:
    text = Path(
        'ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime/layout_runtime.py'
    ).read_text(encoding="utf-8")
    assert "Generate Draft" in text
    assert "_review_generate_draft_button" in text


if __name__ == "__main__":
    test_save_review_decision_does_not_generate_hidden_ai_draft()
    test_generate_draft_then_save_review_decision_uses_ai_without_source_write()
    test_generate_draft_button_is_wired_to_selected_row_generation()
    test_layout_declares_generate_draft_button()
    print("PA045 Tab 3 selected-row Generate Draft button tests passed.")
