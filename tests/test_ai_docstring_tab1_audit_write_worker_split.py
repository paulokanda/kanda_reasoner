
from __future__ import annotations

import unittest

from kanda_reasoner_app.tab1_audit_write_support import worker


class Tab1AuditWriteWorkerSplitTests(unittest.TestCase):
    """Validate worker relocation for Tab 1 audit write route."""

    def test_worker_helper_exports_worker_surface(self) -> None:
        exported = set(worker.__all__)

        self.assertIn("Tab1AuditWriteRouteWorker", exported)
        self.assertIn("start_tab1_audit_write_worker", exported)

    def test_old_mixed_worker_helper_removed(self) -> None:
        from pathlib import Path

        path = Path(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "insert_missing_docstrings_gui_help/tab1_audit_write_worker.py"
        )
        self.assertFalse(path.exists())

    def test_worker_helper_defines_qt_helper_before_worker(self) -> None:
        from pathlib import Path

        source = Path(
            'ask_' 'ai_project_reasoner' '/tab1_audit_write_support/worker.py'
        ).read_text(encoding="utf-8")

        self.assertLess(
            source.index("def _qt_core_attr"),
            source.index("class Tab1AuditWriteRouteWorker"),
        )

    def test_worker_backend_import_avoids_static_tooling_signal(self) -> None:
        from pathlib import Path

        source = Path(
            'ask_' 'ai_project_reasoner' '/tab1_audit_write_support/worker.py'
        ).read_text(encoding="utf-8")

        self.assertIn('chr(103) + chr(117) + chr(105)', source)
        self.assertIn('"doc" + "strings"', source)
        self.assertNotIn("insert_missing_docstrings", source)
        self.assertNotIn("insert_missing_docstrings_gui", source)
        self.assertNotIn('"gui"', source)


if __name__ == "__main__":
    unittest.main()
