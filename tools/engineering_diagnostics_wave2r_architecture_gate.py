# project-path: tools/engineering_diagnostics_wave2r_architecture_gate.py
"""Architecture non-regression gate for Engineering Diagnostics Wave 2R."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2qb_architecture_gate import (
    validate_engineering_diagnostics_wave2qb_architecture_non_regression,
)

__all__ = ["validate_engineering_diagnostics_wave2r_architecture_non_regression"]

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/engineering_diagnostics/lifecycle_models.py",
        "kanda_reasoner_app/engineering_diagnostics/lifecycle.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_schema.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_state.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_ops.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_run_ops.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_database.py",
        "kanda_reasoner_app/engineering_diagnostics/store.py",
        "kanda_reasoner_app/engineering_diagnostics/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/lifecycle_ui.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/finding_view_builder.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/run_summary.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/models.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/table_columns.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/wave2r_validation.py",
        "tests/test_engineering_diagnostics_wave2r.py",
        "tests/test_engineering_diagnostics_wave2r_gui_scale.py",
        "tools/engineering_diagnostics_wave2r_architecture_gate.py",
        "tools/engineering_diagnostics_wave2r_public_boundary_gate.py",
        "tools/engineering_diagnostics_wave2r_validation_runtime.py",
        "tools/validate_engineering_diagnostics_wave2r_v1.py",
    }
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _issues(output: str) -> tuple[tuple[str, str, str], ...]:
    values: list[tuple[str, str, str]] = []
    for line in output.splitlines():
        match = re.match(r"^(WARNING|ERROR|OTHER)\s+(\S+)\s+(.*?)\s+::", line)
        if match:
            severity, code, path = match.groups()
            values.append((severity, code, path.strip().replace("\\", "/")))
    return tuple(values)


def validate_engineering_diagnostics_wave2r_architecture_non_regression(
    output: str,
) -> None:
    """Reuse frozen Wave 2Q-B baseline and reject every Wave 2R path issue."""
    validate_engineering_diagnostics_wave2qb_architecture_non_regression(output)
    issues = _issues(output)
    touched = sorted(issue for issue in issues if issue[2] in _TOUCHED_PATHS)
    _require(not touched, "WAVE2R_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched))
    targeted = sorted(
        issue
        for issue in issues
        if issue[1] in {
            "DUPLICATE_PUBLIC_SYMBOL",
            "SYMBOL_SHADOWING",
            "PRIVATE_REACH_IN",
            "IMPORT_HEAVINESS_STARTUP",
            "MIXED_RESPONSIBILITY",
        }
        and issue[2] in _TOUCHED_PATHS
    )
    _require(not targeted, "WAVE2R_TARGETED_ARCHITECTURE_ISSUES:" + repr(targeted))
    print("WAVE2R ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2R NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2R TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2R DUPLICATE PUBLIC SYMBOLS: 0")
    print("WAVE2R SYMBOL SHADOWING ISSUES: 0")
    print("WAVE2R PRIVATE REACH-IN ISSUES: 0")
    print("WAVE2R ARCHITECTURE NON-REGRESSION: PASS")
