
from __future__ import annotations

import unittest

from kanda_reasoner_app.tab1_audit_write_support.worker import (
    Tab1AuditWriteRouteWorker,
    start_tab1_audit_write_worker,
)


class Tab1AuditWriteWorkerDirectImportTests(unittest.TestCase):
    """Validate direct public import protection for the relocated write worker."""

    def test_worker_public_symbols_import_directly(self) -> None:
        self.assertTrue(Tab1AuditWriteRouteWorker)
        self.assertTrue(callable(start_tab1_audit_write_worker))


if __name__ == "__main__":
    unittest.main()
