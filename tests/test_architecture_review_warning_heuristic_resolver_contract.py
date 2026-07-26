# project-path: tests/test_architecture_review_warning_heuristic_resolver_contract.py
"""Focused contract tests for the Architecture Review warning resolver."""

from __future__ import annotations

import unittest

from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import (
    ROUTE_HEURISTIC,
    ROUTE_META,
    ROUTE_WEB_AI,
    format_warning_resolution_report,
    resolve_warning_audit,
)


class WarningHeuristicResolverContractTests(unittest.TestCase):
    """Protect parsing, routing, and non-recursive report formatting."""

    def setUp(self) -> None:
        """Create a mixed warning sample for every test."""
        self.audit_text = "\n".join(
            [
                "INFO startup line",
                "WARNING TEST_PROTECTION_GAP          pkg/service.py :: Important active module has no direct test module import.",
                "WARNING SIDE_EFFECT_ON_IMPORT       pkg/runtime.py :: Module may perform work during import.",
                "WARNING MISSING_DOCSTRING           pkg/plain.py :: Missing module docstring.",
                "WARNING TEST_PROTECTION_GAP          . :: Additional test-protection gaps suppressed after 80 findings.",
            ]
        )

    def test_routes_known_candidates_and_unknown_complex_warning(self) -> None:
        """Known bounded candidates use heuristics and complex warning uses Web AI."""
        report = resolve_warning_audit(self.audit_text)
        self.assertEqual(report.total_findings, 4)
        self.assertEqual(report.heuristic_count, 2)
        self.assertEqual(report.web_ai_count, 1)
        self.assertEqual(report.meta_count, 1)
        self.assertEqual(
            [item.route for item in report.decisions],
            [ROUTE_HEURISTIC, ROUTE_WEB_AI, ROUTE_HEURISTIC, ROUTE_META],
        )

    def test_report_is_not_reparsed_as_new_warning_input(self) -> None:
        """Formatted resolver output does not create recursive warning findings."""
        report = resolve_warning_audit(self.audit_text)
        rendered = format_warning_resolution_report(report)
        self.assertIn("WARNING HEURISTIC RESOLVER REPORT", rendered)
        self.assertIn("WEB AI HANDOFF", rendered)
        self.assertEqual(resolve_warning_audit(rendered).total_findings, 0)


if __name__ == "__main__":
    unittest.main()
