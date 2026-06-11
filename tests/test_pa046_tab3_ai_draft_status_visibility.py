"""Focused tests for PA046 selected-row draft status visibility."""

from __future__ import annotations

from pathlib import Path
import tempfile

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderResult,
)
from kanda_reasoner_app.tab3_manual_review_runtime.inline_corrector_runtime import (
    generate_current_draft,
    refresh_inline_corrector_for_selection,
    refresh_review_draft_status,
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


class _Label:
    def __init__(self) -> None:
        self.text_value = ""

    def setText(self, value: str) -> None:
        self.text_value = value


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
        self._review_draft_status_label = _Label()
        self._review_engine_status_label = _Label()
        self._review_list = _List(_Item(row))
        self._review_generate_draft_button = _Button()
        self._review_save_change_button = None
        self._review_previous_button = None
        self._review_next_button = None
        self._review_reset_button = None
        self._review_approve_row_button = None
        self._review_reject_row_button = None
        self._review_undo_button = None
        self._review_save_all_button = None
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


def test_heuristic_generate_draft_updates_visible_status() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "app.py").write_text("def main() -> int:\n    return 0\n", encoding="utf-8")
        row = _row()
        owner = _Owner(root, row, checked=False)

        generate_current_draft(owner)

        assert owner._review_draft_status_label.text_value == "HEURISTIC DRAFT GENERATED"
        assert "HEURISTIC DRAFT GENERATED" in "".join(owner.output)
        assert row["selected_draft_source"] == "heuristic"


def test_ai_generate_draft_updates_visible_status_and_provider_log() -> None:
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
                docstring_body="Return the AI status code.",
                status="ai_draft_generated",
            )

        owner._ai_docstring_provider = provider
        generate_current_draft(owner)

        assert owner._review_draft_status_label.text_value == "AI DRAFT GENERATED"
        output = "".join(owner.output)
        assert "AI DRAFT GENERATED" in output
        assert "AI provider: fake_ai" in output
        assert row["selected_draft_source"] == "ai"


def test_ai_fallback_updates_visible_status_and_error_log() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "app.py").write_text("def main() -> int:\n    return 0\n", encoding="utf-8")
        row = _row()
        owner = _Owner(root, row, checked=True)

        def provider(request):
            del request
            return AIProviderResult(
                provider_name="fake_ai",
                success=False,
                docstring_body="",
                status="failed",
                error_message="server unavailable",
            )

        owner._ai_docstring_provider = provider
        generate_current_draft(owner)

        assert owner._review_draft_status_label.text_value == "AI UNAVAILABLE - HEURISTIC FALLBACK"
        output = "".join(owner.output)
        assert "AI UNAVAILABLE - HEURISTIC FALLBACK" in output
        assert "AI error: server unavailable" in output
        assert row["selected_draft_source"] == "heuristic_fallback"


def test_row_refresh_recomputes_existing_draft_status() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "app.py").write_text("def main() -> int:\n    return 0\n", encoding="utf-8")
        row = _row()
        row["draft_docstring"] = "Return the value."
        row["selected_draft_source"] = "heuristic"
        owner = _Owner(root, row, checked=False)

        refresh_inline_corrector_for_selection(owner, row)
        assert owner._review_draft_status_label.text_value == "HEURISTIC DRAFT GENERATED"

        row["selected_draft_source"] = "ai"
        row["ai_draft_docstring"] = "Return the AI value."
        refresh_review_draft_status(owner, row)
        assert owner._review_draft_status_label.text_value == "AI DRAFT GENERATED"


def test_layout_declares_draft_status_label() -> None:
    text = Path(
        'ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime/layout_runtime.py'
    ).read_text(encoding="utf-8")
    assert "_review_draft_status_label" in text
    assert "NO DRAFT GENERATED" in text


if __name__ == "__main__":
    test_heuristic_generate_draft_updates_visible_status()
    test_ai_generate_draft_updates_visible_status_and_provider_log()
    test_ai_fallback_updates_visible_status_and_error_log()
    test_row_refresh_recomputes_existing_draft_status()
    test_layout_declares_draft_status_label()
    print("PA046 Tab 3 AI draft status visibility tests passed.")
