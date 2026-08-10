# project-path: tools/engineering_diagnostics_wave2oc_architecture_gate.py
"""Architecture non-regression gate for Engineering Diagnostics Wave 2O-C."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2ob_architecture_gate import (
    validate_engineering_diagnostics_wave2ob_architecture_non_regression,
)

__all__ = [
    "validate_engineering_diagnostics_wave2oc_architecture_non_regression"
]

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/engineering_diagnostics/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py",
        "kanda_reasoner_app/engineering_diagnostics/fingerprinting.py",
        "kanda_reasoner_app/engineering_diagnostics/collectors/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics/collectors/ruff_collector.py",
        "kanda_reasoner_app/engineering_diagnostics/collectors/ruff_normalizer.py",
        "kanda_reasoner_app/engineering_diagnostics/rules/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics/rules/ruff_rule_registry.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/diagnostic_table_model.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
        "tests/test_engineering_diagnostics_wave2oc.py",
        "tools/engineering_diagnostics_wave2oc_architecture_gate.py",
        "tools/engineering_diagnostics_wave2oc_public_boundary_gate.py",
        "tools/validate_engineering_diagnostics_wave2oc_v1.py",
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


def validate_engineering_diagnostics_wave2oc_architecture_non_regression(
    output: str,
) -> None:
    """Reuse frozen baselines and reject every Wave 2O-C touched-path issue."""
    validate_engineering_diagnostics_wave2ob_architecture_non_regression(output)
    issues = _issues(output)
    touched = sorted(issue for issue in issues if issue[2] in _TOUCHED_PATHS)
    _require(not touched, "WAVE2OC_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched))
    print("WAVE2OC ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2OC NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2OC TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2OC ARCHITECTURE NON-REGRESSION: PASS")
