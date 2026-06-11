"""PA050F tests for AI style diagnostic trace flow."""

from __future__ import annotations

import tempfile
from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime import ai_docstring_row_bridge_runtime
from kanda_reasoner_app.tab3_manual_review_runtime import inline_preview_runtime
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderResult,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_style_diagnostics_runtime import (
    append_ai_style_trace,
    source_names_from_snippet,
)


class _Combo:
    def __init__(self, text: str) -> None:
        self._text = text

    def currentText(self) -> str:
        return self._text


class _LineEdit:
    def __init__(self, text: str) -> None:
        self._text = text

    def text(self) -> str:
        return self._text


class _Owner:
    def __init__(self, root: str = "") -> None:
        self._ai_docstring_verbosity_combo = _Combo("Detailed")
        self._root_path_edit = _LineEdit(root)
        self.output: list[str] = []

    def _append_text(self, text: str) -> None:
        self.output.append(text)


def _provider(request):
    assert request.docstring_verbosity == "detailed"
    return AIProviderResult(
        provider_name="test_provider",
        success=True,
        docstring_body="Reads and strips the value of an HTTP header.",
        status="ai_draft_generated",
    )


def test_ai_style_diagnostic_trace_records_request_result_and_row_store() -> None:
    owner = _Owner()
    row = {
        "action": "inserted",
        "target_kind": "module",
        "target_name": "module",
        "file": "app/main.py",
        "line": 1,
    }
    module_text = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations


def read_header_value(raw: str) -> str:
    return raw.strip()
"""

    draft = ai_docstring_row_bridge_runtime.generate_ai_review_draft_for_row(
        owner,
        row,
        module_text,
        provider=_provider,
    )

    output = "".join(owner.output)
    assert "[review-style-trace] request" in output
    assert 'style="detailed"' in output
    assert "source_len=" in output
    assert "read_header_value" in output
    assert "[review-style-trace] provider_result" in output
    assert "[review-style-trace] row_store" in output
    assert "changed=" in output
    assert row["ai_docstring_verbosity"] == "detailed"
    assert row["draft_docstring"] == draft
    assert "selected source snippet" in draft


def test_preview_trace_records_final_preview_input() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / "app" / "main.py"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            "#!/usr/bin/env python3\n"
            "# -*- coding: utf-8 -*-\n\n"
            "from __future__ import annotations\n\n"
            "\ndef read_header_value(raw: str) -> str:\n"
            "    return raw.strip()\n",
            encoding="utf-8",
        )
        owner = _Owner(str(root))
        row = {
            "action": "inserted",
            "target_kind": "module",
            "target_name": "module",
            "file": "app/main.py",
            "line": 1,
            "draft_docstring": "Reads and strips the value of an HTTP header.\n\n"
            "This module includes read_header_value based on the selected source snippet.",
            "ai_draft_docstring": "Reads and strips the value of an HTTP header.\n\n"
            "This module includes read_header_value based on the selected source snippet.",
            "ai_docstring_verbosity": "detailed",
        }

        preview = inline_preview_runtime.build_corrected_snippet_text(owner, row, "ai")
        output = "".join(owner.output)

    assert "[review-style-trace] preview_input" in output
    assert 'style="detailed"' in output
    assert "selected source snippet" in output
    assert "selected source snippet" in preview


def test_source_name_diagnostic_parser() -> None:
    names = source_names_from_snippet(
        "class Runner:\n"
        "    pass\n\n"
        "def build_runner(name: str):\n"
        "    return Runner()\n"
    )
    assert names == ["build_runner", "Runner"]


def test_append_ai_style_trace_is_optional() -> None:
    owner = _Owner()
    owner._ai_style_trace_enabled = False
    append_ai_style_trace(owner, "hidden", style="concise")
    assert owner.output == []


if __name__ == "__main__":
    test_ai_style_diagnostic_trace_records_request_result_and_row_store()
    test_preview_trace_records_final_preview_input()
    test_source_name_diagnostic_parser()
    test_append_ai_style_trace_is_optional()
    print("PA050F AI style diagnostic trace tests passed.")
