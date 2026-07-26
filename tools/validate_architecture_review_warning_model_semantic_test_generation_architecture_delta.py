# project-path: tools/validate_architecture_review_warning_model_semantic_test_generation_architecture_delta.py
"""Reject Architecture Review findings owned by Warning Local AI Resolver v2 files."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

__all__ = ["main"]

FEATURE_ID = "architecture-review-warning-local-ai-resolver-architecture-delta-v2"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUDIT_CLI = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "manage_architecture.py"
)
NEW_OWNER_PATHS = (
    "kanda_reasoner_app/manage_architecture/warning_test_protection_gap_resolver.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_context.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_resolver.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_formatting.py",
    "kanda_reasoner_app/manage_architecture/warning_model_resolver_sonar.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_semantic_evidence.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_generation_contract.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_sandbox_validation.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_apply.py",
    "tests/test_warning_model_test_protection_v2.py",
    "tests/test_warning_model_test_sandbox_validation.py",
    "tools/validate_architecture_review_warning_model_semantic_test_generation.py",
    "tools/validate_architecture_review_warning_model_semantic_test_generation_architecture_delta.py",
)

ALLOWED_BASELINE_FINDING_PREFIXES = (
    "WARNING MIXED_RESPONSIBILITY_FILE    kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py ::",
)


def main() -> int:
    completed = subprocess.run(
        [
            sys.executable,
            str(AUDIT_CLI),
            "--root",
            str(PROJECT_ROOT),
            "--validate",
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = completed.stdout + ("\n" + completed.stderr if completed.stderr else "")
    if "ARCHITECTURE VALIDATION SUMMARY" not in output:
        print("VALIDATION FAIL: " + FEATURE_ID)
        print("Architecture Review output was not produced.")
        return 1
    issue_lines = [
        line
        for line in output.splitlines()
        if line.startswith("WARNING ") or line.startswith("ERROR   ")
    ]
    offenders = [
        line
        for line in issue_lines
        if (
            any(path in line for path in NEW_OWNER_PATHS)
            or (
                "architecture_audit_actions_gui.py" in line
                and not any(
                    line.startswith(prefix)
                    for prefix in ALLOWED_BASELINE_FINDING_PREFIXES
                )
            )
        )
    ]
    if offenders:
        print("VALIDATION FAIL: " + FEATURE_ID)
        print("Warning Local AI Resolver v2 owner(s) produced Architecture Review findings:")
        for line in offenders:
            print(line)
        return 1
    print("WARNING_MODEL_RESOLVER_V2_BASELINE_FINDING_ALLOWLIST: PASS")
    print("WARNING_MODEL_RESOLVER_V2_NEW_OWNER_ARCHITECTURE_FINDINGS: 0")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
