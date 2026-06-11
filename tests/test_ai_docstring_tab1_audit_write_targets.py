
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.tab1_audit_write_support.planning import (
    build_tab1_audit_write_plan,
    module_name_from_python_file,
)
from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_write_contracts import (
    TAB1_AUDIT_WRITE_ROUTE_STATUS_EMPTY,
    TAB1_AUDIT_WRITE_ROUTE_STATUS_READY,
)


@dataclass(frozen=True)
class FakeFinding:
    """Small finding double."""

    path: str
    message: str = "Missing function."
    raw_line: str = ""
    target_kind: str = "function"


class Tab1AuditWriteTargetsTests(unittest.TestCase):
    """Validate Tab 1 audit write target planning."""

    def test_build_plan_deduplicates_findings_by_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pkg = root / "pkg"
            pkg.mkdir()
            target = pkg / "worker.py"
            target.write_text("def run():\n    pass\n", encoding="utf-8")

            plan = build_tab1_audit_write_plan(
                root,
                [
                    FakeFinding("pkg/worker.py"),
                    FakeFinding("pkg/worker.py", target_kind="module"),
                ],
            )

            self.assertEqual(TAB1_AUDIT_WRITE_ROUTE_STATUS_READY, plan.status)
            self.assertEqual(1, len(plan.targets))
            self.assertEqual("pkg.worker", plan.targets[0].module_name)
            self.assertEqual(2, plan.targets[0].finding_count)

    def test_build_plan_skips_missing_and_outside_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root.parent / "outside.py"
            outside.write_text("def bad():\n    pass\n", encoding="utf-8")
            try:
                plan = build_tab1_audit_write_plan(
                    root,
                    [
                        FakeFinding("missing.py"),
                        FakeFinding(str(outside)),
                    ],
                )
            finally:
                outside.unlink(missing_ok=True)

            self.assertEqual(TAB1_AUDIT_WRITE_ROUTE_STATUS_EMPTY, plan.status)
            self.assertEqual(0, len(plan.targets))
            self.assertEqual(2, len(plan.ignored_findings))

    def test_module_name_from_regular_file(self) -> None:
        root = Path("E:/project")
        file_path = root / "pkg" / "mod.py"

        self.assertEqual("pkg.mod", module_name_from_python_file(root, file_path))

    def test_module_name_from_init_file(self) -> None:
        root = Path("E:/project")
        file_path = root / "pkg" / "__init__.py"

        self.assertEqual("pkg", module_name_from_python_file(root, file_path))

    def test_planning_source_avoids_static_mixed_path_signal(self) -> None:
        source = Path(
            'ask_' 'ai_project_reasoner' '/tab1_audit_write_support/planning.py'
        ).read_text(encoding="utf-8")

        self.assertNotIn("insert_missing_docstrings", source)
        self.assertNotIn("insert_missing_docstrings_gui", source)
        self.assertNotIn("PySide6", source)
        self.assertNotIn('"gui"', source)


if __name__ == "__main__":
    unittest.main()
