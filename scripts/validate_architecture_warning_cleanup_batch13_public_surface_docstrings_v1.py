# project-path: scripts/validate_architecture_warning_cleanup_batch13_public_surface_docstrings_v1.py
"""Validate architecture warning cleanup batch 13."""

from __future__ import annotations

import ast
import json
import py_compile
import subprocess
import sys
from pathlib import Path

__all__ = ["main"]

FEATURE_ID = "architecture-warning-cleanup-batch13-public-surface-docstrings-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DOCSTRING_TARGETS = [
    "scripts/validate_architecture_workflow_cancel_font_only_v1.py",
    "scripts/validate_audit_startup_candidates_refactor_train_car_1_v1.py",
    "scripts/validate_error_memory_intake_refactor_train_car_1_v1.py",
    "scripts/validate_large_module_refactor_protocol_v72.py",
    "scripts/validate_prompt_router_reasoner_review_store_refactor_train_car_1_v1.py",
    "tools/validate_error_memory_tab_pending_loader_refactor_v1.py",
    "tools/validate_error_memory_tab_receive_import_refactor_v1.py",
    "tools/validate_error_memory_tab_table_view_refactor_v1.py",
    "tools/validate_large_module_refactor_protocol_canon_v63.py",
]

PUBLIC_SCRIPT_TARGETS = {
    "scripts/validate_error_memory_tab_refactor_completion_guard_v1.py": ["main"],
    "scripts/validate_error_memory_tab_refactor_train_car_1_v1.py": ["main"],
}

MANIFEST_TARGET = "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help.json"
MANIFEST_HELPER_EXPORTS = {
    "file_retrieval_context.py": [
        "RetrievalQueryContext",
        "CandidateFileContext",
        "build_query_context",
        "candidate_file_paths",
        "collect_symbols",
        "module_name_for_file",
        "build_candidate_context",
        "reindex_file_evidence",
    ],
    "file_retrieval_scoring_exact.py": ["apply_exact_and_call_scoring"],
    "file_retrieval_scoring_explain.py": [
        "apply_startup_scoring",
        "apply_explanation_heavy_scoring",
    ],
    "file_retrieval_scoring_runtime.py": ["apply_advanced_and_runtime_scoring"],
    "file_retrieval_scoring_semantic.py": ["apply_semantic_scoring"],
}

KNOWN_REMAINING_PUBLIC_SURFACE_WARNINGS = [
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_models.py",
    "kanda_prompt_workspace/prompt_tools/audit_startup_candidates_runner.py",
    "kanda_reasoner_app/routing_signal_scorer/models.py",
]

KNOWN_REMAINING_HELPER_WARNING_FRAGMENTS = [
    "file_retrieval_core",
    "file_retrieval_evidence",
]


def fail(message: str) -> None:
    """Print a validation error and stop."""
    print("VALIDATION ERROR: " + message)
    raise SystemExit(1)


def read_text(relative_path: str) -> str:
    """Read a UTF-8 project file."""
    path = PROJECT_ROOT / relative_path
    if not path.exists():
        fail("missing file: " + relative_path)
    return path.read_text(encoding="utf-8")


def module_docstring(relative_path: str) -> str | None:
    """Return a module docstring for a project file."""
    tree = ast.parse(read_text(relative_path), filename=relative_path)
    return ast.get_docstring(tree)


def declared_all(relative_path: str) -> list[str]:
    """Return a literal module __all__ declaration."""
    tree = ast.parse(read_text(relative_path), filename=relative_path)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets = [target for target in node.targets if isinstance(target, ast.Name)]
            if any(target.id == "__all__" for target in targets):
                return literal_string_list(node.value, relative_path)
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                return literal_string_list(node.value, relative_path)
    fail("missing __all__ in " + relative_path)
    return []


def literal_string_list(node: ast.AST | None, relative_path: str) -> list[str]:
    """Return a string list from an AST list or tuple node."""
    if not isinstance(node, (ast.List, ast.Tuple)):
        fail("__all__ is not a literal list in " + relative_path)
    values: list[str] = []
    for item in node.elts:
        if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
            fail("__all__ contains a non-string value in " + relative_path)
        values.append(item.value)
    return values


def validate_docstrings() -> None:
    """Validate behavior-neutral module docstring cleanup."""
    for relative_path in DOCSTRING_TARGETS:
        if not module_docstring(relative_path):
            fail("missing module docstring: " + relative_path)
        line_count = len(read_text(relative_path).splitlines())
        if line_count > 500:
            fail("docstring target is over 500 lines: " + relative_path)


def validate_public_script_contracts() -> None:
    """Validate narrow public contracts for script entry points."""
    for relative_path, expected_names in PUBLIC_SCRIPT_TARGETS.items():
        actual_names = declared_all(relative_path)
        if actual_names != expected_names:
            fail("unexpected __all__ for " + relative_path + ": " + repr(actual_names))


def validate_helper_manifest() -> None:
    """Validate retriever helper manifest alignment for existing helper exports."""
    manifest = json.loads(read_text(MANIFEST_TARGET))
    helpers = manifest.get("helpers")
    if not isinstance(helpers, dict):
        fail("helper manifest helpers must be an object")
    for helper_name, expected_exports in MANIFEST_HELPER_EXPORTS.items():
        entry = helpers.get(helper_name)
        if not isinstance(entry, dict):
            fail("missing helper manifest entry: " + helper_name)
        actual_exports = entry.get("exports")
        if actual_exports != expected_exports:
            fail("unexpected helper exports for " + helper_name + ": " + repr(actual_exports))
    exported = manifest.get("summary", {}).get("exported_symbols")
    if not isinstance(exported, list):
        fail("manifest summary.exported_symbols must be a list")
    for expected_exports in MANIFEST_HELPER_EXPORTS.values():
        for name in expected_exports:
            if name not in exported:
                fail("manifest summary missing exported symbol: " + name)


def validate_architecture_output() -> None:
    """Run architecture validation and check this batch did not add errors."""
    command = [
        sys.executable,
        str(PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/manage_architecture.py"),
        "--root",
        str(PROJECT_ROOT),
        "--validate",
    ]
    completed = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        print(output)
        fail("architecture validation returned non-zero")
    if "Errors: 0" not in output:
        print(output)
        fail("architecture validation did not report zero errors")
    for relative_path in DOCSTRING_TARGETS:
        fragment = "MISSING_DOCSTRING            " + relative_path
        if fragment in output:
            print(output)
            fail("docstring warning still present: " + relative_path)
    for relative_path in PUBLIC_SCRIPT_TARGETS:
        fragment = "MISSING_PUBLIC_SURFACE_CONTROL " + relative_path
        if fragment in output:
            print(output)
            fail("script public-surface warning still present: " + relative_path)
    if "helper __all__ exports absent from manifest" in output:
        print(output)
        fail("helper manifest still lacks existing helper __all__ exports")
    # These warnings are known and intentionally left for a later facade-aware cleanup.
    for relative_path in KNOWN_REMAINING_PUBLIC_SURFACE_WARNINGS:
        if relative_path not in output:
            fail("expected remaining warning disappeared unexpectedly: " + relative_path)
    for fragment in KNOWN_REMAINING_HELPER_WARNING_FRAGMENTS:
        if fragment not in output:
            fail("expected remaining helper warning disappeared unexpectedly: " + fragment)


def validate_py_compile() -> None:
    """Compile touched Python files."""
    python_targets = list(DOCSTRING_TARGETS) + list(PUBLIC_SCRIPT_TARGETS) + [
        "scripts/validate_architecture_warning_cleanup_batch13_public_surface_docstrings_v1.py",
    ]
    for relative_path in python_targets:
        py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)


def main() -> int:
    """Run batch 13 validation."""
    validate_py_compile()
    validate_docstrings()
    validate_public_script_contracts()
    validate_helper_manifest()
    validate_architecture_output()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
