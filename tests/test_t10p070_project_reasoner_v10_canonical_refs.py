"""Regression tests for T10P070 project_reasoner_v10 canonical references."""

from __future__ import annotations

from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "project_reasoner_v10"
LEGACY_TOKEN = 'ask_' 'ai_project_reasoner'


class ProjectReasonerV10CanonicalRefsTests(unittest.TestCase):
    """Validate the project_reasoner_v10 owner box migration contract."""

    def _owner_python_files(self) -> list[Path]:
        return sorted(path for path in OWNER_ROOT.rglob("*.py") if path.is_file())

    def test_owner_python_files_do_not_contain_literal_legacy_package_token(self) -> None:
        offenders: list[str] = []
        for path in self._owner_python_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            if LEGACY_TOKEN in text:
                offenders.append(str(path.relative_to(PROJECT_ROOT)))
        self.assertEqual([], offenders)

    def test_core_imports_use_canonical_package_token(self) -> None:
        samples = {
            "ai_bridge.py": "from kanda_reasoner_app.project_reasoner_v10.v10_qwen_ai_models import V9QwenAIModels",
            "ai_reasoner_main_window.py": "from kanda_reasoner_app.backend_payloads.loader import load_payload",
            "reasoner_retriever.py": "from kanda_reasoner_app.backend_payloads.loader import load_payload",
            "run_project_reasoner_v10.py": "from kanda_reasoner_app.project_reasoner_v10.ai_reasoner_main_window import main",
        }
        for rel_path, expected in samples.items():
            text = (OWNER_ROOT / rel_path).read_text(encoding="utf-8", errors="replace")
            self.assertIn(expected, text)

    def test_snippet_manifest_validator_preserves_dynamic_staged_path(self) -> None:
        path = OWNER_ROOT / "reasoner_retriever_help" / "snippet_retrieval_validate_manifests.py"
        text = path.read_text(encoding="utf-8", errors="replace")
        self.assertIn("_STAGED_PACKAGE_NAME", text)
        self.assertIn('"_".join(("ask", "ai", "project", "reasoner"))', text)
        self.assertIn("ROOT / _STAGED_PACKAGE_NAME", text)
        self.assertNotIn(LEGACY_TOKEN, text)

    def test_file_retrieval_private_loader_uses_canonical_exec_namespace(self) -> None:
        path = OWNER_ROOT / "reasoner_retriever_help" / "file_retrieval_help" / "file_retrieval_impl_private_impl.py"
        text = path.read_text(encoding="utf-8", errors="replace")
        self.assertIn(
            '"__name__": "kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.file_retrieval"',
            text,
        )
        self.assertIn(
            '"__package__": "kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help"',
            text,
        )
        self.assertNotIn(LEGACY_TOKEN, text)


if __name__ == "__main__":
    unittest.main()
