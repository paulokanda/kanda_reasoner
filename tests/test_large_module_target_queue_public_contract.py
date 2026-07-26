"""Public contract tests for the Large Module AST target queue helpers."""
from __future__ import annotations

from kanda_reasoner_app.manage_architecture.large_module_target_queue import format_target_counter, parse_module_too_large_findings, LargeModuleTarget


def test_parse_module_too_large_findings_sorts_descending_and_filters_resolved() -> None:
    text = """
WARNING MODULE_TOO_LARGE             small.py :: Module has 500 lines; split threshold is 500.
WARNING MODULE_TOO_LARGE             medium.py :: Module has 835 lines; split threshold is 500.
WARNING MODULE_TOO_LARGE             huge.py :: Module has 1438 lines; split threshold is 500.
WARNING MIXED_RESPONSIBILITY_FILE    other.py :: ignored
"""
    targets = parse_module_too_large_findings(text)
    assert targets == [
        LargeModuleTarget(path="huge.py", line_count=1438),
        LargeModuleTarget(path="medium.py", line_count=835),
    ]


def test_format_target_counter_reports_position_and_lines() -> None:
    targets = [LargeModuleTarget(path="a.py", line_count=900), LargeModuleTarget(path="b.py", line_count=700)]
    assert format_target_counter(targets, 1) == "2/2 | 700 lines"
    assert format_target_counter([], -1) == "0 large modules"
