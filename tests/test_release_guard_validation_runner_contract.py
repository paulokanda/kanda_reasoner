from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = PROJECT_ROOT / "scripts" / "validate_release_guard_zip_contract_v1.py"


class ReleaseGuardValidationRunnerContractTests(unittest.TestCase):
    def test_runner_exists_and_is_python_subprocess_based(self) -> None:
        self.assertTrue(RUNNER_PATH.exists())
        text = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertIn("subprocess.run", text)
        self.assertIn("stderr=subprocess.STDOUT", text)
        self.assertIn("stdout=subprocess.PIPE", text)

    def test_runner_syncs_before_running_prompt_contract_tests(self) -> None:
        text = RUNNER_PATH.read_text(encoding="utf-8")
        sync_position = text.index("checking startup sync before prompt contract tests")
        tests_position = text.index("running release guard unit tests")
        self.assertLess(sync_position, tests_position)
        self.assertIn("VALIDATION OK: {FEATURE_ID}", text)
        self.assertIn("STATUS: IN_SYNC", text)

    def test_runner_uses_ascii_only_text(self) -> None:
        raw = RUNNER_PATH.read_bytes()
        raw.decode("ascii")


if __name__ == "__main__":
    unittest.main()
