# project-path: tools/engineering_diagnostics_wave2oa_architecture_gate.py
"""Architecture gate for Engineering Diagnostics Wave 2O-A."""

from __future__ import annotations

import re

from tools.reasoner_symbol_atlas_wave2n_architecture_gate import (
    validate_architecture_non_regression,
)

__all__ = ["validate_engineering_diagnostics_wave2oa_architecture_non_regression"]

_TOUCHED_PATHS = frozenset(
    {
        "kanda_reasoner_app/engineering_diagnostics/__init__.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py",
        "kanda_reasoner_app/engineering_diagnostics/_store_database.py",
        "kanda_reasoner_app/engineering_diagnostics/baseline.py",
        "kanda_reasoner_app/engineering_diagnostics/bom_adapter.py",
        "kanda_reasoner_app/engineering_diagnostics/fingerprinting.py",
        "kanda_reasoner_app/engineering_diagnostics/models.py",
        "kanda_reasoner_app/engineering_diagnostics/paths.py",
        "kanda_reasoner_app/engineering_diagnostics/store.py",
        "tests/test_engineering_diagnostics_wave2oa.py",
        "tools/engineering_diagnostics_wave2oa_architecture_gate.py",
        "tools/engineering_diagnostics_wave2oa_public_boundary_gate.py",
        "tools/validate_engineering_diagnostics_wave2oa_v1.py",
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


def validate_engineering_diagnostics_wave2oa_architecture_non_regression(
    output: str,
) -> None:
    """Reuse the frozen Wave 2N baseline and protect the new owner paths."""
    validate_architecture_non_regression(output)
    issues = _issues(output)
    touched = sorted(issue for issue in issues if issue[2] in _TOUCHED_PATHS)
    _require(
        not touched,
        "WAVE2OA_TOUCHED_PATH_ARCHITECTURE_ISSUES:" + repr(touched),
    )
    print("WAVE2OA ARCHITECTURE BASELINE OWNER REUSED: PASS")
    print("WAVE2OA NEW ARCHITECTURE ISSUES: 0")
    print("WAVE2OA TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("WAVE2OA ARCHITECTURE NON-REGRESSION: PASS")
