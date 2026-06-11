"""Tests for PA043 Tab 3 AI row bridge."""

from __future__ import annotations

from pathlib import Path
import tempfile

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderResult,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_row_bridge_runtime import (
    apply_ai_result_to_review_row,
    build_review_row_ai_request,
    generate_ai_review_draft_for_row,
)
from kanda_reasoner_app.tab3_manual_review_runtime.inline_corrector_runtime import (
    generate_current_draft,
    save_current_correction,
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
    def __init__(self, root: Path, row: dict, checked: bool = True) -> None:
        self._root_path_edit = _TextBox(str(root))
        self._ai_enabled_checkbox = _CheckBox(checked)
        self._review_original_snippet = _TextBox()
        self._review_corrected_snippet = _TextBox()
        self._review_list = _List(_Item(row))
        self.output = []

    def _append_text(self, value: str) -> None:
        self.output.append(value)


def test_build_review_row_ai_request_uses_row_and_project_root() -> None:
    row = {
        "file": r"E:\project\app\main.py",
        "target_kind": "function",
        "target_name": "build_runner",
        "signature": "build_runner(name: str)",
        "line": 3,
        "suggested_docstring": "Build a runner.",
    }
    owner = _Owner(Path(r"E:\project"), row)
    request = build_review_row_ai_request(
        owner,
        row,
        "def build_runner(name: str):\n    return name\n",
    )
    assert request.relative_file_path == "app/main.py"
    assert request.symbol_kind == "function"
    assert request.symbol_name == "build_runner"
    assert request.heuristic_draft == "Build a runner."
    assert "def build_runner" in request.source_snippet


def test_generate_ai_review_draft_stores_normalized_provider_result() -> None:
    row = {
        "file": "app/main.py",
        "target_kind": "function",
        "target_name": "build_runner",
        "line": 1,
        "suggested_docstring": "Build a runner.",
    }
    owner = _Owner(Path(r"E:\project"), row)

    def provider(request):
        assert request.heuristic_draft == "Build a runner."
        return AIProviderResult(
            provider_name="fake_ai",
            success=True,
            docstring_body='```python\n"""Build an improved runner."""\n```',
            status="ai_draft_generated",
        )

    draft = generate_ai_review_draft_for_row(
        owner,
        row,
        "def build_runner(name: str):\n    return name\n",
        provider=provider,
    )
    assert draft == "Build an improved runner."
    assert row["draft_docstring"] == "Build an improved runner."
    assert row["ai_draft_docstring"] == "Build an improved runner."
    assert row["ai_provider"] == "fake_ai"
    assert row["ai_status"] == "ai_draft_generated"
    assert row["selected_draft_source"] == "ai"
    assert row["ai_used_fallback"] is False


def test_generate_ai_review_draft_falls_back_to_frozen_heuristic_when_provider_fails() -> None:
    row = {
        "file": "app/main.py",
        "target_kind": "function",
        "target_name": "read_value",
        "line": 1,
        "suggested_docstring": "Return the value.",
    }
    owner = _Owner(Path(r"E:\project"), row)

    def provider(request):
        del request
        raise RuntimeError("offline")

    draft = generate_ai_review_draft_for_row(
        owner,
        row,
        "def read_value():\n    return 1\n",
        provider=provider,
    )
    assert draft == "Return the value."
    assert row["draft_docstring"] == "Return the value."
    assert row["ai_used_fallback"] is True
    assert row["selected_draft_source"] == "heuristic_fallback"
    assert "HEURISTIC FALLBACK" in row["ai_status"]


def test_apply_ai_result_to_review_row_does_not_write_source_files() -> None:
    row = {}
    result = AIProviderResult(
        provider_name="fake_ai",
        success=True,
        docstring_body="Return clean text.",
        status="ok",
    )
    apply_ai_result_to_review_row(row, result)
    assert row["draft_docstring"] == "Return clean text."
    assert "file" not in row


def test_inline_save_uses_ai_bridge_attached_provider_without_source_write() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / "app.py"
        source.write_text("def build_runner(name: str):\n    return name\n", encoding="utf-8")
        row = {
            "file": "app.py",
            "action": "inserted",
            "target_kind": "function",
            "target_name": "build_runner",
            "line": 1,
            "suggested_docstring": "Build a runner.",
        }
        owner = _Owner(root, row, checked=True)

        def provider(request):
            del request
            return AIProviderResult(
                provider_name="fake_ai",
                success=True,
                docstring_body="Build an AI runner.",
                status="ai_draft_generated",
            )

        owner._ai_docstring_provider = provider
        before = source.read_text(encoding="utf-8")
        save_current_correction(owner)
        assert "Click Generate Draft first" in "".join(owner.output)
        assert row.get("approval_state") != "review_saved"

        generate_current_draft(owner)
        save_current_correction(owner)
        after = source.read_text(encoding="utf-8")
        assert before == after
        assert row["draft_docstring"] == "Build an AI runner."
        assert row["ai_provider"] == "fake_ai"
        assert row["approval_state"] == "review_saved"
        assert "Build an AI runner." in owner._review_corrected_snippet.plain_text


if __name__ == "__main__":
    test_build_review_row_ai_request_uses_row_and_project_root()
    test_generate_ai_review_draft_stores_normalized_provider_result()
    test_generate_ai_review_draft_falls_back_to_frozen_heuristic_when_provider_fails()
    test_apply_ai_result_to_review_row_does_not_write_source_files()
    test_inline_save_uses_ai_bridge_attached_provider_without_source_write()
    print("PA043 Tab 3 AI row bridge tests passed.")
