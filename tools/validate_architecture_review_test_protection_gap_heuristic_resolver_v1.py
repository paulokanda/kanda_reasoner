# project-path: tools/validate_architecture_review_test_protection_gap_heuristic_resolver_v1.py
"""Validate non-blocking TEST_PROTECTION_GAP resolver sonar integration."""

from __future__ import annotations

import ast
import importlib.util
import py_compile
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-warning-heuristic-resolver-async-sonar-v1"

__all__ = ["main"]
PROJECT_ROOT = Path(__file__).resolve().parents[1]

PRODUCTION_PATHS = (
    Path("kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py"),
    Path("kanda_reasoner_app/manage_architecture/warning_test_protection_gap_resolver.py"),
    Path("kanda_reasoner_app/manage_architecture/warning_test_protection_gap_formatting.py"),
    Path("kanda_reasoner_app/manage_architecture/warning_test_protection_family_evidence.py"),
    Path("kanda_reasoner_app/manage_architecture/warning_heuristic_resolver_qt_worker.py"),
    Path("kanda_reasoner_app/manage_architecture/warning_heuristic_resolver_qt_controller.py"),
    Path("kanda_reasoner_app/manage_architecture/warning_heuristic_resolver_sonar.py"),
)
TEST_PATH = Path("tests/test_warning_test_protection_gap_resolver.py")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_python_syntax() -> None:
    for relative in (*PRODUCTION_PATHS, TEST_PATH):
        py_compile.compile(str(PROJECT_ROOT / relative), doraise=True)
    print("PYTHON_SYNTAX: PASS")


def validate_module_size_gate() -> None:
    for relative in PRODUCTION_PATHS:
        line_count = len((PROJECT_ROOT / relative).read_text(encoding="utf-8").splitlines())
        require(line_count <= 500, f"module exceeds 500 physical lines: {relative}")
    print("MODULE_SIZE_GATE: PASS")


def validate_gui_confirmation_gate() -> None:
    path = PROJECT_ROOT / PRODUCTION_PATHS[0]
    text = path.read_text(encoding="utf-8")
    required = (
        "QMessageBox.question",
        "QMessageBox.Yes | QMessageBox.No",
        "QMessageBox.No",
        "apply_test_protection_gap_plan",
        "controller.start(root_path, test_gap_findings)",
        "start_warning_resolver_sonar",
        "update_warning_resolver_sonar",
        "format_test_protection_gap_plan",
    )
    for marker in required:
        require(marker in text, f"GUI confirmation marker missing: {marker}")
    require(
        "build_test_protection_gap_plan(" not in text,
        "heavy specialist plan build still runs directly in GUI action module",
    )
    require(
        text.index("QMessageBox.question") < text.index("apply_result = apply_test_protection_gap_plan"),
        "apply call is not guarded behind explicit GUI confirmation",
    )
    print("TEST_PROTECTION_GAP_GUI_CONFIRMATION_GATE: PASS")


def validate_focused_test_protection_imports() -> None:
    path = PROJECT_ROOT / TEST_PATH
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imported_modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module)

    required_modules = {
        "kanda_reasoner_app.manage_architecture.warning_test_protection_gap_resolver",
        "kanda_reasoner_app.manage_architecture.warning_test_protection_gap_formatting",
        "kanda_reasoner_app.manage_architecture.warning_test_protection_family_evidence",
        "kanda_reasoner_app.manage_architecture.warning_heuristic_resolver_qt_worker",
        "kanda_reasoner_app.manage_architecture.warning_heuristic_resolver_qt_controller",
        "kanda_reasoner_app.manage_architecture.warning_heuristic_resolver_sonar",
    }
    missing = sorted(required_modules - imported_modules)
    require(not missing, "focused direct test-protection imports missing: " + ", ".join(missing))
    print("FOCUSED_TEST_PROTECTION_IMPORTS: PASS")


def validate_specialist_is_conservative() -> None:
    path = PROJECT_ROOT / PRODUCTION_PATHS[1]
    text = path.read_text(encoding="utf-8")
    required = (
        "ACTION_LINK_EXISTING_TEST",
        "ACTION_WEB_AI",
        "TEST SOURCE FRESHNESS CONFLICT",
        "TYPE_CHECKING",
        "imports_public_symbol_from_ancestor_facade",
        "warning_heuristic_resolver",
        "test_protection_gap",
    )
    for marker in required:
        require(marker in text, f"conservative resolver marker missing: {marker}")
    tree = ast.parse(text, filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            require(
                node.func.id not in {"eval", "exec"},
                "unexpected dynamic execution primitive in resolver: " + node.func.id,
            )
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            require(
                not (
                    node.func.value.id == "subprocess"
                    and node.func.attr in {"run", "Popen"}
                ),
                "unexpected subprocess execution primitive in resolver",
            )
    family_path = PROJECT_ROOT / PRODUCTION_PATHS[3]
    family_text = family_path.read_text(encoding="utf-8")
    for marker in (
        "imports_source_package_sibling",
        "test_name_matches_feature_family",
        "references_source_public_symbol",
        "strong_existing_test_family",
    ):
        require(marker in family_text, f"family evidence marker missing: {marker}")
    print("TEST_PROTECTION_GAP_CONSERVATIVE_POLICY: PASS")



def validate_async_qthread_and_sonar_contract() -> None:
    worker_text = (PROJECT_ROOT / PRODUCTION_PATHS[4]).read_text(encoding="utf-8")
    controller_text = (PROJECT_ROOT / PRODUCTION_PATHS[5]).read_text(encoding="utf-8")
    sonar_text = (PROJECT_ROOT / PRODUCTION_PATHS[6]).read_text(encoding="utf-8")
    resolver_text = (PROJECT_ROOT / PRODUCTION_PATHS[1]).read_text(encoding="utf-8")
    for marker in ("QObject", "Signal", "Slot", "progress_callback=self._emit_progress"):
        require(marker in worker_text, f"worker async marker missing: {marker}")
    for marker in ("QThread", "worker.moveToThread(thread)", "thread.start()", "if self._running"):
        require(marker in controller_text, f"controller QThread marker missing: {marker}")
    for marker in (
        "GreenSonarActivityMonitor",
        "Resolver: total {total} | to go {to_go}",
        "done {done} | Web AI {web_ai} (AI necessary)",
        "AI necessary: ",
    ):
        require(marker in sonar_text, f"sonar progress marker missing: {marker}")
    for marker in ("progress_callback", "total - len(decisions)", "decision.action"):
        require(marker in resolver_text, f"resolver progress marker missing: {marker}")
    print("WARNING_RESOLVER_ASYNC_QTHREAD: PASS")
    print("WARNING_RESOLVER_SONAR_COUNTERS: PASS")

def validate_focused_tests() -> None:
    path = PROJECT_ROOT / TEST_PATH
    spec = importlib.util.spec_from_file_location(
        "test_warning_test_protection_gap_resolver",
        path,
    )
    require(spec is not None and spec.loader is not None, "focused test module could not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    test_names = (
        "test_plan_links_only_existing_related_test",
        "test_apply_adds_type_checking_link_and_reaudit_detects_direct_import",
        "test_unrelated_test_routes_to_web_ai",
        "test_apply_blocks_stale_test_source",
        "test_family_evidence_links_existing_sibling_test_family",
        "test_sibling_import_without_feature_name_match_stays_web_ai",
        "test_broad_family_name_plus_sibling_import_stays_web_ai",
        "test_exact_source_stem_test_plus_sibling_import_is_safe",
        "test_progress_callback_reports_total_to_go_done_and_web_ai",
        "test_async_worker_controller_and_sonar_have_direct_test_imports",
    )
    for name in test_names:
        getattr(module, name)()
    print("TEST_PROTECTION_GAP_FOCUSED_TESTS: PASS")


def validate_phase1_output_non_reparse_regression() -> None:
    from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import (
        format_warning_resolution_report,
        parse_warning_findings,
        resolve_warning_audit,
    )

    sample = (
        "WARNING TEST_PROTECTION_GAP          sample_pkg/owner.py :: "
        "Important active module has no direct test module import.\n"
        "WARNING UNKNOWN_WARNING_CODE         sample_pkg/other.py :: "
        "Needs contextual review.\n"
    )
    report = resolve_warning_audit(sample)
    rendered = format_warning_resolution_report(report)
    require(report.heuristic_count == 1, "Phase 1 heuristic routing regressed")
    require(report.web_ai_count == 1, "Phase 1 Web AI fallback regressed")
    require(
        not parse_warning_findings(rendered),
        "resolver output can be reparsed as new Architecture Review warnings",
    )
    print("PHASE1_ROUTING_AND_NO_REPARSE_REGRESSION: PASS")


def main() -> int:
    validate_python_syntax()
    validate_module_size_gate()
    validate_gui_confirmation_gate()
    validate_focused_test_protection_imports()
    validate_specialist_is_conservative()
    validate_async_qthread_and_sonar_contract()
    validate_focused_tests()
    validate_phase1_output_non_reparse_regression()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
