# project-path: validation/test_architecture_review_large_file_refactor_dependency_clustering_v1.py
"""Focused validation for dependency-aware clustering in the refactor planner."""
from __future__ import annotations

import py_compile
from pathlib import Path
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.dependency_clusterer import (
    build_dependency_clusters,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    ImportRecord,
    ModuleAnalysisReport,
    PlannerSettings,
    RefactorSymbol,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan


class DependencyClusteringTests(unittest.TestCase):
    """Validate dependency-aware helper clustering behavior."""

    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parents[1]
        self.pkg = self.project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"

    def test_dependent_symbols_are_kept_in_one_helper(self) -> None:
        """A symbol that references another movable symbol must cluster with it."""
        report = _fake_report([
            _symbol("_alpha", 10, references=["_beta"]),
            _symbol("_beta", 30),
            _symbol("_lonely", 50),
        ])
        plan = build_split_plan(report, PlannerSettings())
        clusters = plan.import_migration["dependency_clustering"]["clusters"]
        clustered = [item for item in clusters if "_alpha" in item["symbols"]]
        self.assertEqual(clustered[0]["symbols"], ["_alpha", "_beta"])
        helper = [module for module in plan.proposed_modules if set(module.symbols) == {"_alpha", "_beta"}][0]
        self.assertEqual(helper.role, "dependency_cluster_helper")
        self.assertIn("Cohesive dependency cluster", helper.line_limit_justification)

    def test_oversized_dependency_cluster_blocks_plan(self) -> None:
        """An oversized dependency component must remain visible as a blocker."""
        report = _fake_report([
            _symbol("_large_a", 10, lines=290, references=["_large_b"]),
            _symbol("_large_b", 330, lines=290),
        ])
        clustering = build_dependency_clusters(report, PlannerSettings(), ["_large_a", "_large_b"])
        self.assertIn("DEPENDENCY_CLUSTER_TOO_LARGE", clustering.risk_flags)
        self.assertTrue(clustering.blockers)
        plan = build_split_plan(report, PlannerSettings())
        self.assertEqual(plan.status, "blocked")
        self.assertIn("DEPENDENCY_CLUSTER_TOO_LARGE", plan.risks)

    def test_public_facade_symbols_remain_facade_owned(self) -> None:
        """Public API ownership must still stay with the facade before clustering."""
        report = _fake_report([
            _symbol("public_api", 10, visibility="public", references=["_helper"]),
            _symbol("_helper", 40),
        ], public_api=["public_api"])
        plan = build_split_plan(report, PlannerSettings())
        facade = [module for module in plan.proposed_modules if module.role == "public_facade"][0]
        self.assertIn("public_api", facade.symbols)
        helpers = [module for module in plan.proposed_modules if module.role != "public_facade"]
        self.assertTrue(any("_helper" in module.symbols for module in helpers))
        self.assertFalse(any("public_api" in module.symbols for module in helpers))

    def test_changed_modules_compile_and_stay_under_size_cap(self) -> None:
        """Changed modules and validation files must compile and stay under 500 lines."""
        files = [
            self.pkg / "dependency_clusterer.py",
            self.pkg / "split_planner.py",
            self.pkg / "__init__.py",
            Path(__file__),
            self.project_root / "tools/validate_architecture_review_large_file_refactor_dependency_clustering_v1.py",
        ]
        for path in files:
            self.assertTrue(path.is_file(), str(path))
            py_compile.compile(str(path), doraise=True)
            self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 500, str(path))


def _symbol(
    name: str,
    start: int,
    *,
    lines: int = 20,
    visibility: str = "private",
    kind: str = "function",
    references: list[str] | None = None,
) -> RefactorSymbol:
    return RefactorSymbol(
        schema_version="1.0",
        name=name,
        kind=kind,
        visibility=visibility,
        start_line=start,
        end_line=start + lines - 1,
        physical_lines=lines,
        references=references or [],
        atomic_cluster_id=f"symbol:{name}",
    )


def _fake_report(symbols: list[RefactorSymbol], public_api: list[str] | None = None) -> ModuleAnalysisReport:
    return ModuleAnalysisReport(
        schema_version="1.0",
        feature_id=FEATURE_ID,
        target_file=str(Path("/tmp/example_module.py")),
        source_content_hash="hash",
        line_count_physical=900,
        module_docstring_present=True,
        module_docstring_preview="Example.",
        all_names=public_api or [],
        public_api_symbols=public_api or [],
        imports=[ImportRecord(schema_version="1.0", original_module="x", imported_name="os")],
        symbols=symbols,
        constants=[],
        assignments=[],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
    )


if __name__ == "__main__":
    unittest.main()
