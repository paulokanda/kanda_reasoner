# project-path: tools/engineering_diagnostics_wave2v_architecture_gate.py
"""Architecture non-regression gate for corrected Wave 2V surfaces."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2u_architecture_gate import (
    validate_engineering_diagnostics_wave2u_architecture_non_regression,
)

__all__ = ["validate_engineering_diagnostics_wave2v_architecture_non_regression"]

_TOUCHED_PATHS = frozenset(
    {
        "reasoner_tools_gui_engineering_safety_panel.py",
        "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_sonar.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_workspace.py",
        "tests/test_engineering_diagnostics_wave2v.py",
        "tests/test_engineering_diagnostics_wave2v_gui_scale.py",
        "tools/engineering_diagnostics_wave2v_architecture_gate.py",
        "tools/engineering_diagnostics_wave2v_gui_validation.py",
        "tools/engineering_diagnostics_wave2v_public_boundary_gate.py",
        "tools/engineering_diagnostics_wave2v_validation_runtime.py",
        "tools/validate_engineering_diagnostics_wave2v_v1.py",
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


def validate_engineering_diagnostics_wave2v_architecture_non_regression(
    output: str,
) -> None:
    """Reuse Wave 2U baseline and reject current corrected Wave 2V issues."""
    validate_engineering_diagnostics_wave2u_architecture_non_regression(output)
    touched = sorted(issue for issue in _issues(output) if issue[2] in _TOUCHED_PATHS)
    _require(
        not touched,
        "WAVE2V_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched),
    )
    print("WAVE2V ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2V NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2V TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2V ARCHITECTURE NON-REGRESSION: PASS")
