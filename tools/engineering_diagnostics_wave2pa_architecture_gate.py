# project-path: tools/engineering_diagnostics_wave2pa_architecture_gate.py
"""Architecture non-regression gate for Engineering Diagnostics Wave 2P-A."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2od_architecture_gate import (
    validate_engineering_diagnostics_wave2od_architecture_non_regression,
)

__all__ = [
    "validate_engineering_diagnostics_wave2pa_architecture_non_regression"
]

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/engineering_diagnostics/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics/enrichment.py",
        "kanda_reasoner_app/engineering_diagnostics/enrichment_models.py",
        "kanda_reasoner_app/engineering_diagnostics/frozen_path_enrichment.py",
        "kanda_reasoner_app/engineering_diagnostics/scope_enrichment.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/models.py",
        "tests/test_engineering_diagnostics_wave2pa.py",
        "tools/engineering_diagnostics_wave2pa_architecture_gate.py",
        "tools/engineering_diagnostics_wave2pa_public_boundary_gate.py",
        "tools/validate_engineering_diagnostics_wave2pa_v1.py",
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


def validate_engineering_diagnostics_wave2pa_architecture_non_regression(
    output: str,
) -> None:
    """Reuse frozen Wave 2O-D baselines and reject touched-path issues."""
    validate_engineering_diagnostics_wave2od_architecture_non_regression(output)
    issues = _issues(output)
    touched = sorted(issue for issue in issues if issue[2] in _TOUCHED_PATHS)
    _require(not touched, "WAVE2PA_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched))
    print("WAVE2PA ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2PA NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2PA TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2PA ARCHITECTURE NON-REGRESSION: PASS")
