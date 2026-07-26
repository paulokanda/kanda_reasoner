# project-path: tools/validate_architecture_review_large_file_refactor_behavior_validation_v1.py
"""Validate Workbench optional behavior/test validation train."""
from __future__ import annotations

from importlib import import_module
import unittest

_TEST_MODULE = "validation.test_architecture_review_large_file_refactor_behavior_validation_v1"


def main() -> int:
    """Load and run the validation-only test module without a static import edge."""
    module = import_module(_TEST_MODULE)
    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    marker = str(getattr(module, "FEATURE_MARKER"))
    print("VALIDATION OK: " + marker)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
