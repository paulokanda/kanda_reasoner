# project-path: tools/engineering_diagnostics_wave2qb_architecture_gate.py
"""Architecture non-regression gate for Engineering Diagnostics Wave 2Q-B."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2qa_architecture_gate import (
    validate_engineering_diagnostics_wave2qa_architecture_non_regression,
)

__all__ = ["validate_engineering_diagnostics_wave2qb_architecture_non_regression"]

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/engineering_diagnostics/collectors/shadow_collector.py",
        "kanda_reasoner_app/engineering_diagnostics/collectors/shadow_normalizer.py",
        "kanda_reasoner_app/engineering_diagnostics/collectors/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics/shadow_relational_models.py",
        "kanda_reasoner_app/engineering_diagnostics/shadow_relational_grouping.py",
        "kanda_reasoner_app/engineering_diagnostics/grouping.py",
        "kanda_reasoner_app/engineering_diagnostics/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/shadow_controller.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/wave2qb_validation.py",
        "tests/test_engineering_diagnostics_wave2qb.py",
        "tests/test_engineering_diagnostics_wave2qb_gui_scale.py",
        "tools/engineering_diagnostics_wave2qb_architecture_gate.py",
        "tools/engineering_diagnostics_wave2qb_public_boundary_gate.py",
        "tools/engineering_diagnostics_wave2qb_validation_runtime.py",
        "tools/validate_engineering_diagnostics_wave2qb_v1.py",
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


def validate_engineering_diagnostics_wave2qb_architecture_non_regression(
    output: str,
) -> None:
    """Reuse frozen Wave 2Q-A baseline and reject every owned-path issue."""
    validate_engineering_diagnostics_wave2qa_architecture_non_regression(output)
    issues = _issues(output)
    touched = sorted(issue for issue in issues if issue[2] in _TOUCHED_PATHS)
    _require(not touched, "WAVE2QB_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched))
    targeted = sorted(
        issue
        for issue in issues
        if issue[1] in {"DUPLICATE_PUBLIC_SYMBOL", "SYMBOL_SHADOWING", "PRIVATE_REACH_IN"}
        and issue[2] in _TOUCHED_PATHS
    )
    _require(not targeted, "WAVE2QB_TARGETED_ARCHITECTURE_ISSUES:" + repr(targeted))
    print("WAVE2QB ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2QB NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2QB TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2QB DUPLICATE PUBLIC SYMBOLS: 0")
    print("WAVE2QB SYMBOL SHADOWING ISSUES: 0")
    print("WAVE2QB PRIVATE REACH-IN ISSUES: 0")
    print("WAVE2QB ARCHITECTURE NON-REGRESSION: PASS")
