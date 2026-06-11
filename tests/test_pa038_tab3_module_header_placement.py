"""Focused tests for PA038 module docstring preview placement."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime.inline_preview_runtime import (
    build_corrected_snippet_text,
)


class _TextEdit:
    """Minimal text edit fake."""

    def __init__(self, value: str) -> None:
        self._value = value

    def text(self) -> str:
        """Return the stored text value."""
        return self._value


class _Owner:
    """Minimal owner fake for preview helpers."""

    def __init__(self, project_root: Path) -> None:
        self._root_path_edit = _TextEdit(str(project_root))


def _snippet_payload_lines(snippet: str) -> list[str]:
    """Return the code payload from a numbered snippet."""
    payload: list[str] = []
    for line in snippet.splitlines():
        if " | " in line:
            payload.append(line.split(" | ", 1)[1])
    return payload


def test_module_docstring_stays_after_shebang_and_encoding() -> None:
    """Module docstrings should not push encoding cookies below line two."""
    root = Path("tests") / "_tmp_pa038" / "encoding_case"
    root.mkdir(parents=True, exist_ok=True)
    source = root / "module_with_encoding.py"
    source.write_text(
        "#!/usr/bin/env python3\n"
        "# -*- coding: utf-8 -*-\n"
        "\n"
        "from __future__ import annotations\n"
        "\n"
        "VALUE = 1\n",
        encoding="utf-8",
    )
    row = {
        "action": "inserted",
        "target_kind": "module",
        "file": str(source.resolve()),
        "line": 1,
        "suggested_docstring": "Utilities for encoded module.",
    }

    snippet = build_corrected_snippet_text(_Owner(root), row)
    payload = _snippet_payload_lines(snippet)

    assert payload[0] == "#!/usr/bin/env python3"
    assert payload[1] == "# -*- coding: utf-8 -*-"
    assert payload[2] == '"""Utilities for encoded module."""'
    assert "from __future__ import annotations" in payload[4]


def test_module_docstring_stays_before_future_imports() -> None:
    """Future imports should remain before normal imports but after docstring."""
    root = Path("tests") / "_tmp_pa038" / "future_case"
    root.mkdir(parents=True, exist_ok=True)
    source = root / "module_with_future.py"
    source.write_text(
        "# Project path: app/module_with_future.py\n"
        "\n"
        "from __future__ import annotations\n"
        "\n"
        "import os\n"
        "\n"
        "VALUE = 1\n",
        encoding="utf-8",
    )
    row = {
        "action": "inserted",
        "target_kind": "module",
        "file": str(source.resolve()),
        "line": 1,
        "suggested_docstring": "Utilities for future import module.",
    }

    snippet = build_corrected_snippet_text(_Owner(root), row)
    payload = _snippet_payload_lines(snippet)

    doc_index = payload.index('"""Utilities for future import module."""')
    future_index = payload.index("from __future__ import annotations")
    import_index = payload.index("import os")

    assert doc_index < future_index < import_index
    assert payload[0] == "# Project path: app/module_with_future.py"


if __name__ == "__main__":
    test_module_docstring_stays_after_shebang_and_encoding()
    test_module_docstring_stays_before_future_imports()
    print("PA038 Tab 3 module header placement tests passed.")
