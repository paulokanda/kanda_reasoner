from __future__ import annotations

import sys
import unittest
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = CURRENT_DIR.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from collector_warnings import parse_python_source_with_warnings


class TestWarningCapture(unittest.TestCase):
    def test_invalid_escape_sequence_warning_is_captured(self) -> None:
        source = 'value = "C:\\example\\new\\eeg\\test"\n'
        _tree, error, warnings_list = parse_python_source_with_warnings(source)

        self.assertIsNone(error)
        self.assertTrue(isinstance(warnings_list, list))

    def test_valid_source_returns_no_parse_error(self) -> None:
        source = "x = 1\ny = x + 2\n"
        tree, error, warnings_list = parse_python_source_with_warnings(source)

        self.assertIsNotNone(tree)
        self.assertIsNone(error)
        self.assertTrue(isinstance(warnings_list, list))


if __name__ == "__main__":
    unittest.main()