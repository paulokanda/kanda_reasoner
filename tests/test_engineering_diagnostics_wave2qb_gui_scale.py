# project-path: tests/test_engineering_diagnostics_wave2qb_gui_scale.py
"""GUI, scale, and public-boundary tests for Wave 2Q-B."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from threading import Event
import time
import unittest
from unittest.mock import patch

from kanda_reasoner_app.engineering_diagnostics import (
    RELATIONAL_EDGE_KINDS,
    RELATIONAL_NODE_KINDS,
    SHADOW_PRODUCER_ID,
    EngineeringDiagnosticsStore,
    ShadowCollectionResult,
    ShadowIssueEvidence,
    build_deterministic_diagnostic_groups,
)
from kanda_reasoner_app.engineering_diagnostics_gui.controller import (
    EngineeringDiagnosticsController,
)
from kanda_reasoner_app.engineering_diagnostics_gui.owner_ui import (
    build_finding_detail_lines,
)
from tools.engineering_diagnostics_wave2qa_fixture_support import (
    wave2qa_disposable_boundary_fixture,
    wave2qa_finding_fixture,
    wave2qa_run_record_fixture,
)


def _collection(root: Path) -> ShadowCollectionResult:
    return ShadowCollectionResult(
        project_root=str(root),
        collector_version="1.0",
        audit_source="public.shadow.audit",
        audit_source_sha256="a" * 64,
        started_at_utc="2026-08-06T00:00:00Z",
        completed_at_utc="2026-08-06T00:00:01Z",
        issues=(
            ShadowIssueEvidence(
                code="DUPLICATE_PUBLIC_SYMBOL",
                relative_path="ARCHITECTURE.md",
                message="Duplicate Thing.",
                severity="warning",
                confidence="medium",
                line=None,
                evidence={"symbol": "Thing", "owners": ["pkg/__init__.py", "pkg/impl.py"]},
                suggested_action="Select one owner.",
            ),
            ShadowIssueEvidence(
                code="BEHAVIOR_DEFINED_IN_FACADE",
                relative_path="pkg/__init__.py",
                message="Facade defines Thing.",
                severity="warning",
                confidence="high",
                line=4,
                evidence={"symbol": "Thing"},
                suggested_action="Move behavior.",
            ),
        ),
        assessment="ISSUES",
        coverage_valid=True,
        metadata={},
    )


class EngineeringDiagnosticsWave2QBGuiScaleTests(unittest.TestCase):
    def test_controller_collects_and_commits_shadow_through_store(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                boundary_resolver=lambda root: boundary,
                store_factory=lambda value: store,
            )
            with patch(
                "kanda_reasoner_app.engineering_diagnostics_gui.shadow_controller.collect_shadow_findings",
                return_value=_collection(boundary.active_project_root),
            ), patch(
                "kanda_reasoner_app.engineering_diagnostics_gui.shadow_controller.project_source_fingerprint",
                return_value="source-shadow",
            ), patch(
                "kanda_reasoner_app.engineering_diagnostics_gui.controller.project_source_fingerprint",
                return_value="source-shadow",
            ):
                candidate = controller.collect_shadow_candidate(
                    boundary.active_project_root,
                    3,
                    Event(),
                )
                run = controller.commit_candidate(
                    boundary.active_project_root,
                    candidate,
                    current_generation=3,
                )
            self.assertEqual(run.producer_id, SHADOW_PRODUCER_ID)
            self.assertEqual(len(store.list_findings(boundary, run.run_id)), 2)
            view = controller.load_run_view(boundary.active_project_root, run.run_id)
            self.assertEqual(len(view.groups), 1)
            self.assertEqual(view.groups[0].recipe_id, "shadow.relational_component.v1")

    def test_gui_source_declares_shadow_public_producer(self) -> None:
        source = (
            Path(__file__).resolve().parents[1]
            / "kanda_reasoner_app"
            / "engineering_diagnostics_gui"
            / "engineering_diagnostics_tab.py"
        ).read_text(encoding="utf-8")
        self.assertIn('producer_combo.addItem("Shadow", SHADOW_PRODUCER_ID)', source)
        self.assertIn("active_controller.collect_shadow_candidate", source)
        self.assertNotIn("source_hygiene._shadow_audit_ast", source)

    def test_public_facade_exposes_relational_contracts(self) -> None:
        self.assertEqual(
            RELATIONAL_NODE_KINDS,
            frozenset({"file", "symbol", "public_surface", "facade", "implementation_owner", "export"}),
        )
        self.assertEqual(
            RELATIONAL_EDGE_KINDS,
            frozenset({"duplicate_of", "reexports", "facade_of", "implements", "unbound_export"}),
        )

    def test_detail_presents_diagnostic_group_not_confirmed_root_cause(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                boundary_resolver=lambda root: boundary,
                store_factory=lambda value: store,
            )
            with patch(
                "kanda_reasoner_app.engineering_diagnostics_gui.shadow_controller.collect_shadow_findings",
                return_value=_collection(boundary.active_project_root),
            ), patch(
                "kanda_reasoner_app.engineering_diagnostics_gui.shadow_controller.project_source_fingerprint",
                return_value="source-shadow",
            ), patch(
                "kanda_reasoner_app.engineering_diagnostics_gui.controller.project_source_fingerprint",
                return_value="source-shadow",
            ):
                candidate = controller.collect_shadow_candidate(boundary.active_project_root, 1, Event())
                run = controller.commit_candidate(boundary.active_project_root, candidate, current_generation=1)
            view = controller.load_run_view(boundary.active_project_root, run.run_id)
            text = "\n".join(build_finding_detail_lines(view.findings[0], "excerpt"))
            self.assertIn("Diagnostic groups:", text)
            self.assertNotIn("Confirmed root cause", text)
            self.assertIn('"all_edges_deterministic": true', text.lower())

    def test_relational_grouping_handles_25000_findings(self) -> None:
        run = replace(
            wave2qa_run_record_fixture(SHADOW_PRODUCER_ID, "run-scale"),
            finding_count=25000,
        )
        findings = []
        component_count = 100
        for index in range(25000):
            component = index % component_count
            symbol = "Symbol" + str(component)
            facade = "pkg" + str(component) + "/__init__.py"
            implementation = "pkg" + str(component) + "/impl.py"
            if index % 2 == 0:
                findings.append(
                    wave2qa_finding_fixture(
                        "dup-" + str(index),
                        "DUPLICATE_PUBLIC_SYMBOL",
                        "ARCHITECTURE.md",
                        symbol=symbol,
                        evidence={"symbol": symbol, "owners": [facade, implementation]},
                        run_id="run-scale",
                    )
                )
            else:
                findings.append(
                    wave2qa_finding_fixture(
                        "facade-" + str(index),
                        "BEHAVIOR_DEFINED_IN_FACADE",
                        facade,
                        symbol=symbol,
                        evidence={"symbol": symbol},
                        run_id="run-scale",
                    )
                )
        started = time.perf_counter()
        groups = build_deterministic_diagnostic_groups(run, tuple(findings))
        elapsed = time.perf_counter() - started
        self.assertEqual(len(groups), component_count)
        self.assertEqual(
            sum(len(group.member_issue_fingerprints) for group in groups),
            25000,
        )
        self.assertLess(elapsed, 15.0)
        self.assertTrue(all(group.evidence["all_edges_deterministic"] for group in groups))

    def test_shadow_collection_does_not_write_grouping_or_freeze_state(self) -> None:
        with wave2qa_disposable_boundary_fixture() as boundary:
            before = set(boundary.active_project_support_root.rglob("*"))
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                boundary_resolver=lambda root: boundary,
            )
            with patch(
                "kanda_reasoner_app.engineering_diagnostics_gui.shadow_controller.collect_shadow_findings",
                return_value=_collection(boundary.active_project_root),
            ), patch(
                "kanda_reasoner_app.engineering_diagnostics_gui.shadow_controller.project_source_fingerprint",
                return_value="source-shadow",
            ), patch(
                "kanda_reasoner_app.engineering_diagnostics_gui.controller.project_source_fingerprint",
                return_value="source-shadow",
            ):
                controller.collect_shadow_candidate(boundary.active_project_root, 1, Event())
            after = set(boundary.active_project_support_root.rglob("*"))
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
