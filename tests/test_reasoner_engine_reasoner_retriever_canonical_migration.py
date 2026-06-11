"""Regression tests for the staged reasoner_retriever canonical migration."""

from __future__ import annotations

import importlib
import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_ENGINE = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine"
LEGACY_ENGINE = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10"
CANONICAL_HELP = CANONICAL_ENGINE / "reasoner_retriever_help"


class ReasonerEngineReasonerRetrieverCanonicalMigrationTests(unittest.TestCase):
    """Protect the staged reasoner_retriever migration contract."""

    def test_canonical_reasoner_retriever_implementation_files_exist(self) -> None:
        expected = [
            CANONICAL_ENGINE / "reasoner_retriever.py",
            CANONICAL_ENGINE / "reasoner_retriever_help.json",
            CANONICAL_ENGINE / "reasoner_retriever_validate_manifests.py",
            CANONICAL_HELP / "__init__.py",
            CANONICAL_HELP / "bundle_merge.py",
            CANONICAL_HELP / "file_context_scoring.py",
            CANONICAL_HELP / "file_retrieval.py",
            CANONICAL_HELP / "live_source_fallback.py",
            CANONICAL_HELP / "profile_support.py",
            CANONICAL_HELP / "query_text.py",
            CANONICAL_HELP / "section_retrieval.py",
            CANONICAL_HELP / "snippet_retrieval.py",
            CANONICAL_HELP / "symbol_retrieval.py",
        ]

        for path in expected:
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), str(path))

    def test_legacy_reasoner_retriever_remains_available_during_migration(self) -> None:
        self.assertTrue((LEGACY_ENGINE / "reasoner_retriever.py").is_file())
        self.assertTrue((LEGACY_ENGINE / "reasoner_retriever_help").is_dir())

    def test_canonical_and_legacy_reasoner_retriever_imports_resolve(self) -> None:
        canonical = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.reasoner_retriever"
        )
        legacy = importlib.import_module(
            "kanda_reasoner_app.project_reasoner_v10.reasoner_retriever"
        )

        self.assertTrue(hasattr(canonical, "__all__"))
        self.assertTrue(hasattr(legacy, "__all__"))

    def test_canonical_reasoner_retriever_helpers_import_through_public_contracts(self) -> None:
        module_names = [
            "bundle_merge",
            "file_context_scoring",
            "file_retrieval",
            "live_source_fallback",
            "profile_support",
            "query_text",
            "section_retrieval",
            "snippet_retrieval",
            "symbol_retrieval",
        ]

        for name in module_names:
            with self.subTest(module=name):
                module = importlib.import_module(
                    f"kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.{name}"
                )
                self.assertTrue(hasattr(module, "__all__"), name)

    def test_canonical_reasoner_retriever_uses_reasoner_engine_manifest_paths(self) -> None:
        manifest_path = CANONICAL_ENGINE / "reasoner_retriever_help.json"
        text = manifest_path.read_text(encoding="utf-8-sig")
        payload = json.loads(text)

        self.assertIsInstance(payload, dict)
        self.assertIn("reasoner_engine", text)
        self.assertNotIn("kanda_reasoner_app/project_reasoner_v10", text)
        self.assertNotIn("kanda_reasoner_app\\project_reasoner_v10", text)

    def test_query_text_helpers_match_legacy_behavior(self) -> None:
        canonical = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text"
        )
        legacy = importlib.import_module(
            "kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text"
        )

        sample = "  Hello  WORLD  "
        self.assertEqual(canonical.norm_text(sample), legacy.norm_text(sample))
        self.assertEqual(canonical.tokenize_query("Alpha beta"), legacy.tokenize_query("Alpha beta"))


if __name__ == "__main__":
    unittest.main()
