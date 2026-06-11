
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help import (
    tab1_audit_write_contracts,
)


class Tab1AuditWriteContractsTests(unittest.TestCase):
    """Validate neutral Tab 1 audit write contracts."""

    def test_contracts_export_plan_and_target(self) -> None:
        exported = set(tab1_audit_write_contracts.__all__)

        self.assertIn("Tab1AuditWritePlan", exported)
        self.assertIn("Tab1AuditWriteTarget", exported)
        self.assertIn("TAB1_AUDIT_WRITE_ROUTE_STATUS_READY", exported)

    def test_contracts_do_not_import_route_or_worker(self) -> None:
        from pathlib import Path

        source = Path(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "insert_missing_docstrings_gui_help/tab1_audit_write_contracts.py"
        ).read_text(encoding="utf-8")

        self.assertNotIn("tab1_audit_write_route", source)
        self.assertNotIn("tab1_audit_write_worker", source)


if __name__ == "__main__":
    unittest.main()
