"""Focused tests for the reasoner_symbol_atlas folder rename."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OLD_FOLDER = PROJECT_ROOT / "kanda_reasoner_app" / "project_symbol_atlas"
NEW_FOLDER = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_symbol_atlas"


def run_python_probe(code: str) -> subprocess.CompletedProcess[str]:
    """Run a Python probe in a fresh interpreter."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    env["kanda_reasoner_project_root"] = str(PROJECT_ROOT)

    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(PROJECT_ROOT),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


class ReasonerSymbolAtlasFolderRenameTests(unittest.TestCase):
    """Protect the final reasoner_symbol_atlas canonical folder name."""

    def test_new_symbol_atlas_folder_exists(self) -> None:
        self.assertTrue(NEW_FOLDER.exists(), str(NEW_FOLDER))
        self.assertTrue(NEW_FOLDER.is_dir(), str(NEW_FOLDER))

    def test_old_symbol_atlas_folder_is_absent(self) -> None:
        self.assertFalse(OLD_FOLDER.exists(), str(OLD_FOLDER))

    def test_canonical_symbol_atlas_imports(self) -> None:
        import kanda_reasoner_app.reasoner_symbol_atlas as symbol_atlas

        self.assertIsNotNone(symbol_atlas)

    def test_old_symbol_atlas_import_is_absent_in_fresh_interpreter(self) -> None:
        result = run_python_probe(
            "import importlib.util; "
            "spec = importlib.util.find_spec('kanda_reasoner_app.project_symbol_atlas'); "
            "raise SystemExit(0 if spec is None else 1)"
        )
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_canonical_symbol_atlas_imports_in_fresh_interpreter(self) -> None:
        result = run_python_probe(
            "import kanda_reasoner_app.reasoner_symbol_atlas; "
            "print('reasoner_symbol_atlas fresh import ok')"
        )
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_no_direct_deleted_folder_import_reference_in_runtime_sources(self) -> None:
        banned_tokens = (
            "kanda_reasoner_app.project_symbol_atlas",
            "kanda_reasoner_app/project_symbol_atlas",
            "kanda_reasoner_app\\project_symbol_atlas",
        )

        checked_extensions = {".py", ".json", ".md", ".txt", ".yml", ".yaml", ".ps1"}
        ignored_parts = {
            ".git",
            "__pycache__",
            "_kanda_patch_backups",
        }

        offenders = []

        for path in PROJECT_ROOT.rglob("*"):
            if not path.is_file():
                continue

            if path.suffix.lower() not in checked_extensions:
                continue

            parts = set(path.parts)
            if parts.intersection(ignored_parts):
                continue

            relative = path.relative_to(PROJECT_ROOT).as_posix()
            if relative.startswith("tests/"):
                continue

            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in banned_tokens:
                if token in text:
                    offenders.append(f"{relative}: {token}")

        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
