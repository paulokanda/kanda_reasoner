from __future__ import annotations

import ast
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_tools_shell.runner_help import (  # noqa: E402
    zip_json_files_private_impl as module,
)


def _source_path() -> Path:
    return (
        PROJECT_ROOT
        / 'ask_' 'ai_project_reasoner'
        / "reasoner_tools_shell"
        / "runner_help"
        / "zip_json_files_private_impl.py"
    )


def test_zip_json_files_qtwidgets_import_is_lazy() -> None:
    source = _source_path().read_text(encoding="utf-8")
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module_name = node.module or ""
            assert not module_name.startswith("PySide6"), module_name
        elif isinstance(node, ast.Import):
            for alias in node.names:
                assert not alias.name.startswith("PySide6"), alias.name

    assert "from PySide6" not in source
    assert "import PySide6" not in source
    assert "importlib.import_module" in source


def test_zip_json_files_public_contract_still_available() -> None:
    assert module.CONSERVATIVE_ZIP_SIZE_MB == 25
    assert module.DEFAULT_ZIP_SIZE_MB == 40
    assert callable(module.run_zip_json_files)


def main() -> int:
    test_zip_json_files_qtwidgets_import_is_lazy()
    test_zip_json_files_public_contract_still_available()
    print("JSONCTX014J ZIP JSON files QtWidgets lazy import tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
