# project-path: tools/engineering_diagnostics_wave2t_architecture_gate.py
"""Architecture non-regression gate for Engineering Diagnostics Wave 2T."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2s_architecture_gate import (
    validate_engineering_diagnostics_wave2s_architecture_non_regression,
)

__all__ = ["validate_engineering_diagnostics_wave2t_architecture_non_regression"]

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/engineering_diagnostics_gui/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/_navigation_ui.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/full_audit_drillthrough_ui.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/navigation.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/navigation_models.py",
        "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py",
        "kanda_reasoner_app/manage_architecture/full_audit_diagnostics_drillthrough.py",
        "tests/test_engineering_diagnostics_wave2t.py",
        "tests/test_engineering_diagnostics_wave2t_gui_scale.py",
        "tools/engineering_diagnostics_wave2t_architecture_gate.py",
        "tools/engineering_diagnostics_wave2t_gui_validation.py",
        "tools/engineering_diagnostics_wave2t_public_boundary_gate.py",
        "tools/engineering_diagnostics_wave2t_validation_runtime.py",
        "tools/validate_engineering_diagnostics_wave2t_v1.py",
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


def validate_engineering_diagnostics_wave2t_architecture_non_regression(
    output: str,
) -> None:
    """Reuse the frozen Wave 2S baseline and reject Wave 2T path issues."""
    validate_engineering_diagnostics_wave2s_architecture_non_regression(output)
    issues = _issues(output)
    touched = sorted(issue for issue in issues if issue[2] in _TOUCHED_PATHS)
    _require(not touched, "WAVE2T_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched))
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
    _require(not targeted, "WAVE2T_TARGETED_ARCHITECTURE_ISSUES:" + repr(targeted))
    print("WAVE2T ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2T NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2T TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2T DUPLICATE PUBLIC SYMBOLS: 0")
    print("WAVE2T SYMBOL SHADOWING ISSUES: 0")
    print("WAVE2T PRIVATE REACH-IN ISSUES: 0")
    print("WAVE2T ARCHITECTURE NON-REGRESSION: PASS")
