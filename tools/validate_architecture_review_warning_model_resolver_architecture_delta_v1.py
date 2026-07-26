# project-path: tools/validate_architecture_review_warning_model_resolver_architecture_delta_v1.py
"""Reject Architecture Review findings owned by new Warning Local AI feature files."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

__all__ = ["main"]

FEATURE_ID = "architecture-review-warning-local-ai-resolver-architecture-delta-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUDIT_CLI = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "manage_architecture.py"
)
NEW_OWNER_PATHS = (
    "kanda_reasoner_app/manage_architecture/warning_resolver_split_control.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_context.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_resolver.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_protection_formatting.py",
    "kanda_reasoner_app/manage_architecture/warning_model_resolver_sonar.py",
    "tests/test_warning_model_test_protection_resolver.py",
    "tests/test_warning_resolver_split_control.py",
    "tests/test_warning_resolver_shared_worker_routes.py",
    "tools/validate_architecture_review_warning_model_resolver_v1.py",
    "tools/validate_architecture_review_warning_model_resolver_architecture_delta_v1.py",
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
        if any(path in line for path in NEW_OWNER_PATHS)
    ]
    if offenders:
        print("VALIDATION FAIL: " + FEATURE_ID)
        print("New feature owner(s) produced Architecture Review findings:")
        for line in offenders:
            print(line)
        return 1

    print("WARNING_MODEL_RESOLVER_NEW_OWNER_ARCHITECTURE_FINDINGS: 0")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
