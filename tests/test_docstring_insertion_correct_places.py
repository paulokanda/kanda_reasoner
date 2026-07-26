"""Regression tests for missing-docstring insertion placement."""

from __future__ import annotations

import ast
import contextlib
import io
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.run_orchestrator import (
    run,
)


def test_write_places_docstrings_at_module_class_and_function_boundaries() -> None:
    """Write mode should insert docstrings where Python expects them."""
    source = textwrap.dedent(
        """\
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        # SPDX-License-Identifier: MIT
        # Copyright Example
        # ruff: noqa

        import os


        class Worker:
            value = 1

            def run(self, path: str) -> str:
                return os.fspath(path)


        def build_worker() -> Worker:
            return Worker()
        """
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        path = root / "module_case.py"
        report = root / "report.jsonl"
        path.write_text(source, encoding="utf-8")

        exit_code = run(
            root,
            "write",
            include_module=True,
            include_classes=True,
            include_functions=True,
            include_init=True,
            report_path=str(report),
        )

        assert exit_code == 0
        updated = path.read_text(encoding="utf-8")
        lines = updated.splitlines()
        assert lines[0] == "#!/usr/bin/env python"
        assert lines[1] == "# -*- coding: utf-8 -*-"
        assert lines[2] == "# SPDX-License-Identifier: MIT"
        assert lines[3] == "# Copyright Example"
        assert lines[4] == "# ruff: noqa"
        assert lines[6].startswith('"""')
        assert lines.index("import os") > 6

        tree = ast.parse(updated)
        classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        method = next(
            node
            for node in ast.walk(classes[0])
            if isinstance(node, ast.FunctionDef) and node.name == "run"
        )

        assert ast.get_docstring(tree)
        assert ast.get_docstring(classes[0])
        assert ast.get_docstring(method)
        assert ast.get_docstring(functions[0])
        assert isinstance(tree.body[0], ast.Expr)
        assert isinstance(classes[0].body[0], ast.Expr)
        assert isinstance(method.body[0], ast.Expr)
        assert isinstance(functions[0].body[0], ast.Expr)


def test_diff_previews_docstrings_without_writing_source() -> None:
    """Diff mode should show insertions without modifying the source file."""
    source = textwrap.dedent(
        """\
        def calculate_total(value: int) -> int:
            return value
        """
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        path = root / "preview_case.py"
        report = root / "report.jsonl"
        path.write_text(source, encoding="utf-8")

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = run(
                root,
                "diff",
                include_module=False,
                include_classes=False,
                include_functions=True,
                include_init=True,
                report_path=str(report),
            )

        assert exit_code == 0
        assert "preview_case.py (generated)" in output.getvalue()
        assert "Calculate the total" in output.getvalue()
        assert path.read_text(encoding="utf-8") == source


if __name__ == "__main__":
    test_write_places_docstrings_at_module_class_and_function_boundaries()
    test_diff_previews_docstrings_without_writing_source()
    print("Docstring insertion placement tests passed.")
