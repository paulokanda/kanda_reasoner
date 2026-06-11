
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_write_contracts import (
    TAB1_AUDIT_WRITE_ROUTE_STATUS_EMPTY,
    TAB1_AUDIT_WRITE_ROUTE_STATUS_READY,
    TAB1_AUDIT_WRITE_ROUTE_STATUS_SKIPPED,
    Tab1AuditWritePlan,
    Tab1AuditWriteTarget,
)


class Tab1AuditWriteContractsDirectTests(unittest.TestCase):
    """Directly protect the Tab 1 audit write contracts public API."""

    def test_public_contract_symbols_import_directly(self) -> None:
        self.assertEqual("empty", TAB1_AUDIT_WRITE_ROUTE_STATUS_EMPTY)
        self.assertEqual("ready", TAB1_AUDIT_WRITE_ROUTE_STATUS_READY)
        self.assertEqual("skipped", TAB1_AUDIT_WRITE_ROUTE_STATUS_SKIPPED)
        self.assertTrue(Tab1AuditWritePlan)
        self.assertTrue(Tab1AuditWriteTarget)


if __name__ == "__main__":
    unittest.main()
