# project-path: tools/engineering_diagnostics_wave2qa_architecture_gate.py
"""Architecture non-regression gate for Engineering Diagnostics Wave 2Q-A."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2pb_architecture_gate import (
    validate_engineering_diagnostics_wave2pb_architecture_non_regression,
)

__all__ = [
    "validate_engineering_diagnostics_wave2qa_architecture_non_regression"
]

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/engineering_diagnostics/grouping_models.py",
        "kanda_reasoner_app/engineering_diagnostics/grouping.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_database.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_grouping_ops.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_grouping_schema.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_grouping_state.py",
        "kanda_reasoner_app/engineering_diagnostics/store.py",
        "kanda_reasoner_app/engineering_diagnostics/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/models.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/grouping_ui.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/table_columns.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/wave2qa_validation.py",
        "tests/test_engineering_diagnostics_wave2qa.py",
        "tests/test_engineering_diagnostics_wave2qa_gui_scale.py",
        "tools/engineering_diagnostics_wave2qa_architecture_gate.py",
        "tools/engineering_diagnostics_wave2qa_fixture_support.py",
        "tools/engineering_diagnostics_wave2qa_public_boundary_gate.py",
        "tools/engineering_diagnostics_wave2qa_validation_runtime.py",
        "tools/validate_engineering_diagnostics_wave2qa_v1.py",
    }
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _issues(output: str) -> tuple[tuple[str, str, str], ...]:
    result: list[tuple[str, str, str]] = []
    for line in output.splitlines():
        match = re.match(r"^(WARNING|ERROR|OTHER)\s+(\S+)\s+(.*?)\s+::", line)
        if match:
            severity, code, path = match.groups()
            result.append((severity, code, path.strip().replace("\\", "/")))
    return tuple(result)


def validate_engineering_diagnostics_wave2qa_architecture_non_regression(
    output: str,
) -> None:
    """Reuse the frozen prior-wave baseline and reject Wave 2Q-A issues."""
    validate_engineering_diagnostics_wave2pb_architecture_non_regression(output)
    issues = _issues(output)
    touched = sorted(issue for issue in issues if issue[2] in _TOUCHED_PATHS)
    _require(not touched, "WAVE2QA_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched))
    targeted_codes = {"DUPLICATE_PUBLIC_SYMBOL", "SYMBOL_SHADOWING"}
    targeted = sorted(
        issue
        for issue in issues
        if issue[1] in targeted_codes and issue[2] in _TOUCHED_PATHS
    )
    _require(not targeted, "WAVE2QA_TARGETED_ARCHITECTURE_ISSUES:" + repr(targeted))
    print("WAVE2QA ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2QA NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2QA TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2QA DUPLICATE PUBLIC SYMBOLS: 0")
    print("WAVE2QA SYMBOL SHADOWING ISSUES: 0")
    print("WAVE2QA ARCHITECTURE NON-REGRESSION: PASS")
