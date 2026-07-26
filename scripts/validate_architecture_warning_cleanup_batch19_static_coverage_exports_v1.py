# project-path: scripts/validate_architecture_warning_cleanup_batch19_static_coverage_exports_v1.py
"""Focused validator for Batch 19 static coverage/export cleanup."""

from __future__ import annotations
__all__: list[str] = []


import ast
import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch19-static-coverage-exports-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

REPAIR_SCRIPT = PROJECT_ROOT / "scripts/repair_architecture_warning_cleanup_batch19_static_coverage_exports_v1.py"
TEST_FILE = PROJECT_ROOT / "tests/test_architecture_warning_cleanup_batch19_static_public_contract_coverage.py"
RETRIEVER_HELP_INIT = PROJECT_ROOT / "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/__init__.py"
ARCHITECTURE_VALIDATOR = PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture.py"

LINE_COUNT_TARGETS = (
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_finalization_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_implementation_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_patch_boundary_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_patch_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_patch_file_set_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_patch_preflight_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_proposal_review_design.py",
    "kanda_reasoner_app/routing_signal_scorer/adviser_offline/gold_expansion/gold_set_expansion_plan.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_layout_index.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_state_lifecycle.py",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/snippet_retrieval.py",
)

STATIC_IMPORT_TARGETS = (
    "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_core_mixin",
    "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_intent_section_mixin",
    "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_snippet_evidence_mixin",
    "scripts.validate_ai_response_patch_delivery_audit_runner",
    "scripts.validate_ai_response_patch_delivery_contract",
    "scripts.validate_ai_response_patch_delivery_text_helpers",
    "scripts.validate_architecture_warning_cleanup_batch17_line_count_smoke_v1",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _literal_dunder_all(path: Path) -> list[str]:
    tree = ast.parse(_read_text(path), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    value = ast.literal_eval(node.value)
                    if isinstance(value, (list, tuple)) and all(isinstance(item, str) for item in value):
                        return list(value)
    return []


def validate_py_compile() -> None:
    for path in (REPAIR_SCRIPT, TEST_FILE, Path(__file__)):
        require(path.is_file(), f"Missing validation target: {path}")
        py_compile.compile(str(path), doraise=True)


def validate_repair_script_idempotent() -> None:
    result = subprocess.run(
        [sys.executable, str(REPAIR_SCRIPT)],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, result.stdout + result.stderr)
    require(f"REPAIR OK: {FEATURE_ID}" in result.stdout, result.stdout + result.stderr)


def validate_line_count_targets() -> None:
    for relative in LINE_COUNT_TARGETS:
        path = PROJECT_ROOT / relative
        if not path.is_file():
            continue
        line_count = len(_read_text(path).splitlines())
        require(line_count <= 500, f"{relative} still has {line_count} lines")
        py_compile.compile(str(path), doraise=True)


def validate_retriever_exports_docstring() -> None:
    if not RETRIEVER_HELP_INIT.is_file():
        return
    exported = _literal_dunder_all(RETRIEVER_HELP_INIT)
    if not exported:
        return
    text = _read_text(RETRIEVER_HELP_INIT)
    desired_line = "EXPORTS: " + ", ".join(exported)
    require(desired_line in text, "reasoner_retriever_help __init__ docstring EXPORTS does not match __all__")


def validate_static_test_targets() -> None:
    text = _read_text(TEST_FILE)
    for module_name in STATIC_IMPORT_TARGETS:
        require(module_name in text, f"Static coverage target missing from Batch 19 test: {module_name}")


def validate_architecture_no_errors_or_target_mismatch() -> None:
    result = subprocess.run(
        [sys.executable, str(ARCHITECTURE_VALIDATOR), "--root", str(PROJECT_ROOT), "--validate"],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    require(result.returncode == 0, output)
    require("Errors: 0" in output, output)
    require("DUPLICATE_PUBLIC_SYMBOL" not in output, output)
    require(
        "EXPOSES_MISMATCH             kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/__init__.py" not in output,
        output,
    )


def main() -> int:
    validate_py_compile()
    validate_repair_script_idempotent()
    validate_line_count_targets()
    validate_retriever_exports_docstring()
    validate_static_test_targets()
    validate_architecture_no_errors_or_target_mismatch()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
