# project-path: tools/validate_architecture_review_warning_heuristic_resolver_v1.py
"""Validate the Architecture Review Warning Heuristic Resolver feature."""

from __future__ import annotations

import ast
import py_compile
from pathlib import Path
import sys

__all__ = [
    "main",
]

FEATURE_ID = "architecture-review-warning-heuristic-resolver-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAX_CODE_LINES = 500

RESOLVER_PATH = Path(
    "kanda_reasoner_app/manage_architecture/warning_heuristic_resolver.py"
)
ACTIONS_PATH = Path(
    "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py"
)
SUBTABS_PATH = Path(
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
)
TEST_PATH = Path(
    "tests/test_architecture_review_warning_heuristic_resolver_contract.py"
)

TOUCHED_SOURCE_FILES = [RESOLVER_PATH, ACTIONS_PATH, SUBTABS_PATH]


def _fail(message: str) -> int:
    """Print a focused validation failure and return a nonzero status."""
    print(f"VALIDATION FAIL: {FEATURE_ID}")
    print(message)
    return 1


def _read(relative_path: Path) -> str:
    """Read one project file as UTF-8 text."""
    path = PROJECT_ROOT / relative_path
    if not path.is_file():
        raise AssertionError(f"Missing expected file: {relative_path.as_posix()}")
    return path.read_text(encoding="utf-8")


def _validate_python_sources() -> None:
    """Compile and line-count every touched production module."""
    for relative_path in TOUCHED_SOURCE_FILES:
        text = _read(relative_path)
        ast.parse(text, filename=relative_path.as_posix())
        py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)
        line_count = len(text.splitlines())
        if line_count > MAX_CODE_LINES:
            raise AssertionError(
                f"{relative_path.as_posix()} has {line_count} lines; maximum is {MAX_CODE_LINES}"
            )
    test_text = _read(TEST_PATH)
    ast.parse(test_text, filename=TEST_PATH.as_posix())
    py_compile.compile(str(PROJECT_ROOT / TEST_PATH), doraise=True)


def _validate_direct_test_protection_link() -> None:
    """Ensure the new public resolver module has a direct focused test import."""
    text = _read(TEST_PATH)
    required = (
        "from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import",
        "WarningHeuristicResolverContractTests",
    )
    for fragment in required:
        if fragment not in text:
            raise AssertionError("Missing direct test-protection fragment: " + fragment)


def _validate_no_mutation_primitive() -> None:
    """Ensure the phase-1 resolver cannot write project source."""
    text = _read(RESOLVER_PATH)
    forbidden = (
        ".write_text(",
        ".write_bytes(",
        "shutil.copy",
        "shutil.move",
        "os.replace(",
        "subprocess.run(",
    )
    for fragment in forbidden:
        if fragment in text:
            raise AssertionError(
                "Resolver phase 1 must remain read-only; found: " + fragment
            )


def _validate_gui_wiring() -> None:
    """Ensure the button is visible and connected through the existing mixin."""
    subtabs = _read(SUBTABS_PATH)
    actions = _read(ACTIONS_PATH)
    required_subtab_fragments = (
        '"Warning Heuristic Resolver"',
        "QPushButton",
        '"architecture_review_warning_heuristic_resolver_button"',
        "window.run_warning_heuristic_resolver",
    )
    for fragment in required_subtab_fragments:
        if fragment not in subtabs:
            raise AssertionError("Missing GUI wiring fragment: " + fragment)

    required_action_fragments = (
        "def run_warning_heuristic_resolver(self) -> None:",
        "resolve_warning_audit(audit_text)",
        "format_warning_resolution_report(report)",
        "self._output.appendPlainText",
    )
    for fragment in required_action_fragments:
        if fragment not in actions:
            raise AssertionError("Missing action wiring fragment: " + fragment)


def _validate_runtime_routing() -> None:
    """Run deterministic parsing, routing, formatting, and recursion checks."""
    project_root_text = str(PROJECT_ROOT)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)

    from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import (
        ROUTE_HEURISTIC,
        ROUTE_META,
        ROUTE_WEB_AI,
        format_warning_resolution_report,
        resolve_warning_audit,
    )

    audit = "\n".join(
        [
            "INFO startup line",
            "WARNING TEST_PROTECTION_GAP          pkg/service.py :: Important active module has no direct test module import.",
            "WARNING SIDE_EFFECT_ON_IMPORT       pkg/runtime.py :: Module may perform work during import.",
            "WARNING MISSING_DOCSTRING           pkg/plain.py :: Missing module docstring.",
            "WARNING TEST_PROTECTION_GAP          . :: Additional test-protection gaps suppressed after 80 findings.",
        ]
    )
    report = resolve_warning_audit(audit)
    if report.total_findings != 4:
        raise AssertionError("Expected four parsed warnings")
    if report.heuristic_count != 2:
        raise AssertionError("Expected two heuristic-routed warnings")
    if report.web_ai_count != 1:
        raise AssertionError("Expected one Web AI-routed warning")
    if report.meta_count != 1:
        raise AssertionError("Expected one suppression notice")

    routes = [item.route for item in report.decisions]
    expected = [ROUTE_HEURISTIC, ROUTE_WEB_AI, ROUTE_HEURISTIC, ROUTE_META]
    if routes != expected:
        raise AssertionError(f"Unexpected route sequence: {routes}")

    rendered = format_warning_resolution_report(report)
    required_markers = (
        "WARNING HEURISTIC RESOLVER REPORT",
        "Heuristic queue: 2",
        "Web AI queue: 1",
        "HEURISTIC QUEUE",
        "WEB AI QUEUE",
        "WEB AI HANDOFF",
        "TEST_PROTECTION_GAP",
        "SIDE_EFFECT_ON_IMPORT",
    )
    for marker in required_markers:
        if marker not in rendered:
            raise AssertionError("Formatted report missing marker: " + marker)

    reparsed = resolve_warning_audit(rendered)
    if reparsed.total_findings != 0:
        raise AssertionError(
            "Resolver output must not be reparsed as new Architecture WARNING lines"
        )


def main() -> int:
    """Run focused validation for the Warning Heuristic Resolver feature."""
    try:
        _validate_python_sources()
        _validate_direct_test_protection_link()
        _validate_no_mutation_primitive()
        _validate_gui_wiring()
        _validate_runtime_routing()
    except Exception as exc:
        return _fail(str(exc))

    print("WARNING_HEURISTIC_RESOLVER_CORE: PASS")
    print("WARNING_HEURISTIC_RESOLVER_GUI_WIRING: PASS")
    print("WARNING_HEURISTIC_RESOLVER_READ_ONLY_PHASE1: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
