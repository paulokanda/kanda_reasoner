"""Focused public-contract tests for PA035D Tab 3 inline preview stability."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime import inline_preview_runtime


class _LineEdit:
    """Minimal line-edit fake."""

    def __init__(self, value: str) -> None:
        self.value = value

    def text(self) -> str:
        return self.value


class _Owner:
    """Minimal owner with a project root field."""

    def __init__(self, project: Path) -> None:
        self._root_path_edit = _LineEdit(str(project))


def test_empty_selection_placeholder_mentions_review_item() -> None:
    """Empty inline previews must use the canonical review item placeholder."""
    original = inline_preview_runtime.build_original_snippet_text(object(), None)
    corrected = inline_preview_runtime.build_corrected_snippet_text(object(), None)

    assert "No review item" in original
    assert "No review item" in corrected


def test_non_reviewable_row_does_not_generate_correction(tmp_path: Path) -> None:
    """Non-docstring report rows must not be treated as correction rows."""
    source = tmp_path / "module.py"
    source.write_text("def documented():\n    return 1\n", encoding="utf-8")
    owner = _Owner(tmp_path)
    row = {
        "file": "module.py",
        "line": 1,
        "action": "inserted",
        "target_kind": "file_address",
        "docstring": "Not a docstring row.",
    }

    corrected = inline_preview_runtime.build_corrected_snippet_text(owner, row)

    assert "not a missing-docstring correction row" in corrected


def test_reviewable_row_without_draft_has_clear_placeholder(tmp_path: Path) -> None:
    """A real row without a generated draft should explain what is missing."""
    source = tmp_path / "module.py"
    source.write_text("def missing():\n    return 1\n", encoding="utf-8")
    owner = _Owner(tmp_path)
    row = {
        "file": "module.py",
        "line": 1,
        "action": "inserted",
        "target_kind": "function",
        "target_name": "missing",
    }

    corrected = inline_preview_runtime.build_corrected_snippet_text(owner, row)

    assert "No draft docstring" in corrected


def test_reviewable_row_preview_inserts_inside_function(tmp_path: Path) -> None:
    """A function draft preview must be inserted inside the function block."""
    source = tmp_path / "module.py"
    source.write_text("def missing():\n    return 1\n", encoding="utf-8")
    owner = _Owner(tmp_path)
    row = {
        "file": "module.py",
        "line": 1,
        "action": "inserted",
        "target_kind": "function",
        "target_name": "missing",
        "suggested_docstring": "Return one.",
    }

    corrected = inline_preview_runtime.build_corrected_snippet_text(owner, row)

    assert "def missing():" in corrected
    assert '    """Return one."""' in corrected
    assert corrected.index('    """Return one."""') > corrected.index("def missing():")


if __name__ == "__main__":
    test_root = Path(__file__).resolve().parent / "_tmp_pa035d"
    if test_root.exists():
        import shutil

        shutil.rmtree(test_root)
    test_root.mkdir(parents=True)
    test_empty_selection_placeholder_mentions_review_item()
    case1 = test_root / "case1"
    case1.mkdir(exist_ok=True)
    test_non_reviewable_row_does_not_generate_correction(case1)
    case2 = test_root / "case2"
    case2.mkdir(exist_ok=True)
    test_reviewable_row_without_draft_has_clear_placeholder(case2)
    case3 = test_root / "case3"
    case3.mkdir(exist_ok=True)
    test_reviewable_row_preview_inserts_inside_function(case3)
    print("PA035D Tab 3 inline corrector runtime stability tests passed.")
