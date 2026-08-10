"""Validate Error Memory tab project-root helper extraction."""
from __future__ import annotations

import ast
import py_compile
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "error-memory-tab-project-roots-refactor-v1"
ROOT = Path(__file__).resolve(strict=False).parents[1]
TAB = ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
HELPER = ROOT / "kanda_reasoner_app/error_memory_gui/_project_roots.py"
TEST = ROOT / "tests/test_error_memory_tab_project_roots_public_contract.py"

REQUIRED_TAB_SNIPPETS = [
    "from kanda_reasoner_app.error_memory_gui._project_roots import (",
    "def _source_root_peer_from_generated_output(path: Path) -> Path | None:",
    "return source_root_peer_from_generated_output(path)",
    "def _source_root_from_directory_hint(cls, path: Path) -> Path | None:",
    "return source_root_from_directory_hint(",
    "def _existing_directory_from_text(cls, text: str) -> Path | None:",
    "return existing_directory_from_text(",
    "def set_project_root(self, project_root: str | Path) -> None:",
    "def _current_project_root(self) -> Path:",
]

REQUIRED_HELPER_SNIPPETS = [
    "__all__ = [",
    "GENERATED_OUTPUT_SUFFIXES =",
    "def source_root_peer_from_generated_output(path: Path) -> Path | None:",
    "def source_root_from_directory_hint(",
    "def existing_directory_from_text(",
    "resolved back to an existing sibling source project root",
]


def _fail(message: str) -> None:
    raise SystemExit("VALIDATION FAIL: " + message)


def _read(path: Path) -> str:
    if not path.exists():
        _fail("missing file: " + str(path))
    return path.read_text(encoding="utf-8")


def _assert_no_upward_or_gui_imports(source: str) -> None:
    forbidden = ["PySide", "QtCore", "QtGui", "QtWidgets", "error_memory_tab", "ErrorMemoryTab"]
    for token in forbidden:
        if token in source:
            _fail("_project_roots.py contains forbidden dependency token: " + token)
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = ""
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
            for alias in getattr(node, "names", []):
                module = module + " " + alias.name
            if "PySide" in module or "error_memory_tab" in module:
                _fail("_project_roots.py imports forbidden module: " + module)


def main() -> None:
    tab_text = _read(TAB)
    helper_text = _read(HELPER)
    _read(TEST)
    for snippet in REQUIRED_TAB_SNIPPETS:
        if snippet not in tab_text:
            _fail("error_memory_tab.py missing snippet: " + snippet)
    for snippet in REQUIRED_HELPER_SNIPPETS:
        if snippet not in helper_text:
            _fail("_project_roots.py missing snippet: " + snippet)
    _assert_no_upward_or_gui_imports(helper_text)
    if "generated_suffixes = ('_show_project_to_AI', '_delete_after_daily_work')" in tab_text:
        _fail("error_memory_tab.py still owns old generated suffix project-root implementation")
    if len(tab_text.splitlines()) >= 1627:
        _fail("error_memory_tab.py did not shrink below cluster 5 line count")
    for path in [TAB, HELPER, TEST]:
        py_compile.compile(str(path), doraise=True)
    sys.path.insert(0, str(ROOT))
    from kanda_reasoner_app.error_memory_gui import _project_roots
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        project = temp / "kanda_reasoner"
        show = temp / "kanda_reasoner_show_project_to_AI"
        pending = show / "project_error_memory" / "pending_ai_assisted_error_lesson_intake"
        project.mkdir()
        pending.mkdir(parents=True)
        if _project_roots.existing_directory_from_text(str(project)) != project.resolve(strict=False):
            _fail("helper did not accept existing source project root")
        if _project_roots.existing_directory_from_text(str(show)) != project.resolve(strict=False):
            _fail("helper did not resolve generated show_project root to source peer")
        if _project_roots.existing_directory_from_text(str(pending)) != project.resolve(strict=False):
            _fail("helper did not resolve generated pending child to source peer")
        missing_show = temp / "missing_show_project_to_AI"
        missing_show.mkdir()
        if _project_roots.existing_directory_from_text(str(missing_show)) is not None:
            _fail("helper accepted generated output without source peer")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
