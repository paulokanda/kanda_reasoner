"""Tests for the canonical reasoner_engine.core migration gate."""

from __future__ import annotations

import importlib
from pathlib import Path
import unittest

import kanda_reasoner_app.reasoner_engine.core.retrieval_section_priorities as canonical_priorities


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_CORE = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine" / "core"
LEGACY_CORE = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10" / "core"


class ReasonerEngineCoreCanonicalMigrationTests(unittest.TestCase):
    def test_reasoner_engine_namespace_prefers_canonical_package_path(self) -> None:
        package = importlib.import_module("kanda_reasoner_app.reasoner_engine")
        package_paths = [Path(item).resolve() for item in package.__path__]

        self.assertGreaterEqual(len(package_paths), 2)
        self.assertEqual(package_paths[0], (PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_engine").resolve())
        self.assertIn((PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10").resolve(), package_paths)

    def test_core_package_has_canonical_implementation_files(self) -> None:
        self.assertTrue((CANONICAL_CORE / "__init__.py").is_file())
        self.assertTrue((CANONICAL_CORE / "retrieval_section_priorities.py").is_file())

    def test_legacy_core_imports_resolve_same_public_api(self) -> None:
        canonical = importlib.import_module(
            "kanda_reasoner_app.reasoner_engine.core.retrieval_section_priorities"
        )
        legacy = importlib.import_module(
            "kanda_reasoner_app.project_reasoner_v10.core.retrieval_section_priorities"
        )

        self.assertIs(legacy.get_section_priority, canonical.get_section_priority)
        self.assertIs(legacy.normalize_query_kind, canonical.normalize_query_kind)
        self.assertIs(legacy.SECTION_PRIORITY_BY_QUERY_KIND, canonical.SECTION_PRIORITY_BY_QUERY_KIND)
        self.assertIs(canonical.get_section_priority, canonical_priorities.get_section_priority)
        self.assertEqual(canonical.get_section_priority("startup"), legacy.get_section_priority("startup"))

    def test_legacy_core_is_compatibility_wrapper_only(self) -> None:
        legacy_source = (LEGACY_CORE / "retrieval_section_priorities.py").read_text(encoding="utf-8")

        self.assertIn(
            "from kanda_reasoner_app.reasoner_engine.core.retrieval_section_priorities import",
            legacy_source,
        )
        self.assertNotIn("SECTION_PRIORITY_BY_QUERY_KIND: dict", legacy_source)


if __name__ == "__main__":
    unittest.main()
