#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PA050G tests for AI style trace preview import repair."""

from __future__ import annotations

import tempfile
from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime import inline_preview_runtime


class Owner:
    """Minimal owner used by preview tests."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = str(project_root)
        self.messages: list[str] = []
        self._ai_style_trace_enabled = True

    def _append_text(self, text: str) -> None:
        self.messages.append(text)


def test_preview_trace_imports_are_defined() -> None:
    """Ensure trace helpers used by preview runtime are available."""
    assert callable(inline_preview_runtime.append_ai_style_trace)
    assert callable(inline_preview_runtime.short_trace_text)


def test_preview_trace_records_without_name_error() -> None:
    """Build a corrected preview and ensure trace logging does not crash."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source_dir = root / "app"
        source_dir.mkdir()
        source_path = source_dir / "sample.py"
        source_path.write_text(
            "#!/usr/bin/env python3\n"
            "# -*- coding: utf-8 -*-\n"
            "\n"
            "from __future__ import annotations\n"
            "\n"
            "\n"
            "def read_header_value(raw: str) -> str:\n"
            "    return raw.strip()\n",
            encoding="utf-8",
        )
        owner = Owner(root)
        row = {
            "action": "inserted",
            "target_kind": "module",
            "file": "app/sample.py",
            "line": 1,
            "draft_docstring": "Reads and strips the value of an HTTP header.",
            "ai_draft_docstring": "Reads and strips the value of an HTTP header.",
            "ai_docstring_verbosity": "detailed",
        }

        preview = inline_preview_runtime.build_corrected_snippet_text(owner, row, "ai")

        assert isinstance(preview, str)
        assert preview.strip()
        assert not any("NameError" in item for item in owner.messages)


if __name__ == "__main__":
    test_preview_trace_imports_are_defined()
    test_preview_trace_records_without_name_error()
    print("PA050G AI style trace preview import repair tests passed.")
