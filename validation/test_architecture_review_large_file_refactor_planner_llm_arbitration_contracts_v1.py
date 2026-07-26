# project-path: validation/test_architecture_review_large_file_refactor_planner_llm_arbitration_contracts_v1.py
"""Focused validation for Large File Refactor Planner LLM arbitration contracts."""
from __future__ import annotations

import json
import py_compile
import shutil
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-planner-llm-arbitration-contracts-v1"
DOC_FEATURE_ID = "architecture-review-large-file-refactor-planner-docstring-contracts-v1"
SPLIT_FEATURE_ID = "architecture-review-large-file-refactor-planner-split-contracts-v1"
AST_FEATURE_ID = "architecture-review-large-file-refactor-planner-ast-v1"


def main() -> int:
    """Run focused LLM arbitration contract validation."""
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    changed = _changed_files(project_root)
    _assert_module_sizes(changed)
    _compile_files(changed)
    _run_docstring_baseline(project_root)
    _validate_llm_contracts()
    _validate_gui_contract(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"VALIDATION OK: {DOC_FEATURE_ID}")
    print(f"VALIDATION OK: {SPLIT_FEATURE_ID}")
    print(f"VALIDATION OK: {AST_FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


def _changed_files(project_root: Path) -> list[Path]:
    """Return files touched by this train."""
    rels = [
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/models.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/llm_arbitration.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/llm_formatting.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py",
        "validation/test_architecture_review_large_file_refactor_planner_llm_arbitration_contracts_v1.py",
        "tools/validate_architecture_review_large_file_refactor_planner_llm_arbitration_contracts_v1.py",
    ]
    return [project_root / rel for rel in rels]


def _assert_module_sizes(paths: list[Path]) -> None:
    """Assert every touched Python file remains under the hard limit."""
    for path in paths:
        if not path.exists():
            raise AssertionError(f"Missing changed file: {path}")
        line_count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        if line_count > 500:
            raise AssertionError(f"Module exceeds 500 physical lines: {path} ({line_count})")


def _compile_files(paths: list[Path]) -> None:
    """Compile every changed Python file."""
    for path in paths:
        py_compile.compile(str(path), doraise=True)


def _run_docstring_baseline(project_root: Path) -> None:
    """Run the frozen docstring-contract validator when available."""
    validator = project_root / "validation/test_architecture_review_large_file_refactor_planner_docstring_contracts_v1.py"
    if not validator.exists():
        raise AssertionError("Docstring contracts v1 validator is required before LLM contracts.")
    namespace = {"__name__": "docstring_v1_embedded", "__file__": str(validator)}
    code = compile(validator.read_text(encoding="utf-8"), str(validator), "exec")
    exec(code, namespace)
    result = namespace["main"]()
    if result != 0:
        raise AssertionError("Docstring contracts v1 baseline validation returned nonzero.")


def _validate_llm_contracts() -> None:
    """Validate JSON-only LLM arbitration behavior."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import analyze_python_file
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.llm_arbitration import (
        arbitrate_symbol_assignment,
        build_llm_arbitration_request,
        parse_llm_arbitration_response,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.llm_formatting import (
        format_llm_arbitration_report,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
        LLMArbitrationRequest,
        LLMArbitrationResult,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import build_split_plan

    temp_dir = Path(tempfile.mkdtemp(prefix="large_file_llm_contracts_"))
    try:
        sample = temp_dir / "sample_llm.py"
        sample.write_text(_sample_source(), encoding="utf-8")
        report = analyze_python_file(sample)
        plan = build_split_plan(report)
        request = build_llm_arbitration_request(report, plan, model_name="local-test")
        if not isinstance(request, LLMArbitrationRequest):
            raise AssertionError("Request must use the LLMArbitrationRequest contract.")
        required_hash_fields = [
            request.file_content_hash,
            request.symbol_body_hash,
            request.candidate_module_list_hash,
            request.cache_key,
            request.prompt_version,
        ]
        if not all(required_hash_fields):
            raise AssertionError("LLM cache key inputs must be present.")
        disabled = arbitrate_symbol_assignment(request)
        if disabled.status != "LLM_DISABLED" or not disabled.fallback_used:
            raise AssertionError("Disabled local LLM must fall back safely.")
        unavailable = arbitrate_symbol_assignment(
            build_llm_arbitration_request(report, plan, local_llm_enabled=True)
        )
        if unavailable.status != "LLM_UNAVAILABLE" or not unavailable.fallback_used:
            raise AssertionError("Unavailable local LLM must fall back safely.")
        valid_payload = json.dumps({
            "selected_module": plan.proposed_modules[0].filename,
            "confidence": "medium",
            "rationale": "Cohesive public facade preservation.",
            "warnings": ["review required"],
        })
        valid = parse_llm_arbitration_response(
            build_llm_arbitration_request(report, plan, local_llm_enabled=True),
            valid_payload,
        )
        if not isinstance(valid, LLMArbitrationResult) or valid.fallback_used:
            raise AssertionError("Valid JSON response should produce a non-fallback result.")
        invalid = arbitrate_symbol_assignment(
            build_llm_arbitration_request(report, plan, local_llm_enabled=True),
            "not json",
        )
        if invalid.status != "LLM_INVALID_RESPONSE":
            raise AssertionError("Invalid JSON must be rejected and converted to fallback.")
        forbidden = arbitrate_symbol_assignment(
            build_llm_arbitration_request(report, plan, local_llm_enabled=True),
            json.dumps({"actions": ["create_patch"], "confidence": "high"}),
        )
        if forbidden.status != "LLM_INVALID_RESPONSE":
            raise AssertionError("Forbidden LLM actions must be rejected.")
        text = format_llm_arbitration_report(request, disabled)
        for marker in ("JSON-only", "does not create patches", "fallback"):
            if marker not in text:
                raise AssertionError(f"LLM format text missing marker: {marker}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def _validate_gui_contract(project_root: Path) -> None:
    """Confirm GUI exposes LLM arbitration without enabling preview writes."""
    gui = project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_shell.py"
    text = gui.read_text(encoding="utf-8", errors="replace")
    required = [
        "Ask Local LLM for Ambiguous Symbols",
        "build_llm_arbitration_request(report, plan",
        "arbitrate_symbol_assignment(request)",
        "format_llm_arbitration_report(request, result)",
        "PlannerState.LLM_REVIEW_READY",
        "Generate Preview",
        "Create Patch ZIP",
    ]
    for marker in required:
        if marker not in text:
            raise AssertionError(f"GUI LLM contract marker missing: {marker}")
    if "safe_write_text(" in text or "safe_write_bytes(" in text:
        raise AssertionError("LLM-contract GUI must not write preview files.")


def _sample_source() -> str:
    """Return a synthetic module for LLM arbitration validation."""
    return (
        "def public_function(value: int) -> int:\n"
        "    return value + 1\n\n"
        "class PublicClass:\n"
        "    def run(self, value: int) -> int:\n"
        "        return public_function(value)\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
