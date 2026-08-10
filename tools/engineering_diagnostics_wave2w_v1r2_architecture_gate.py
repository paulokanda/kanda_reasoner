# project-path: tools/engineering_diagnostics_wave2w_v1r2_architecture_gate.py
"""Architecture non-regression gate for Wave 2W v1r2 runtime correction."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2w_architecture_gate import (
    validate_engineering_diagnostics_wave2w_architecture_non_regression,
)

__all__ = ["validate_engineering_diagnostics_wave2w_v1r2_architecture"]

_TOUCHED = frozenset(
    {
        "kanda_reasoner_app/safety_suite_cli/__main__.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/bom_provider.py",
        "kanda_reasoner_app/engineering_diagnostics/collectors/ruff_collector.py",
        "kanda_reasoner_app/source_hygiene/shadow_audit.py",
        "kanda_reasoner_app/engineering_diagnostics/collectors/shadow_normalizer.py",
        "tests/test_engineering_diagnostics_wave2w_runtime_corrections.py",
        "tools/engineering_diagnostics_wave2w_v1r2_validation_runtime.py",
        "tools/engineering_diagnostics_wave2w_v1r2_architecture_gate.py",
        "tools/engineering_diagnostics_wave2w_v1r2_public_boundary_gate.py",
        "tools/validate_engineering_diagnostics_wave2w_v1r2.py",
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


def validate_engineering_diagnostics_wave2w_v1r2_architecture(output: str) -> None:
    validate_engineering_diagnostics_wave2w_architecture_non_regression(output)
    touched = sorted(issue for issue in _issues(output) if issue[2] in _TOUCHED)
    _require(not touched, "WAVE2W_V1R2_TOUCHED_ARCHITECTURE_ISSUES:" + repr(touched))
    print("WAVE2W V1R2 NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2W V1R2 TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2W V1R2 ARCHITECTURE NON-REGRESSION: PASS")
