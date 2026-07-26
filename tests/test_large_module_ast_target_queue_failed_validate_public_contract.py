"""Public contract tests for AST target population from failed Validate output."""
from __future__ import annotations

from kanda_reasoner_app.manage_architecture.large_module_target_queue import parse_module_too_large_findings


def test_module_too_large_findings_are_parsed_even_when_validate_failed() -> None:
    output = """
ARCHITECTURE VALIDATION SUMMARY
Total issues: 106 | Errors: 1 | Warnings: 105 | Other: 0
DETAILS
ERROR   DEPRECATED_VARIANT_STILL_REFERENCED kanda_reasoner_app/error_memory_gui/_draft_deletion.py :: Stale/deprecated variant.
WARNING MODULE_TOO_LARGE             kanda_reasoner_app/error_memory_gui/error_memory_tab.py :: Module has 835 lines; split threshold is 500.
WARNING MODULE_TOO_LARGE             kanda_reasoner_app/freeze_hint_intake/contract.py :: Module has 1848 lines; split threshold is 500.
[finished] mode=validate exit_code=1
"""
    targets = parse_module_too_large_findings(output)
    assert [target.path for target in targets] == [
        "kanda_reasoner_app/freeze_hint_intake/contract.py",
        "kanda_reasoner_app/error_memory_gui/error_memory_tab.py",
    ]
    assert [target.line_count for target in targets] == [1848, 835]
