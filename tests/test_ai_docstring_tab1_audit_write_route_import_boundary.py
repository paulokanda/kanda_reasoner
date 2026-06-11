
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help import (
    tab1_audit_write_route,
)


class Tab1AuditWriteRouteImportBoundaryTests(unittest.TestCase):
    """Validate import safety and explicit worker error boundary."""

    def test_module_imports_without_qt_helper_name_error(self) -> None:
        self.assertTrue(hasattr(tab1_audit_write_route, "Tab1AuditWriteRouteWorker"))
        self.assertTrue(hasattr(tab1_audit_write_route, "_qt_core_attr"))

    def test_qt_helper_is_defined_before_worker_class_in_source(self) -> None:
        from pathlib import Path

        source = Path(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "insert_missing_docstrings_gui_help/tab1_audit_write_route.py"
        ).read_text(encoding="utf-8")

        helper_index = source.index("def _qt_core_attr")
        class_index = source.index("class Tab1AuditWriteRouteWorker")
        self.assertLess(helper_index, class_index)

    def test_worker_run_uses_explicit_exception_tuple(self) -> None:
        from pathlib import Path

        source = Path(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "insert_missing_docstrings_gui_help/tab1_audit_write_route.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "except (AttributeError, ImportError, OSError, RuntimeError, TypeError, ValueError) as exc:",
            source,
        )
        self.assertNotIn("except Exception:\n            self.finished_error.emit", source)


if __name__ == "__main__":
    unittest.main()
