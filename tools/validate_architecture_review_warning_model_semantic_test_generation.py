# project-path: tools/validate_architecture_review_warning_model_semantic_test_generation.py
"""Validate semantic retrieval and disposable-project real-test generation for Local AI v2."""

from __future__ import annotations

import ast
from pathlib import Path
import py_compile
import subprocess
import sys

FEATURE_ID = "architecture-review-warning-local-ai-resolver-v2"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAX_LINES = 500

__all__ = ["main"]

PRODUCTION_FILES = (
    "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py",
    "kanda_reasoner_app/manage_architecture/warning_test_protection_gap_resolver.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_semantic_evidence.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_generation_contract.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_sandbox_validation.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_apply.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_context.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_resolver.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_formatting.py",
    "kanda_reasoner_app/manage_architecture/warning_model_resolver_sonar.py",
)
TEST_FILES = (
    "tests/test_warning_model_test_protection_resolver.py",
    "tests/test_warning_resolver_split_control.py",
    "tests/test_warning_resolver_shared_worker_routes.py",
    "tests/test_warning_model_test_protection_v2.py",
    "tests/test_warning_model_test_sandbox_validation.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(relative: str) -> str:
    path = PROJECT_ROOT / relative
    require(path.is_file(), "Missing expected file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_python_contract() -> None:
    for relative in PRODUCTION_FILES + TEST_FILES:
        text = read(relative)
        ast.parse(text, filename=relative)
        py_compile.compile(str(PROJECT_ROOT / relative), doraise=True)
        if relative in PRODUCTION_FILES:
            line_count = len(text.splitlines())
            require(line_count <= MAX_LINES, relative + " exceeds 500 lines")
            if relative not in {
                "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py",
                "kanda_reasoner_app/manage_architecture/warning_test_protection_gap_resolver.py",
            }:
                require(line_count >= 101, relative + " is below the 101-line permanent-module floor")
    print("WARNING_MODEL_RESOLVER_V2_PYTHON_SYNTAX: PASS")
    print("WARNING_MODEL_RESOLVER_V2_MODULE_SIZE_GATE: PASS")


def validate_semantic_retrieval_contract() -> None:
    context = read(
        "kanda_reasoner_app/manage_architecture/warning_model_test_protection_context.py"
    )
    semantic = read(
        "kanda_reasoner_app/manage_architecture/warning_model_test_semantic_evidence.py"
    )
    required = (
        "_MAX_CANDIDATES_PER_SOURCE = 8",
        "build_semantic_source_evidence",
        "build_semantic_test_evidence",
        '"mock_targets"',
        '"assertion_symbols"',
        '"public_signatures"',
        '"suggested_new_test_path"',
    )
    for marker in required:
        require(marker in context, "Missing semantic context contract: " + marker)
    for marker in ("PUBLIC CONTRACT BODY", "RELEVANT TEST", "pytest.raises", "mock_targets"):
        require(marker in semantic, "Missing AST semantic evidence marker: " + marker)
    print("WARNING_MODEL_RESOLVER_V2_AST_SEMANTIC_RETRIEVAL: PASS")


def validate_generation_and_sandbox_contract() -> None:
    generation = read(
        "kanda_reasoner_app/manage_architecture/warning_model_test_generation_contract.py"
    )
    sandbox = read(
        "kanda_reasoner_app/manage_architecture/warning_model_test_sandbox_validation.py"
    )
    resolver = read(
        "kanda_reasoner_app/manage_architecture/warning_model_test_protection_resolver.py"
    )
    required_generation = (
        'ACTION_EXTEND_EXISTING_TEST = "extend_existing_test"',
        'ACTION_CREATE_FOCUSED_TEST = "create_focused_test"',
        "Generated test code must directly import the exact source module",
        "assertion or expected-exception evidence",
        "blocked dynamic/process execution API",
        "exact deterministic suggested test path",
    )
    for marker in required_generation:
        require(marker in generation, "Missing fail-closed generation gate: " + marker)
    required_sandbox = (
        "shutil.copytree(",
        '"pytest", test_path, "-q"',
        '"--root", str(sandbox), "--validate"',
        "Targeted pytest timed out",
        "TEST_PROTECTION_GAP remained after",
    )
    for marker in required_sandbox:
        require(marker in sandbox, "Missing disposable validation gate: " + marker)
    require("sandbox_validator(" in resolver, "Resolver must validate generated tests before acceptance")
    require("_accepted_mutation_decision(" in resolver, "Only accepted sandbox outcomes may become done")
    print("WARNING_MODEL_RESOLVER_V2_REAL_TEST_GENERATION_FAIL_CLOSED: PASS")
    print("WARNING_MODEL_RESOLVER_V2_DISPOSABLE_PROJECT_PYTEST_AND_AUDIT: PASS")


def validate_gui_and_progress_contract() -> None:
    actions = read(
        "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py"
    )
    resolver = read(
        "kanda_reasoner_app/manage_architecture/warning_model_test_protection_resolver.py"
    )
    sonar = read(
        "kanda_reasoner_app/manage_architecture/warning_model_resolver_sonar.py"
    )
    require("if plan.safe_change_count:" in actions, "Human confirmation gate must cover test changes")
    require("Validated Local AI test changes" in actions, "GUI confirmation must disclose generated test changes")
    require("queue_model_apply_verify(plan)" in actions, "Confirmed live apply must remain explicit after QMessageBox and run through background verification")
    require('"local_ai_reviewing"' in resolver, "Progress must emit before blocking model call")
    require('"sandbox_pytest"' in sonar, "Sonar must expose disposable pytest phase")
    require('"sandbox_audit"' in sonar, "Sonar must expose disposable audit phase")
    print("WARNING_MODEL_RESOLVER_V2_PRE_CHAT_PROGRESS: PASS")
    print("WARNING_MODEL_RESOLVER_V2_HUMAN_CONFIRMATION_GATE: PASS")


def validate_direct_test_protection_imports() -> None:
    combined = "\n".join(read(path) for path in TEST_FILES)
    modules = (
        "warning_model_test_semantic_evidence",
        "warning_model_test_generation_contract",
        "warning_model_test_sandbox_validation",
        "warning_model_test_apply",
        "warning_model_test_protection_context",
        "warning_model_test_protection_resolver",
    )
    for module in modules:
        require(module in combined, "Focused tests lack direct protection import for: " + module)
    print("WARNING_MODEL_RESOLVER_V2_FOCUSED_TEST_PROTECTION_IMPORTS: PASS")


def run_focused_tests() -> None:
    for relative in TEST_FILES:
        completed = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / relative)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.stdout:
            print(completed.stdout.rstrip())
        if completed.stderr:
            print(completed.stderr.rstrip())
        require(completed.returncode == 0, "Focused v2 test failed: " + relative)
    print("WARNING_MODEL_RESOLVER_V2_FOCUSED_TESTS: PASS")


def main() -> int:
    try:
        validate_python_contract()
        validate_semantic_retrieval_contract()
        validate_generation_and_sandbox_contract()
        validate_gui_and_progress_contract()
        validate_direct_test_protection_imports()
        run_focused_tests()
    except Exception as exc:
        print("VALIDATION FAIL: " + FEATURE_ID)
        print(str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
