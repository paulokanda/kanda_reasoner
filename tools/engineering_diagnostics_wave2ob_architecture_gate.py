# project-path: tools/engineering_diagnostics_wave2ob_architecture_gate.py
"""Architecture non-regression gate for Engineering Diagnostics GUI Wave 2O-B."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2oa_architecture_gate import (
    validate_engineering_diagnostics_wave2oa_architecture_non_regression,
)

__all__ = [
    "validate_engineering_diagnostics_wave2ob_architecture_non_regression"
]

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/engineering_diagnostics_gui/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/bom_provider.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/models.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/source_identity.py",
        "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py",
        "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py",
        "tests/test_engineering_diagnostics_wave2ob.py",
        "tools/engineering_diagnostics_wave2ob_architecture_gate.py",
        "tools/engineering_diagnostics_wave2ob_public_boundary_gate.py",
        "tools/validate_engineering_diagnostics_wave2ob_v1.py",
    }
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _issues(output: str) -> tuple[tuple[str, str, str], ...]:
    found: list[tuple[str, str, str]] = []
    for line in output.splitlines():
        match = re.match(r"^(WARNING|ERROR|OTHER)\s+(\S+)\s+(.*?)\s+::", line)
        if match:
            severity, code, path = match.groups()
            found.append((severity, code, path.strip().replace("\\", "/")))
    return tuple(found)


def validate_engineering_diagnostics_wave2ob_architecture_non_regression(
    output: str,
) -> None:
    """Reuse frozen 2O-A baseline and reject every touched-path issue."""
    validate_engineering_diagnostics_wave2oa_architecture_non_regression(output)
    issues = _issues(output)
    touched = sorted(issue for issue in issues if issue[2] in _TOUCHED_PATHS)
    _require(not touched, "WAVE2OB_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched))
    print("WAVE2OB ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2OB NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2OB TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2OB ARCHITECTURE NON-REGRESSION: PASS")
