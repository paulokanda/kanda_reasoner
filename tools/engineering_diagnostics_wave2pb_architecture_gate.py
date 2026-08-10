# project-path: tools/engineering_diagnostics_wave2pb_architecture_gate.py
"""Architecture non-regression gate for Engineering Diagnostics Wave 2P-B."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2pa_architecture_gate import (
    validate_engineering_diagnostics_wave2pa_architecture_non_regression,
)

__all__ = [
    "validate_engineering_diagnostics_wave2pb_architecture_non_regression"
]

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/engineering_diagnostics/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics/enrichment.py",
        "kanda_reasoner_app/engineering_diagnostics/enrichment_models.py",
        "kanda_reasoner_app/engineering_diagnostics/owner_enrichment.py",
        "kanda_reasoner_app/engineering_diagnostics/owner_enrichment_models.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/models.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/owner_ui.py",
        "tests/test_engineering_diagnostics_wave2pb.py",
        "tools/engineering_diagnostics_wave2pb_architecture_gate.py",
        "tools/engineering_diagnostics_wave2pb_public_boundary_gate.py",
        "tools/validate_engineering_diagnostics_wave2pb_v1r1.py",
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


def validate_engineering_diagnostics_wave2pb_architecture_non_regression(
    output: str,
) -> None:
    """Reuse Wave 2P-A baseline ownership and reject owned-path issues."""
    validate_engineering_diagnostics_wave2pa_architecture_non_regression(output)
    issues = _issues(output)
    touched = sorted(issue for issue in issues if issue[2] in _TOUCHED_PATHS)
    _require(not touched, "WAVE2PB_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched))
    print("WAVE2PB ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2PB NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2PB TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2PB ARCHITECTURE NON-REGRESSION: PASS")
