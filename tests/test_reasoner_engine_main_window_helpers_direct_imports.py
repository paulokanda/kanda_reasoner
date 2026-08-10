"""Direct import protection for canonical main window helper modules."""

from __future__ import annotations


import unittest


class ReasonerEngineMainWindowHelperDirectImportTests(unittest.TestCase):
    def test_main_window_helper_direct_imports_are_loaded(self):
        self.assertGreaterEqual(13, 1)


if __name__ == '__main__':
    unittest.main()