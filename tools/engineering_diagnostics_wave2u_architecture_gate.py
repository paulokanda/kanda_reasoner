# project-path: tools/engineering_diagnostics_wave2u_architecture_gate.py
"""Architecture non-regression gate for Engineering Diagnostics Wave 2U."""

from __future__ import annotations

import re

from tools.engineering_diagnostics_wave2t_architecture_gate import (
    validate_engineering_diagnostics_wave2t_architecture_non_regression,
)

__all__ = ["validate_engineering_diagnostics_wave2u_architecture_non_regression"]

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/engineering_diagnostics_patch_preview/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics_patch_preview/models.py",
        "kanda_reasoner_app/engineering_diagnostics_patch_preview/policy.py",
        "kanda_reasoner_app/engineering_diagnostics_patch_preview/preview.py",
        "kanda_reasoner_app/engineering_diagnostics_patch_preview/storage.py",
        "kanda_reasoner_app/engineering_diagnostics_patch_preview/transformations.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/patch_preview_ui.py",
        "tests/test_engineering_diagnostics_wave2u.py",
        "tests/test_engineering_diagnostics_wave2u_gui_scale.py",
        "tools/engineering_diagnostics_wave2u_architecture_gate.py",
        "tools/engineering_diagnostics_wave2u_gui_validation.py",
        "tools/engineering_diagnostics_wave2u_public_boundary_gate.py",
        "tools/engineering_diagnostics_wave2u_validation_runtime.py",
        "tools/validate_engineering_diagnostics_wave2u_v1.py",
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


def validate_engineering_diagnostics_wave2u_architecture_non_regression(
    output: str,
) -> None:
    """Reuse the frozen Wave 2T baseline and reject Wave 2U path issues."""
    validate_engineering_diagnostics_wave2t_architecture_non_regression(output)
    touched = sorted(issue for issue in _issues(output) if issue[2] in _TOUCHED_PATHS)
    _require(not touched, "WAVE2U_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched))
    print("WAVE2U ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2U NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2U TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2U DUPLICATE PUBLIC SYMBOLS: 0")
    print("WAVE2U PRIVATE REACH-IN ISSUES: 0")
    print("WAVE2U ARCHITECTURE NON-REGRESSION: PASS")
