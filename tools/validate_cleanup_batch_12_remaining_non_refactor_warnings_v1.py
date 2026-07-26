"""Validate Cleanup Batch 12 remaining non-refactor warning cleanup."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "cleanup-batch-12-remaining-non-refactor-warnings-v1"

BLOCKED_VALIDATION_SNIPPETS = [
    "WARNING MISPLACED_TEST               tests/test_reasoner_static_import_contracts_01.py :: Test file imports a stale or reference-looking target: kanda_reasoner_app.local_ai_json_working_copy",
    "WARNING MISPLACED_TEST               tests/test_t10p029_local_ai_json_working_copy_canonical_imports.py :: Test file imports a stale or reference-looking target: kanda_reasoner_app.local_ai_json_working_copy",
    "WARNING MISSING_DOCSTRING            tools/validate_cleanup_batch_10_misplaced_test_policy_v1.py :: Missing module docstring.",
    "WARNING MISSING_DOCSTRING            tools/validate_cleanup_batch_11_test_internal_contract_policy_v1.py :: Missing module docstring.",
    "WARNING TEST_ASSERTS_INTERNAL_DETAIL tests/test_refactor_report_help_button.py :: Test imports private implementation detail '_format_help_catalog_text'",
    "WARNING TEST_PROTECTION_GAP          kanda_reasoner_app/templates/floating_windows/clipboard_message_window.py :: Important active module has no direct test module import.",
]

REQUIRED_SOURCE_MARKERS = [
    "imported_module_id.startswith(item +",
    "resolved is not None and _is_documented_test_compatibility_shim_import(resolved.module_id)",
    "_format_help_catalog_text",
]


def fail(message: str) -> None:
    print("VALIDATION ERROR: " + message)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle}")


def assert_module_docstring(path: Path) -> None:
    text = read_text(path).lstrip()
    if not text.startswith('"""'):
        fail(f"missing module docstring: {path}")


def run_architecture_validation(root: Path) -> str:
    command = [
        sys.executable,
        "kanda_reasoner_app/manage_architecture/manage_architecture.py",
        "--root",
        str(root),
        "--validate",
    ]
    completed = subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout
    if "ARCHITECTURE VALIDATION SUMMARY" not in output:
        fail("architecture validation did not produce a summary")
    return output


def main() -> None:
    root = Path(__file__).resolve().parents[1]

    loader = root / "kanda_reasoner_app/manage_architecture/manage_architecture_help/source_loader_private_impl.py"
    loader_text = read_text(loader)
    if sum(1 for _ in loader.open(encoding="utf-8")) > 500:
        fail("source_loader_private_impl.py exceeds 500 lines")
    for marker in REQUIRED_SOURCE_MARKERS:
        assert_contains(loader_text, marker, "source-loader non-refactor policy marker")

    assert_module_docstring(root / "tools/validate_cleanup_batch_10_misplaced_test_policy_v1.py")
    assert_module_docstring(root / "tools/validate_cleanup_batch_11_test_internal_contract_policy_v1.py")

    test_file = root / "tests/test_templates_floating_windows_clipboard_message_window_public_contract.py"
    test_text = read_text(test_file)
    assert_contains(test_text, "TYPE_CHECKING", "static type-checking import guard")
    assert_contains(test_text, "kanda_reasoner_app.templates.floating_windows.clipboard_message_window", "direct public-contract test import")
    assert_contains(test_text, "CopyMessageFloatingWindow", "CopyMessageFloatingWindow static import")
    assert_contains(test_text, "show_copy_message_window", "show_copy_message_window static import")

    output = run_architecture_validation(root)
    if "Errors: 0" not in output:
        fail("architecture validation still reports errors")
    for snippet in BLOCKED_VALIDATION_SNIPPETS:
        if snippet in output:
            fail("blocked non-refactor warning still present: " + snippet[:180])

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
