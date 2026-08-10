# project-path: tests/test_engineering_diagnostics_wave2qa_gui_scale.py
"""GUI, schema, and scale tests for Engineering Diagnostics Wave 2Q-A."""

from __future__ import annotations

from contextlib import closing
from dataclasses import replace
import sqlite3
import time
import unittest

from kanda_reasoner_app.engineering_diagnostics import (
    BOM_PRODUCER_ID,
    RUFF_PRODUCER_ID,
    DiagnosticGroupRecord,
    DiagnosticStateError,
    EngineeringDiagnosticsStore,
    build_deterministic_diagnostic_groups,
    index_diagnostic_groups,
)
from kanda_reasoner_app.engineering_diagnostics_gui.diagnostic_table_model import (
    create_finding_table_model_class,
)
from kanda_reasoner_app.engineering_diagnostics_gui.models import (
    DiagnosticFindingView,
)
from kanda_reasoner_app.engineering_diagnostics_gui.owner_ui import (
    build_finding_detail_lines,
)
from tools.engineering_diagnostics_wave2qa_fixture_support import (
    wave2qa_disposable_boundary_fixture,
    wave2qa_finding_fixture,
    wave2qa_run_record_fixture,
)


class EngineeringDiagnosticsWave2QAGuiScaleTests(unittest.TestCase):
    def test_grouping_schema_is_separate_from_finding_identity_schema(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            with closing(sqlite3.connect(store.database_path)) as connection:
                rows = dict(connection.execute("SELECT key, value FROM diagnostics_metadata"))
            self.assertEqual(rows["schema_version"], "1.0")
            self.assertEqual(rows["grouping_schema_version"], "1.0")

    def test_existing_wave2pb_database_migrates_without_identity_change(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            database = (
                boundary.active_project_support_root
                / "project_engineering_diagnostics"
                / "engineering_diagnostics.sqlite3"
            )
            database.parent.mkdir(parents=True, exist_ok=True)
            with closing(sqlite3.connect(database)) as connection:
                connection.execute(
                    "CREATE TABLE diagnostics_metadata "
                    "(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
                )
                connection.executemany(
                    "INSERT INTO diagnostics_metadata (key, value) VALUES (?, ?)",
                    (("schema_version", "1.0"), ("legacy_sentinel", "preserved")),
                )
                connection.commit()
            EngineeringDiagnosticsStore(boundary)
            with closing(sqlite3.connect(database)) as connection:
                metadata = dict(
                    connection.execute(
                        "SELECT key, value FROM diagnostics_metadata"
                    )
                )
                tables = {
                    row[0]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }
            self.assertEqual(metadata["schema_version"], "1.0")
            self.assertEqual(metadata["grouping_schema_version"], "1.0")
            self.assertEqual(metadata["legacy_sentinel"], "preserved")
            self.assertIn("diagnostic_group_decisions", tables)

    def test_grouping_migration_rolls_back_on_schema_mismatch(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            database = (
                boundary.active_project_support_root
                / "project_engineering_diagnostics"
                / "engineering_diagnostics.sqlite3"
            )
            database.parent.mkdir(parents=True, exist_ok=True)
            with closing(sqlite3.connect(database)) as connection:
                connection.execute(
                    "CREATE TABLE diagnostics_metadata "
                    "(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
                )
                connection.executemany(
                    "INSERT INTO diagnostics_metadata (key, value) VALUES (?, ?)",
                    (("schema_version", "1.0"), ("grouping_schema_version", "999")),
                )
                connection.commit()
            with self.assertRaises(DiagnosticStateError) as context:
                EngineeringDiagnosticsStore(boundary)
            self.assertIn(
                "ENGINEERING_DIAGNOSTICS_GROUPING_SCHEMA_UNSUPPORTED",
                str(context.exception),
            )
            with closing(sqlite3.connect(database)) as connection:
                tables = {
                    row[0]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }
            self.assertNotIn("diagnostic_group_heads", tables)
            self.assertNotIn("diagnostic_group_decisions", tables)

    def test_group_index_prefers_manual_without_hiding_deterministic_groups(self) -> None:
        deterministic = DiagnosticGroupRecord(
            "d",
            "project-id-2qa",
            RUFF_PRODUCER_ID,
            "scope",
            "DETERMINISTIC",
            "ruff.rule_file.v1",
            "F401 in pkg/a.py",
            "high",
            ("issue", "other"),
        )
        manual = DiagnosticGroupRecord(
            "m",
            "project-id-2qa",
            RUFF_PRODUCER_ID,
            "scope",
            "MANUAL",
            "manual.user_defined.v1",
            "Reviewed imports",
            "high",
            ("issue",),
            author="tester",
        )
        indexed = index_diagnostic_groups((deterministic, manual))
        self.assertEqual(indexed["issue"][0].kind, "MANUAL")
        self.assertEqual(len(indexed["issue"]), 2)

    def test_gui_detail_uses_diagnostic_group_not_root_cause_terminology(self) -> None:
        group = DiagnosticGroupRecord(
            "d",
            "project-id-2qa",
            BOM_PRODUCER_ID,
            "scope",
            "DETERMINISTIC",
            "bom.rule_file.v1",
            "BOM_UTF8 in pkg/a.py",
            "high",
            ("a", "b"),
            evidence={"root_cause_claimed": False},
        )
        view = DiagnosticFindingView(
            wave2qa_finding_fixture("a", "BOM_UTF8", "pkg/a.py"),
            "current",
            groups=(group,),
        )
        rendered = "\n".join(build_finding_detail_lines(view, "excerpt"))
        self.assertIn("Diagnostic groups:", rendered)
        self.assertNotIn("Confirmed root cause", rendered)

    def test_table_model_group_filter_preserves_prior_signatures(self) -> None:
        class FakeIndex:
            def __init__(self, row: int = -1, column: int = -1) -> None:
                self._row = row
                self._column = column

            def isValid(self) -> bool:  # noqa: N802
                return self._row >= 0 and self._column >= 0

            def row(self) -> int:
                return self._row

            def column(self) -> int:
                return self._column

        class FakeModel:
            def beginResetModel(self) -> None:  # noqa: N802
                pass

            def endResetModel(self) -> None:  # noqa: N802
                pass

        class FakeQt:
            DisplayRole = 0
            ToolTipRole = 1
            Horizontal = 2
            AscendingOrder = 3
            DescendingOrder = 4

        model_type = create_finding_table_model_class(
            FakeModel,
            FakeIndex,
            FakeQt,
            (("group_kind", "Group"), ("relative_path", "Path")),
        )
        manual = DiagnosticGroupRecord(
            "m",
            "project-id-2qa",
            BOM_PRODUCER_ID,
            "scope",
            "MANUAL",
            "manual.user_defined.v1",
            "Manual",
            "high",
            ("a",),
            author="tester",
        )
        rows = (
            DiagnosticFindingView(
                wave2qa_finding_fixture("a", "BOM_UTF8", "pkg/a.py"),
                "current",
                groups=(manual,),
            ),
            DiagnosticFindingView(
                wave2qa_finding_fixture("b", "BOM_UTF8", "pkg/b.py"),
                "current",
            ),
        )
        model = model_type()
        model.set_rows(rows)
        model.set_filters("all", "all", "all", "all", "all", "manual", "")
        self.assertEqual(model.rowCount(), 1)
        model.set_filters("all", "all", "pkg/b.py")
        self.assertEqual(model.rowCount(), 1)

    def test_batch_grouping_handles_25000_findings(self) -> None:
        run = replace(wave2qa_run_record_fixture(RUFF_PRODUCER_ID), finding_count=25000)
        findings = tuple(
            wave2qa_finding_fixture(
                str(index),
                "F401",
                "pkg/file_" + str(index % 100).zfill(3) + ".py",
                symbol="Module.function_" + str(index % 10),
            )
            for index in range(25000)
        )
        started = time.perf_counter()
        groups = build_deterministic_diagnostic_groups(run, findings)
        elapsed = time.perf_counter() - started
        self.assertTrue(groups)
        self.assertLess(elapsed, 5.0)


if __name__ == "__main__":
    unittest.main()
