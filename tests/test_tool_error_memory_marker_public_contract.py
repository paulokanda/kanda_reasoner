"""Public-contract tests for Error Memory marker ownership."""
from __future__ import annotations
import ast
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MARKERS = ("ERROR_LESSON_JSON_BEGIN", "ERROR_LESSON_JSON_END")
class ErrorMemoryMarkerPublicContractTests(unittest.TestCase):
    def test_public_package_exports_marker_values(self) -> None:
        from kanda_reasoner_app.error_memory import ERROR_LESSON_JSON_BEGIN, ERROR_LESSON_JSON_END
        self.assertEqual(ERROR_LESSON_JSON_BEGIN, "KANDA_ERROR_LESSON_JSON_BEGIN")
        self.assertEqual(ERROR_LESSON_JSON_END, "KANDA_ERROR_LESSON_JSON_END")
    def test_gui_marker_consumers_use_public_package(self) -> None:
        gui_root = ROOT / "kanda_reasoner_app/error_memory_gui"
        violations = []
        for path in gui_root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8-sig"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.ImportFrom):
                    continue
                if node.module in {
                    "kanda_reasoner_app.error_memory.intake",
                    "kanda_reasoner_app.error_memory.intake_normalization",
                } and any(alias.name in MARKERS for alias in node.names):
                    violations.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(violations, [])
    def test_marker_definition_owner_is_single(self) -> None:
        owners = {name: [] for name in MARKERS}
        domain = ROOT / "kanda_reasoner_app/error_memory"
        for path in domain.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8-sig"))
            for node in tree.body:
                targets = []
                if isinstance(node, ast.Assign):
                    targets = node.targets
                elif isinstance(node, ast.AnnAssign):
                    targets = [node.target]
                for target in targets:
                    if isinstance(target, ast.Name) and target.id in owners:
                        owners[target.id].append(path.relative_to(ROOT).as_posix())
        expected = ["kanda_reasoner_app/error_memory/intake_normalization.py"]
        self.assertEqual(owners[MARKERS[0]], expected)
        self.assertEqual(owners[MARKERS[1]], expected)
if __name__ == "__main__":
    unittest.main()
