"""Regression tests for static context smoke scripts using canonical paths."""

from __future__ import annotations

from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET_FILES = (
    Path("kanda_reasoner_app/run_real_project_static_context_smoke.py"),
    Path("kanda_reasoner_app/run_static_context_test_suite.py"),
)
RETIRED_PATTERNS = (
    "kanda_reasoner_app.project_reasoner_v10",
    "kanda_reasoner_app/project_reasoner_v10",
    "kanda_reasoner_app\\project_reasoner_v10",
    "ask_ai_project_reasoner.project_reasoner_v10",
    "ask_ai_project_reasoner/project_reasoner_v10",
    "ask_ai_project_reasoner\\project_reasoner_v10",
)
CANONICAL_PATTERN = "kanda_reasoner_app.reasoner_engine"


class StaticContextSmokeScriptsCanonicalPathCleanupTests(unittest.TestCase):
    """Verify static context smoke scripts no longer depend on deleted engine path."""

    def test_static_context_smoke_scripts_exist(self):
        for relative_path in TARGET_FILES:
            with self.subTest(path=str(relative_path)):
                self.assertTrue((PROJECT_ROOT / relative_path).exists(), str(relative_path))

    def test_static_context_smoke_scripts_do_not_reference_deleted_engine_package(self):
        offenders = []
        for relative_path in TARGET_FILES:
            path = PROJECT_ROOT / relative_path
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in RETIRED_PATTERNS:
                if pattern in text:
                    offenders.append(f"{relative_path}: {pattern}")
        self.assertEqual([], offenders)

    def test_static_context_smoke_scripts_prefer_canonical_engine_package(self):
        joined_text = "\n".join(
            (PROJECT_ROOT / relative_path).read_text(encoding="utf-8", errors="replace")
            for relative_path in TARGET_FILES
        )
        self.assertIn(CANONICAL_PATTERN, joined_text)


if __name__ == "__main__":
    unittest.main()
