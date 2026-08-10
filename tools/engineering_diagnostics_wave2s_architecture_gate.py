# project-path: tools/engineering_diagnostics_wave2s_architecture_gate.py
"""Architecture non-regression gate for Engineering Diagnostics Wave 2S."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2r_architecture_gate import (
    validate_engineering_diagnostics_wave2r_architecture_non_regression,
)

__all__ = ["validate_engineering_diagnostics_wave2s_architecture_non_regression"]

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/engineering_diagnostics/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics/remediation.py",
        "kanda_reasoner_app/engineering_diagnostics/remediation_models.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/finding_view_builder.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/models.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/run_summary.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/table_columns.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/wave2s_validation.py",
        "tests/test_engineering_diagnostics_wave2s.py",
        "tests/test_engineering_diagnostics_wave2s_gui_scale.py",
        "tools/engineering_diagnostics_wave2s_architecture_gate.py",
        "tools/engineering_diagnostics_wave2s_public_boundary_gate.py",
        "tools/engineering_diagnostics_wave2s_validation_runtime.py",
        "tools/validate_engineering_diagnostics_wave2s_v1.py",
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


def validate_engineering_diagnostics_wave2s_architecture_non_regression(
    output: str,
) -> None:
    """Reuse frozen Wave 2R baseline and reject every Wave 2S path issue."""
    validate_engineering_diagnostics_wave2r_architecture_non_regression(output)
    issues = _issues(output)
    touched = sorted(issue for issue in issues if issue[2] in _TOUCHED_PATHS)
    _require(not touched, "WAVE2S_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched))
    targeted = sorted(
        issue
        for issue in issues
        if issue[1]
        in {
            "DUPLICATE_PUBLIC_SYMBOL",
            "SYMBOL_SHADOWING",
            "PRIVATE_REACH_IN",
            "IMPORT_HEAVINESS_STARTUP",
            "MIXED_RESPONSIBILITY",
        }
        and issue[2] in _TOUCHED_PATHS
    )
    _require(not targeted, "WAVE2S_TARGETED_ARCHITECTURE_ISSUES:" + repr(targeted))
    print("WAVE2S ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2S NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2S TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2S DUPLICATE PUBLIC SYMBOLS: 0")
    print("WAVE2S SYMBOL SHADOWING ISSUES: 0")
    print("WAVE2S PRIVATE REACH-IN ISSUES: 0")
    print("WAVE2S ARCHITECTURE NON-REGRESSION: PASS")
