"""Tests for PA044 Tab 3 local OpenAI-compatible provider."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderRequest,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_row_bridge_runtime import (
    generate_ai_review_draft_for_row,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_openai_compatible_provider_runtime import (
    build_local_openai_compatible_provider,
    local_openai_compatible_provider_from_owner,
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


class _ComboBox:
    def __init__(self, value: str = "") -> None:
        self._value = value

    def currentText(self) -> str:
        return self._value


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
        self._base_url_edit = _TextBox("http://localhost:11434/v1")
        self._model_combo = _ComboBox("qwen2.5-coder:7b")
        self._ai_enabled_checkbox = _CheckBox(checked)
        self._review_original_snippet = _TextBox()
        self._review_corrected_snippet = _TextBox()
        self._review_list = _List(_Item(row))
        self.output = []

    def _append_text(self, value: str) -> None:
        self.output.append(value)


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        del exc_type, exc, traceback

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


class _FakeOpener:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.request = None
        self.timeout = None

    def __call__(self, request, timeout: float):
        self.request = request
        self.timeout = timeout
        return _FakeResponse(self.payload)


def test_local_openai_provider_posts_chat_completion_and_normalizes_result() -> None:
    opener = _FakeOpener(
        {
            "choices": [
                {
                    "message": {
                        "content": '```python\n"""Return the AI status code."""\n```'
                    }
                }
            ]
        }
    )
    provider = build_local_openai_compatible_provider(
        base_url="http://localhost:11434/v1",
        model="qwen2.5-coder:7b",
        timeout_seconds=12,
        opener=opener,
    )
    request = AIProviderRequest(
        project_root=r"E:\project",
        relative_file_path="app/main.py",
        symbol_kind="function",
        symbol_name="main",
        signature="main() -> int",
        source_snippet="def main() -> int:\n    return 0",
        heuristic_draft="Return the integer status code.",
    )
    result = provider(request)
    assert result.success is True
    assert result.provider_name == "local_openai_compatible"
    assert result.docstring_body == "Return the AI status code."
    assert opener.timeout == 12
    assert opener.request.full_url == "http://localhost:11434/v1/chat/completions"
    raw = opener.request.data.decode("utf-8")
    payload = json.loads(raw)
    assert payload["model"] == "qwen2.5-coder:7b"
    assert payload["messages"][0]["role"] == "system"
    assert "Symbol name: main" in payload["messages"][1]["content"]


def test_local_provider_from_owner_uses_existing_local_ai_controls() -> None:
    row = {"file": "app/main.py", "target_kind": "function", "target_name": "main", "line": 1}
    owner = _Owner(Path(r"E:\project"), row)
    provider = local_openai_compatible_provider_from_owner(owner)
    assert callable(provider)


def test_row_bridge_uses_owner_local_ai_provider_when_available() -> None:
    row = {
        "file": "app/main.py",
        "target_kind": "function",
        "target_name": "main",
        "line": 1,
        "suggested_docstring": "Return the integer status code.",
    }
    owner = _Owner(Path(r"E:\project"), row)

    opener = _FakeOpener(
        {
            "choices": [
                {"message": {"content": "Return the AI generated status code."}}
            ]
        }
    )
    owner._ai_docstring_provider = build_local_openai_compatible_provider(
        base_url="http://localhost:11434/v1",
        model="qwen2.5-coder:7b",
        opener=opener,
    )
    draft = generate_ai_review_draft_for_row(
        owner,
        row,
        "def main() -> int:\n    return 0\n",
    )
    assert draft == "Return the AI generated status code."
    assert row["ai_provider"] == "local_openai_compatible"
    assert row["selected_draft_source"] == "ai"
    assert row["ai_used_fallback"] is False


def test_inline_save_uses_local_ai_provider_without_writing_source_files() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / "app.py"
        source.write_text("def main() -> int:\n    return 0\n", encoding="utf-8")
        row = {
            "file": "app.py",
            "action": "inserted",
            "target_kind": "function",
            "target_name": "main",
            "line": 1,
            "suggested_docstring": "Return the integer status code.",
        }
        owner = _Owner(root, row, checked=True)
        opener = _FakeOpener(
            {
                "choices": [
                    {"message": {"content": "Return the AI generated status code."}}
                ]
            }
        )
        owner._ai_docstring_provider = build_local_openai_compatible_provider(
            base_url="http://localhost:11434/v1",
            model="qwen2.5-coder:7b",
            opener=opener,
        )
        before = source.read_text(encoding="utf-8")
        save_current_correction(owner)
        assert "Click Generate Draft first" in "".join(owner.output)
        assert row.get("approval_state") != "review_saved"

        generate_current_draft(owner)
        save_current_correction(owner)
        after = source.read_text(encoding="utf-8")
        assert before == after
        assert row["draft_docstring"] == "Return the AI generated status code."
        assert row["ai_provider"] == "local_openai_compatible"
        assert row["approval_state"] == "review_saved"
        assert "Return the AI generated status code." in owner._review_corrected_snippet.plain_text


if __name__ == "__main__":
    test_local_openai_provider_posts_chat_completion_and_normalizes_result()
    test_local_provider_from_owner_uses_existing_local_ai_controls()
    test_row_bridge_uses_owner_local_ai_provider_when_available()
    test_inline_save_uses_local_ai_provider_without_writing_source_files()
    print("PA044 Tab 3 local OpenAI-compatible provider tests passed.")
